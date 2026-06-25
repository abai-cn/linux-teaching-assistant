"""
学情分析模块 —— 完成情况统计 + 学情诊断
"""
from .llm import ask

ANALYZER_SYSTEM = """你是 Linux 课程教学分析专家，帮助老师分析学生作业完成情况和学习状况。

## Linux 知识体系（12 模块）
1. 基础入门（基本命令、文件系统）  2. 文件与权限管理  3. 文本处理（grep/sed/awk/管道）
4. 用户与组管理  5. 进程管理  6. Shell 脚本编程  7. 软件包管理
8. 网络配置  9. 存储管理  10. 系统监控与日志  11. 服务管理（systemd）
12. 安全基础

## 分析任务
根据老师提供的数据，分析提交率、分数分布、高频错误、班级共性问题、教学建议。"""


def analyze_completion(api_key: str, data: str, model: str = "deepseek-v4-flash") -> str:
    """分析作业完成情况"""
    prompt = f"""请分析以下作业数据，输出完成情况报告。

{data}

请包含：
1. 总体数据（提交率、平均分）
2. 分数分布表（优秀90+/良好75-89/及格60-74/不及格<60）
3. 高频错误 TOP 3（知识模块 + 错误描述 + 涉及人数）
4. 教学建议（重点讲解内容、推荐实验练习）"""

    return ask(api_key, prompt, system=ANALYZER_SYSTEM, model=model)


def diagnose_student(api_key: str, student_records: str, model: str = "deepseek-v4-flash") -> str:
    """诊断学生学习状况"""
    prompt = f"""请根据以下学生多次作业记录做学情诊断。

{student_records}

请输出：
1. 各知识模块掌握程度表（🟢熟练/🟡一般/🟠薄弱/🔴未掌握）
2. 知识漏洞总结
3. 建议的补救练习（具体到命令/概念）
4. 若是班级共性问题请标注"""

    return ask(api_key, prompt, system=ANALYZER_SYSTEM, model=model)
