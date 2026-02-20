"""
AI 图像生成器 - 使用示例
"""

import os
from image_generator import AIGenerator, generate_image

# ============================================
# 方式 1: 快速生成 (使用默认配置)
# ============================================
# 注意：需要先设置环境变量 OPENAI_API_KEY
# result = generate_image("一只可爱的猫咪在阳光下玩耍")
# print(f"图像已保存至：{result.get('saved_path')}")


# ============================================
# 方式 2: 使用 DALL-E 3 生成
# ============================================
def test_dalle3():
    """使用 OpenAI DALL-E 3 生成图像"""
    print("\n=== 使用 DALL-E 3 生成图像 ===")

    # 检查 API 密钥
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  未设置 OPENAI_API_KEY 环境变量")
        print("请在 https://platform.openai.com/api-keys 获取密钥")
        print("并设置：export OPENAI_API_KEY=your_key")
        return

    generator = AIGenerator(provider="dall-e-3")

    # 生成图像
    prompt = "上海陆家嘴天际线，现代都市，黄昏时分，金色阳光，电影质感，超高清"
    print(f"提示词：{prompt}")

    result = generator.generate(
        prompt=prompt,
        size="1024x1024",
        style="vivid",
        save=True
    )

    print(f"✅ 生成成功!")
    print(f"保存路径：{result.get('saved_path')}")
    print(f"修订提示词：{result.get('revised_prompt', 'N/A')}")


# ============================================
# 方式 3: 使用 Stable Diffusion 生成
# ============================================
def test_stable_diffusion():
    """使用 Stability AI SD3 生成图像"""
    print("\n=== 使用 Stable Diffusion 3 生成图像 ===")

    if not os.getenv("STABILITY_API_KEY"):
        print("⚠️  未设置 STABILITY_API_KEY 环境变量")
        print("请在 https://platform.stability.ai/ 获取密钥")
        return

    generator = AIGenerator(provider="stable-diffusion")

    prompt = "A futuristic city with flying cars, cyberpunk style, neon lights, detailed"
    negative_prompt = "blurry, low quality, distorted"

    print(f"提示词：{prompt}")
    print(f"负面提示词：{negative_prompt}")

    result = generator.generate(
        prompt=prompt,
        negative_prompt=negative_prompt,
        size="1024x1024",
        style="digital-art",
        save=True
    )

    print(f"✅ 生成成功!")
    print(f"保存路径：{result.get('saved_path')}")


# ============================================
# 方式 4: 使用通义万相生成
# ============================================
def test_tongyi():
    """使用阿里巴巴通义万相生成图像"""
    print("\n=== 使用通义万相生成图像 ===")

    if not os.getenv("DASHSCOPE_API_KEY"):
        print("⚠️  未设置 DASHSCOPE_API_KEY 环境变量")
        print("请在 https://dashscope.console.aliyun.com/ 获取密钥")
        return

    generator = AIGenerator(provider="tongyi")

    prompt = "杭州西湖美景，山水画风格，宁静祥和"
    print(f"提示词：{prompt}")

    result = generator.generate(
        prompt=prompt,
        size="1024x1024",
        save=True
    )

    print(f"✅ 生成成功!")
    print(f"保存路径：{result.get('saved_path')}")


# ============================================
# 方式 5: 批量生成
# ============================================
def test_batch_generation():
    """批量生成图像"""
    print("\n=== 批量生成图像 ===")

    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  需要设置 OPENAI_API_KEY")
        return

    generator = AIGenerator(provider="dall-e-3")

    prompts = [
        "春天的樱花盛开，粉色花瓣飘落，浪漫氛围",
        "夏日海滩，蓝天白云，椰子树，度假风情",
        "秋天的枫叶，金黄色，温暖阳光",
        "冬日雪景，白雪皑皑，宁静祥和"
    ]

    results = generator.generate_batch(
        prompts=prompts,
        size="1024x1024",
        style="natural"
    )

    print(f"\n✅ 批量生成完成!")
    for i, result in enumerate(results):
        if "error" in result:
            print(f"图像 {i+1} 失败：{result['error']}")
        else:
            print(f"图像 {i+1}: {result.get('saved_path')}")


# ============================================
# 方式 6: 使用文心一格生成
# ============================================
def test_ernie():
    """使用百度文心一格生成图像"""
    print("\n=== 使用文心一格生成图像 ===")

    if not os.getenv("BAIDU_API_KEY"):
        print("⚠️  未设置 BAIDU_API_KEY 环境变量")
        print("请在 https://cloud.baidu.com/ 获取密钥")
        return

    generator = AIGenerator(provider="ernie")

    prompt = "北京故宫，宏伟建筑，历史文化，高清摄影"
    print(f"提示词：{prompt}")

    result = generator.generate(
        prompt=prompt,
        save=True
    )

    print(f"✅ 生成成功!")
    print(f"保存路径：{result.get('saved_path')}")


# ============================================
# 主函数
# ============================================
if __name__ == "__main__":
    print("=" * 60)
    print("AI 图像生成器 - 使用示例")
    print("=" * 60)

    print("\n请选择要测试的功能:")
    print("1. DALL-E 3 生成")
    print("2. Stable Diffusion 3 生成")
    print("3. 通义万相生成")
    print("4. 文心一格生成")
    print("5. 批量生成")
    print("6. 全部测试")
    print()

    # 默认运行 DALL-E 3 测试
    # 你可以修改这里来选择不同的测试
    test_dalle3()

    # 或者取消注释运行其他测试
    # test_stable_diffusion()
    # test_tongyi()
    # test_ernie()
    # test_batch_generation()
