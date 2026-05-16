import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-base"
_tokenizer = None
_model = None


def _require_columns(df: pd.DataFrame) -> None:
    required = {"Sales", "Profit", "Region", "Category", "Segment"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")


def build_sales_summary(df: pd.DataFrame) -> str:
    _require_columns(df)

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()

    best_region = df.groupby("Region")["Profit"].sum().idxmax()
    worst_region = df.groupby("Region")["Profit"].sum().idxmin()
    top_category = df.groupby("Category")["Sales"].sum().idxmax()
    top_segment = df.groupby("Segment")["Sales"].sum().idxmax()

    return f"""
Sales Performance Summary:
- Total Sales: ${total_sales:,.2f}
- Total Profit: ${total_profit:,.2f}
- Best Region by Profit: {best_region}
- Worst Region by Profit: {worst_region}
- Top Category by Sales: {top_category}
- Top Segment by Sales: {top_segment}
""".strip()


def build_context(df: pd.DataFrame, question: str) -> str:
    _require_columns(df)
    q = question.lower()

    parts = [build_sales_summary(df)]

    if "region" in q or "regions" in q:
        region_tbl = (
            df.groupby("Region", as_index=False)[["Sales", "Profit"]]
            .sum()
            .sort_values("Profit", ascending=False)
            .head(5)
        )
        parts.append("Region Performance:\n" + region_tbl.to_string(index=False))

    if "category" in q or "product" in q or "sub-category" in q or "subcategory" in q:
        category_tbl = (
            df.groupby("Category", as_index=False)[["Sales", "Profit"]]
            .sum()
            .sort_values("Profit", ascending=False)
        )
        parts.append("Category Performance:\n" + category_tbl.to_string(index=False))

    if any(word in q for word in ["profit", "loss", "decline", "declining", "low", "worst", "weak"]):
        low_regions = (
            df.groupby("Region")["Profit"]
            .sum()
            .sort_values()
            .head(3)
            .reset_index()
        )
        parts.append("Lowest Profit Regions:\n" + low_regions.to_string(index=False))

    return "\n\n".join(parts)


def _load_model():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return _tokenizer, _model

def ask_llm(df: pd.DataFrame, question: str) -> str:
    context = build_context(df, question)

    # Lightweight answer using the context only
    q = question.lower()

    if "region" in q:
        return (
            "Regional performance is uneven. "
            "The weakest region should be reviewed for pricing, discounting, and cost control. "
            "Context:\n" + context
        )

    if "profit" in q or "loss" in q:
        return (
            "Profit appears to be concentrated in the stronger regions, while weaker regions are dragging overall performance. "
            "Review margins, discounts, and operating costs in the low-profit areas. "
            "Context:\n" + context
        )

    if "category" in q or "product" in q:
        return (
            "Category performance varies, and weaker categories may need pricing or demand review. "
            "Context:\n" + context
        )

    return (
        "Here is a short business interpretation based on the dataset. "
        "Context:\n" + context
    )
