import pandas as pd

def main():
    df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")
    df.to_csv("data/superstore_clean.csv", index=False)
    print("Data loaded and cleaned successfully.")

if __name__ == "__main__":
    main()