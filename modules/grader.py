"""
作业批改模块 —— 分析学生 Linux 命令/脚本 + 截图 OCR
"""
import base64
from .llm import ask, ask_with_image

GRADER_SYSTEM = """你是一位 Linux 课程助教，专门批改学生的命令操作和 Shell 脚本作业。

## 评分标准

从三个维度评分（总分 100）：

### 正确性（40分）
- 命令/脚本能否正确执行？是否达到题目要求？边界情况是否处理？

### 规范性（30分）
- 脚本是否有 shebang（#!/bin/bash）？变量命名是否清晰？注释是否合理？错误处理？

### 效率（30分）
- 命令组合是否简洁？是否避免了不必要的管道/子进程？

## 输出格式

## 作业批改结果

**总分：XX/100**
- 正确性：XX/40 — [评语]
- 规范性：XX/30 — [评语]
- 效率：XX/30 — [评语]

### 存在的问题
1. [具体问题 + 修改建议]
2. ...

### 修改后参考
```bash
[正确的命令或脚本]
```

### 学习建议
[1-2 条改进方向]

## 注意
- 遇到 rm -rf /、chmod 777 等危险操作要重点警告
- 语言简洁，对事不对人"""


def ocr_image(api_key: str, image_data: bytes, mime_type: str = "image/png", model: str = "deepseek-v4-flash") -> str:
    """用 DeepSeek V4 视觉能力从截图中提取文字"""
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    return ask_with_image(
        api_key=api_key,
        prompt="请从这张截图中提取所有文字内容，保持原有的代码格式和缩进。只输出提取的文字，不要添加额外说明。",
        image_base64=image_base64,
        mime_type=mime_type,
        system="你是一个 OCR 工具，专门从截图中提取代码和命令。输出原文，不要修改内容。",
        model=model,
    )


def grade(api_key: str, assignment: str, task_description: str = "", language: str = "bash", model: str = "deepseek-v4-flash") -> str:
    """批改一份学生作业"""
    prompt = "请批改以下学生作业。\n\n"
    if task_description:
        prompt += f"## 作业题目\n{task_description}\n\n"

    prompt += f"""## 学生提交（{language}）

```{language}
{assignment}
```

请按照评分标准从正确性、规范性、效率三个维度评价。"""

    return ask(api_key, prompt, system=GRADER_SYSTEM, model=model)
