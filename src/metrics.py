import pandas as pd

def prepare(df):
    df["event_date"] = pd.to_datetime(df["event_date"])
    df["install_date"] = pd.to_datetime(df["install_date"])
    df["days_since_install"] = (df["event_date"] - df["install_date"]).dt.days
    return df

def retention(df, day):
    user_days = df.groupby("user_id")["days_since_install"].apply(set)
    total = len(user_days)
    return sum(1 for d in user_days if day in d) / total if total else 0

def arpu(df):
    return df["revenue"].sum() / df["user_id"].nunique()

def sessions_per_user(df):
    return df.groupby("user_id").size().mean()

def engagement_conversion(df):
    sessions = df.groupby("user_id").size()
    return (sessions >= 3).sum() / len(sessions)

def purchase_conversion(df):
    return df[df["revenue"] > 0]["user_id"].nunique() / df["user_id"].nunique()