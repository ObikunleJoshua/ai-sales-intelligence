import streamlit as st
import pandas as pd
from src.llm_engine import build_sales_summary, ask_llm

st.set_page_config(page_title="AI Sales Intelligence Assistant", layout="wide")

st.title("🛒 AI Sales Intelligence Assistant")
st.write("Upload a sales dataset and ask business questions in plain English.")

def get_rule_based_insight(df: pd.DataFrame, question: str) -> str:
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    best_region = df.groupby("Region")["Profit"].sum().idxmax()
    worst_region = df.groupby("Region")["Profit"].sum().idxmin()
    top_category = df.groupby("Category")["Sales"].sum().idxmax()

    question_lower = question.lower()

    if "profit" in question_lower:
        return (
            f"Profit is a key concern here. Total profit is ${total_profit:,.2f}. "
            f"The best region is {best_region}, while the weakest region is {worst_region}. "
            f"A practical move is to review pricing, discounting, and costs in the weakest region."
        )

    if "region" in question_lower:
        return (
            f"Region performance differs across the dataset. "
            f"{best_region} performs best by profit, while {worst_region} performs worst. "
            f"Focus on improving sales mix and cost control in the weaker region."
        )

    if "category" in question_lower or "product" in question_lower:
        return (
            f"The top category by sales is {top_category}. "
            f"This suggests demand is stronger in that area. "
            f"Review the weaker categories for discounting or low demand issues."
        )

    return (
        f"Total sales are ${total_sales:,.2f} and total profit is ${total_profit:,.2f}. "
        f"The strongest region is {best_region} and the weakest is {worst_region}. "
        f"Use these signals to focus on underperforming areas."
    )

uploaded_file = st.file_uploader("Upload your Superstore CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="latin1")
else:
    df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")

summary = build_sales_summary(df)

st.subheader("Business Summary")
st.code(summary)

question = st.text_input(
    "Ask a question about the sales data",
    placeholder="Why is profit low in some regions?"
)

if st.button("Ask AI"):
    if not question.strip():
        st.warning("Type a question first.")
    else:
        fallback_answer = get_rule_based_insight(df, question)

        hf_token = st.secrets["HF_TOKEN"] if "HF_TOKEN" in st.secrets else ""
        hf_model_id = st.secrets["HF_MODEL_ID"] if "HF_MODEL_ID" in st.secrets else "mistralai/Mistral-7B-Instruct-v0.3"

        if not hf_token:
            st.info("Hugging Face token is missing. Showing fallback insight.")
            st.subheader("Answer")
            st.write(fallback_answer)
        else:
            with st.spinner("Thinking..."):
                try:
                    answer = ask_llm(summary, question, hf_token, hf_model_id)

                    if not answer or "Error:" in answer or "unavailable" in answer.lower():
                        st.warning("LLM could not answer properly. Showing fallback insight instead.")
                        st.subheader("Answer")
                        st.write(fallback_answer)
                    else:
                        st.subheader("AI Answer")
                        st.write(answer)

                except Exception:
                    st.warning("LLM failed. Showing fallback insight instead.")
                    st.subheader("Answer")
                    st.write(fallback_answer)