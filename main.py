import lark_oapi as lark
from lark_oapi.api.im.v1 import *
import json
from datetime import datetime, timedelta
import calendar
import requests
from requests_toolbelt import MultipartEncoder
import os
import threading
import time
import schedule

# 获取应用配置
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")


# 上传图片到飞书（用于发送消息）
def upload_image_for_message(image_path):
    if not os.path.exists(image_path):
        return None

    try:
        url = "https://open.feishu.cn/open-apis/im/v1/images"
        form = {
            'image_type': 'message',
            'image': (open(image_path, 'rb'))
        }
        multi_form = MultipartEncoder(form)

        # 获取tenant_access_token
        try:
            # 直接使用 HTTP 请求获取 token
            token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            token_data = {
                "app_id": APP_ID,
                "app_secret": APP_SECRET
            }
            token_response = requests.post(token_url, json=token_data)

            if token_response.status_code == 200:
                token_result = token_response.json()
                if token_result.get('code') == 0:
                    tenant_access_token = token_result.get('tenant_access_token')
                else:
                    print(f"获取token失败: {token_result.get('msg')}")
                    return None
            else:
                print(f"获取token HTTP错误: {token_response.status_code}")
                return None
        except Exception as e:
            print(f"获取token异常: {e}")
            return None

        headers = {
            'Authorization': f'Bearer {tenant_access_token}',
        }
        headers['Content-Type'] = multi_form.content_type

        response = requests.request("POST", url, headers=headers, data=multi_form)

        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                return result.get('data', {}).get('image_key')
            else:
                print(f"上传图片失败: {result.get('msg')}")
        else:
            print(f"上传图片HTTP错误: {response.status_code}")

    except Exception as e:
        print(f"上传图片异常: {e}")

    return None


# 上传图片到飞书（用于设置头像）
def upload_image_for_avatar(image_path):
    if not os.path.exists(image_path):
        return None

    try:
        url = "https://open.feishu.cn/open-apis/im/v1/images"
        form = {
            'image_type': 'avatar',
            'image': (open(image_path, 'rb'))
        }
        multi_form = MultipartEncoder(form)

        # 获取tenant_access_token
        try:
            # 直接使用 HTTP 请求获取 token
            token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            token_data = {
                "app_id": APP_ID,
                "app_secret": APP_SECRET
            }
            token_response = requests.post(token_url, json=token_data)

            if token_response.status_code == 200:
                token_result = token_response.json()
                if token_result.get('code') == 0:
                    tenant_access_token = token_result.get('tenant_access_token')
                else:
                    print(f"获取token失败: {token_result.get('msg')}")
                    return None
            else:
                print(f"获取token HTTP错误: {token_response.status_code}")
                return None
        except Exception as e:
            print(f"获取token异常: {e}")
            return None

        headers = {
            'Authorization': f'Bearer {tenant_access_token}',
        }
        headers['Content-Type'] = multi_form.content_type

        response = requests.request("POST", url, headers=headers, data=multi_form)

        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                return result.get('data', {}).get('image_key')
            else:
                print(f"上传头像失败: {result.get('msg')}")
        else:
            print(f"上传头像HTTP错误: {response.status_code}")

    except Exception as e:
        print(f"上传头像异常: {e}")

    return None


# 修改群头像
def update_group_avatar(chat_id, image_key):
    try:
        print(f"开始更新群头像: chat_id={chat_id}, image_key={image_key}")

        # 注意：此功能需要机器人具有以下权限：
        # 1. 获取与更新群组信息 (im:chat) 或 更新群信息 (im:chat:update)
        # 2. 机器人必须是群管理员或群主，或者群设置了"所有群成员可编辑群信息"
        # 3. 上传头像时需要使用 image_type="avatar"
        # 如果权限不足，更新会失败但不影响消息发送

        # 权限检查提示
        print("权限提醒：确保已开通 im:chat 或 im:chat:update 权限")

        # 使用飞书的群信息修改API
        # 参考：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/chats/patch
        url = f"https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}?user_id_type=open_id"

        # 获取tenant_access_token
        try:
            token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            token_data = {
                "app_id": APP_ID,
                "app_secret": APP_SECRET
            }
            token_response = requests.post(token_url, json=token_data)

            if token_response.status_code == 200:
                token_result = token_response.json()
                if token_result.get('code') == 0:
                    tenant_access_token = token_result.get('tenant_access_token')
                else:
                    print(f"获取token失败: {token_result.get('msg')}")
                    return False
            else:
                print(f"获取token HTTP错误: {token_response.status_code}")
                return False
        except Exception as e:
            print(f"获取token异常: {e}")
            return False

        # 构建请求头
        headers = {
            'Authorization': f'Bearer {tenant_access_token}',
            'Content-Type': 'application/json'
        }

        # 构建请求体
        patch_data = {
            "avatar": image_key
        }

        # 发送PUT请求修改群头像
        print(f"发送PUT请求到: {url}")
        print(f"请求数据: {json.dumps(patch_data, indent=2)}")
        response = requests.put(url, headers=headers, json=patch_data)

        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")

        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print(f"群头像更新成功")
                return True
            else:
                error_msg = result.get('msg', '未知错误')
                error_code = result.get('code', '未知错误码')
                print(f"群头像更新失败: {error_msg} (错误码: {error_code})")

                # 检查是否是权限问题
                if error_code == 99991672:
                    print("==========================================")
                    print("权限不足！需要开通以下权限之一：")
                    print("1. im:chat (获取与更新群组信息)")
                    print("2. im:chat:update (更新群信息)")
                    print("==========================================")
                    print("解决方案：")
                    print("1. 访问飞书开发者后台: https://open.feishu.cn/app")
                    print("2. 找到你的应用，进入 '权限管理' 页面")
                    print("3. 搜索并开通 'im:chat' 或 'im:chat:update' 权限")
                    print("4. 重新发布应用使权限生效")
                    print("==========================================")

                # 检查其他常见错误
                if "avatar" in error_msg.lower() and ("illegal" in error_msg.lower() or "invalid" in error_msg.lower()):
                    print("==========================================")
                    print("头像图片key无效！可能的原因：")
                    print("1. 图片上传时没有使用 image_type='avatar'")
                    print("2. 图片key已过期")
                    print("3. 图片格式不支持")
                    print("==========================================")

                return False
        else:
            print(f"群头像更新HTTP错误: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False

    except Exception as e:
        print(f"更新群头像异常: {e}")
        return False


# 自动更新群头像
def auto_update_group_avatar():
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始自动更新群头像")

        # 计算距离发薪日的天数
        days_left = calculate_days_to_payday()
        print(f"今天距离发薪日还有: {days_left}天")

        # 构建图片路径
        image_path = f"goldp/{days_left}.jpg"

        if not os.path.exists(image_path):
            print(f"头像图片不存在: {image_path}")
            return False

        print(f"准备上传头像图片: {image_path}")

        # 上传头像图片
        avatar_image_key = upload_image_for_avatar(image_path)
        if not avatar_image_key:
            print("头像图片上传失败")
            return False

        print(f"头像图片上传成功: {avatar_image_key}")

        # 获取需要更新头像的群列表
        # 这里你可以配置需要更新头像的群ID列表
        group_ids = [
            "oc_89e029526cf54ba7bedd149dabc7fe55",  # 替换为你的群ID
            # 可以添加更多群ID
        ]

        success_count = 0
        for group_id in group_ids:
            print(f"尝试更新群 {group_id} 的头像")
            if update_group_avatar(group_id, avatar_image_key):
                success_count += 1

        print(f"群头像更新完成，成功更新 {success_count}/{len(group_ids)} 个群")
        return True

    except Exception as e:
        print(f"自动更新群头像异常: {e}")
        return False


# 定时任务运行器
def schedule_runner():
    """运行定时任务"""
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


# 计算距离下个月10日的天数
def calculate_days_to_payday():
    today = datetime.now()
    current_day = today.day

    if current_day <= 10:
        # 如果今天在10日或之前，计算距离本月10日的天数
        payday = datetime(today.year, today.month, 10)
        if current_day == 10:
            days_left = 0
        else:
            days_left = (payday - today).days
    else:
        # 如果今天在10日之后，计算距离下个月10日的天数
        if today.month == 12:
            # 如果是12月，下个月是1月
            next_month_payday = datetime(today.year + 1, 1, 10)
        else:
            next_month_payday = datetime(today.year, today.month + 1, 10)
        days_left = (next_month_payday - today).days

    return days_left


# 注册接收消息事件，处理接收到的消息。
# Register event handler to handle received messages.
# https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/events/receive
def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    res_content = ""
    if data.event.message.message_type == "text":
        text_content = json.loads(data.event.message.content)
        res_content = text_content.get("text", "")
    else:
        res_content = ""

    # 检查是否有人在群聊中@机器人
    if data.event.message.chat_type != "p2p":
        # 群聊消息，检查是否@机器人
        print(f"收到群聊消息，内容: {res_content}")

        # 简化@检测，任何群聊消息都回复
        days_left = calculate_days_to_payday()
        print(f"距离发薪日还有: {days_left}天")

        # 准备文本内容
        if days_left == 0:
            text_message = "今天是发薪日！💰\nToday is payday! 💰"
        else:
            text_message = f"距离发薪还有{days_left}天\n你准备好了吗🏃"

        # 尝试发送富文本消息（文本+图片合并）
        try:
            image_key = None  # 初始化image_key变量
            if days_left == 0:
                # 发薪日当天只发送文本消息
                content = json.dumps({"text": text_message})
                msg_type = "text"
                print(f"准备发送文本消息: {text_message}")
            else:
                # 尝试上传图片并发送富文本消息
                image_path = f"goldp/{days_left}.jpg"
                if os.path.exists(image_path):
                    print(f"准备上传图片: {image_path}")

                    # 上传图片用于消息
                    message_image_key = upload_image_for_message(image_path)
                    if message_image_key:
                        print(f"消息图片上传成功，image_key: {message_image_key}")

                        # 根据官方文档构建富文本消息，包含文本和图片
                        rich_content = {
                            "zh_cn": {
                                "title": "发薪日倒计时",
                                "content": [
                                    [
                                        {
                                            "tag": "text",
                                            "text": text_message
                                        },
                                        {
                                            "tag": "img",
                                            "image_key": message_image_key
                                        }
                                    ]
                                ]
                            }
                        }
                        content = json.dumps(rich_content)
                        msg_type = "post"
                        print("准备发送富文本消息（文本+图片）")
                    else:
                        print("图片上传失败，发送纯文本消息")
                        content = json.dumps({"text": text_message})
                        msg_type = "text"
                else:
                    print(f"图片文件不存在: {image_path}，发送纯文本消息")
                    content = json.dumps({"text": text_message})
                    msg_type = "text"

            # 发送消息
            request = (
                ReplyMessageRequest.builder()
                .message_id(data.event.message.message_id)
                .request_body(
                    ReplyMessageRequestBody.builder()
                    .content(content)
                    .msg_type(msg_type)
                    .build()
                )
                .build()
            )
            response = client.im.v1.message.reply(request)

            if response.success():
                if msg_type == "post":
                    print("富文本消息发送成功")
                else:
                    print("文本消息发送成功")
            else:
                print(f"消息发送失败: {response.code}, {response.msg}")

                # 如果回复失败，尝试创建新消息
                new_request = (
                    CreateMessageRequest.builder()
                    .receive_id_type("chat_id")
                    .request_body(
                        CreateMessageRequestBody.builder()
                        .receive_id(data.event.message.chat_id)
                        .msg_type(msg_type)
                        .content(content)
                        .build()
                    )
                    .build()
                )
                new_response = client.im.v1.message.create(new_request)
                if new_response.success():
                    if msg_type == "post":
                        print("新富文本消息发送成功")
                    else:
                        print("新文本消息发送成功")
                else:
                    print(f"新消息发送也失败: {new_response.code}, {new_response.msg}")

        except Exception as e:
            print(f"发送消息时出错: {e}")

    elif data.event.message.chat_type == "p2p":
        # 私聊消息，也发送发薪日倒计时
        days_left = calculate_days_to_payday()

        # 准备文本内容
        if days_left == 0:
            text_message = "今天是发薪日！💰\nToday is payday! 💰"
        else:
            text_message = f"距离发薪还有{days_left}天"

        # 构建富文本消息（文本+图片合并）
        try:
            if days_left == 0:
                # 发薪日当天只发送文本消息
                content = json.dumps({"text": text_message})
                msg_type = "text"
                print(f"私聊准备发送文本消息: {text_message}")
            else:
                # 尝试上传图片并发送富文本消息
                image_path = f"goldp/{days_left}.jpg"
                if os.path.exists(image_path):
                    print(f"私聊准备上传图片: {image_path}")
                    image_key = upload_image_for_message(image_path)
                    if image_key:
                        print(f"私聊图片上传成功，image_key: {image_key}")
                        # 根据官方文档构建富文本消息，包含文本和图片
                        rich_content = {
                            "zh_cn": {
                                "title": "发薪日倒计时",
                                "content": [
                                    [
                                        {
                                            "tag": "text",
                                            "text": text_message
                                        },
                                        {
                                            "tag": "img",
                                            "image_key": image_key
                                        }
                                    ]
                                ]
                            }
                        }
                        content = json.dumps(rich_content)
                        msg_type = "post"
                        content = json.dumps(rich_content)
                        msg_type = "post"
                        print("私聊准备发送富文本消息（文本+图片）")
                    else:
                        print("私聊图片上传失败，发送纯文本消息")
                        content = json.dumps({"text": text_message})
                        msg_type = "text"
                else:
                    print(f"私聊图片文件不存在: {image_path}，发送纯文本消息")
                    content = json.dumps({"text": text_message})
                    msg_type = "text"

            # 发送消息
            request = (
                CreateMessageRequest.builder()
                .receive_id_type("chat_id")
                .request_body(
                    CreateMessageRequestBody.builder()
                    .receive_id(data.event.message.chat_id)
                    .msg_type(msg_type)
                    .content(content)
                    .build()
                )
                .build()
            )
            response = client.im.v1.message.create(request)

            if response.success():
                if msg_type == "post":
                    print("私聊富文本消息发送成功")
                else:
                    print("私聊文本消息发送成功")
            else:
                print(f"私聊消息发送失败: {response.code}, {response.msg}")

        except Exception as e:
            print(f"私聊发送消息时出错: {e}")
    else:
        # 其他情况不回复
        return


# 注册事件回调
# Register event handler.
event_handler = (
    lark.EventDispatcherHandler.builder("", "")
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1)
    .build()
)


# 检查配置
if not APP_ID or not APP_SECRET:
    print("请设置环境变量 APP_ID 和 APP_SECRET")
    exit(1)

# 创建 LarkClient 对象，用于请求OpenAPI, 并创建 LarkWSClient 对象，用于使用长连接接收事件。
# Create LarkClient object for requesting OpenAPI, and create LarkWSClient object for receiving events using long connection.
client = lark.Client.builder().app_id(APP_ID).app_secret(APP_SECRET).build()
wsClient = lark.ws.Client(
    APP_ID,
    APP_SECRET,
    event_handler=event_handler,
    log_level=lark.LogLevel.DEBUG,
)


def main():
    # 设置定时任务 - 每天凌晨0点更新群头像
    schedule.every().day.at("00:00").do(auto_update_group_avatar)
    print("定时任务已设置：每天0:00自动更新群头像")

    # 启动定时任务线程
    schedule_thread = threading.Thread(target=schedule_runner, daemon=True)
    schedule_thread.start()
    print("定时任务线程已启动")

    # 立即执行一次头像更新（可选）
    print("立即执行一次群头像更新...")
    auto_update_group_avatar()

    #  启动长连接，并注册事件处理器。
    #  Start long connection and register event handler.
    wsClient.start()


if __name__ == "__main__":
    main()