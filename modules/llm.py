"""
LLM 接口模块 —— DeepSeek V4 API（OpenAI 兼容）
"""
from openai import OpenAI

BASE_URL = "https://api.deepseek.com"


def get_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key, base_url=BASE_URL)


def ask(api_key: str, prompt: str, system: str = "", model: str = "deepseek-v4-flash") -> str:
    """发送请求到 DeepSeek，返回模型回复"""
    client = get_client(api_key)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=4096,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[错误] API 调用失败：{e}"


def ask_with_image(api_key: str, prompt: str, image_base64: str, mime_type: str = "image/png", system: str = "", model: str = "deepseek-v4-flash") -> str:
    """发送图文请求到 DeepSeek（用于 OCR / 截图识别）"""
    client = get_client(api_key)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})

    messages.append({
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_base64}"}},
        ],
    })

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
            max_tokens=4096,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[错误] 图像识别失败：{e}"
