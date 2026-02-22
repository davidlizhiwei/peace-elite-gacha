/**
 * CoinGecko Crypto Price API - 免费版
 * 无需 API Key，可直接使用
 *
 * 限制：
 * - 每月 10,000 次调用
 * - 每分钟 30 次调用
 * - 数据更新延迟约 60 秒
 */

const BASE_URL = 'https://api.coingecko.com/api/v3';

/**
 * 获取加密货币实时价格
 * @param {string[]} coinIds - 加密货币 ID 列表，如 ['bitcoin', 'ethereum']
 * @param {string} currency - 法币单位，如 'usd', 'cny'
 * @returns {Promise<Object>} 价格数据
 */
async function getCryptoPrices(coinIds = ['bitcoin'], currency = 'usd') {
  const ids = Array.isArray(coinIds) ? coinIds.join(',') : coinIds;
  const url = `${BASE_URL}/simple/price?ids=${ids}&vs_currencies=${currency}&include_24hr_vol=true&include_24hr_change=true`;

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
 * 获取所有支持的加密货币列表
 * @returns {Promise<Array>} 币种列表
 */
async function getCoinsList() {
  const url = `${BASE_URL}/coins/list`;
  const response = await fetch(url);
  return await response.json();
}

/**
 * 获取市场行情数据
 * @param {string} currency - 法币单位
 * @param {number} limit - 返回数量限制
 * @returns {Promise<Array>} 市场数据
 */
async function getMarketData(currency = 'usd', limit = 100) {
  const url = `${BASE_URL}/coins/markets?vs_currency=${currency}&order=market_cap_desc&per_page=${limit}&page=1&sparkline=false`;
  const response = await fetch(url);
  return await response.json();
}

/**
 * 获取全球加密货币市场概览
 * @returns {Promise<Object>} 全球市场数据
 */
async function getGlobalMarketData() {
  const url = `${BASE_URL}/global`;
  const response = await fetch(url);
  return await response.json();
}

// ============ 使用示例 ============

async function main() {
  console.log('=== CoinGecko Crypto Price API ===\n');

  // 1. 获取比特币、以太坊、Solana 价格
  console.log('1. 获取主流币种价格:');
  const prices = await getCryptoPrices(['bitcoin', 'ethereum', 'solana'], 'usd');
  console.log('Bitcoin:', `$${prices.bitcoin.usd.toLocaleString()} (+${prices.bitcoin.usd_24h_change.toFixed(2)}%)`);
  console.log('Ethereum:', `$${prices.ethereum.usd.toLocaleString()} (+${prices.ethereum.usd_24h_change.toFixed(2)}%)`);
  console.log('Solana:', `$${prices.solana.usd.toLocaleString()} (+${prices.solana.usd_24h_change.toFixed(2)}%)`);
  console.log('');

  // 2. 获取市场前 10 大币种
  console.log('2. 市场前 10 大币种:');
  const marketData = await getMarketData('usd', 10);
  marketData.forEach((coin, index) => {
    console.log(`${index + 1}. ${coin.name} (${coin.symbol.toUpperCase()}): $${coin.current_price.toLocaleString()}`);
  });
  console.log('');

  // 3. 获取全球市场概览
  console.log('3. 全球市场概览:');
  const global = await getGlobalMarketData();
  console.log('总币种数量:', global.data.active_cryptocurrencies);
  console.log('总交易所数量:', global.data.markets);
  console.log('全球市值:', `$${(global.data.total_market_volume.usd / 1e12).toFixed(2)}T`);
}

// 导出函数供其他模块使用
module.exports = { getCryptoPrices, getCoinsList, getMarketData, getGlobalMarketData };

// 如果直接运行此文件则执行 main 函数
if (require.main === module) {
  main().catch(console.error);
}
