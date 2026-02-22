/**
 * 贵金属价格 API - 免费版
 * 无需 API Key，可直接使用
 *
 * 支持:
 * - 黄金 (XAU)
 * - 白银 (XAG)
 * - 铂金 (XPT)
 * - 钯金 (XPD)
 */

const BASE_URL = 'https://api.gold-api.com/price';

/**
 * 获取贵金属价格
 * @param {string} symbol - 贵金属代码 (XAU, XAG, XPT, XPD)
 * @returns {Promise<Object>} 价格数据
 */
async function getMetalPrice(symbol = 'XAU') {
  const url = `${BASE_URL}/${symbol}`;

  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('获取价格失败:', error.message);
    throw error;
  }
}

/**
 * 获取所有贵金属价格
 * @returns {Promise<Object[]>} 所有价格数据
 */
async function getAllMetalPrices() {
  const symbols = ['XAU', 'XAG', 'XPT', 'XPD'];
  const prices = [];

  for (const symbol of symbols) {
    try {
      const data = await getMetalPrice(symbol);
      prices.push(data);
    } catch (error) {
      console.error(`获取 ${symbol} 价格失败:`, error.message);
    }
  }

  return prices;
}

/**
 * 格式化价格显示
 * @param {Object} data - 价格数据
 * @returns {string} 格式化后的字符串
 */
function formatPrice(data) {
  const names = {
    'XAU': '黄金',
    'XAG': '白银',
    'XPT': '铂金',
    'XPD': '钯金'
  };

  const name = names[data.symbol] || data.name;
  const price = data.price.toFixed(2);
  const time = new Date(data.updatedAt).toLocaleString('zh-CN');

  return `${name}: $${price}/盎司 (更新于 ${time})`;
}

// ============ 使用示例 ============

async function main() {
  console.log('=== 贵金属实时价格 ===\n');

  // 1. 获取单个金属价格
  console.log('1. 黄金价格:');
  const gold = await getMetalPrice('XAU');
  console.log(formatPrice(gold));
  console.log('');

  // 2. 获取所有贵金属价格
  console.log('2. 所有贵金属价格:');
  const allPrices = await getAllMetalPrices();
  console.log('┌────────────┬─────────────────┬──────────────────────┐');
  console.log('│ 金属       │ 价格 (USD)      │ 更新时间             │');
  console.log('├────────────┼─────────────────┼──────────────────────┤');
  allPrices.forEach(metal => {
    const name = (metal.symbol + ' - ' + metal.name).padEnd(10);
    const price = `$${metal.price.toFixed(2)}`.padEnd(15);
    const time = new Date(metal.updatedAt).toLocaleString('zh-CN').padEnd(20);
    console.log(`│ ${name} │ ${price} │ ${time} │`);
  });
  console.log('└────────────┴─────────────────┴──────────────────────┘');
  console.log('');

  // 3. 金银比
  const goldPrice = allPrices.find(p => p.symbol === 'XAU')?.price;
  const silverPrice = allPrices.find(p => p.symbol === 'XAG')?.price;
  if (goldPrice && silverPrice) {
    const ratio = (goldPrice / silverPrice).toFixed(2);
    console.log(`金银比：${ratio}:1 (1 盎司黄金 = ${ratio} 盎司白银)`);
  }
}

// 导出函数
module.exports = { getMetalPrice, getAllMetalPrices, formatPrice };

// 直接运行则执行 main
if (require.main === module) {
  main().catch(console.error);
}
