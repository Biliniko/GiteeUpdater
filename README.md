# GiteeUpdater

GiteeUpdater 是一个用于 QChatGPT 的插件，可以方便地将内容提交到 Gitee 仓库。


## 主要特性

🚀 **快速更新**: 通过 QQ 消息和Gitee官方API即可快速更新 Gitee 仓库内容

🕒 **时间戳转换**: 自动将日期转换为时间戳，便于数据处理

🌐 **云端授权管理**: 
  - 利用 Gitee 作为云端数据库，实现高效的授权管理
  - 支持各种限时授权场景，如：
    - 记录设备 MAC 地址和授权到期时间
    - 软件可实时读取仓库数据进行授权验证
    - 授权过期后自动失效，确保安全可控

💡 **国内友好**: 得益于 Gitee 在国内的稳定访问，提供流畅的用户体验


## 安装

配置完成 [QChatGPT](https://github.com/RockChinQ/QChatGPT) 主程序后，使用管理员账号向机器人发送以下命令即可安装：

```
!plugin get https://github.com/Biliniko/GiteeUpdater
```
或查看详细的[插件安装说明](https://qchatgpt.rockchin.top/develop/plugin-intro.html#%E6%8F%92%E4%BB%B6%E7%94%A8%E6%B3%95)


## 使用

更多详情，请查看 [插件安装说明](https://qchatgpt.rockchin.top/develop/plugin-intro.html#%E6%8F%92%E4%BB%B6%E7%94%A8%E6%B3%95)。


## 使用方法

1. 确保您已经在 `config.json` 文件中正确配置了 Gitee 的访问令牌、仓库信息和管理员 QQ 号。

2. 向机器人发送以下格式的消息来更新 Gitee 仓库内容（在仓库中新增一行内容）：

   ```
   topper <您的内容>
   ```
   如果包含日期YYYY/MM/DD，它将被自动转换为时间戳，并添加上当前的时分秒。
   
   比如在05:18:15输入：topper aabbcc 2024/11/16
   
   将会在Gitee仓库新增一行：aabbcc 1731705495

4. 只有在 `config.json` 中列为管理员的 QQ 号才能使用此功能。


## 配置说明

在 `config.json` 文件中，您需要设置以下字段：

- `access_token`: Gitee 的访问令牌
- `owner`: Gitee 仓库所有者的用户名
- `repo`: Gitee 仓库名称
- `path`: 要更新的文件在仓库中的路径
- `admin_qq`: 允许使用此插件的管理员 QQ 号列表


## 贡献

欢迎提交 issues 和 pull requests 来帮助改进这个插件。
