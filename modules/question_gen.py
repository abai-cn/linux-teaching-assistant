"""
个性化出题模块 —— 生成 Linux 实验练习题
"""
from .llm import ask

GEN_SYSTEM = """你是 Linux 课程出题专家，为高校教师生成高质量 Linux 实验题。

## 题目类型
- 命令行操作题：给定场景，写出正确命令序列
- Shell 脚本题：编写脚本完成特定任务
- 故障排查题：分析错误现象并修复
- 综合实验题：多知识点组合的实际场景

## 难度
- 入门：单命令，5min | 基础：2-3命令组合，10min
- 进阶：需脚本编写，20min | 综合：多知识点，30min+

## 输出格式

### 第 N 题：[题目名称]
**类型：** [类型]  **难度：** [难度]  **预计用时：** X 分钟  **知识点：** [知识点]

**题目描述：**
[场景化问题]

**要求：**
1. [具体要求]

**评分要点：**
- [ ] 评分项（X分）

**参考答案：**
```bash
[正确命令/脚本]
```"""


def generate_questions(
    api_key: str,
    topic: str,
    difficulty: str = "基础",
    count: int = 2,
    question_type: str = "混合",
    model: str = "deepseek-v4-flash",
) -> str:
    """生成 Linux 练习题"""
    prompt = f"请生成 {count} 道 Linux 练习题。\n知识点：{topic}\n难度：{difficulty}\n题目类型：{question_type}\n"

    if difficulty == "基础":
        prompt += "学生应能在 10 分钟内完成。"
    elif difficulty == "进阶":
        prompt += "需要一定综合能力，约 20 分钟。"
    elif difficulty == "综合":
        prompt += "需多知识点综合应用，30 分钟以上。"

    if question_type == "混合":
        prompt += "请混合不同题型。"

    return ask(api_key, prompt, system=GEN_SYSTEM, model=model)
