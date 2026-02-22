# 钉钉发送文件/图片完整指南

## 配置信息

### 群聊 Webhook
```
https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf
```

### 钉钉应用凭证
- **Client ID (AppKey):** `dingdwlipjehprtrzc6s`
- **Client Secret (AppSecret):** `oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL`

---

## API 端点

| 用途 | URL |
|------|-----|
| 获取 Access Token | `https://oapi.dingtalk.com/gettoken?appkey=xxx&appsecret=xxx` |
| 上传媒体文件 | `https://oapi.dingtalk.com/media/upload?access_token=xxx&type=file` (文件) |
| 上传图片 | `https://oapi.dingtalk.com/media/upload?access_token=xxx&type=image` (图片) |
| 发送消息 | `https://oapi.dingtalk.com/robot/send?access_token=xxx` |

---

## 发送文件的完整步骤

### 步骤 1: 获取 Access Token

```python
import requests

CLIENT_ID = 'dingdwlipjehprtrzc6s'
CLIENT_SECRET = 'oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL'

def get_access_token():
    params = {'appkey': CLIENT_ID, 'appsecret': CLIENT_SECRET}
    response = requests.get('https://oapi.dingtalk.com/gettoken', params=params)
    result = response.json()
    return result['access_token']

access_token = get_access_token()
```

### 步骤 2: 上传文件

```python
def upload_file(access_token, file_path):
    params = {'access_token': access_token, 'type': 'file'}
    with open(file_path, 'rb') as f:
        files = {'media': (os.path.basename(file_path), f)}
        response = requests.post('https://oapi.dingtalk.com/media/upload', params=params, files=files)
    result = response.json()
    return result

upload_result = upload_file(access_token, '/path/to/your/file.pdf')
media_id = upload_result['media_id']
```

### 步骤 3: 发送文件消息

```python
WEBHOOK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf'

def send_file(webhook_url, media_id, file_name, file_type='pdf'):
    payload = {
        "msgtype": "file",
        "file": {
            "mediaId": media_id,      # 注意：大写 I
            "fileType": file_type,    # 注意：大写 T
            "fileName": file_name     # 注意：大写 N
        }
    }
    response = requests.post(webhook_url, json=payload)
    return response.json()

result = send_file(WEBHOOK_URL, media_id, file_name, 'pdf')
```

---

## 发送图片的完整步骤

### 步骤 1: 获取 Access Token（同上）

### 步骤 2: 上传图片

```python
def upload_image(access_token, image_path):
    params = {'access_token': access_token, 'type': 'image'}
    with open(image_path, 'rb') as f:
        files = {'media': (os.path.basename(image_path), f)}
        response = requests.post('https://oapi.dingtalk.com/media/upload', params=params, files=files)
    result = response.json()
    return result

upload_result = upload_image(access_token, '/path/to/your/image.jpg')
media_id = upload_result['media_id']
```

### 步骤 3: 发送图片消息

**重要：** 发送图片必须提供 `picURL` 参数，使用钉钉的 media 下载链接格式！

```python
WEBHOOK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf'

def send_image(webhook_url, media_id, access_token):
    # picURL 必须使用钉钉的 media 下载链接格式
    pic_url = f"https://oapi.dingtalk.com/media/download?access_token={access_token}&media_id={media_id}"

    payload = {
        "msgtype": "image",
        "image": {
            "mediaId": media_id,      # 注意：大写 I
            "picURL": pic_url         # 必需！使用钉钉 media 下载链接
        }
    }
    response = requests.post(webhook_url, json=payload)
    return response.json()

result = send_image(WEBHOOK_URL, media_id, access_token)
```

---

## 完整的 Python 脚本（可直接运行）

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钉钉文件/图片发送工具
"""

import os
import requests

# ========== 配置 ==========
CLIENT_ID = 'dingdwlipjehprtrzc6s'
CLIENT_SECRET = 'oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL'
WEBHOOK_URL = 'https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf'

def get_access_token():
    """获取访问令牌"""
    params = {'appkey': CLIENT_ID, 'appsecret': CLIENT_SECRET}
    response = requests.get('https://oapi.dingtalk.com/gettoken', params=params)
    result = response.json()
    if result.get('errcode') == 0:
        return result['access_token']
    else:
        raise Exception(f"获取 access_token 失败：{result}")

def upload_media(access_token, file_path, media_type='file'):
    """上传媒体文件（文件或图片）"""
    params = {'access_token': access_token, 'type': media_type}
    with open(file_path, 'rb') as f:
        files = {'media': (os.path.basename(file_path), f)}
        response = requests.post('https://oapi.dingtalk.com/media/upload', params=params, files=files)
    result = response.json()
    if result.get('errcode') == 0:
        return result
    else:
        raise Exception(f"上传失败：{result}")

def send_file_message(webhook_url, media_id, file_name, file_type='pdf'):
    """发送文件消息"""
    payload = {
        "msgtype": "file",
        "file": {
            "mediaId": media_id,
            "fileType": file_type,
            "fileName": file_name
        }
    }
    response = requests.post(webhook_url, json=payload)
    return response.json()

def send_image_message(webhook_url, media_id, access_token):
    """发送图片消息"""
    # picURL 必须使用钉钉的 media 下载链接格式
    pic_url = f"https://oapi.dingtalk.com/media/download?access_token={access_token}&media_id={media_id}"

    payload = {
        "msgtype": "image",
        "image": {
            "mediaId": media_id,
            "picURL": pic_url  # 必需！
        }
    }
    response = requests.post(webhook_url, json=payload)
    return response.json()

def send_text_message(webhook_url, content):
    """发送文本消息"""
    payload = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    response = requests.post(webhook_url, json=payload)
    return response.json()

def send_markdown_message(webhook_url, title, text):
    """发送 Markdown 消息"""
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text
        }
    }
    response = requests.post(webhook_url, json=payload)
    return response.json()

# ========== 使用示例 ==========
if __name__ == '__main__':
    # 1. 获取 access token
    access_token = get_access_token()
    print(f"✓ Access token 获取成功")

    # 2. 发送文件
    file_path = '/path/to/your/file.pdf'
    if os.path.exists(file_path):
        upload_result = upload_media(access_token, file_path, 'file')
        media_id = upload_result['media_id']
        print(f"✓ 文件上传成功，media_id: {media_id}")

        result = send_file_message(
            WEBHOOK_URL,
            media_id,
            os.path.basename(file_path),
            'pdf'  # 或 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip' 等
        )

        if result.get('errcode') == 0:
            print("✅ 文件发送成功！")
        else:
            print(f"❌ 发送失败：{result}")

    # 3. 发送图片
    image_path = '/path/to/your/image.jpg'
    if os.path.exists(image_path):
        upload_result = upload_media(access_token, image_path, 'image')
        media_id = upload_result['media_id']
        print(f"✓ 图片上传成功，media_id: {media_id}")

        result = send_image_message(WEBHOOK_URL, media_id, access_token)

        if result.get('errcode') == 0:
            print("✅ 图片发送成功！")
        else:
            print(f"❌ 发送失败：{result}")
```

---

## 关键参数说明

### 发送文件消息的必需参数
| 参数名 | 说明 | 示例 |
|--------|------|------|
| `msgtype` | 消息类型 | `"file"` |
| `file.mediaId` | 上传后获得的媒体 ID | `"@lBDPD0XMA6vPNeHOIFViO84VX45-"` |
| `file.fileType` | 文件类型 | `"pdf"`, `"doc"`, `"xls"`, `"ppt"`, `"zip"` 等 |
| `file.fileName` | 文件名（包含扩展名） | `"简历.pdf"` |

### 发送图片消息的必需参数
| 参数名 | 说明 | 示例 |
|--------|------|------|
| `msgtype` | 消息类型 | `"image"` |
| `image.mediaId` | 上传后获得的媒体 ID | `"@lBDPD0XMA6vPNeHOIFViO84VX45-"` |
| `image.picURL` | **必需！** 图片下载链接 | `"https://oapi.dingtalk.com/media/download?access_token=xxx&media_id=xxx"` |

---

## 常见错误及解决方案

| 错误码 | 错误信息 | 解决方案 |
|--------|----------|----------|
| 401102 | 参数 file --》mediaId 缺失 | 确保使用 `mediaId`（大写 I），不是 `media_id` |
| 401103 | 参数 file --》fileName 缺失 | 添加 `fileName` 参数，包含完整文件名 |
| 401103 | 参数 file --》fileType 缺失 | 添加 `fileType` 参数，如 `"pdf"` |
| 400304 | 参数 link --》messageUrl 缺失 | 发送 link 类型消息时必须提供 `messageUrl` |
| 404 | 请求的 URI 地址不存在 | 检查 API URL 是否正确 |

---

## 支持的媒体类型

### 文件上传 (type=file)
- PDF: `.pdf`
- Word: `.doc`, `.docx`
- Excel: `.xls`, `.xlsx`
- PowerPoint: `.ppt`, `.pptx`
- 压缩文件: `.zip`, `.rar`
- 文本文件: `.txt`

### 图片上传 (type=image)
- JPEG: `.jpg`, `.jpeg`
- PNG: `.png`
- GIF: `.gif`
- BMP: `.bmp`

---

## 注意事项

1. **Access Token 有效期**: 7200 秒（2 小时），建议缓存并复用
2. **媒体文件有效期**: 上传后的媒体文件有有效期（通常 3 天），过期后 media_id 失效
3. **参数大小写**: `mediaId`、`fileType`、`fileName` 必须使用驼峰命名（大写 I/T/N）
4. **文件大小限制**: 钉钉对上传文件大小有限制（通常不超过 50MB）
5. **Webhook 限制**: 群聊机器人 webhook 只能发送到配置该 webhook 的群聊
6. **图片显示限制**: 钉钉 webhook 机器人发送的 `image` 类型消息在某些客户端可能无法显示图片预览
   - **原因**: `picURL` 需要公网可访问的图片 URL，钉钉内部 media 下载链接可能需要额外认证
   - **解决方案 1**: 将图片上传到公网图床（如阿里云 OSS、腾讯云 COS），使用公网 URL 发送
   - **解决方案 2**: 使用 Markdown 消息嵌入图片（部分客户端支持）
   - **解决方案 3**: 以 `file` 类型发送图片（作为附件，可以下载查看）

---

## 快速测试命令

```bash
# 发送文件
python3 -c "
import sys
sys.path.insert(0, '/Users/davidli/lobsterai/project/dingtalk-file-sender')
from dingtalk_sender import send_file_to_dingtalk
send_file_to_dingtalk('/path/to/your/file.pdf')
"

# 发送图片
python3 -c "
import sys
sys.path.insert(0, '/Users/davidli/lobsterai/project/dingtalk-file-sender')
from dingtalk_sender import send_image_to_dingtalk
send_image_to_dingtalk('/path/to/your/image.jpg')
"
```

---

**文档创建时间:** 2026-02-21
**最后更新:** 2026-02-21
