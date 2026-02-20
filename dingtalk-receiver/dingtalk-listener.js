#!/usr/bin/env node
/**
 * LobsterAI 钉钉消息监听器
 * 接收钉钉推送的 IM 消息并转发给 LobsterAI 处理
 *
 * 使用方法：
 * 1. 启动服务：node dingtalk-listener.js
 * 2. 使用 ngrok 暴露到公网：ngrok http 9999
 * 3. 在钉钉后台配置回调地址：https://xxx.ngrok.io/dingtalk/callback
 */

const http = require('http');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// ========== 配置 ==========
const CONFIG = {
    port: 9999,
    host: '0.0.0.0',
    token: 'LOBSTER_AI_TOKEN',  // 需要与钉钉后台配置的 Token 一致
    appKey: 'dingdwlipjehprtrzc6s',
    appSecret: 'oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL',
    webhook: 'https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf'
};

// 消息队列目录
const MESSAGES_DIR = path.join(__dirname, 'messages');
const INCOMING_DIR = path.join(MESSAGES_DIR, 'incoming');
const PROCESSED_DIR = path.join(MESSAGES_DIR, 'processed');

// 确保目录存在
[MESSAGES_DIR, INCOMING_DIR, PROCESSED_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
});

// ========== 工具函数 ==========

// 日志
function log(message, level = 'INFO') {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [${level}] ${message}`);
}

// 验证签名
function verifySignature(timestamp, nonce, signature) {
    const checkSignature = [CONFIG.token, timestamp, nonce].sort().join('');
    const sha1 = crypto.createHash('sha1');
    sha1.update(checkSignature);
    const encrypt = sha1.digest('hex');
    return encrypt === signature;
}

// 获取访问令牌
let accessTokenCache = null;
let accessTokenExpireTime = 0;

async function getAccessToken() {
    const now = Date.now();
    if (accessTokenCache && now < accessTokenExpireTime) {
        return accessTokenCache;
    }

    try {
        const url = `https://oapi.dingtalk.com/gettoken?appkey=${CONFIG.appKey}&appsecret=${CONFIG.appSecret}`;
        const response = await fetch(url);
        const result = await response.json();

        if (result.errcode === 0) {
            accessTokenCache = result.access_token;
            accessTokenExpireTime = now + 7200000 - 1000000; // 7200 秒有效期，提前 1000 秒刷新
            log(`获取 access_token 成功`);
            return accessTokenCache;
        } else {
            log(`获取 access_token 失败：${JSON.stringify(result)}`, 'ERROR');
            return null;
        }
    } catch (error) {
        log(`获取 access_token 异常：${error.message}`, 'ERROR');
        return null;
    }
}

// 发送消息到钉钉
async function sendToDingTalk(conversationId, content) {
    try {
        const accessToken = await getAccessToken();
        if (!accessToken) {
            log('无法获取 access_token', 'ERROR');
            return false;
        }

        const url = `https://oapi.dingtalk.com/topapi/chat/send?access_token=${accessToken}`;

        const payload = {
            chatid: conversationId,
            msgtype: 'text',
            text: { content }
        };

        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (result.errcode === 0) {
            log(`消息发送成功到会话：${conversationId}`);
            return true;
        } else {
            log(`消息发送失败：${JSON.stringify(result)}`, 'ERROR');
            return false;
        }
    } catch (error) {
        log(`发送消息异常：${error.message}`, 'ERROR');
        return false;
    }
}

// 保存消息到队列
function saveMessage(messageData) {
    const messageId = messageData.message_id || Date.now().toString();
    const filePath = path.join(INCOMING_DIR, `${messageId}.json`);
    fs.writeFileSync(filePath, JSON.stringify(messageData, null, 2), 'utf-8');
    log(`消息已保存到队列：${filePath}`);
    return filePath;
}

// 生成 AI 回复
function generateReply(text, senderNick) {
    const lowerText = text.toLowerCase();
    const now = new Date();
    const timeStr = now.toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });

    if (lowerText.includes('你好') || lowerText.includes('hello') || lowerText.includes('hi') || lowerText.includes('哈喽')) {
        return `👋 你好 ${senderNick}！\n\n我是 LobsterAI，你的智能助手。\n有什么我可以帮助你的吗？\n\n我可以帮你：\n• 回答问题\n• 编写代码\n• 分析文档\n• 创建报表\n• 查询时间日期`;
    }

    if (lowerText.includes('时间') || lowerText.includes('几点')) {
        return `🕐 当前时间是：${timeStr}\n\n时区：Asia/Shanghai`;
    }

    if (lowerText.includes('日期') || lowerText.includes('几号') || lowerText.includes('今天') || lowerText.includes('明天')) {
        const dateStr = now.toLocaleDateString('zh-CN', { timeZone: 'Asia/Shanghai', year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' });
        return `📅 今天是：${dateStr}`;
    }

    if (lowerText.includes('帮助') || lowerText.includes('help') || lowerText.includes('功能') || lowerText.includes('能做什么')) {
        return `🤖 LobsterAI 帮助菜单\n\n可用的命令：\n• 你好 - 打招呼\n• 时间 - 查询当前时间\n• 日期 - 查询当前日期\n• 帮助 - 显示帮助信息\n\n更多功能正在开发中...`;
    }

    if (lowerText.includes('谢谢') || lowerText.includes('thank')) {
        return `😊 不客气！如果有任何问题，随时找我~`;
    }

    if (lowerText.includes('再见') || lowerText.includes('bye')) {
        return `👋 再见！期待下次与你交流~`;
    }

    // 通用回复
    return `🤖 LobsterAI 已收到您的消息\n\n📝 发送者：${senderNick}\n💬 内容：${text.substring(0, 100)}${text.length > 100 ? '...' : ''}\n\n✅ 消息已成功接收！\n\n我目前还在学习中，完整的 AI 对话功能正在开发中。\n当前支持：\n• 打招呼（你好）\n• 查时间（时间）\n• 查日期（日期）\n• 看帮助（帮助）`;
}

// 处理 IM 消息
async function handleImMessage(content) {
    try {
        const senderId = content.senderId;
        const senderNick = content.senderNick || '未知用户';
        const conversationId = content.conversationId;
        const conversationType = content.conversationType; // 1: 单聊，2: 群聊
        const msgType = content.msgtype;

        // 提取文本内容
        let text = '';
        if (msgType === 'text') {
            text = content.text?.content || '';
        } else if (msgType === 'richText') {
            text = content.richText?.map(r => r.content || '').join('') || '';
        } else if (msgType === 'markdown') {
            text = content.markdown?.content || '';
        }

        log(`收到消息 - 发送者：${senderNick}, 类型：${msgType}, 会话类型：${conversationType}`);
        log(`消息内容：${text.substring(0, 100)}${text.length > 100 ? '...' : ''}`);

        // 保存消息到队列
        const messageData = {
            message_id: `msg_${Date.now()}`,
            sender_id: senderId,
            sender_nick: senderNick,
            conversation_id: conversationId,
            conversation_type: conversationType,
            msg_type: msgType,
            content: text,
            timestamp: new Date().toISOString(),
            status: 'pending'
        };
        saveMessage(messageData);

        // 生成并发送回复
        const reply = generateReply(text, senderNick);
        if (conversationId && reply) {
            await sendToDingTalk(conversationId, reply);
        }

        log(`消息处理完成`);
    } catch (error) {
        log(`处理消息失败：${error.message}`, 'ERROR');
    }
}

// ========== HTTP 服务器 ==========

const server = http.createServer((req, res) => {
    const url = new URL(req.url, `http://${req.headers.host}`);

    // 设置 CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }

    if (url.pathname === '/dingtalk/callback') {
        if (req.method === 'GET') {
            // 验证回调
            const signature = url.searchParams.get('signature');
            const timestamp = url.searchParams.get('timestamp');
            const nonce = url.searchParams.get('nonce');

            log(`收到 GET 验证请求 - signature: ${signature?.substring(0, 10)}...`);

            if (verifySignature(timestamp, nonce, signature)) {
                log('签名验证成功 ✓');
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ code: 0, message: 'success' }));
            } else {
                log('签名验证失败 ✗', 'WARN');
                res.writeHead(403, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ code: -1, message: 'signature verify failed' }));
            }
        } else if (req.method === 'POST') {
            // 处理事件推送
            let body = '';
            req.on('data', chunk => {
                body += chunk.toString();
            });
            req.on('end', async () => {
                try {
                    const signature = url.searchParams.get('signature');
                    const timestamp = url.searchParams.get('timestamp');
                    const nonce = url.searchParams.get('nonce');

                    log(`收到 POST 请求`);

                    if (!verifySignature(timestamp, nonce, signature)) {
                        log('签名验证失败 ✗', 'WARN');
                        res.writeHead(403, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ code: -1, message: 'signature verify failed' }));
                        return;
                    }

                    const data = JSON.parse(body);
                    log(`收到事件：${JSON.stringify(data, null, 2).substring(0, 500)}...`);

                    // 处理事件
                    const eventType = data.EventType;
                    if (eventType === 'im') {
                        log('收到 IM 消息事件');
                        await handleImMessage(data.content);
                    } else {
                        log(`其他事件类型：${eventType}`);
                    }

                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ code: 0, message: 'success' }));
                } catch (error) {
                    log(`处理请求失败：${error.message}`, 'ERROR');
                    res.writeHead(500, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ code: -1, message: error.message }));
                }
            });
        } else {
            res.writeHead(405, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ code: -1, message: 'Method not allowed' }));
        }
    } else if (url.pathname === '/health') {
        // 健康检查
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'ok', timestamp: new Date().toISOString() }));
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found\n\nAvailable endpoints:\n- GET/POST /dingtalk/callback\n- GET /health');
    }
});

// 启动服务器
server.listen(CONFIG.port, CONFIG.host, () => {
    console.log('');
    console.log('╔═══════════════════════════════════════════════════════════╗');
    console.log('║     LobsterAI 钉钉消息监听器启动成功！                     ║');
    console.log('╠═══════════════════════════════════════════════════════════╣');
    console.log(`║  本地地址：http://localhost:${CONFIG.port}/dingtalk/callback        ║`);
    console.log(`║  Token: ${CONFIG.token.padEnd(20, ' ')}                          ║`);
    console.log('╠═══════════════════════════════════════════════════════════╣');
    console.log('║  下一步配置：                                              ║');
    console.log('║  1. 启动内网穿透：ngrok http 9999                          ║');
    console.log('║  2. 在钉钉后台配置回调地址：                               ║');
    console.log('║     https://xxx.ngrok.io/dingtalk/callback                 ║');
    console.log('║  3. Token 配置为：LOBSTER_AI_TOKEN                            ║');
    console.log('║  4. 订阅事件：IM 消息                                        ║');
    console.log('╚═══════════════════════════════════════════════════════════╝');
    console.log('');
    log('服务已启动，等待钉钉消息...');
});

// 优雅退出
process.on('SIGINT', () => {
    log('收到退出信号，正在关闭...');
    server.close(() => {
        log('服务已停止');
        process.exit(0);
    });
});
