import pandas as pd

def load_data(path):
    try:
        return pd.read_csv(path)
    except:
        return pd.DataFrame(columns=["date", "category", "amount"])


def save_data(df, path):
    df.to_csv(path, index=False)


def generate_insights(df):
    insights = []

    if df.empty:
        return ["No data available"]

    df["amount"] = df["amount"].astype(float)

    total = df["amount"].sum()
    top_category = df.groupby("category")["amount"].sum().idxmax()

    insights.append(f"💡 Highest spending category: {top_category}")

    avg = df["amount"].mean()
    insights.append(f"📊 Average expense: {avg:.2f}")

    category_sum = df.groupby("category")["amount"].sum()

    if len(category_sum) > 1:
        biggest = category_sum.max()
        smallest = category_sum.min()

        insights.append(f"🔺 Highest category spend: {biggest}")
        insights.append(f"🔻 Lowest category spend: {smallest}")

    if total > 1000:
        insights.append("⚠️ High spending detected!")

    return insights