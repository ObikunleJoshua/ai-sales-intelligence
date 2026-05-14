import pandas as pd

def main():
    df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    best_region = df.groupby("Region")["Profit"].sum().idxmax()
    worst_region = df.groupby("Region")["Profit"].sum().idxmin()
    top_category = df.groupby("Category")["Sales"].sum().idxmax()

    print(f"Total Sales: ${total_sales:,.2f}")
    print(f"Total Profit: ${total_profit:,.2f}")
    print(f"Best Region: {best_region}")
    print(f"Worst Region: {worst_region}")
    print(f"Top Category: {top_category}")

if __name__ == "__main__":
    main()