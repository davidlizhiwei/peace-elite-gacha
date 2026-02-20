"""
AI 图像生成器
支持多种大模型图像生成 API:
- DALL-E 3 (OpenAI)
- Stable Diffusion (本地或 API)
- 通义万相 (阿里巴巴)
- 文心一格 (百度)
"""

import os
import requests
import base64
import json
from datetime import datetime
from pathlib import Path


class AIGenerator:
    """AI 图像生成器"""

    def __init__(self, api_key=None, provider="dall-e-3"):
        """
        初始化图像生成器

        Args:
            api_key: API 密钥 (如果为 None，则从环境变量读取)
            provider: 提供商选择："dall-e-3", "stable-diffusion", "tongyi", "ernie"
        """
        self.provider = provider
        self.output_dir = Path(__file__).parent / "generated_images"
        self.output_dir.mkdir(exist_ok=True)

        # 根据提供商配置 API
        self._setup_api(api_key)

    def _setup_api(self, api_key):
        """根据提供商设置 API 配置"""
        if self.provider == "dall-e-3":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.api_url = "https://api.openai.com/v1/images/generations"
            self.headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

        elif self.provider == "stable-diffusion":
            # 支持多种 Stable Diffusion API
            self.api_key = api_key or os.getenv("STABILITY_API_KEY")
            self.api_url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "image/*"
            }

        elif self.provider == "tongyi":
            # 通义万相
            self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
            self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

        elif self.provider == "ernie":
            # 文心一格
            self.api_key = api_key or os.getenv("BAIDU_API_KEY")
            self.secret_key = os.getenv("BAIDU_SECRET_KEY", "")
            # 获取 access token
            self._get_baidu_token()

    def _get_baidu_token(self):
        """获取百度文心一格 access token"""
        if not self.api_key or not self.secret_key:
            raise ValueError("百度 API 需要设置 BAIDU_API_KEY 和 BAIDU_SECRET_KEY")

        token_url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        response = requests.post(token_url, params=params)
        data = response.json()
        self.access_token = data.get("access_token")
        self.api_url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/text2image/sd_xl?access_token={self.access_token}"
        self.headers = {"Content-Type": "application/json"}

    def generate(self, prompt, negative_prompt=None, size="1024x1024",
                 style="natural", save=True, return_base64=False):
        """
        生成图像

        Args:
            prompt: 提示词
            negative_prompt: 负面提示词 (不希望出现的内容)
            size: 图像尺寸，如 "1024x1024", "1792x1024"
            style: 风格，"natural"(自然), "vivid"(生动), "digital-art"(数字艺术) 等
            save: 是否保存到本地
            return_base64: 是否返回 base64 编码

        Returns:
            dict: 包含生成结果的信息
        """
        width, height = map(int, size.split("x"))

        if self.provider == "dall-e-3":
            result = self._generate_dalle(prompt, size, style)
        elif self.provider == "stable-diffusion":
            result = self._generate_sd(prompt, negative_prompt, width, height, style)
        elif self.provider == "tongyi":
            result = self._generate_tongyi(prompt, size)
        elif self.provider == "ernie":
            result = self._generate_ernie(prompt, negative_prompt)
        else:
            raise ValueError(f"不支持的提供商：{self.provider}")

        # 保存图像
        if save and result.get("image_data"):
            result["saved_path"] = self._save_image(result["image_data"], prompt)

        return result

    def _generate_dalle(self, prompt, size, style):
        """使用 DALL-E 3 生成图像"""
        if not self.api_key:
            raise ValueError("请设置 OPENAI_API_KEY 环境变量")

        # 映射风格
        style_map = {
            "natural": "natural",
            "vivid": "vivid",
            "digital-art": "vivid",
            "photo": "natural"
        }

        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": size,
            "style": style_map.get(style, "natural"),
            "quality": "standard"
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # DALL-E 返回 URL
        image_url = data["data"][0]["url"]
        # 下载图像
        image_response = requests.get(image_url)
        image_data = image_response.content

        return {
            "provider": "dall-e-3",
            "image_data": image_data,
            "url": image_url,
            "revised_prompt": data["data"][0].get("revised_prompt", prompt)
        }

    def _generate_sd(self, prompt, negative_prompt, width, height, style):
        """使用 Stable Diffusion 3 生成图像"""
        if not self.api_key:
            raise ValueError("请设置 STABILITY_API_KEY 环境变量")

        # 映射风格
        style_preset_map = {
            "natural": "photographic",
            "vivid": "vivid",
            "digital-art": "digital-art",
            "photo": "photographic",
            "anime": "anime",
            "3d": "3d-model"
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*"
        }

        payload = {
            "prompt": prompt,
            "output_format": "png",
            "width": width,
            "height": height,
        }

        if negative_prompt:
            payload["negative_prompt"] = negative_prompt

        if style in style_preset_map:
            payload["style_preset"] = style_preset_map[style]

        response = requests.post(self.api_url, headers=headers, data=payload)
        response.raise_for_status()

        return {
            "provider": "stable-diffusion",
            "image_data": response.content
        }

    def _generate_tongyi(self, prompt, size):
        """使用通义万相生成图像"""
        if not self.api_key:
            raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")

        # 通义万相 API
        payload = {
            "model": "wanx-v1",
            "input": {
                "prompt": prompt
            },
            "parameters": {
                "style": "<auto>",
                "size": size,
                "n": 1
            }
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # 通义返回 URL
        if "output" in data and "results" in data["output"]:
            image_url = data["output"]["results"][0]["url"]
            image_response = requests.get(image_url)

            return {
                "provider": "tongyi",
                "image_data": image_response.content,
                "url": image_url
            }

        raise ValueError(f"通义万相 API 返回错误：{data}")

    def _generate_ernie(self, prompt, negative_prompt):
        """使用文心一格生成图像"""
        if not hasattr(self, 'access_token'):
            self._get_baidu_token()

        payload = {
            "prompt": prompt,
            "width": 1024,
            "height": 1024,
            "image_num": 1,
        }

        if negative_prompt:
            payload["negative_prompt"] = negative_prompt

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # 文心一格返回 base64
        if "data" in data and "data" in data["data"]:
            image_base64 = data["data"]["data"][0]
            image_data = base64.b64decode(image_base64)

            return {
                "provider": "ernie",
                "image_data": image_data,
                "url": data["data"]["data"][0].get("img_url", "")
            }

        raise ValueError(f"文心一格 API 返回错误：{data}")

    def _save_image(self, image_data, prompt):
        """保存图像到本地"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 从提示词生成文件名
        safe_prompt = prompt[:30].replace(" ", "_").replace("/", "_")
        filename = f"{timestamp}_{safe_prompt}.png"
        filepath = self.output_dir / filename

        with open(filepath, "wb") as f:
            f.write(image_data)

        return str(filepath)

    def generate_batch(self, prompts, **kwargs):
        """
        批量生成图像

        Args:
            prompts: 提示词列表
            **kwargs: 其他参数传递给 generate 方法

        Returns:
            list: 生成结果列表
        """
        results = []
        for i, prompt in enumerate(prompts, 1):
            print(f"生成图像 {i}/{len(prompts)}: {prompt[:50]}...")
            try:
                result = self.generate(prompt, **kwargs)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e), "prompt": prompt})
        return results


# 便捷函数
def generate_image(prompt, provider="dall-e-3", **kwargs):
    """
    快速生成图像

    Args:
        prompt: 提示词
        provider: 提供商
        **kwargs: 其他参数

    Returns:
        dict: 生成结果
    """
    generator = AIGenerator(provider=provider)
    return generator.generate(prompt, **kwargs)


if __name__ == "__main__":
    # 测试示例
    print("AI 图像生成器")
    print("=" * 50)
    print("支持的提供商:")
    print("  - dall-e-3: OpenAI DALL-E 3")
    print("  - stable-diffusion: Stability AI SD3")
    print("  - tongyi: 阿里巴巴通义万相")
    print("  - ernie: 百度文心一格")
    print()
    print("使用示例:")
    print('  generator = AIGenerator(provider="dall-e-3")')
    print('  result = generator.generate("一只可爱的猫咪在阳光下")')
