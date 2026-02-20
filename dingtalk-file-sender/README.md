# 钉钉机器人发送文件实现指南

## 概述

钉钉机器人发送文件需要两个步骤：
1. **上传文件** - 调用上传接口获取 `media_id`
2. **发送消息** - 使用 `media_id` 发送文件消息到群聊

## 前置准备

### 1. 创建钉钉机器人

1. 登录 [钉钉开发者后台](https://open-dev.dingtalk.com/)
2. 创建企业内部应用
3. 添加「机器人」应用能力
4. 获取以下信息：
   - `client_id` (AppKey)
   - `client_secret` (AppSecret)
   - 机器人 Webhook URL（如使用 webhook 方式）

### 2. 权限配置

确保应用有以下权限：
- 群机器人消息发送权限
- 文件上传权限

## API 说明

### 上传文件接口

```
POST https://api.dingtalk.com/v1.0/robot/messageFiles/upload
```

**请求头：**
```
x-acs-dingtalk-access-token: <access_token>
Content-Type: multipart/form-data
```

**请求体：**
- `file`: 要上传的文件（二进制）

**响应：**
```json
{
  "mediaId": "xxx",
  "fileName": "example.pdf"
}
```

### 发送文件消息接口

```
POST https://api.dingtalk.com/v1.0/robot/messageFiles/send
```

**请求头：**
```
x-acs-dingtalk-access-token: <access_token>
Content-Type: application/json
```

**请求体：**
```json
{
  "robotCode": "<robotCode>",
  "msgKey": "sampleFile",
  "msgParam": {
    "mediaId": "<media_id>",
    "fileName": "<file_name>"
  },
  "conversationId": "<conversation_id>"
}
```

## Access Token 获取

```
POST https://api.dingtalk.com/v1.0/oauth2/accessToken
```

**请求体：**
```json
{
  "appKey": "<client_id>",
  "appSecret": "<client_secret>"
}
```

**响应：**
```json
{
  "accessToken": "xxx",
  "expireIn": 7200
}
```

## 文件大小限制

- 普通文件：最大 20MB
- 支持格式：pdf, doc, docx, xls, xlsx, ppt, pptx, jpg, png, zip 等

## 注意事项

1. `media_id` 有效期为 3 天
2. 文件消息只能发送到群聊
3. 需要获取群聊的 `conversationId`
4. access_token 有效期为 2 小时，建议缓存复用
