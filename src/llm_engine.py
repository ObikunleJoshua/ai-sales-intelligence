import pandas as pd
from huggingface_hub import InferenceClient

def build_sales_summary(df: pd.DataFrame) -> str:
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

def ask_llm(summary: str, question: str, hf_token: str, model_id: str) -> str:
    client = InferenceClient(provider="hf-inference", api_key=hf_token)

    prompt = f"""
You are a sales analyst.

Use the business summary below to answer the user's question.

BUSINESS SUMMARY:
{summary}

QUESTION:
{question}

Answer in this format:
1. Direct answer
2. Two short reasons
3. One practical recommendation
"""

    try:
        response = client.text_generation(
            prompt=prompt,
            model=model_id,
            max_new_tokens=250,
            temperature=0.2,
        )
        return response.strip()
    except Exception as e:
        return f"LLM temporarily unavailable.\n\nError: {e}"