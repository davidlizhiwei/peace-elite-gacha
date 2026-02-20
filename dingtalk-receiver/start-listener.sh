#!/bin/bash

# LobsterAI 钉钉消息监听器启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     LobsterAI 钉钉消息监听器                               ║"
echo "╠═══════════════════════════════════════════════════════════╣"
echo "║  检查依赖...                                               ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误：未找到 Node.js"
    echo "请先安装 Node.js: brew install node"
    exit 1
fi
echo "✓ Node.js 版本：$(node --version)"

# 创建消息目录
mkdir -p messages/{incoming,processed}

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  启动服务...                                               ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# 启动服务
node dingtalk-listener.js
