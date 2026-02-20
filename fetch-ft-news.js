#!/usr/bin/env node

/**
 * 从 FT.com 获取真实新闻
 * 使用 Playwright 访问 FT.com 并提取新闻标题和链接
 */

const https = require('https');
const http = require('http');

// FT.com API 端点（公开可用的 RSS 和 API）
const FT_FEED_URLS = [
  'https://www.ft.com/world?format=rss',
  'https://www.ft.com/companies?format=rss',
  'https://www.ft.com/technology?format=rss',
  'https://www.ft.com/markets?format=rss'
];

// 解析 RSS feed
function parseRSS(xml) {
  const items = [];
  const itemRegex = /<item>([\s\S]*?)<\/item>/g;
  const titleRegex = /<title>([^<]*)<\/title>/;
  const linkRegex = /<link>([^<]*)<\/link>/;
  const descRegex = /<description>([\s\S]*?)<\/description>/;
  const pubDateRegex = /<pubDate>([^<]*)<\/pubDate>/;

  let match;
  while ((match = itemRegex.exec(xml)) !== null) {
    const itemContent = match[1];
    const titleMatch = titleRegex.exec(itemContent);
    const linkMatch = linkRegex.exec(itemContent);
    const descMatch = descRegex.exec(itemContent);
    const pubDateMatch = pubDateRegex.exec(itemContent);

    if (titleMatch && linkMatch) {
      items.push({
        title: titleMatch[1],
        url: linkMatch[1],
        summary: descMatch ? descMatch[1].replace(/<[^>]*>/g, '') : '',
        pubDate: pubDateMatch ? pubDateMatch[1] : ''
      });
    }
  }

  return items;
}

// 获取 RSS feed
function fetchRSS(url) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;

    lib.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

// 主函数
async function main() {
  console.log('📰 正在获取 FT.com 最新新闻...\n');

  try {
    // 获取世界新闻
    const worldFeed = await fetchRSS('https://www.ft.com/world?format=rss');
    const worldNews = parseRSS(worldFeed);

    // 获取公司新闻
    const companiesFeed = await fetchRSS('https://www.ft.com/companies?format=rss');
    const companiesNews = parseRSS(companiesFeed);

    // 获取科技新闻
    const techFeed = await fetchRSS('https://www.ft.com/technology?format=rss');
    const techNews = parseRSS(techFeed);

    // 获取市场新闻
    const marketsFeed = await fetchRSS('https://www.ft.com/markets?format=rss');
    const marketsNews = parseRSS(marketsFeed);

    // 合并并去重
    const allNews = [...worldNews, ...companiesNews, ...techNews, ...marketsNews];
    const uniqueNews = allNews.filter((v, i, a) =>
      a.findIndex(t => t.url === v.url) === i
    ).slice(0, 15);

    console.log(`✅ 获取到 ${uniqueNews.length} 条新闻\n`);
    console.log('📋 新闻列表:\n');

    uniqueNews.forEach((item, index) => {
      console.log(`${index + 1}. ${item.title}`);
      console.log(`   链接：${item.url}`);
      console.log(`   时间：${item.pubDate}`);
      console.log('');
    });

    // 返回 JSON
    console.log('\n📦 JSON 数据:');
    console.log(JSON.stringify(uniqueNews, null, 2));

  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

main();
