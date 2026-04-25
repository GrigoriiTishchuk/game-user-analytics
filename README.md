# Game User Analytics Dashboard

An end-to-end data analytics project simulating player behavior in a mobile game environment.  
The project demonstrates how data can be used to evaluate **player engagement, monetization, and acquisition efficiency**, as well as **A/B testing for product decisions**.

---

## Overview

This project simulates a real-world game analytics workflow:

- Generate realistic player and session data
- Analyze user behavior and key performance metrics
- Evaluate an A/B test experiment
- Compare acquisition channels using business metrics
- Deliver insights through an interactive Streamlit dashboard

---

## Key Questions Answered

- Do players return to the game after installation?
- Which users are more engaged?
- Does the new feature (A/B test) improve retention?
- Which acquisition channels bring the most valuable users?
- Are we acquiring users profitably?

---

## Metrics Covered

### Retention
- **Day 1 Retention**
- **Day 7 Retention**

### Engagement
- **Sessions per User**
- **Engagement Conversion** (users with ≥ 3 sessions)

### Monetization
- **ARPU (Average Revenue Per User)**
- **Purchase Conversion Rate**

### Acquisition
- **CPI (Cost Per Install)**
- **IPM (Installs Per Mille)**

---

## A/B Testing

Users are split into:
- **Group A** → Control
- **Group B** → Experiment

The experiment simulates a gameplay change affecting:
- Retention
- Engagement
- Monetization

---

## Dataset Description

### `game_events.csv`
- Session-level data
- Includes:
  - user_id
  - event_date
  - session_length
  - revenue
  - acquisition_channel
  - ab_group

### `users.csv`
- User-level attributes:
  - install_date
  - country
  - device
  - acquisition_channel
  - A/B group

### `marketing.csv`
- Acquisition metrics:
  - impressions
  - installs
  - spend
  - CPI
  - IPM

---

## Dashboard Features

- KPI overview (Retention, ARPU, Conversion)
- A/B test comparison
- Retention curve visualization
- Channel performance analysis
- CPI vs ARPU efficiency view

---

## Key Insights

- **Group B improves retention and engagement**, indicating stronger player experience.
- **Purchase conversion may slightly decrease**, suggesting a trade-off between accessibility and monetization.
- **Referral users show the highest value**, with strong retention and ARPU at low acquisition cost.
- **Paid acquisition drives volume but lower-quality users**, indicating potential inefficiencies.

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Streamlit
- Matplotlib

---

## How to Run

### 1. Clone repository
```bash
git clone <your-repo-url>
cd game-analytics