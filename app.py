import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Sales Intelligence Assistant", layout="wide")

st.title("🛒 AI Sales Intelligence Assistant")
st.write("Upload a sales dataset and ask business questions in plain English.")


def get_rule_based_insight(df: pd.DataFrame, question: str) -> str:
    q = question.lower()

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()

    region_profit = (
        df.groupby("Region")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    category_profit = (
        df.groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    best_region = region_profit.idxmax()
    worst_region = region_profit.idxmin()
    best_category = category_profit.idxmax()
    worst_category = category_profit.idxmin()

    if "region" in q:
        return f"""
Regional analysis shows that {best_region} is currently the strongest performing region by profit, while {worst_region} performs the weakest.

This suggests operational or sales inefficiencies may exist in {worst_region}. Potential causes could include lower order volume, weaker product mix, or aggressive discounting.

A recommended action would be to review pricing strategy and customer demand patterns in the weaker region.
"""

    if "profit" in q or "loss" in q:
        low_regions = region_profit.tail(3)

        return f"""
Total profit across the dataset is ${total_profit:,.2f}.

The weakest profit performance comes mainly from these regions:
{low_regions.to_string()}

One likely explanation is that discounts or operational costs are reducing margins in these areas.

A practical recommendation is to review discount policies and identify low-margin products affecting profitability.
"""

    if "category" in q or "product" in q:
        return f"""
{best_category} is currently the strongest category by profit performance, while {worst_category} contributes the least.

This indicates that customer demand and profitability vary significantly between product categories.

A useful next step would be to investigate whether weaker categories are suffering from excessive discounts, low demand, or high shipping costs.
"""

    if "sales" in q or "revenue" in q:
        monthly_sales = None

        if "Order Date" in df.columns:
            temp = df.copy()
            temp["Order Date"] = pd.to_datetime(temp["Order Date"], errors="coerce")
            temp["Month"] = temp["Order Date"].dt.to_period("M")

            monthly_sales = (
                temp.groupby("Month")["Sales"]
                .sum()
                .tail(6)
            )

        response = f"""
Total sales across the dataset are ${total_sales:,.2f}.

{best_region} currently contributes the strongest regional performance.

Sales performance differences may be influenced by customer demand, shipping patterns, product mix, and regional purchasing behavior.
"""

        if monthly_sales is not None:
            response += f"""

Recent monthly sales trend:
{monthly_sales.to_string()}
"""

        return response

    if "discount" in q:
        if "Discount" in df.columns:
            discount_profit = (
                df.groupby("Discount")["Profit"]
                .mean()
                .sort_index()
            )

            return f"""
Discount analysis suggests that profitability changes significantly across discount levels.

Average profit by discount level:
{discount_profit.head(10).to_string()}

High discount levels may be reducing profitability even when sales volume increases.

A recommended strategy would be to optimize discounting policies to balance sales growth with margin protection.
"""

    return f"""
Business performance analysis shows total sales of ${total_sales:,.2f} and total profit of ${total_profit:,.2f}.

{best_region} is the strongest region by profit, while {worst_region} is currently underperforming.

The strongest category is {best_category}, while {worst_category} contributes the weakest profitability.

Overall, the business would benefit from improving low-performing regions and optimizing pricing and discount strategies.
"""


uploaded_file = st.file_uploader("Upload your Superstore CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="latin1")
else:
    df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")

st.subheader("Business Summary")

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
best_region = df.groupby("Region")["Profit"].sum().idxmax()
worst_region = df.groupby("Region")["Profit"].sum().idxmin()
top_category = df.groupby("Category")["Sales"].sum().idxmax()

summary_text = f"""
Total Sales: ${total_sales:,.2f}
Total Profit: ${total_profit:,.2f}
Best Region by Profit: {best_region}
Worst Region by Profit: {worst_region}
Top Category by Sales: {top_category}
"""

st.code(summary_text)

question = st.text_input(
    "Ask a question about the sales data",
    placeholder="Why is profit low in some regions?"
)

if st.button("Ask AI"):
    if not question.strip():
        st.warning("Type a question first.")
    else:
        answer = get_rule_based_insight(df, question)
        st.subheader("Answer")
        st.write(answer)
