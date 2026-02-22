#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钉钉文件/图片发送工具
用于发送文件和图片到指定的钉钉群聊

使用方法:
    python3 dingtalk_sender.py send_file /path/to/file.pdf
    python3 dingtalk_sender.py send_image /path/to/image.jpg
"""

import os
import sys
import requests
import argparse

# ========== 配置 (硬编码，无需修改) ==========
CLIENT_ID = 'dingdwlipjehprtrzc6s'
CLIENT_SECRET = 'oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL'
WEBHOOK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf'

# API 端点
TOKEN_URL = 'https://oapi.dingtalk.com/gettoken'
UPLOAD_URL = 'https://oapi.dingtalk.com/media/upload'
SEND_URL = WEBHOOK_URL


def get_access_token():
    """获取访问令牌"""
    try:
        params = {'appkey': CLIENT_ID, 'appsecret': CLIENT_SECRET}
        response = requests.get(TOKEN_URL, params=params, timeout=10)
        response.raise_for_status()
        result = response.json()

        if result.get('errcode') == 0:
            return result['access_token']
        else:
            raise Exception(f"获取 access_token 失败：{result.get('errmsg')}")
    except Exception as e:
        print(f"❌ 获取 access_token 失败：{e}")
        raise


def get_mime_type(file_path):
    """根据文件扩展名获取 MIME 类型"""
    ext = os.path.splitext(file_path)[1].lower()
    mime_types = {
        '.jpeg': 'image/jpeg',
        '.jpg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.zip': 'application/zip',
        '.txt': 'text/plain',
    }
    return mime_types.get(ext, 'application/octet-stream')

def upload_media(access_token, file_path, media_type='file'):
    """上传媒体文件（文件或图片）"""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")

        params = {'access_token': access_token, 'type': media_type}

        with open(file_path, 'rb') as f:
            file_name = os.path.basename(file_path)
            mime_type = get_mime_type(file_path)
            # 关键：指定正确的文件名和 MIME 类型，保持原始扩展名
            files = {'media': (file_name, f, mime_type)}
            response = requests.post(UPLOAD_URL, params=params, files=files, timeout=60)
            response.raise_for_status()

        result = response.json()

        if result.get('errcode') == 0:
            return {
                'media_id': result.get('media_id'),
                'created_at': result.get('created_at'),
                'type': result.get('type'),
                'file_name': file_name
            }
        else:
            raise Exception(f"上传失败：{result.get('errmsg')}")

    except FileNotFoundError as e:
        print(f"❌ {e}")
        raise
    except Exception as e:
        print(f"❌ 上传失败：{e}")
        raise


def send_file_message(media_id, file_name, file_type='pdf'):
    """发送文件消息到钉钉群聊"""
    try:
        payload = {
            "msgtype": "file",
            "file": {
                "mediaId": media_id,      # 注意：大写 I
                "fileType": file_type,    # 注意：大写 T
                "fileName": file_name     # 注意：大写 N
            }
        }

        response = requests.post(SEND_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        return result

    except Exception as e:
        print(f"❌ 发送失败：{e}")
        raise


def send_image_message(media_id, access_token):
    """发送图片消息到钉钉群聊"""
    try:
        # picURL 必须使用钉钉的 media 下载链接格式
        pic_url = f"https://oapi.dingtalk.com/media/download?access_token={access_token}&media_id={media_id}"

        payload = {
            "msgtype": "image",
            "image": {
                "mediaId": media_id,      # 注意：大写 I
                "picURL": pic_url         # 必需！
            }
        }

        response = requests.post(SEND_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        return result

    except Exception as e:
        print(f"❌ 发送失败：{e}")
        raise


def send_text_message(content):
    """发送文本消息到钉钉群聊"""
    try:
        payload = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }

        response = requests.post(SEND_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        return result

    except Exception as e:
        print(f"❌ 发送失败：{e}")
        raise


def send_markdown_message(title, text):
    """发送 Markdown 消息到钉钉群聊"""
    try:
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": text
            }
        }

        response = requests.post(SEND_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        return result

    except Exception as e:
        print(f"❌ 发送失败：{e}")
        raise


# ========== 主函数 ==========

def send_file(file_path):
    """发送文件的完整流程"""
    print(f"📄 准备发送文件：{os.path.basename(file_path)}")
    print(f"📍 目标群聊：{WEBHOOK_URL.split('=')[1][:30]}...")
    print()

    # 1. 获取 access token
    print("步骤 1/3: 获取 access token...")
    access_token = get_access_token()
    print(f"✓ Access token 获取成功")
    print()

    # 2. 上传文件
    print("步骤 2/3: 上传文件...")
    upload_result = upload_media(access_token, file_path, 'file')
    media_id = upload_result['media_id']
    print(f"✓ 文件上传成功")
    print(f"  media_id: {media_id}")
    print()

    # 3. 发送文件消息
    print("步骤 3/3: 发送文件消息...")
    file_name = os.path.basename(file_path)

    # 根据文件扩展名确定 file_type
    ext = os.path.splitext(file_name)[1].lower().lstrip('.')
    file_type = ext if ext else 'file'

    result = send_file_message(media_id, file_name, file_type)

    if result.get('errcode') == 0:
        print()
        print("✅ 文件发送成功！")
        return True
    else:
        print()
        print(f"❌ 发送失败：{result.get('errmsg')}")
        return False


def send_image(file_path, use_file_mode=False):
    """
    发送图片的完整流程

    注意：钉钉 webhook 机器人发送的 image 类型消息在某些客户端可能无法显示预览
    如果 use_file_mode=True，则以文件附件形式发送图片（确保可以下载查看）
    """
    image_name = os.path.basename(file_path)
    print(f"🖼️ 准备发送图片：{image_name}")
    if use_file_mode:
        print("📝 模式：以文件附件形式发送（确保可以下载查看）")
    print(f"📍 目标群聊：{WEBHOOK_URL.split('=')[1][:30]}...")
    print()

    # 1. 获取 access token
    print("步骤 1/3: 获取 access token...")
    access_token = get_access_token()
    print(f"✓ Access token 获取成功")
    print()

    # 2. 上传图片（或文件）
    if use_file_mode:
        print("步骤 2/3: 上传文件...")
        upload_result = upload_media(access_token, file_path, 'file')
    else:
        print("步骤 2/3: 上传图片...")
        upload_result = upload_media(access_token, file_path, 'image')

    media_id = upload_result['media_id']
    print(f"✓ 上传成功")
    print(f"  media_id: {media_id}")
    print()

    # 3. 发送消息
    if use_file_mode:
        # 以文件形式发送
        print("步骤 3/3: 发送文件消息...")
        ext = os.path.splitext(image_name)[1].lower().lstrip('.')
        result = send_file_message(media_id, image_name, ext)
    else:
        # 以图片形式发送
        print("步骤 3/3: 发送图片消息...")
        result = send_image_message(media_id, access_token)

        # 如果图片发送失败，尝试以文件形式发送
        if result.get('errcode') != 0:
            print("\n⚠️ 图片消息发送失败，尝试以文件附件形式发送...")
            # 重新上传为文件
            params = {'access_token': access_token, 'type': 'file'}
            with open(file_path, 'rb') as f:
                files = {'media': (image_name, f)}
                response = requests.post(UPLOAD_URL, params=params, files=files, timeout=60)
            file_upload_result = response.json()
            file_media_id = file_upload_result.get('media_id')
            ext = os.path.splitext(image_name)[1].lower().lstrip('.')
            result = send_file_message(file_media_id, image_name, ext)

    if result.get('errcode') == 0:
        print()
        print("✅ 图片发送成功！")
        return True
    else:
        print()
        print(f"❌ 发送失败：{result.get('errmsg')}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='钉钉文件/图片发送工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python3 dingtalk_sender.py send_file /path/to/file.pdf     发送 PDF 文件
  python3 dingtalk_sender.py send_image /path/to/image.jpg   发送图片
  python3 dingtalk_sender.py send_text "Hello World"         发送文本消息
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # send_file 命令
    file_parser = subparsers.add_parser('send_file', help='发送文件')
    file_parser.add_argument('file_path', help='文件路径')

    # send_image 命令
    image_parser = subparsers.add_parser('send_image', help='发送图片')
    image_parser.add_argument('file_path', help='图片路径')
    image_parser.add_argument('--as-file', action='store_true',
                              help='以文件附件形式发送图片（确保可以下载查看，某些客户端 image 类型可能无法显示）')

    # send_text 命令
    text_parser = subparsers.add_parser('send_text', help='发送文本消息')
    text_parser.add_argument('content', help='消息内容')

    args = parser.parse_args()

    if args.command == 'send_file':
        success = send_file(args.file_path)
        sys.exit(0 if success else 1)

    elif args.command == 'send_image':
        success = send_image(args.file_path, use_file_mode=args.as_file)
        sys.exit(0 if success else 1)

    elif args.command == 'send_text':
        result = send_text_message(args.content)
        if result.get('errcode') == 0:
            print("✅ 消息发送成功！")
            sys.exit(0)
        else:
            print(f"❌ 发送失败：{result.get('errmsg')}")
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
