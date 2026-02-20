#!/bin/bash
# 通用 Gitee Pages 部署脚本
# 用法：./deploy-to-gitee.sh <应用名称> <应用目录>

set -e

APP_NAME=$1
APP_DIR=$2
GITEE_REPO="games"
GITEE_USER="david-li-zhiwei"

if [ -z "$APP_NAME" ] || [ -z "$APP_DIR" ]; then
    echo "用法：$0 <应用名称> <应用目录>"
    echo "示例：$0 '石头剪刀布' 'rock-paper-scissors'"
    exit 1
fi

echo "🚀 开始部署 $APP_NAME 到 Gitee Pages..."
echo "📁 应用目录：$APP_DIR"

cd "$APP_DIR" || exit 1

# 确保是 main 分支
git checkout main 2>/dev/null || true

# 检查 gh-pages 分支是否存在
if ! git rev-parse --verify gh-pages >/dev/null 2>&1; then
    echo "📋 创建 gh-pages 分支..."
    git checkout --orphan gh-pages
    git reset --hard
    git commit --allow-empty -m "init: 初始化 gh-pages 分支"
    git push origin gh-pages
    git checkout main
fi

# 复制静态文件到临时目录
echo "📦 准备部署文件..."
DEPLOY_DIR="/tmp/gitee-deploy-$$"
rm -rf "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR"

# 复制 HTML/CSS/JS 文件
cp -r *.html *.css *.js *.png *.jpg *.svg *.ico 2>/dev/null "$DEPLOY_DIR/" || true
if [ -d "assets" ]; then cp -r assets "$DEPLOY_DIR/"; fi
if [ -d "static" ]; then cp -r static "$DEPLOY_DIR/"; fi

# 如果没有 index.html，检查是否有其他入口
if [ ! -f "$DEPLOY_DIR/index.html" ]; then
    echo "⚠️ 未找到 index.html，检查其他入口文件..."
    ls -la "$DEPLOY_DIR/" 2>/dev/null || true
fi

# 切换到 gh-pages 分支进行部署
git checkout gh-pages

# 清理旧文件（保留 .git）
find . -type f -not -name '.git' -delete 2>/dev/null || true
find . -mindepth 1 -type d -not -name '.git' -exec rm -rf {} + 2>/dev/null || true

# 复制新文件
cp -r "$DEPLOY_DIR"/* . 2>/dev/null || true

# 提交并推送
git add -A
if git diff --staged --quiet; then
    echo "ℹ️ 没有更改需要提交"
else
    git commit -m "deploy: $APP_NAME - $(date '+%Y-%m-%d %H:%M:%S')"
    git push origin gh-pages
    echo "✅ 推送完成！"
fi

# 切回 main 分支
git checkout main

# 清理
rm -rf "$DEPLOY_DIR"

echo ""
echo "======================================"
echo "✅ $APP_NAME 部署完成！"
echo "======================================"
echo "📍 访问地址：https://$GITEE_USER.gitee.io/$GITEE_REPO/"
echo "======================================"
