import streamlit as st
import pandas as pd
from src.metrics import *

st.set_page_config(layout="wide")

@st.cache_data
def load():
    df = pd.read_csv("data/game_events.csv")
    marketing = pd.read_csv("data/marketing.csv")
    return prepare(df), marketing

df, marketing = load()

st.title("Game Analytics Dashboard")

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("D1 Retention", f"{retention(df,1):.2%}")
col2.metric("D7 Retention", f"{retention(df,7):.2%}")
col3.metric("Engagement Conversion", f"{engagement_conversion(df):.2%}")
col4.metric("Purchase Conversion", f"{purchase_conversion(df):.2%}")
col5.metric("ARPU", f"€{arpu(df):.2f}")

# A/B
st.subheader("A/B Test")
ab = []
for group in ["A","B"]:
    filtered_data = df[df["ab_group"]==group]
    ab.append({
        "Group": group,
        "D7 Ret": retention(filtered_data,7),
        "Engagement Conversion": engagement_conversion(filtered_data),
        "Purchase Conversion": purchase_conversion(filtered_data),
        "ARPU": arpu(filtered_data)
    })

st.dataframe(pd.DataFrame(ab))

# Channel
st.subheader("Channel Performance")
channel = df.groupby("acquisition_channel").agg({
    "user_id":"nunique",
    "revenue":"sum"
}).rename(columns={"user_id":"Users"})

channel["ARPU"] = channel["revenue"]/channel["Users"]

merged = marketing.merge(channel, on="acquisition_channel")
st.dataframe(merged)

# Insight
st.subheader("Insights")

st.write("""
Group B improves retention and engagement but slightly reduces monetization.
Referral channels bring highest value users, while Ads generate volume but lower efficiency.
""")