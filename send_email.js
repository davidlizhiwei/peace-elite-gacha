#!/usr/bin/env node

const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

// 163 邮箱配置
const transporter = nodemailer.createTransport({
  host: 'smtp.163.com',
  port: 465,
  secure: true,
  auth: {
    user: 'davidlizhiwei@163.com',
    pass: 'DYLRfBYYkAmuaX2f',
  },
  tls: {
    rejectUnauthorized: false,
  },
  connectionTimeout: 30000,
  socketTimeout: 60000,
});

async function sendEmail() {
  // 读取 HTML 内容
  const htmlContent = fs.readFileSync(
    '/Users/davidli/lobsterai/project/shanghai_top10_attractions.html',
    'utf8'
  );

  const mailOptions = {
    from: '"David Li" <davidlizhiwei@163.com>',
    to: 'david.li.zhiwei@gmail.com',
    subject: '🏙️ 上海 Top 10 旅游景点推荐',
    html: htmlContent,
  };

  try {
    console.log('正在连接 SMTP 服务器...');
    await transporter.verify();
    console.log('SMTP 服务器连接成功！');

    console.log('正在发送邮件...');
    const info = await transporter.sendMail(mailOptions);
    console.log('✅ 邮件发送成功！');
    console.log('Message ID:', info.messageId);
    console.log('Response:', info.response);
  } catch (error) {
    console.error('❌ 发送失败:', error.message);
    throw error;
  }
}

// 重试逻辑
async function sendWithRetry(maxRetries = 3) {
  for (let i = 1; i <= maxRetries; i++) {
    try {
      console.log(`\n=== 尝试第 ${i} 次发送 (共 ${maxRetries} 次) ===`);
      await sendEmail();
      return true;
    } catch (error) {
      console.log(`第 ${i} 次尝试失败`);
      if (i < maxRetries) {
        const waitTime = i * 2000;
        console.log(`等待 ${waitTime}ms 后重试...\n`);
        await new Promise(resolve => setTimeout(resolve, waitTime));
      }
    }
  }
  return false;
}

sendWithRetry(3).then(success => {
  if (success) {
    console.log('\n🎉 邮件已成功发送！');
    process.exit(0);
  } else {
    console.log('\n❌ 所有重试均失败');
    process.exit(1);
  }
});
