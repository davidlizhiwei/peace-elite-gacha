# CoinGecko 加密货币价格 API 配置说明

## 📊 数据源信息

**提供商**: CoinGecko
**计划**: Demo (免费版)
**价格**: $0/月
**数据延迟**: 约 60 秒

## 🎯 调用限制

| 限制项 | 数值 |
|--------|------|
| 每月调用次数 | 10,000 次 |
| 每分钟调用次数 | 30 次 |
| 数据更新频率 | 60 秒 |
| 需要 API Key | ❌ 否 |

## 📁 配置文件

- **配置路径**: `./crypto-api-config.json`
- **API 基础 URL**: `https://api.coingecko.com/api/v3`

## 🚀 快速开始

### 方法 1: 使用 curl 命令

```bash
# 获取单个币种价格
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

# 获取多个币种价格（推荐）
curl "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true"

# 获取市场行情前 100 大币种
curl "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1"

# 获取全球市场概览
curl "https://api.coingecko.com/api/v3/global"
```

### 方法 2: 使用 JavaScript

```javascript
const BASE_URL = 'https://api.coingecko.com/api/v3';

// 获取价格
async function getPrice(coinIds) {
  const url = `${BASE_URL}/simple/price?ids=${coinIds.join(',')}&vs_currencies=usd`;
  const res = await fetch(url);
  return await res.json();
}

// 使用示例
const prices = await getPrice(['bitcoin', 'ethereum']);
console.log(prices);
```

### 方法 3: 使用 Python

```python
import requests

BASE_URL = 'https://api.coingecko.com/api/v3'

# 获取价格
def get_price(coin_ids):
    url = f"{BASE_URL}/simple/price"
    params = {
        'ids': ','.join(coin_ids),
        'vs_currencies': 'usd',
        'include_24hr_vol': 'true',
        'include_24hr_change': 'true'
    }
    response = requests.get(url, params=params)
    return response.json()

# 使用示例
prices = get_price(['bitcoin', 'ethereum', 'solana'])
print(prices)
```

## 📝 常用 API 端点

### 1. 简单价格查询
```
GET /simple/price
参数:
  - ids: 币种 ID 列表（逗号分隔）
  - vs_currencies: 法币单位（逗号分隔，如 usd,cny）
  - include_24hr_vol: 包含 24h 交易量 (true/false)
  - include_24hr_change: 包含 24h 涨跌幅 (true/false)
  - include_market_cap: 包含市值 (true/false)
```

### 2. 市场行情
```
GET /coins/markets
参数:
  - vs_currency: 法币单位
  - order: 排序方式 (market_cap_desc, volume_desc, etc.)
  - per_page: 每页数量 (最大 250)
  - page: 页码
  - sparkline: 是否包含 K 线数据 (true/false)
```

### 3. 币种列表
```
GET /coins/list
返回所有支持的币种及其 ID
```

### 4. 全球市场数据
```
GET /global
返回全球加密货币市场总览
```

## 🔍 常用币种 ID

| 币种名称 | CoinGecko ID |
|---------|-------------|
| Bitcoin | bitcoin |
| Ethereum | ethereum |
| Tether | tether |
| BNB | binancecoin |
| Solana | solana |
| XRP | ripple |
| USDC | usd-coin |
| Cardano | cardano |
| Dogecoin | dogecoin |
| Polkadot | polkadot |
| TRON | tron |
| Avalanche | avalanche-2 |

👉 **完整列表**: https://api.coingecko.com/api/v3/coins/list

## ⚠️ 注意事项

1. **品牌标识要求**: 免费版需要在应用中显示 "数据来源于 CoinGecko"
2. **速率限制**: 超过限制会返回 HTTP 429 错误
3. **数据延迟**: 免费版数据约有 60 秒延迟
4. **生产环境**: 如需更频繁调用，建议升级到付费计划

## 📈 升级到付费计划

如需更高频率的调用和实时数据，可考虑升级：

| 计划 | 价格/月 | 调用次数/月 | 速率限制 | 数据延迟 |
|------|---------|------------|---------|---------|
| Demo | $0 | 10k | 30/min | 60 秒 |
| Basic | $29 | 100k | 250/min | 10 秒 |
| Analyst | $103.2 | 500k | 500/min | 实时 |

升级链接：https://www.coingecko.com/en/api/pricing

## 🛠️ 错误处理

```javascript
async function safeFetch(url) {
  try {
    const response = await fetch(url);
    if (response.status === 429) {
      console.error('超过速率限制，请稍后重试');
      return null;
    }
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('API 调用失败:', error.message);
    return null;
  }
}
```

## 📞 技术支持

- **API 文档**: https://docs.coingecko.com
- **帮助中心**: https://support.coingecko.com
- **状态页面**: https://status.coingecko.com

---

**最后更新**: 2026-02-21
**配置状态**: ✅ 已完成并测试通过
