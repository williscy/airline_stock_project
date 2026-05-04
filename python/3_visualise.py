import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, "..", "data", "processed")
DASHBOARD_DIR = os.path.join(BASE_DIR, "..", "dashboard")

daily_path = os.path.join(PROCESSED_DIR, "all_airlines_combined.csv")
monthly_path = os.path.join(PROCESSED_DIR, "all_airlines_monthly.csv")

df = pd.read_csv(daily_path, parse_dates=["date"])
monthly = pd.read_csv(monthly_path)



COLORS = {
    "Cathay Pacific": "#1e8449",
    "Singapore Airlines": "#e67e22",
    "Qantas": "#e74c3c",
    "Korean Air": "#1a5276"
}
COVID_START = "2020-01-01"
COVID_END = "2023-01-01"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
})


# Chart 1 - Normalised Price
fig, ax = plt.subplots(figsize=(14, 6))

for airline, group in df.groupby("airline"):
    ax.plot(group["date"], group["normalised_price"], label=airline, color=COLORS[airline], linewidth=1.5)

ax.axvspan(pd.Timestamp(COVID_START), pd.Timestamp(COVID_END), color="#fadbd8", alpha=0.5, label="COVID period")

ax.axhline(100, color="black", linewidth=0.8, linestyle='--', label="2015 baseline")

ax.set_title("Stock Price Recovery - Normalised to 100 at Jan 2015", fontsize=13, fontweight="bold")
ax.set_xlabel("")
ax.set_ylabel("Normalised Price")
ax.legend(loc="upper left", fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(DASHBOARD_DIR, "1_normalised_price.png"), dpi=150, bbox_inches="tight")

plt.show()


# Chart 2 - Rolling Volatility
fig, ax = plt.subplots(figsize=(14, 6))

for airline, group in df.groupby("airline"):
    ax.plot(group["date"], group["volatility_30d"], label=airline, color=COLORS[airline], linewidth=1.5)

ax.axvspan(pd.Timestamp(COVID_START), pd.Timestamp(COVID_END), color="#fadbd8", alpha=0.5, label="COVID period")

ax.set_title("30-Day Rolling Volatility by Airline (2015-2025)", fontsize=13, fontweight="bold")
ax.set_xlabel("")
ax.set_ylabel("Volatility (%)")
ax.legend(loc="upper left", fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(DASHBOARD_DIR, "2_rolling_volatility.png"), dpi=150, bbox_inches="tight")

plt.show()


# Chart 3 - Monthly Returns
heatmap_data = monthly.pivot_table(
    index="month",
    columns="airline",
    values="avg_daily_return",
    aggfunc="mean"
)

month_names = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}
heatmap_data.index = heatmap_data.index.map(month_names)

fig, ax = plt.subplots(figsize=(10, 6))

sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".2f",
    cmap="RdYlGn",
    center=0,
    linewidths=0.5,
    ax=ax,
    cbar_kws={"label": "Avg Daily Return (%)"}
)

ax.set_title("Average Daily Return by Month & Airline (2015-2025)", fontsize=13, fontweight="bold")
ax.set_xlabel("")
ax.set_ylabel("Month")

plt.tight_layout()
plt.savefig(os.path.join(DASHBOARD_DIR, "3_monthly_heatmap.png"), dpi=150, bbox_inches="tight")

plt.show()


# Chart 4 - COVID Drawdorn & Recovery
covid_df = df[(df["date"] >= "2020-01-01") & (df["date"] <= "2023-12-31")].copy()

covid_df["covid_normalised"] = (covid_df.groupby("airline")["close"].transform(
    lambda x: x / x.iloc[0] * 100
    )
)
OFFSETS = {
    "Cathay Pacific":     (-60, -30),
    "Korean Air":         (60,  -30),
    "Qantas":             (-60, -50),
    "Singapore Airlines": (60,  -50)
}

fig, ax = plt.subplots(figsize=(14, 6))

for airline, group in covid_df.groupby("airline"):
    ax.plot(group["date"], group["covid_normalised"], label=airline, color=COLORS[airline], linewidth=1.8)


    min_row = group["covid_normalised"].idxmin()
    min_row = group.loc[min_row]
    ax.annotate(
        f"{airline.split()[0]} \n {min_row['covid_normalised']: .0f}",
        xy=(min_row["date"], min_row["covid_normalised"]),
        xytext=OFFSETS[airline],
        textcoords="offset points",
        ha="center",
        fontsize=8,
        color=COLORS[airline],
        arrowprops=dict(
            arrowstyle="->",
            color=COLORS[airline],
            lw=1.2
        )
    )


ax.axvspan(pd.Timestamp(COVID_START), pd.Timestamp(COVID_END), color="#fadbd8", alpha=0.5, label="COVID period")

ax.axhline(100, color="black", linewidth=0.8, linestyle="--", label="Pre-COVID baseline")

ax.set_title("COVID Drawdown & Recovery - Normalised to Jan 2020 = 100", fontsize=13, fontweight="bold")
ax.set_xlabel("")
ax.set_ylabel("Normalised Price")
ax.legend(loc="upper right", fontsize=9)
ax.set_ylim(0, 200)

plt.tight_layout()
plt.savefig(os.path.join(DASHBOARD_DIR, "4_covid_drawdown.png"), dpi=150, bbox_inches="tight")

plt.show()
