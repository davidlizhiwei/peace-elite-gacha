# 🚀 LobsterAI 钉钉消息接收 - 快速恢复指南

## 问题分析

你之前可以通过钉钉直接给 LobsterAI 发消息，我能收到并回复。但现在这个功能不工作了。

**原因**：LobsterAI 的钉钉配置缺少回调 URL 和端口配置，导致消息接收服务无法启动。

## 解决方案

### 方案 A：使用 LobsterAI 内置服务（推荐）

1. **配置已更新**
   - 我已经更新了 LobsterAI 数据库中的钉钉配置
   - 添加了回调 URL：`http://localhost:8888/dingtalk/callback`
   - 添加了端口：`8888`

2. **重启 LobsterAI**
   - 完全退出 LobsterAI 应用
   - 重新打开 LobsterAI

3. **启动内网穿透**
   ```bash
   # 安装 ngrok（如果还没有）
   brew install ngrok

   # 启动 ngrok
   ngrok http 8888
   ```

4. **配置钉钉后台**
   - 访问 https://open-dev.dingtalk.com/
   - 进入你的应用 → 事件订阅
   - 修改回调地址为 ngrok 提供的地址 + `/dingtalk/callback`
   - 例如：`https://xxx.ngrok.io/dingtalk/callback`
   - Token: `LOBSTER_AI_TOKEN`
   - 保存并验证

### 方案 B：使用独立服务（备选）

如果 LobsterAI 内置服务不工作，可以使用我创建的独立服务：

```bash
cd /Users/davidli/lobsterai/project/dingtalk-receiver

# 启动服务
node lobsterai-dingtalk-server.js
```

然后按照上述步骤 3-4 配置内网穿透和钉钉后台。

## 验证

1. 在钉钉上给应用发送：`你好`
2. 如果收到回复，说明配置成功！🎉

## 当前配置

- **App Key**: `dingdwlipjehprtrzc6s`
- **App Secret**: `oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL`
- **Token**: `LOBSTER_AI_TOKEN`
- **回调地址**: `http://localhost:8888/dingtalk/callback`
- **Webhook**: `https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf`

## 下一步：集成真实 AI

目前回复是预设的。要集成真实的 AI 处理能力，需要：

1. 在 LobsterAI 应用中实现钉钉消息处理逻辑
2. 或者在 `lobsterai-dingtalk-server.js` 的 `handleImMessage` 函数中调用 AI API

## 需要帮助？

如果遇到问题，请查看日志：
- LobsterAI 日志：`/Users/davidli/Library/Application Support/LobsterAI/logs/cowork.log`
- 独立服务日志：控制台输出
