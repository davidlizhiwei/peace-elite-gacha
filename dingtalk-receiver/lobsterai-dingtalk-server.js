#!/usr/bin/env node
/**
 * LobsterAI 钉钉消息接收服务器
 * 接收钉钉推送的 IM 消息并转发给 LobsterAI 处理
 */

const http = require('http');
const crypto = require('crypto');
const path = require('path');
const fs = require('fs');

// 配置
const CONFIG = {
    port: 8888,
    host: 'localhost',
    token: 'LOBSTER_AI_TOKEN',
    appKey: 'dingdwlipjehprtrzc6s',
    appSecret: 'oNDrxvKBzScD7VdXH--aBWke4F2230Im4sDvvTZawsaN2o-1mmVIlOUDCr3Pn1GL',
    webhook: 'https://oapi.dingtalk.com/robot/send?access_token=a28857b2fb6219f617702dda638035351329fd6dd4fdcc8ac875f4ff8fb698bf'
};

// 钉钉配置路径
const DINGTALK_CONFIG_PATH = path.join(
    process.env.HOME,
    'Library/Application Support/LobsterAI/dingtalk-config.json'
);

// 保存配置
function saveDingtalkConfig(config) {
    const dir = path.dirname(DINGTALK_CONFIG_PATH);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(DINGTALK_CONFIG_PATH, JSON.stringify(config, null, 2));
}

// 加载配置
function loadDingtalkConfig() {
    if (fs.existsSync(DINGTALK_CONFIG_PATH)) {
        return JSON.parse(fs.readFileSync(DINGTALK_CONFIG_PATH, 'utf-8'));
    }
    return null;
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
async function getAccessToken() {
    const config = loadDingtalkConfig();
    if (config && config.accessToken && config.tokenExpireTime > Date.now()) {
        return config.accessToken;
    }

    try {
        const url = `https://oapi.dingtalk.com/gettoken?appkey=${CONFIG.appKey}&appsecret=${CONFIG.appSecret}`;
        const response = await fetch(url);
        const result = await response.json();

        if (result.errcode === 0) {
            const accessToken = result.access_token;
            saveDingtalkConfig({
                accessToken,
                tokenExpireTime: Date.now() + 7200000 - 1000000 // 7200 秒有效期，提前 1000 秒刷新
            });
            console.log(`[${new Date().toISOString()}] 获取 access_token 成功`);
            return accessToken;
        } else {
            console.error(`[${new Date().toISOString()}] 获取 access_token 失败:`, result);
            return null;
        }
    } catch (error) {
        console.error(`[${new Date().toISOString()}] 获取 access_token 异常:`, error.message);
        return null;
    }
}

// 发送消息到钉钉
async function sendToDingTalk(conversationId, content) {
    try {
        const accessToken = await getAccessToken();
        if (!accessToken) {
            console.error('无法获取 access_token');
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
            console.log(`[${new Date().toISOString()}] 消息发送成功到会话：${conversationId}`);
            return true;
        } else {
            console.error(`[${new Date().toISOString()}] 消息发送失败:`, result);
            return false;
        }
    } catch (error) {
        console.error(`[${new Date().toISOString()}] 发送消息异常:`, error.message);
        return false;
    }
}

// 处理 IM 消息
async function handleImMessage(content) {
    try {
        const senderNick = content.senderNick || '未知用户';
        const text = content.text?.content || content.richText?.map(r => r.content || '').join('') || '';
        const conversationId = content.conversationId;
        const conversationType = content.conversationType; // 1: 单聊，2: 群聊

        console.log(`[${new Date().toISOString()}] 收到消息 - 发送者：${senderNick}, 内容：${text.substring(0, 50)}...`);

        // TODO: 这里需要调用 LobsterAI 来处理消息
        // 目前 LobsterAI 是通过 Claude Code 运行的，可以通过以下方式集成：
        // 1. 写入消息队列文件，让 LobsterAI 轮询处理
        // 2. 通过 LobsterAI 的 API 调用
        // 3. 直接调用 LobsterAI 的处理模块

        // 临时实现：生成一个简单回复
        const reply = generateReply(text, senderNick);

        // 发送回复
        if (conversationId && reply) {
            await sendToDingTalk(conversationId, reply);
        }
    } catch (error) {
        console.error(`[${new Date().toISOString()}] 处理消息失败:`, error.message);
    }
}

// 生成回复
function generateReply(text, senderNick) {
    const lowerText = text.toLowerCase();

    if (lowerText.includes('你好') || lowerText.includes('hello') || lowerText.includes('hi')) {
        return `👋 你好 ${senderNick}！\n\n我是 LobsterAI，你的智能助手。\n有什么我可以帮助你的吗？`;
    }

    if (lowerText.includes('时间') || lowerText.includes('几点')) {
        const now = new Date();
        return `🕐 当前时间是：${now.toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`;
    }

    if (lowerText.includes('日期') || lowerText.includes('几号')) {
        const now = new Date();
        return `📅 今天是：${now.toLocaleDateString('zh-CN', { timeZone: 'Asia/Shanghai' })}`;
    }

    if (lowerText.includes('帮助') || lowerText.includes('help')) {
        return `🤖 LobsterAI 帮助菜单\n\n可用的命令：\n• 你好 - 打招呼\n• 时间 - 查询当前时间\n• 日期 - 查询当前日期\n• 帮助 - 显示帮助信息`;
    }

    // 通用回复
    return `🤖 LobsterAI 回复\n\n${senderNick}，我收到了你的消息：\n\n> ${text}\n\n✅ 消息已成功接收和处理！`;
}

// 创建 HTTP 服务器
const server = http.createServer((req, res) => {
    const url = new URL(req.url, `http://${req.headers.host}`);

    if (url.pathname === '/dingtalk/callback') {
        if (req.method === 'GET') {
            // 验证回调
            const signature = url.searchParams.get('signature');
            const timestamp = url.searchParams.get('timestamp');
            const nonce = url.searchParams.get('nonce');

            console.log(`[${new Date().toISOString()}] 收到 GET 验证请求`);

            if (verifySignature(timestamp, nonce, signature)) {
                console.log(`[${new Date().toISOString()}] 签名验证成功`);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ code: 0, message: 'success' }));
            } else {
                console.log(`[${new Date().toISOString()}] 签名验证失败`);
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

                    console.log(`[${new Date().toISOString()}] 收到 POST 请求`);

                    if (!verifySignature(timestamp, nonce, signature)) {
                        console.log(`[${new Date().toISOString()}] 签名验证失败`);
                        res.writeHead(403, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ code: -1, message: 'signature verify failed' }));
                        return;
                    }

                    const data = JSON.parse(body);
                    console.log(`[${new Date().toISOString()}] 收到消息:`, JSON.stringify(data, null, 2));

                    // 处理事件
                    const eventType = data.EventType;
                    if (eventType === 'im') {
                        await handleImMessage(data.content);
                    }

                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ code: 0, message: 'success' }));
                } catch (error) {
                    console.error(`[${new Date().toISOString()}] 处理消息失败:`, error.message);
                    res.writeHead(500, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ code: -1, message: error.message }));
                }
            });
        } else {
            res.writeHead(405, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ code: -1, message: 'Method not allowed' }));
        }
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
    }
});

// 启动服务器
server.listen(CONFIG.port, CONFIG.host, () => {
    console.log('==================================================');
    console.log('LobsterAI 钉钉消息接收服务器启动成功！');
    console.log('==================================================');
    console.log(`回调地址：http://${CONFIG.host}:${CONFIG.port}/dingtalk/callback`);
    console.log(`Token: ${CONFIG.token}`);
    console.log('==================================================');
    console.log('请在钉钉开发者后台配置：');
    console.log(`1. 回调地址：http://<你的公网地址>:${CONFIG.port}/dingtalk/callback`);
    console.log(`2. Token: ${CONFIG.token}`);
    console.log('3. 订阅事件：IM 消息');
    console.log('==================================================');
    console.log('如需公网访问，请使用内网穿透工具（如 ngrok）:');
    console.log(`ngrok http ${CONFIG.port}`);
    console.log('==================================================');
});
