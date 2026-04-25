import streamlit as st
import pandas as pd
from src.metrics import *
import matplotlib.pyplot as plt

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

st.subheader("Retention Curve")
days = list(range(0, 8))
ret_curve = [retention(df, d) for d in days]
fig, ax = plt.subplots()
ax.plot(days, ret_curve)
ax.set_xlabel("Days Since Install")
ax.set_ylabel("Retention")
ax.set_title("Retention Over Time")

st.pyplot(fig)

# A/B
st.subheader("A/B Test")
ab = []
for group in ["A","B"]:
    filtered_data = df[df["ab_group"]==group]
    ab.append({
        "Group": group,
        "D7 Retention": retention(filtered_data,7),
        "Engagement Conversion": engagement_conversion(filtered_data),
        "Purchase Conversion": purchase_conversion(filtered_data),
        "ARPU": arpu(filtered_data)
    })

st.dataframe(pd.DataFrame(ab))

st.subheader("A/B Comparison")
ab_metrics = pd.DataFrame({
    "Group": ["A", "B"],
    "D7 Retention": [
        retention(df[df["ab_group"]=="A"],7),
        retention(df[df["ab_group"]=="B"],7)
    ],
    "ARPU": [
        arpu(df[df["ab_group"]=="A"]),
        arpu(df[df["ab_group"]=="B"])
    ]
})

st.bar_chart(ab_metrics.set_index("Group"))

# Channel
st.subheader("Channel Performance")
channel = df.groupby("acquisition_channel").agg({
    "user_id":"nunique",
    "revenue":"sum"
}).rename(columns={"user_id":"Users"})
channel["ARPU"] = channel["revenue"]/channel["Users"]
st.subheader("📊 ARPU by Channel")
channel_arpu = df.groupby("acquisition_channel").apply(
    lambda x: x["revenue"].sum() / x["user_id"].nunique()
)
st.bar_chart(channel_arpu)

merged = marketing.merge(channel, on="acquisition_channel")
st.dataframe(merged)



st.subheader("CPI vs ARPU")
channel = df.groupby("acquisition_channel").agg({
    "user_id":"nunique",
    "revenue":"sum"
}).rename(columns={"user_id":"Users"})
channel["ARPU"] = channel["revenue"] / channel["Users"]
merged = marketing.merge(channel, on="acquisition_channel")
fig, ax = plt.subplots()
ax.scatter(merged["CPI"], merged["ARPU"])
for i, row in merged.iterrows():
    ax.text(row["CPI"], row["ARPU"], row["acquisition_channel"])
ax.set_xlabel("CPI")
ax.set_ylabel("ARPU")
ax.set_title("Channel Efficiency")

st.pyplot(fig)


# Insight
st.subheader("Insights")

st.write("""
Group B improves retention and engagement but slightly reduces monetization.
Referral channels bring highest value users, while Ads generate volume but lower efficiency.
""")