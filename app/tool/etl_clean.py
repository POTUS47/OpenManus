from typing import Any, Dict, List, Union
import pandas as pd
import numpy as np
from app.tool.base import BaseTool

class ETLCleanTool(BaseTool):
    name: str = "etl_clean"
    description: str = "轻量级ETL工具,用于数据清洗、转换和标准化"

    parameters: dict = {
        "type": "object",
        "properties": {
            "data": {
                "type": "object",
                "description": "输入数据,支持DataFrame、字典或列表格式"
            },
            "operations": {
                "type": "array",
                "description": "清洗操作列表",
                "items": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "操作类型",
                            "enum": ["remove_duplicates", "fill_missing", "remove_outliers",
                                   "standardize", "normalize", "convert_types"]
                        },
                        "params": {
                            "type": "object",
                            "description": "操作参数"
                        }
                    }
                }
            }
        },
        "required": ["data", "operations"]
    }

    async def execute(self, data: Union[Dict, List], operations: List[Dict]) -> Dict:
        try:
            # 转换输入数据为DataFrame
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # 处理嵌套字典的情况
                if any(isinstance(v, dict) for v in data.values()):
                    df = pd.DataFrame.from_dict(data, orient='index')
                else:
                    df = pd.DataFrame(data)
            else:
                df = data

            # 执行清洗操作
            for op in operations:
                operation = op["operation"]
                params = op.get("params", {})

                if operation == "remove_duplicates":
                    df = df.drop_duplicates(**params)
                elif operation == "fill_missing":
                    # 处理 fill_missing 操作
                    if "fields" in params and "value" in params:
                        # 如果指定了字段列表和值，填充指定字段的空值
                        for field in params["fields"]:
                            df[field] = df[field].fillna(params["value"])
                    elif "column" in params and "value" in params:
                        # 兼容 column 参数
                        df[params["column"]] = df[params["column"]].fillna(params["value"])
                    elif "fill_value" in params:
                        # 兼容 fill_value 参数
                        df = df.fillna(value=params["fill_value"])
                    else:
                        # 否则使用默认的 fillna 参数
                        df = df.fillna(**params)
                elif operation == "remove_outliers":
                    # 获取参数
                    columns = params.get("columns")
                    if not columns:
                        # 兼容 field 和 column 参数
                        field = params.get("field") or params.get("column")
                        if field:
                            columns = [field]

                    if not columns:
                        raise ValueError("必须提供 columns、column 或 field 参数")

                    # 获取其他参数
                    method = params.get("method", "zscore")
                    threshold = params.get("threshold", 3)
                    min_value = params.get("min_value") or params.get("lower_bound")
                    max_value = params.get("max_value") or params.get("upper_bound")

                    # 处理每个列
                    df_clean = df.copy()
                    for col in columns:
                        # 应用最小值过滤
                        if min_value is not None:
                            df_clean = df_clean[df_clean[col] >= min_value]
                        # 应用最大值过滤
                        if max_value is not None:
                            df_clean = df_clean[df_clean[col] <= max_value]
                        # 应用统计方法过滤
                        if method == "zscore":
                            z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / df_clean[col].std())
                            df_clean = df_clean[z_scores < threshold]
                        elif method == "iqr":
                            Q1 = df_clean[col].quantile(0.25)
                            Q3 = df_clean[col].quantile(0.75)
                            IQR = Q3 - Q1
                            df_clean = df_clean[~((df_clean[col] < (Q1 - 1.5 * IQR)) | (df_clean[col] > (Q3 + 1.5 * IQR)))]
                    df = df_clean

                elif operation == "standardize":
                    df = self._standardize(df, **params)
                elif operation == "normalize":
                    df = self._normalize(df, **params)
                elif operation == "convert_types":
                    df = self._convert_types(df, **params)

            # 转换回字典格式
            result_dict = df.to_dict(orient='records')

            return {
                "success": True,
                "data": result_dict,
                "shape": df.shape,
                "columns": list(df.columns)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _standardize(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """标准化数据"""
        df_std = df.copy()
        for col in columns:
            df_std[col] = (df_std[col] - df_std[col].mean()) / df_std[col].std()
        return df_std

    def _normalize(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """归一化数据"""
        df_norm = df.copy()
        for col in columns:
            df_norm[col] = (df_norm[col] - df_norm[col].min()) / (df_norm[col].max() - df_norm[col].min())
        return df_norm

    def _convert_types(self, df: pd.DataFrame, type_map: Dict[str, str]) -> pd.DataFrame:
        """转换数据类型"""
        df_conv = df.copy()
        for col, dtype in type_map.items():
            if col in df_conv.columns:
                df_conv[col] = df_conv[col].astype(dtype)
        return df_conv
