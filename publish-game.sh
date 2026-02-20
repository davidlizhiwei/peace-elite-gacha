#!/bin/bash
# 一键部署游戏到 GitHub Pages
# 用法：./publish-game.sh <游戏目录>

set -e

GAME_DIR=$1

if [ -z "$GAME_DIR" ]; then
    echo "❌ 请指定游戏目录"
    echo "用法：$0 <游戏目录>"
    echo "示例：$0 rock-paper-scissors"
    exit 1
fi

if [ ! -d "$GAME_DIR" ]; then
    echo "❌ 目录不存在：$GAME_DIR"
    exit 1
fi

if [ ! -f "$GAME_DIR/index.html" ]; then
    echo "❌ 未找到 index.html"
    exit 1
fi

echo "🚀 开始部署 $GAME_DIR 到 GitHub Pages..."

# 保存当前分支
CURRENT_BRANCH=$(git branch --show-current)

# 切换到 gh-pages 分支（如果不存在则创建）
if git rev-parse --verify gh-pages >/dev/null 2>&1; then
    git checkout gh-pages
else
    git checkout --orphan gh-pages
    git reset --hard
    git commit --allow-empty -m "init: 初始化 gh-pages 分支"
    git push origin gh-pages
fi

# 创建游戏目录（如果不存在）
GAME_NAME=$(basename "$GAME_DIR")
mkdir -p "$GAME_NAME"

# 复制游戏文件
echo "📦 复制游戏文件..."
cp -r "$GAME_DIR"/* "$GAME_NAME/"

# 提交并推送
git add "$GAME_NAME/"
if git diff --staged --quiet; then
    echo "ℹ️ 没有更改需要提交"
else
    git commit -m "deploy: $GAME_NAME - $(date '+%Y-%m-%d %H:%M')"
    git push origin gh-pages
    echo "✅ 推送完成！"
fi

# 切回原分支
git checkout "$CURRENT_BRANCH"

echo ""
echo "======================================"
echo "✅ $GAME_NAME 部署完成！"
echo "======================================"
echo "📍 访问地址：https://davidlizhiwei.github.io/memory-game/$GAME_NAME/"
echo "======================================"
