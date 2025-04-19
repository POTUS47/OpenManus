from typing import Dict, List, Optional, Union
import json
from app.tool.base import BaseTool
from app.llm import LLM
from pydantic import Field

class SummarizeResultTool(BaseTool):
    name: str = "summarize_result"
    description: str = "生成数据分析报告，包括关键发现、数据洞察、业务建议和风险提示"
    llm: LLM = Field(default_factory=LLM)

    parameters: dict = {
        "type": "object",
        "properties": {
            "data": {
                "type": "array",
                "description": "要分析的数据列表"
            },
            "analysis_type": {
                "type": "string",
                "description": "分析类型，如comparison(对比分析)、trend(趋势分析)等",
                "enum": ["comparison", "trend", "distribution", "correlation"]
            },
            "business_context": {
                "type": "string",
                "description": "业务背景说明"
            }
        },
        "required": ["data", "analysis_type", "business_context"]
    }

    def __init__(self):
        super().__init__()

    async def execute(self, data: List[Dict], analysis_type: str, business_context: str) -> Dict:
        try:
            # 构建提示词
            prompt = f"""请根据以下数据生成一份详细的分析报告：

数据内容：
{json.dumps(data, ensure_ascii=False, indent=2)}

分析类型：{analysis_type}
业务背景：{business_context}

请按照以下结构生成报告：

1. 关键发现
- 列出最重要的数据发现
- 突出显著的趋势和模式
- 注意：如果数据中包含"未知"或"Unknown"地区，不要将其纳入正常的地区对比分析中

2. 数据洞察
- 深入分析数据背后的含义
- 解释关键指标之间的关系
- 在地区对比分析中，仅对比有效地区（如北京、广州等）的数据

3. 业务建议
- 提供具体的行动建议
- 针对数据质量问题提出改进方案
- 建议如何完善用户地区信息的收集
- 提供数据质量提升的具体措施

4. 风险提示
- 指出潜在的风险和问题
- 特别关注数据质量问题带来的风险
- 提供风险规避建议
- 说明数据质量问题对业务决策的影响

请确保报告：
- 使用清晰的结构和标题
- 包含具体的数据支持
- 提供可执行的建议
- 突出数据质量问题的影响
- 在地区对比分析中明确排除"未知"地区
"""

            # 调用 LLM 生成分析报告
            summary = await self.llm.ask(messages=[{"role": "user", "content": prompt}], stream=False)

            return {
                "success": True,
                "summary": summary,
                "analysis_type": analysis_type
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
