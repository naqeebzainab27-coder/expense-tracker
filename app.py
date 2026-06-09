import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, save_data, generate_insights

FILE_PATH = "data/expenses.csv"

st.set_page_config(page_title="Advanced Expense Tracker", layout="centered")

st.title("💰 Advanced Expense Tracker Dashboard")

# -------------------------
# Load Data
# -------------------------
df = load_data(FILE_PATH)

# -------------------------
# ADD EXPENSE
# -------------------------
st.header("➕ Add Expense")

with st.form("expense_form"):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
    amount = st.number_input("Amount", min_value=0.0)

    submit = st.form_submit_button("Add Expense")

    if submit:
        new_row = pd.DataFrame([[date, category, amount]],
                               columns=["date", "category", "amount"])

        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df, FILE_PATH)

        st.success("Expense added!")

# -------------------------
# DELETE EXPENSE (NEW FEATURE)
# -------------------------
st.header("🗑️ Delete Expense")

if not df.empty:
    df["index"] = df.index

    delete_index = st.selectbox("Select row to delete", df["index"])

    if st.button("Delete Selected Expense"):
        df = df.drop(delete_index)
        df = df.drop(columns=["index"])

        save_data(df, FILE_PATH)
        st.success("Expense deleted!")

# -------------------------
# VIEW DATA
# -------------------------
st.header("📋 Expense List")

if not df.empty:
    st.dataframe(df)
else:
    st.info("No expenses yet.")

# -------------------------
# CHARTS
# -------------------------
st.header("📊 Analytics")

if not df.empty:
    df["amount"] = df["amount"].astype(float)

    chart_data = df.groupby("category")["amount"].sum().reset_index()

    fig = px.bar(chart_data, x="category", y="amount", title="Spending by Category")
    st.plotly_chart(fig)

# -------------------------
# AI INSIGHTS
# -------------------------
st.header("🧠 AI Insights")

if not df.empty:
    for insight in generate_insights(df):
        st.write("•", insight)
else:
    st.info("Add expenses to see insights")