# 🤖 发薪日倒计时机器人

一个基于飞书开放平台的智能机器人，自动计算并显示距离发薪日的倒计时天数，支持自动更新群头像和富文本消息回复。

## ✨ 功能特性

- 📅 **智能倒计时**: 自动计算距离每月10日发薪日的天数
- 🖼️ **动态头像**: 根据倒计时天数自动更换群头像（0-31天对应不同图片）
- 💬 **富文本回复**: 支持发送包含文字和图片的富文本消息
- 🔄 **定时任务**: 每天凌晨0点自动更新群头像
- 💬 **多场景支持**: 支持群聊@机器人和私聊消息
- 🌐 **跨平台**: 支持 macOS、Linux 和 Windows 系统
- 🔔 **智能提醒**: 发薪日前一天自动发送提醒消息

## 📁 项目结构

```
python/
├── main.py              # 主程序文件
├── requirements.txt     # Python依赖包列表
├── bootstrap.sh        # macOS/Linux启动脚本
├── bootstrap.bat       # Windows启动脚本
├── python-setup.md     # Python环境安装指南
├── assets/             # 项目资源目录
│   └── image.png       # 项目截图
└── goldp/              # 倒计时图片资源
    ├── 0.jpg           # 发薪日图片
    ├── 1.jpg           # 距离发薪日1天
    ├── 2.jpg           # 距离发薪日2天
    └── ...             # 依此类推到31.jpg
```

## 🚀 快速开始

### 1. 环境准备

确保已安装 Python 3.7+，详细安装指南请参考 [python-setup.md](python-setup.md)

### 2. 获取飞书应用凭证

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建应用并获取 `APP_ID` 和 `APP_SECRET`
3. 开通必要的权限：
   - `im:message` (接收与发送消息)
   - `im:message.group_at_msg` (接收群组@消息)
   - `im:chat` 或 `im:chat:update` (更新群头像，可选)

### 3. 配置环境变量

```bash
# macOS/Linux
export APP_ID="your_app_id"
export APP_SECRET="your_app_secret"

# Windows
set APP_ID=your_app_id
set APP_SECRET=your_app_secret
```

### 4. 启动机器人

#### 自动启动（推荐）

```bash
# macOS/Linux
APP_ID=<app_id> APP_SECRET=<app_secret> ./bootstrap.sh

# Windows
set APP_ID=<app_id>&set APP_SECRET=<app_secret>&bootstrap.bat
```

#### 手动启动

```bash
# 安装依赖
pip install -r requirements.txt

# 启动程序
python main.py
```

## 📋 核心功能说明

### 倒计时计算逻辑

- **每月1-10日**: 计算距离当月10日的天数
- **每月11-31日**: 计算距离下月10日的天数
- **发薪日当天**: 显示特殊庆祝消息

### 消息回复机制

1. **群聊消息**: 任何群聊消息都会触发倒计时回复
2. **私聊消息**: 私聊机器人也会获得倒计时信息
3. **富文本格式**: 包含倒计时文字和对应的倒计时图片

### 自动头像更新

- 每天凌晨0点自动执行
- 根据当前倒计时天数选择对应图片
- 自动上传并更新指定群组的头像

## ⚙️ 配置说明

### 群组配置

在 `main.py` 的 `auto_update_group_avatar()` 函数中修改群组ID列表：

```python
group_ids = [
    "oc_89e029526cf54ba7bedd149dabc7fe55",  # 替换为你的群ID
    # 可以添加更多群ID
]
```

### 权限配置

确保机器人具有以下权限：

| 权限名称 | 用途 | 必需性 |
|---------|------|--------|
| `im:message` | 接收和发送消息 | ✅ 必需 |
| `im:message.group_at_msg` | 接收群组@消息 | ✅ 必需 |
| `im:chat` 或 `im:chat:update` | 更新群头像 | ⚠️ 可选 |

## 🛠️ 技术栈

- **Python 3.7+**: 主要开发语言
- **lark-oapi**: 飞书开放平台SDK
- **requests-toolbelt**: HTTP请求工具
- **schedule**: 定时任务调度
- **threading**: 多线程支持

## 📝 API参考

- [飞书开放平台文档](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1)
- [消息接收事件](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/receive)
- [群信息修改](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/chats/patch)

## 🔧 故障排除

### 常见问题

1. **权限不足错误 (99991672)**
   - 检查是否已开通 `im:chat` 或 `im:chat:update` 权限
   - 确保机器人是群管理员或群主

2. **图片上传失败**
   - 检查 `goldp/` 目录下是否存在对应天数的图片文件
   - 确认图片格式是否支持（推荐JPG）

3. **消息发送失败**
   - 检查网络连接
   - 验证 `APP_ID` 和 `APP_SECRET` 是否正确

### 调试模式

程序默认运行在调试模式，会输出详细的日志信息，包括：
- API请求和响应详情
- 图片上传状态
- 错误信息和解决建议

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件

---

**注意**: 使用本机器人前，请确保遵守飞书平台的使用规范和相关法律法规。