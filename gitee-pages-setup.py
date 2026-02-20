#!/usr/bin/env python3
"""
使用 Playwright 自动启用 Gitee Pages 服务
"""

from playwright.sync_api import sync_playwright
import time
import sys

def setup_gitee_pages():
    with sync_playwright() as p:
        # 启动浏览器（有头模式，方便调试）
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        
        print("🌐 正在访问 Gitee 仓库...")
        
        # 访问 Gitee 仓库页面
        page.goto("https://gitee.com/david-li-zhiwei/games", wait_until="networkidle")
        time.sleep(2)
        
        # 截图查看当前页面
        page.screenshot(path="gitee-repo-page.png")
        print("📸 已截取仓库页面截图")
        
        # 尝试点击"服务"标签
        try:
            # 查找服务菜单
            service_link = page.locator('a[href*="/services"], a:has-text("服务"), a:has-text("Pages")').first
            
            if service_link.is_visible():
                print("✅ 找到服务菜单")
                service_link.click()
                time.sleep(2)
                page.screenshot(path="gitee-services-page.png")
            else:
                print("⚠️ 未找到服务菜单，尝试其他方式...")
                
                # 尝试直接访问 Pages 设置页面
                page.goto("https://gitee.com/david-li-zhiwei/games/pages", wait_until="networkidle")
                time.sleep(2)
                page.screenshot(path="gitee-pages-direct.png")
                print("📸 已直接访问 Pages 设置页面")
                
        except Exception as e:
            print(f"⚠️ 操作失败：{e}")
            # 直接访问 Pages 设置
            page.goto("https://gitee.com/david-li-zhiwei/games/pages", wait_until="networkidle")
            time.sleep(2)
            page.screenshot(path="gitee-pages-direct.png")
        
        # 查找 Pages 配置选项
        try:
            # 查找分支选择器
            branch_select = page.locator('select[name*="branch"], select:has-text("gh-pages")').first
            if branch_select.is_visible():
                print("✅ 找到分支选择器")
                branch_select.select_option("gh-pages")
                time.sleep(1)
                
                # 查找保存按钮
                save_btn = page.locator('button:has-text("保存"), button:has-text("确定"), input[value*="保存"]').first
                if save_btn.is_visible():
                    print("✅ 找到保存按钮，点击保存...")
                    save_btn.click()
                    time.sleep(3)
                    page.screenshot(path="gitee-pages-saved.png")
                    print("✅ Pages 服务已启用！")
                else:
                    print("⚠️ 未找到保存按钮")
            else:
                print("⚠️ 未找到分支选择器，请手动配置")
        except Exception as e:
            print(f"⚠️ 配置 Pages 失败：{e}")
        
        print("\n📍 请在浏览器中检查截图，确认配置状态")
        print("   截图保存在当前目录：gitee-*.png")
        
        # 保持浏览器打开，让用户确认
        input("\n按 Enter 关闭浏览器...")
        
        browser.close()

if __name__ == "__main__":
    setup_gitee_pages()
