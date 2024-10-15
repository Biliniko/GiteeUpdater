import json
import os
from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import PersonNormalMessageReceived
import requests
import base64
import re
from datetime import datetime

@register(name="GiteeUpdater", description="提交内容到Gitee仓库", version="0.1", author="Biliniko")
class TopperPlugin(BasePlugin):

    def __init__(self, host: APIHost):
        self.host = host
        self.config = self.load_config()
        self.access_token = self.config["access_token"]
        self.owner = self.config["owner"]
        self.repo = self.config["repo"]
        self.path = self.config["path"]
        self.get_content_url = f"https://gitee.com/api/v5/repos/{self.owner}/{self.repo}/contents/{self.path}"
        self.admin_qq = self.config["admin_qq"]

    def load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        default_config = {
            "access_token": "",
            "owner": "",
            "repo": "",
            "path": "",
            "admin_qq": []
        }
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=4)
            print(f"配置文件 {config_path} 不存在,已创建默认配置文件。请填写正确的配置信息。")
            return default_config
        except json.JSONDecodeError:
            raise ValueError(f"配置文件 {config_path} 格式不正确")

    @handler(PersonNormalMessageReceived)
    async def handle_person_message(self, ctx: EventContext):
        msg = ctx.event.text_message
        sender_id = ctx.event.sender_id

        if msg.startswith("topper "):
            if str(sender_id) in self.admin_qq:
                content = msg[7:]  # 去掉"topper "前缀
                result = await self.submit_content(content)
                ctx.add_return("reply", [result])
            else:
                ctx.add_return("reply", ["抱歉,只有管理员才能使用此功能。"])
            ctx.prevent_default()

    async def submit_content(self, user_input):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/vnd.github.v3.raw"
        }

        try:
            response = requests.get(self.get_content_url, headers=headers)
            response.raise_for_status()
            content_obj = response.json()
            
            print(f"API Response: {content_obj}")  # 添加这行来打印完整的 API 响应
            
            if 'content' in content_obj:
                content = base64.b64decode(content_obj["content"]).decode("utf-8")
            elif 'download_url' in content_obj:
                content_response = requests.get(content_obj['download_url'])
                content_response.raise_for_status()
                content = content_response.text
            else:
                content = ""  # 如果文件不存在或为空，初始化为空字符串
            
            date_pattern = r'\d{4}/\d{2}/\d{2}'
            date_match = re.search(date_pattern, user_input)

            if date_match:
                date_str = date_match.group()
                try:
                    input_date = datetime.strptime(date_str, "%Y/%m/%d")
                    current_time = datetime.now().time()
                    combined_datetime = datetime.combine(input_date.date(), current_time)
                    timestamp = int(combined_datetime.timestamp())
                    
                    # 直接用时间戳替换日期
                    new_line = re.sub(date_pattern, str(timestamp), user_input).strip()
                except ValueError:
                    return "日期格式错误,请确保日期格式为YYYY/MM/DD。"
            else:
                new_line = user_input.strip()

            if content.strip():
                updated_content = content.strip() + "\n" + new_line
            else:
                updated_content = new_line  # 如果原内容为空，直接使用新行

            base64_content = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")

            headers["Accept"] = "application/vnd.github.v3+json"
            headers["Content-Type"] = "application/json"

            request_body = {
                "message": "添加新记录",
                "content": base64_content,
                "sha": content_obj.get("sha", "")
            }

            response = requests.put(self.get_content_url, headers=headers, json=request_body)
            response.raise_for_status()

            return "内容已成功提交到Gitee仓库!"
        except requests.RequestException as e:
            return f"提交失败: {str(e)}\nURL: {self.get_content_url}\nHeaders: {headers}"
