#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用钉钉工作通知接口发送图片
"""

import os
import requests
import json

CLIENT_ID = "dingdwlipjehprtrzc6s"
CLIENT_SECRET = "oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL"

IMAGE_PATH = "/Users/davidli/lobsterai/project/image_20260220_235137_超写实_Nike_跑鞋，专业运动鞋设计，.png"

# API 端点
TOKEN_URL = "https://oapi.dingtalk.com/gettoken"
UPLOAD_URL = "https://oapi.dingtalk.com/media/upload"
SEND_URL = "https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2"


def get_access_token():
    """获取 access token"""
    resp = requests.get(
        TOKEN_URL,
        params={"appkey": CLIENT_ID, "appsecret": CLIENT_SECRET}
    )
    data = resp.json()
    if data.get("errcode") == 0:
        return data["access_token"]
    raise Exception(f"获取 token 失败：{data}")


def upload_media(access_token, file_path, media_type="image"):
    """上传媒体文件"""
    url = f"{UPLOAD_URL}?access_token={access_token}&type={media_type}"

    with open(file_path, 'rb') as f:
        files = {'media': (os.path.basename(file_path), f)}
        print(f"↑ 正在上传：{os.path.basename(file_path)} ...")
        resp = requests.post(url, files=files)

    data = resp.json()
    print(f"   响应：{json.dumps(data, ensure_ascii=False)}")

    if data.get("errcode") == 0:
        return data.get("media_id")
    raise Exception(f"上传失败：{data}")


def get_user_id(access_token):
    """获取应用可见的用户 ID 列表"""
    # 获取部门列表
    dept_url = "https://oapi.dingtalk.com/department/list"
    resp = requests.get(dept_url, params={"access_token": access_token})
    dept_data = resp.json()
    print(f"部门列表：{json.dumps(dept_data, ensure_ascii=False)}")

    # 获取部门下的用户
    if dept_data.get("errcode") == 0 and dept_data.get("department"):
        dept_id = dept_data["department"][0].get("id")
        user_url = "https://oapi.dingtalk.com/user/simplelist"
        resp = requests.get(user_url, params={
            "access_token": access_token,
            "department_id": dept_id
        })
        user_data = resp.json()
        print(f"用户列表：{json.dumps(user_data, ensure_ascii=False)}")

        if user_data.get("errcode") == 0 and user_data.get("userlist"):
            return user_data["userlist"][0].get("userid")

    return None


def send_image_notification(access_token, media_id, user_id):
    """发送图片通知"""
    # 图片消息内容
    message_content = {
        "media_id": media_id
    }

    payload = {
        "agent_id": CLIENT_ID,
        "userid_list": user_id,
        "msgtype": "image",
        "image": message_content,
        "to_all_user": False
    }

    print(f"→ 发送图片通知给用户：{user_id}")
    resp = requests.post(
        SEND_URL,
        headers={"Content-Type": "application/json"},
        params={"access_token": access_token},
        json=payload
    )
    result = resp.json()
    print(f"   响应：{json.dumps(result, ensure_ascii=False)}")
    return result


def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"❌ 图片不存在：{IMAGE_PATH}")
        return

    print(f"📷 准备发送 Nike 跑鞋图片\n")

    try:
        # 1. 获取 token
        print("1. 获取 access token...")
        access_token = get_access_token()
        print(f"   ✓ Token 获取成功\n")

        # 2. 上传图片
        print("2. 上传图片...")
        media_id = upload_media(access_token, IMAGE_PATH)
        print(f"   ✓ 上传成功，media_id: {media_id}\n")

        # 3. 获取用户 ID
        print("3. 获取用户 ID...")
        user_id = get_user_id(access_token)

        if not user_id:
            print("   ⚠️ 无法获取用户 ID，尝试发送给所有人")
            # 尝试发送给所有人
            payload = {
                "agent_id": CLIENT_ID,
                "to_all_user": True,
                "msgtype": "image",
                "image": {"media_id": media_id}
            }
            print("→ 发送给所有人...")
            resp = requests.post(
                SEND_URL,
                headers={"Content-Type": "application/json"},
                params={"access_token": access_token},
                json=payload
            )
            result = resp.json()
            print(f"   响应：{json.dumps(result, ensure_ascii=False)}")
        else:
            print(f"   ✓ 找到用户 ID: {user_id}")
            # 4. 发送通知
            print("\n4. 发送图片通知...")
            result = send_image_notification(access_token, media_id, user_id)

        print()
        print("=" * 50)
        print("✅ 操作完成！")

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
