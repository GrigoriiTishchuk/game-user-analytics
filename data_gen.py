import pandas as pd
import numpy as np

np.random.seed(42)
n_users = 1000

users = pd.DataFrame({
    "user_id": range(n_users),
    "install_date": pd.to_datetime("2026-01-01") + pd.to_timedelta(np.random.randint(0, 30, n_users), unit="D"),
    "country": np.random.choice(["US", "FI", "DE", "IN"], n_users),
    "device": np.random.choice(["iOS", "Android"], n_users),
    "ab_group": np.random.choice(["A", "B"], n_users)
})

data = []
for _, row in users.iterrows():
    n_sessions = np.random.randint(1, 10)
    for i in range(n_sessions):
        event_date = row["install_date"] + pd.to_timedelta(i, unit="D")
        # retention effect (Group B slightly better)
        active_prob = 0.4 if row["ab_group"] == "A" else 0.5
        if np.random.rand() < active_prob:
            session_length = np.random.randint(1, 60)
            # revenue (Group B slightly lower → trade-off)
            revenue = np.random.choice([0, 0, 0, 5, 10]) if row["ab_group"] == "A" else np.random.choice([0, 0, 0, 3, 8])
            data.append({
                "user_id": row["user_id"],
                "event_date": event_date,
                "install_date": row["install_date"],
                "country": row["country"],
                "device": row["device"],
                "ab_group": row["ab_group"],
                "session_length": session_length,
                "revenue": revenue
            })

df = pd.DataFrame(data)
df.to_csv("game_data.csv", index=False)
print("Dataset created:", df.shape)