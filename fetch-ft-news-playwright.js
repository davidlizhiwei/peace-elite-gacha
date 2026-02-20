#!/usr/bin/env node

/**
 * 使用 Playwright 直接访问 FT.com 获取最新新闻
 * 这样可以确保获取的是最新真实的新闻
 */

const { chromium } = require('playwright');

async function fetchFTNews() {
  console.log('🚀 启动浏览器访问 FT.com...\n');

  let browser;
  try {
    // 启动浏览器
    browser = await chromium.launch({
      headless: true,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage'
      ]
    });

    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });

    const page = await context.newPage();

    // 访问 FT.com 世界新闻页面
    console.log('📰 访问 FT.com 世界新闻页面...');
    await page.goto('https://www.ft.com/world', {
      waitUntil: 'networkidle',
      timeout: 60000
    });

    // 等待页面加载
    await page.waitForTimeout(3000);

    // 尝试接受 Cookie（如果有弹窗）
    try {
      await page.click('button[data-notice="accept"]', { timeout: 2000 });
      console.log('✅ 接受 Cookie');
    } catch (e) {
      // 没有 Cookie 弹窗，继续
    }

    // 提取新闻链接
    const newsItems = await page.evaluate(() => {
      const items = [];

      // 查找 FT.com 的文章链接
      const links = document.querySelectorAll('a[href*="/content/"]');

      links.forEach(link => {
        const href = link.href;
        const title = link.textContent?.trim() || '';

        // 确保是内容页面，不是列表页
        if (href.includes('/content/') &&
            !href.includes('?') &&
            title.length > 10 &&
            title.length < 200) {
          items.push({
            title: title.replace(/\s+/g, ' '),
            url: href
          });
        }
      });

      return items;
    });

    // 去重
    const uniqueNews = [];
    const seenUrls = new Set();

    for (const item of newsItems) {
      if (!seenUrls.has(item.url) && item.title) {
        uniqueNews.push(item);
        seenUrls.add(item.url);
      }
    }

    console.log(`✅ 获取到 ${uniqueNews.length} 条新闻\n`);

    // 显示前 10 条
    console.log('📋 最新新闻列表:');
    uniqueNews.slice(0, 10).forEach((item, index) => {
      console.log(`${index + 1}. ${item.title}`);
      console.log(`   链接：${item.url}\n`);
    });

    return uniqueNews.slice(0, 15);

  } catch (error) {
    console.error('❌ 错误:', error.message);
    throw error;
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

// 运行
fetchFTNews().then(news => {
  console.log('\n✅ 完成！共获取', news.length, '条新闻');
  process.exit(0);
}).catch(err => {
  console.error('失败:', err.message);
  process.exit(1);
});
