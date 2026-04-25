import pandas as pd
import numpy as np

np.random.seed(42)

n_users = 1200

users = pd.DataFrame({
    "user_id": range(n_users),
    "install_date": pd.to_datetime("2026-01-01") + pd.to_timedelta(np.random.randint(0, 30, n_users), unit="D"),
    "country": np.random.choice(["US", "FI", "DE", "IN"], n_users),
    "device": np.random.choice(["iOS", "Android"], n_users),
    "ab_group": np.random.choice(["A", "B"], n_users)
})

users["acquisition_channel"] = np.random.choice(
    ["Ads", "Organic", "Referral", "Influencer"],
    size=n_users,
    p=[0.4, 0.3, 0.2, 0.1]
)

data = []

for _, row in users.iterrows():
    n_days = np.random.randint(1, 10)

    for i in range(n_days):
        event_date = row["install_date"] + pd.to_timedelta(i, unit="D")
        if row["acquisition_channel"] == "Organic":
            base_prob = 0.55
        elif row["acquisition_channel"] == "Referral":
            base_prob = 0.6
        elif row["acquisition_channel"] == "Influencer":
            base_prob = 0.5
        else:
            base_prob = 0.35

        active_prob = base_prob + (0.05 if row["ab_group"] == "B" else 0)
        if np.random.rand() < active_prob:
            session_length = np.random.randint(5, 60)
            if row["acquisition_channel"] == "Ads":
                revenue = np.random.choice([0, 0, 0, 2, 5])
            elif row["acquisition_channel"] == "Organic":
                revenue = np.random.choice([0, 0, 5, 10])
            elif row["acquisition_channel"] == "Referral":
                revenue = np.random.choice([0, 5, 10, 15])
            else:
                revenue = np.random.choice([0, 0, 3, 8])
            data.append({
                "user_id": row["user_id"],
                "install_date": row["install_date"],
                "event_date": event_date,
                "country": row["country"],
                "device": row["device"],
                "ab_group": row["ab_group"],
                "acquisition_channel": row["acquisition_channel"],
                "session_length": session_length,
                "revenue": revenue
            })

df = pd.DataFrame(data)

marketing = pd.DataFrame({
    "acquisition_channel": ["Ads", "Organic", "Referral", "Influencer"],
    "impressions": [80000, 0, 5000, 30000],
    "installs": [
        (users["acquisition_channel"] == "Ads").sum(),
        (users["acquisition_channel"] == "Organic").sum(),
        (users["acquisition_channel"] == "Referral").sum(),
        (users["acquisition_channel"] == "Influencer").sum()
    ],
    "spend": [3000, 0, 400, 1200]
})

marketing["CPI"] = marketing["spend"] / marketing["installs"]
marketing["IPM"] = (marketing["installs"] / marketing["impressions"]) * 1000

df.to_csv("../data/game_events.csv", index=False)
users.to_csv("../data/users.csv", index=False)
marketing.to_csv("../data/marketing.csv", index=False)

print("Data generated.")