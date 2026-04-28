import math
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

CARD_BG = "#261D47"
CARD_BG_ALT = "#34275F"
CARD_TEXT = "#F9F7FF"
PAGE_BG = "#F5F2FB"
TEXT = "#2D2544"
EMPHASIS_TEXT = "#1A1333"
GRID = "#E9E3F4"
PALETTE = ["#D58AE7", "#6E7FE7", "#9AD1C0", "#B4AADF", "#F0C987", "#8E7CC3"]
REPORTING_MONTHS = pd.date_range("2024-01-01", periods=12, freq="MS")
REPLACEMENT_COST = 25000
PAY_SEGMENT_COLUMNS = [
    "Department",
    "Location",
    "Talent_Segment",
    "Employees",
    "Median_Salary",
    "Market_Pay",
    "Pay_Gap_Pct",
    "Attrition_Rate",
    "High_Performer_Share",
    "Flight_Risk_Index",
]
PAY_EQUITY_COLUMNS = [
    "Department",
    "Perf_Rating",
    "Women_Median",
    "Men_Median",
    "Gap_Dollar",
    "Gap_Pct",
]
SCENARIO_COLUMNS = [
    "Scenario",
    "Target_Group",
    "Investment",
    "Estimated_Exits_Avoided",
    "Retention_Lift_Pct_Pts",
    "Estimated_Savings",
    "ROI",
]


def inject_dashboard_css():
    st.markdown(
        """
        <style>
        .stApp {
            color: #2D2544;
            background:
                radial-gradient(circle at top left, rgba(213, 138, 231, 0.10), transparent 24%),
                linear-gradient(180deg, #fbfaff 0%, #f5f2fb 100%);
        }
        [data-testid="stHeader"] {
            background: rgba(245, 242, 251, 0);
        }
        [data-testid="stAppViewContainer"] {
            color: #2D2544;
        }
        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3,
        [data-testid="stAppViewContainer"] h4,
        [data-testid="stAppViewContainer"] label,
        [data-testid="stAppViewContainer"] .stMarkdown,
        [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"] li {
            color: #2D2544;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f4ff 0%, #efe7fb 100%);
            border-right: 1px solid #E9E3F4;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stMultiSelect span,
        [data-testid="stSidebar"] .stMultiSelect svg,
        [data-testid="stSidebar"] [data-baseweb="tag"],
        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            color: #2D2544;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: rgba(255, 255, 255, 0.92);
            border-color: #D8CFF0;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.35rem;
            background: rgba(255, 255, 255, 0.92);
            padding: 0.35rem;
            border: 1px solid #E9E3F4;
            border-radius: 14px;
            flex-wrap: wrap;
        }
        .stTabs [data-baseweb="tab"] {
            height: auto;
            white-space: normal;
            border-radius: 10px;
            color: #2D2544;
            padding: 0.45rem 0.9rem;
        }
        .stTabs [data-baseweb="tab"] [data-testid="stMarkdownContainer"] p {
            color: inherit;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #261d47 0%, #5f4aa0 100%);
            color: #F9F7FF;
        }
        .stTabs [aria-selected="true"] [data-testid="stMarkdownContainer"] p {
            color: #F9F7FF;
        }
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 1rem;
        }
        .dashboard-intro {
            color: #6c6288;
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
        }
        .section-kicker {
            color: #7a7195;
            font-size: 0.78rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 700;
            margin: 1.25rem 0 0.3rem 0;
        }
        .metric-card {
            background: linear-gradient(135deg, #261d47 0%, #34275f 100%);
            border-radius: 18px;
            padding: 1rem 1rem 0.9rem 1rem;
            color: #f9f7ff;
            min-height: 132px;
            box-shadow: 0 14px 28px rgba(38, 29, 71, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 0.5rem;
        }
        .metric-label {
            font-size: 0.76rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            opacity: 0.78;
            margin-bottom: 0.45rem;
        }
        .metric-value {
            font-size: 2.05rem;
            line-height: 1.1;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }
        .metric-caption {
            font-size: 0.87rem;
            color: rgba(249, 247, 255, 0.82);
        }
        .chart-summary {
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid #E9E3F4;
            border-radius: 14px;
            padding: 0.75rem 0.9rem;
            margin: 0.45rem 0 1rem 0;
            color: #4e4566;
            font-size: 0.92rem;
            line-height: 1.45;
        }
        .board-panel {
            background: linear-gradient(135deg, rgba(38, 29, 71, 0.96) 0%, rgba(95, 74, 160, 0.96) 100%);
            border-radius: 20px;
            padding: 1.1rem 1.2rem;
            color: #f9f7ff;
            box-shadow: 0 18px 32px rgba(38, 29, 71, 0.16);
            margin: 0.5rem 0 1rem 0;
        }
        .board-panel,
        .board-panel *,
        .board-panel strong,
        .board-panel li,
        .board-panel p {
            color: rgba(249, 247, 255, 0.96) !important;
        }
        .board-panel p,
        .board-panel li {
            margin: 0.2rem 0 0 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def build_metric_card(label: str, value: str, caption: str) -> str:
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-caption">{caption}</div>
    </div>
    """


def render_chart_summary(summary: str):
    st.markdown(f'<div class="chart-summary">{summary}</div>', unsafe_allow_html=True)


def style_figure(fig, height=340, show_legend=True):
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="white",
        margin=dict(l=14, r=14, t=54, b=18),
        font=dict(color=TEXT, size=12),
        title_font=dict(size=16, color=TEXT),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title_text="",
        ),
        showlegend=show_legend,
    )
    fig.update_xaxes(showgrid=False, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zeroline=False)
    return fig


def style_descriptive_figure(fig, height=340, show_legend=True):
    fig = style_figure(fig, height=height, show_legend=show_legend)
    fig.update_layout(
        font=dict(color=EMPHASIS_TEXT, size=12),
        title_font=dict(size=16, color=EMPHASIS_TEXT),
        legend=dict(font=dict(color=EMPHASIS_TEXT)),
        coloraxis_colorbar=dict(
            tickfont=dict(color=EMPHASIS_TEXT, size=12),
            title=dict(font=dict(color=EMPHASIS_TEXT, size=12)),
        ),
        annotations=[dict(font=dict(color=EMPHASIS_TEXT, size=12)) for _ in fig.layout.annotations],
    )
    fig.update_xaxes(
        tickfont=dict(color=EMPHASIS_TEXT, size=12),
        title_font=dict(color=EMPHASIS_TEXT, size=12),
        linecolor=GRID,
    )
    fig.update_yaxes(
        tickfont=dict(color=EMPHASIS_TEXT, size=12),
        title_font=dict(color=EMPHASIS_TEXT, size=12),
        gridcolor=GRID,
    )
    for trace in fig.data:
        try:
            trace.update(textfont=dict(color=EMPHASIS_TEXT, size=12))
        except ValueError:
            continue
    return fig


@st.cache_data
def load_data():
    rng = np.random.default_rng(42)
    n_employees = 2000
    departments = np.array(["Sales", "R&D", "HR", "Engineering", "Marketing"])
    locations = np.array(["Singapore", "London", "New York", "Tokyo"])
    genders = np.array(["Women", "Men", "Non-binary"])
    month_weights = np.array([0.07, 0.07, 0.08, 0.08, 0.09, 0.08, 0.09, 0.09, 0.09, 0.09, 0.08, 0.09])

    department = rng.choice(departments, size=n_employees, p=[0.21, 0.19, 0.08, 0.32, 0.20])
    location = rng.choice(locations, size=n_employees, p=[0.24, 0.21, 0.31, 0.24])
    gender = rng.choice(genders, size=n_employees, p=[0.46, 0.50, 0.04])
    tenure_years = np.clip(rng.gamma(shape=2.4, scale=1.7, size=n_employees), 0.2, 12.0)
    age = np.clip(np.round(23 + tenure_years * 2.15 + rng.normal(8.5, 4.3, n_employees)), 21, 61).astype(int)
    perf_rating = rng.choice([1, 2, 3, 4, 5], size=n_employees, p=[0.05, 0.15, 0.48, 0.22, 0.10])
    training_hours = rng.poisson(20, n_employees)
    report_month = pd.to_datetime(rng.choice(REPORTING_MONTHS, size=n_employees, p=month_weights))

    df = pd.DataFrame(
        {
            "Employee_ID": np.arange(1001, 1001 + n_employees),
            "Department": department,
            "Location": location,
            "Gender": gender,
            "Age": age,
            "Tenure_Years": tenure_years,
            "Perf_Rating": perf_rating,
            "Training_Hours": training_hours,
            "Report_Month": report_month,
        }
    )

    dept_salary = {"Sales": 72000, "R&D": 90000, "HR": 64000, "Engineering": 98000, "Marketing": 68000}
    location_premium = {"Singapore": 6000, "London": 9000, "New York": 14000, "Tokyo": 5000}
    gender_adjustment = {"Women": -1500, "Men": 1200, "Non-binary": 0}
    salary_noise = rng.normal(0, 9000, n_employees)
    salary = (
        df["Department"].map(dept_salary)
        + df["Location"].map(location_premium)
        + (df["Perf_Rating"] - 3) * 4500
        + df["Gender"].map(gender_adjustment)
        + salary_noise
    )
    df["Salary"] = np.clip(np.round(salary, -2), 38000, 160000)

    promotion_logit = -2.35 + 0.35 * (df["Perf_Rating"] - 3) + 0.20 * np.clip(df["Tenure_Years"] - 2, 0, None)
    promotion_prob = 1 / (1 + np.exp(-promotion_logit))
    df["Promoted"] = (rng.random(n_employees) < promotion_prob).astype(np.int64)

    salary_z = (df["Salary"] - 78000) / 17000
    tenure_z = (df["Tenure_Years"] - 4.0) / 2.6
    dept_risk = df["Department"].map({"Sales": 0.30, "R&D": -0.10, "HR": 0.18, "Engineering": -0.18, "Marketing": 0.14})
    location_risk = df["Location"].map({"Singapore": -0.05, "London": 0.07, "New York": 0.04, "Tokyo": -0.03})
    logit = -1.00 - 0.48 * salary_z - 0.52 * (df["Perf_Rating"] - 3) - 0.18 * tenure_z + dept_risk + location_risk
    df["Exit_Prob"] = 1 / (1 + np.exp(-logit))
    df["Left"] = (rng.random(n_employees) < df["Exit_Prob"]).astype(np.int64)

    hire_prob = 0.03 + df["Department"].map({"Sales": 0.020, "R&D": 0.018, "HR": 0.010, "Engineering": 0.030, "Marketing": 0.015})
    hire_prob += df["Report_Month"].dt.month.isin([1, 7, 9]).astype(float) * 0.02
    df["Hire_Event"] = (rng.random(n_employees) < np.clip(hire_prob, 0.02, 0.12)).astype(np.int64)

    exit_prob = np.clip(df["Exit_Prob"] * 0.42 + df["Report_Month"].dt.month.isin([3, 10]).astype(float) * 0.02, 0.01, 0.16)
    df["Exit_Event"] = (rng.random(n_employees) < exit_prob).astype(np.int64)

    df["Age_Band"] = pd.cut(
        df["Age"],
        bins=[0, 29, 39, 49, 120],
        labels=["Under 30", "30-39", "40-49", "50+"],
        ordered=True,
    )
    df["Tenure_Band"] = pd.cut(
        df["Tenure_Years"],
        bins=[0, 1, 3, 5, 8, np.inf],
        labels=["<1 year", "1-3 years", "3-5 years", "5-8 years", "8+ years"],
        ordered=True,
    )
    df["Salary_Band"] = pd.cut(
        df["Salary"],
        bins=[0, 50000, 70000, 90000, 110000, np.inf],
        labels=["<$50k", "$50-70k", "$70-90k", "$90-110k", "$110k+"],
        ordered=True,
    )
    df["Report_Month_Label"] = df["Report_Month"].dt.strftime("%b %Y")
    return df


def prepare_pay_segment_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=PAY_SEGMENT_COLUMNS)

    working = df.copy()
    working["Talent_Segment"] = np.select(
        [working["Perf_Rating"] >= 4, working["Perf_Rating"] == 3],
        ["Critical Talent", "Core Talent"],
        default="Watchlist Talent",
    )
    base_market = (
        working.groupby(["Department", "Location"], observed=False)["Salary"]
        .median()
        .rename("Base_Market_Pay")
        .reset_index()
    )
    working = working.merge(base_market, on=["Department", "Location"], how="left")
    market_multiplier = {"Critical Talent": 1.10, "Core Talent": 1.02, "Watchlist Talent": 0.96}
    working["Market_Pay"] = working["Base_Market_Pay"] * working["Talent_Segment"].map(market_multiplier)

    summary = (
        working.groupby(["Department", "Location", "Talent_Segment"], observed=False)
        .agg(
            Employees=("Employee_ID", "count"),
            Median_Salary=("Salary", "median"),
            Market_Pay=("Market_Pay", "median"),
            Attrition_Rate=("Left", lambda s: s.mean() * 100),
            High_Performer_Share=("Perf_Rating", lambda s: (s >= 4).mean() * 100),
        )
        .reset_index()
    )
    summary["Pay_Gap_Pct"] = ((summary["Median_Salary"] - summary["Market_Pay"]) / summary["Market_Pay"]) * 100
    summary["Flight_Risk_Index"] = (
        summary["Attrition_Rate"] * 0.55
        + np.maximum(-summary["Pay_Gap_Pct"], 0) * 1.8
        + summary["High_Performer_Share"] * 0.12
    )
    summary[["Median_Salary", "Market_Pay", "Pay_Gap_Pct", "Attrition_Rate", "High_Performer_Share", "Flight_Risk_Index"]] = (
        summary[["Median_Salary", "Market_Pay", "Pay_Gap_Pct", "Attrition_Rate", "High_Performer_Share", "Flight_Risk_Index"]]
        .round(1)
    )
    return summary[PAY_SEGMENT_COLUMNS].sort_values("Flight_Risk_Index", ascending=False).reset_index(drop=True)


def prepare_pay_equity_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=PAY_EQUITY_COLUMNS)

    working = df[df["Gender"].isin(["Women", "Men"])].copy()
    if working.empty:
        return pd.DataFrame(columns=PAY_EQUITY_COLUMNS)

    summary = (
        working.groupby(["Department", "Perf_Rating", "Gender"], observed=False)["Salary"]
        .median()
        .unstack()
        .reset_index()
        .rename(columns={"Women": "Women_Median", "Men": "Men_Median"})
    )
    if "Women_Median" not in summary:
        summary["Women_Median"] = np.nan
    if "Men_Median" not in summary:
        summary["Men_Median"] = np.nan

    summary = summary.dropna(subset=["Women_Median", "Men_Median"]).copy()
    if summary.empty:
        return pd.DataFrame(columns=PAY_EQUITY_COLUMNS)

    summary["Gap_Dollar"] = summary["Women_Median"] - summary["Men_Median"]
    summary["Gap_Pct"] = (summary["Gap_Dollar"] / summary["Men_Median"]) * 100
    summary[["Women_Median", "Men_Median", "Gap_Dollar", "Gap_Pct"]] = (
        summary[["Women_Median", "Men_Median", "Gap_Dollar", "Gap_Pct"]].round(1)
    )
    return summary[PAY_EQUITY_COLUMNS].sort_values("Gap_Pct").reset_index(drop=True)


def prepare_salary_risk_by_talent_segment(df: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "Salary",
        "Exit_Prob",
        "Risk_Pct",
        "Talent_Segment",
        "Tenure_Years",
        "Department",
        "Location",
        "Gender",
    ]
    if df.empty:
        return pd.DataFrame(columns=columns)

    working = df.copy()
    working["Talent_Segment"] = np.select(
        [working["Perf_Rating"] >= 4, working["Perf_Rating"] == 3],
        ["Critical Talent", "Core Talent"],
        default="Watchlist Talent",
    )
    working["Risk_Pct"] = working["Exit_Prob"] * 100
    sample = working.sample(min(len(working), 450), random_state=42).copy()
    return sample[columns].reset_index(drop=True)


def prepare_attrition_by_tenure_performance(df: pd.DataFrame) -> pd.DataFrame:
    columns = ["Tenure_Band", "Perf_Rating", "Attrition_Rate"]
    if df.empty:
        return pd.DataFrame(columns=columns)

    return (
        df.groupby(["Tenure_Band", "Perf_Rating"], observed=False)["Left"]
        .mean()
        .mul(100)
        .reset_index(name="Attrition_Rate")
    )


def prepare_salary_gap_by_talent_segment(df: pd.DataFrame) -> pd.DataFrame:
    columns = ["Talent_Segment", "Attrition_Status", "Median_Salary"]
    if df.empty:
        return pd.DataFrame(columns=columns)

    working = df.copy()
    working["Talent_Segment"] = np.select(
        [working["Perf_Rating"] >= 4, working["Perf_Rating"] == 3],
        ["Critical Talent", "Core Talent"],
        default="Watchlist Talent",
    )
    working["Attrition_Status"] = working["Left"].map({0: "Stayed", 1: "Exited"})
    return (
        working.groupby(["Talent_Segment", "Attrition_Status"], observed=False)["Salary"]
        .median()
        .reset_index(name="Median_Salary")
    )


def prepare_headcount_time_series_demo(df: pd.DataFrame) -> dict[str, pd.DataFrame | dict[str, float]]:
    monthly = prepare_workforce_flow(df).copy()
    monthly["Month_Number"] = REPORTING_MONTHS.month
    monthly["Net_Change"] = monthly["Hires"] - monthly["Exits"]

    ending_headcount = float(len(df))
    cumulative_net = monthly["Net_Change"].cumsum()
    starting_headcount = ending_headcount - float(cumulative_net.iloc[-1]) if not monthly.empty else ending_headcount
    monthly["Actual_Headcount"] = starting_headcount + cumulative_net

    alpha = 0.35
    monthly["Smoothed_Hires"] = monthly["Hires"].ewm(alpha=alpha, adjust=False).mean()
    monthly["Smoothed_Exits"] = monthly["Exits"].ewm(alpha=alpha, adjust=False).mean()
    monthly["Smoothed_Headcount"] = monthly["Actual_Headcount"].ewm(alpha=alpha, adjust=False).mean()

    avg_hires = float(monthly["Hires"].mean()) if not monthly.empty else 0.0
    avg_exits = float(monthly["Exits"].mean()) if not monthly.empty else 0.0
    monthly["Hire_Seasonality_Index"] = (
        (monthly["Hires"] / avg_hires) if avg_hires else 1.0
    )
    monthly["Exit_Seasonality_Index"] = (
        (monthly["Exits"] / avg_exits) if avg_exits else 1.0
    )
    baseline_hires = monthly["Smoothed_Hires"].shift(1).fillna(avg_hires)
    baseline_exits = monthly["Smoothed_Exits"].shift(1).fillna(avg_exits)
    monthly["Forecast_Ready_Net_Change"] = (
        baseline_hires * monthly["Hire_Seasonality_Index"]
        - baseline_exits * monthly["Exit_Seasonality_Index"]
    )

    last_headcount = float(monthly["Actual_Headcount"].iloc[-1]) if not monthly.empty else ending_headcount
    last_net_change = float(monthly["Net_Change"].iloc[-1]) if not monthly.empty else 0.0
    next_month = monthly.iloc[0] if not monthly.empty else None
    next_month_label = str(next_month["Report_Month_Label"]) if next_month is not None else "Next month"
    smoothed_hires = float(monthly["Smoothed_Hires"].iloc[-1]) if not monthly.empty else 0.0
    smoothed_exits = float(monthly["Smoothed_Exits"].iloc[-1]) if not monthly.empty else 0.0
    seasonality_weight = 0.7
    next_hire_index = (
        1.0 + seasonality_weight * (float(next_month["Hire_Seasonality_Index"]) - 1.0)
        if next_month is not None
        else 1.0
    )
    next_exit_index = (
        1.0 + seasonality_weight * (float(next_month["Exit_Seasonality_Index"]) - 1.0)
        if next_month is not None
        else 1.0
    )
    forecast_hires = smoothed_hires * next_hire_index
    forecast_exits = smoothed_exits * next_exit_index
    seasonal_net_forecast = forecast_hires - forecast_exits

    residuals = monthly["Net_Change"] - monthly["Forecast_Ready_Net_Change"]
    residual_volatility = float(residuals.std(ddof=1)) if len(monthly) > 1 else 0.0

    naive_forecast = last_headcount + last_net_change
    seasonal_forecast = last_headcount + seasonal_net_forecast
    lower_bound = seasonal_forecast - 1.96 * residual_volatility
    upper_bound = seasonal_forecast + 1.96 * residual_volatility

    comparison = pd.DataFrame(
        [
            {
                "Method": "Naive HR carry-forward",
                "Forecast_Headcount": naive_forecast,
                "Lower_Bound": naive_forecast,
                "Upper_Bound": naive_forecast,
            },
            {
                "Method": "Exponentially smoothed + seasonal pattern",
                "Forecast_Headcount": seasonal_forecast,
                "Lower_Bound": lower_bound,
                "Upper_Bound": upper_bound,
            },
        ]
    )

    return {
        "monthly_view": monthly[
            [
                "Report_Month_Label",
                "Hires",
                "Exits",
                "Net_Change",
                "Actual_Headcount",
                "Smoothed_Headcount",
                "Forecast_Ready_Net_Change",
            ]
        ],
        "comparison": comparison,
        "summary": {
            "starting_headcount": starting_headcount,
            "naive_forecast": naive_forecast,
            "seasonal_forecast": seasonal_forecast,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "last_net_change": last_net_change,
            "forecast_gap": seasonal_forecast - naive_forecast,
            "forecast_hires": forecast_hires,
            "forecast_exits": forecast_exits,
            "residual_volatility": residual_volatility,
            "next_month_label": next_month_label,
        },
    }


def _format_model_feature(feature: str) -> str:
    if feature == "Salary_10k":
        return "Salary ($10k step)"
    if feature == "Perf_Rating":
        return "Performance rating"
    if feature == "Tenure_Years":
        return "Tenure (years)"
    if feature == "Training_Hours_10":
        return "Training hours (10-hour step)"
    if feature.startswith("Department_"):
        return f"Department: {feature.replace('Department_', '').replace('_', ' ')}"
    if feature.startswith("Location_"):
        return f"Location: {feature.replace('Location_', '').replace('_', ' ')}"
    return feature.replace("_", " ")


def prepare_promotion_logistic_demo(df: pd.DataFrame) -> dict[str, pd.DataFrame | dict[str, float | str]]:
    risk_columns = ["Readiness_Band", "Avg_Predicted_Promotion_Prob", "Actual_Promotion_Rate", "Employees"]
    coef_columns = ["Feature", "Coefficient", "Odds_Ratio"]
    if df.empty:
        return {
            "risk_view": pd.DataFrame(columns=risk_columns),
            "odds_ratio_view": pd.DataFrame(columns=coef_columns),
            "summary": {
                "strongest_promotion_driver": "No data",
                "strongest_promotion_driver_or": 1.0,
                "strongest_promotion_drag": "No data",
                "strongest_promotion_drag_or": 1.0,
                "highest_readiness_band": "No data",
                "highest_readiness_band_actual": 0.0,
            },
        }

    model_frame = pd.DataFrame(
        {
            "Salary_10k": df["Salary"] / 10000.0,
            "Perf_Rating": df["Perf_Rating"].astype(float),
            "Tenure_Years": df["Tenure_Years"].astype(float),
            "Training_Hours_10": df["Training_Hours"] / 10.0,
            "Department": df["Department"],
            "Location": df["Location"],
        }
    )
    x = pd.get_dummies(model_frame, columns=["Department", "Location"], drop_first=True)
    y = df["Promoted"].astype(int)

    model = LogisticRegression(max_iter=2000)
    model.fit(x, y)
    predicted_probability = model.predict_proba(x)[:, 1]

    risk_frame = pd.DataFrame({"Predicted_Probability": predicted_probability, "Promoted": y})
    decile_count = min(10, max(2, len(risk_frame)))
    risk_frame["Readiness_Band"] = pd.qcut(
        risk_frame["Predicted_Probability"],
        q=decile_count,
        labels=[f"Band {idx}" for idx in range(1, decile_count + 1)],
        duplicates="drop",
    )
    risk_view = (
        risk_frame.groupby("Readiness_Band", observed=False)
        .agg(
            Avg_Predicted_Promotion_Prob=("Predicted_Probability", lambda values: values.mean() * 100),
            Actual_Promotion_Rate=("Promoted", lambda values: values.mean() * 100),
            Employees=("Promoted", "size"),
        )
        .reset_index()
    )

    coefficients = pd.DataFrame(
        {
            "Feature": [_format_model_feature(name) for name in x.columns],
            "Coefficient": model.coef_[0],
        }
    )
    coefficients["Odds_Ratio"] = np.exp(coefficients["Coefficient"])
    odds_ratio_view = coefficients.sort_values("Coefficient", ascending=False).reset_index(drop=True)

    strongest_promotion_driver = odds_ratio_view.iloc[0]
    strongest_promotion_drag = odds_ratio_view.iloc[-1]
    highest_readiness_band = risk_view.iloc[-1]

    return {
        "risk_view": risk_view[risk_columns],
        "odds_ratio_view": odds_ratio_view[coef_columns],
        "summary": {
            "strongest_promotion_driver": str(strongest_promotion_driver["Feature"]),
            "strongest_promotion_driver_or": float(strongest_promotion_driver["Odds_Ratio"]),
            "strongest_promotion_drag": str(strongest_promotion_drag["Feature"]),
            "strongest_promotion_drag_or": float(strongest_promotion_drag["Odds_Ratio"]),
            "highest_readiness_band": str(highest_readiness_band["Readiness_Band"]),
            "highest_readiness_band_actual": float(highest_readiness_band["Actual_Promotion_Rate"]),
        },
    }


def prepare_promotion_logit_demo(df: pd.DataFrame) -> dict[str, pd.DataFrame | dict[str, float | str]]:
    summary_columns = ["Variable", "coef", "std err", "z", "P>|z|", "[0.025", "0.975]"]
    readiness_columns = ["Readiness_Band", "Avg_Predicted_Chance", "Actual_Promotion_Rate", "Employees"]
    employee_columns = [
        "Employee_ID",
        "Predicted_Promotion_Chance",
        "Readiness_Band",
        "Perf_Rating",
        "Tenure_Years",
        "Training_Hours",
        "Department",
        "Location",
    ]
    concept_columns = [
        "Employee_ID",
        "Promotion_Readiness_Score",
        "Predicted_Promotion_Chance",
        "Perf_Rating",
        "Tenure_Years",
        "Training_Hours",
        "Promoted_Label",
        "Department",
        "Location",
    ]
    calculation_columns = ["Variable", "Coefficient", "Employee_Value", "Contribution"]
    probability_columns = ["P_Not_Promoted", "P_Promoted"]
    prediction_columns = ["Actual", "Predicted", "Predicted_Promotion_Chance"]
    sklearn_demo_code = """from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
model.predict(X_test)
model.predict_proba(X_test)"""
    statsmodels_summary_code = """import statsmodels.api as sm

X = sm.add_constant(X, has_constant="add")
result = sm.Logit(y, X).fit()
result.summary()"""
    if df.empty:
        return {
            "summary_table": pd.DataFrame(columns=summary_columns),
            "model_stats": {
                "nobs": 0,
                "pseudo_r2": 0.0,
                "llf": 0.0,
                "llr_pvalue": 1.0,
                "converged": False,
            },
            "readiness_view": pd.DataFrame(columns=readiness_columns),
            "employee_sample": pd.DataFrame(columns=employee_columns),
            "concept_view": pd.DataFrame(columns=concept_columns),
            "logistic_curve": pd.DataFrame(columns=["Promotion_Readiness_Score", "Predicted_Promotion_Chance"]),
            "calculation_example": pd.DataFrame(columns=calculation_columns),
            "sklearn_demo": {
                "code": sklearn_demo_code,
                "fit_output": "No data",
                "split_output": "Train rows: 0 | Test rows: 0",
                "prediction_preview": pd.DataFrame(columns=prediction_columns),
                "probability_preview": pd.DataFrame(columns=probability_columns),
            },
            "statsmodels_summary": {
                "code": statsmodels_summary_code,
                "output": "No data",
            },
            "interpretation": {
                "top_positive_factor": "No data",
                "top_negative_factor": "No data",
                "highest_readiness_band": "No data",
                "highest_readiness_rate": 0.0,
            },
        }

    model_frame = pd.DataFrame(
        {
            "Employee_ID": df["Employee_ID"],
            "Promoted": df["Promoted"].astype(int),
            "Performance rating": df["Perf_Rating"].astype(float),
            "Tenure years": df["Tenure_Years"].astype(float),
            "Training hours": df["Training_Hours"].astype(float),
            "Salary ($10k)": df["Salary"] / 10000.0,
            "Department": df["Department"],
            "Location": df["Location"],
        }
    )
    predictors = pd.get_dummies(
        model_frame[
            [
                "Performance rating",
                "Tenure years",
                "Training hours",
                "Salary ($10k)",
                "Department",
                "Location",
            ]
        ],
        columns=["Department", "Location"],
        drop_first=True,
        dtype=float,
    )
    predictors = predictors.rename(
        columns=lambda value: value.replace("Department_", "Dept: ").replace("Location_", "Loc: ")
    )
    x = sm.add_constant(predictors, has_constant="add")
    y = model_frame["Promoted"]

    logit_model = sm.Logit(y, x).fit(disp=False, maxiter=200)
    conf_int = logit_model.conf_int()
    summary_table = pd.DataFrame(
        {
            "Variable": logit_model.params.index,
            "coef": logit_model.params.values,
            "std err": logit_model.bse.values,
            "z": logit_model.tvalues.values,
            "P>|z|": logit_model.pvalues.values,
            "[0.025": conf_int[0].values,
            "0.975]": conf_int[1].values,
        }
    )

    predicted_chance = logit_model.predict(x) * 100
    scored = model_frame.copy()
    scored["Promotion_Readiness_Score"] = np.dot(x, logit_model.params)
    scored["Predicted_Promotion_Chance"] = predicted_chance
    scored["Promoted_Label"] = np.where(scored["Promoted"] == 1, "Promoted before", "Not promoted before")
    scored["Readiness_Band"] = pd.qcut(
        scored["Predicted_Promotion_Chance"],
        q=min(5, max(2, len(scored))),
        labels=["Low", "Lower-mid", "Mid", "Upper-mid", "High"][: min(5, max(2, len(scored)))],
        duplicates="drop",
    )
    readiness_view = (
        scored.groupby("Readiness_Band", observed=False)
        .agg(
            Avg_Predicted_Chance=("Predicted_Promotion_Chance", "mean"),
            Actual_Promotion_Rate=("Promoted", lambda values: values.mean() * 100),
            Employees=("Promoted", "size"),
        )
        .reset_index()
    )

    coefficient_view = summary_table[summary_table["Variable"] != "const"].copy()
    top_positive = coefficient_view.sort_values("coef", ascending=False).iloc[0]
    top_negative = coefficient_view.sort_values("coef", ascending=True).iloc[0]
    highest_band = readiness_view.iloc[-1]
    employee_sample = scored.sort_values("Predicted_Promotion_Chance", ascending=False).head(8)[
        [
            "Employee_ID",
            "Predicted_Promotion_Chance",
            "Readiness_Band",
            "Performance rating",
            "Tenure years",
            "Training hours",
            "Department",
            "Location",
        ]
    ].rename(
        columns={
            "Performance rating": "Perf_Rating",
            "Tenure years": "Tenure_Years",
            "Training hours": "Training_Hours",
        }
    )
    concept_view = scored.sample(min(len(scored), 450), random_state=42)[
        [
            "Employee_ID",
            "Promotion_Readiness_Score",
            "Predicted_Promotion_Chance",
            "Performance rating",
            "Tenure years",
            "Training hours",
            "Promoted_Label",
            "Department",
            "Location",
        ]
    ].rename(
        columns={
            "Performance rating": "Perf_Rating",
            "Tenure years": "Tenure_Years",
            "Training hours": "Training_Hours",
        }
    )
    score_grid = np.linspace(
        scored["Promotion_Readiness_Score"].min(),
        scored["Promotion_Readiness_Score"].max(),
        120,
    )
    logistic_curve = pd.DataFrame(
        {
            "Promotion_Readiness_Score": score_grid,
            "Predicted_Promotion_Chance": (1 / (1 + np.exp(-score_grid))) * 100,
        }
    )
    example_idx = scored["Predicted_Promotion_Chance"].idxmax()
    calculation_example = pd.DataFrame(
        {
            "Variable": logit_model.params.index,
            "Coefficient": logit_model.params.values,
            "Employee_Value": x.loc[example_idx, logit_model.params.index].values,
        }
    )
    calculation_example["Contribution"] = calculation_example["Coefficient"] * calculation_example["Employee_Value"]
    x_train, x_test, y_train, y_test = train_test_split(
        predictors,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )
    sklearn_model = LogisticRegression(max_iter=1000)
    sklearn_model.fit(x_train, y_train)
    y_pred = sklearn_model.predict(x_test)
    y_prob = sklearn_model.predict_proba(x_test)
    probability_preview = pd.DataFrame(y_prob[:8], columns=probability_columns)
    prediction_preview = pd.DataFrame(
        {
            "Actual": y_test.iloc[:8].to_numpy(),
            "Predicted": y_pred[:8],
            "Predicted_Promotion_Chance": y_prob[:8, 1],
        }
    )

    return {
        "summary_table": summary_table[summary_columns],
        "model_stats": {
            "nobs": int(logit_model.nobs),
            "pseudo_r2": float(logit_model.prsquared),
            "llf": float(logit_model.llf),
            "llr_pvalue": float(logit_model.llr_pvalue),
            "converged": bool(logit_model.mle_retvals.get("converged", False)),
        },
        "readiness_view": readiness_view[readiness_columns],
        "employee_sample": employee_sample[employee_columns],
        "concept_view": concept_view[concept_columns],
        "logistic_curve": logistic_curve,
        "calculation_example": calculation_example[calculation_columns],
        "sklearn_demo": {
            "code": sklearn_demo_code,
            "fit_output": str(sklearn_model),
            "split_output": f"Train rows: {len(x_train):,} | Test rows: {len(x_test):,}",
            "prediction_preview": prediction_preview[prediction_columns],
            "probability_preview": probability_preview[probability_columns],
        },
        "statsmodels_summary": {
            "code": statsmodels_summary_code,
            "output": str(logit_model.summary()),
        },
        "interpretation": {
            "top_positive_factor": str(top_positive["Variable"]),
            "top_negative_factor": str(top_negative["Variable"]),
            "highest_readiness_band": str(highest_band["Readiness_Band"]),
            "highest_readiness_rate": float(highest_band["Actual_Promotion_Rate"]),
        },
    }


def prepare_promotion_prescriptive_actions(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    recommendation_columns = [
        "Employee_ID",
        "Department",
        "Location",
        "Gender",
        "Perf_Rating",
        "Tenure_Years",
        "Predicted_Promotion_Chance",
        "Recommended_Action",
        "HR_Rationale",
        "Required_Checks",
    ]
    action_columns = ["Recommended_Action", "Employees", "Avg_Predicted_Promotion_Chance"]
    fairness_columns = ["Gender", "Employees", "Panel_Review_Count", "Panel_Review_Rate"]
    capacity_columns = ["Constraint", "Current_Value", "Guideline", "Status", "Recommended_Response"]
    constraint_columns = ["Required_Check", "Why_It_Matters"]
    evidence_columns = ["Evidence_Needed", "Seen_By_Model", "Employees_Needing_Check", "Example_HR_Question"]
    bias_columns = ["Check", "Group", "Current_Value", "Comparison", "HR_Interpretation"]
    priority_columns = [
        "Business_Priority",
        "Employees",
        "Panel_Review_Count",
        "Stretch_Count",
        "Attrition_Rate",
        "HR_Use",
    ]
    priority_deep_dive_columns = [
        "Business_Priority",
        "Segment_Definition",
        "Employees",
        "Avg_Promotion_Chance",
        "Avg_Exit_Risk",
        "Panel_Review_Count",
        "Stretch_Count",
        "Top_Department",
        "Top_Location",
        "HR_Conclusion",
    ]
    priority_candidate_columns = [
        "Employee_ID",
        "Department",
        "Location",
        "Perf_Rating",
        "Tenure_Years",
        "Predicted_Promotion_Chance",
        "Recommended_Action",
        "Priority_Fit_Score",
        "Matched_Priorities",
        "Promotion_Suggestion",
    ]
    case_study_columns = ["Employee_ID", "Matched_Priorities", "Evidence_To_Check", "Suggested_HR_Wording"]

    constraints = pd.DataFrame(
        [
            {
                "Required_Check": "Manager validation",
                "Why_It_Matters": "Confirm the model signal is supported by day-to-day performance evidence.",
            },
            {
                "Required_Check": "Role readiness",
                "Why_It_Matters": "Check whether the employee is ready for the next role scope, not only strong in the current role.",
            },
            {
                "Required_Check": "Business need",
                "Why_It_Matters": "Promotion advice should align with open roles, growth priorities, and critical skill demand.",
            },
            {
                "Required_Check": "Fairness review",
                "Why_It_Matters": "Check whether recommendations over- or under-represent any group before using the list.",
            },
            {
                "Required_Check": "Succession context",
                "Why_It_Matters": "Confirm whether the recommendation supports pipeline, retention, and continuity needs.",
            },
        ],
        columns=constraint_columns,
    )

    if df.empty:
        return {
            "recommendations": pd.DataFrame(columns=recommendation_columns),
            "action_summary": pd.DataFrame(columns=action_columns),
            "fairness_summary": pd.DataFrame(columns=fairness_columns),
            "capacity_check": pd.DataFrame(columns=capacity_columns),
            "business_constraints": constraints,
            "missing_evidence": pd.DataFrame(columns=evidence_columns),
            "bias_audit": pd.DataFrame(columns=bias_columns),
            "business_priority": pd.DataFrame(columns=priority_columns),
            "priority_deep_dive": pd.DataFrame(columns=priority_deep_dive_columns),
            "priority_candidate_ranking": pd.DataFrame(columns=priority_candidate_columns),
            "priority_case_studies": pd.DataFrame(columns=case_study_columns),
        }

    logit_demo = prepare_promotion_logit_demo(df)
    summary_table = logit_demo["summary_table"]
    model_frame = pd.DataFrame(
        {
            "Employee_ID": df["Employee_ID"],
            "Department": df["Department"],
            "Location": df["Location"],
            "Gender": df["Gender"],
            "Left": df["Left"].astype(int),
            "Exit_Prob": df["Exit_Prob"].astype(float),
            "Promoted": df["Promoted"].astype(int),
            "Perf_Rating": df["Perf_Rating"].astype(float),
            "Tenure_Years": df["Tenure_Years"].astype(float),
            "Training_Hours": df["Training_Hours"].astype(float),
            "Salary ($10k)": df["Salary"] / 10000.0,
        }
    )
    predictors = pd.get_dummies(
        model_frame[
            [
                "Perf_Rating",
                "Tenure_Years",
                "Training_Hours",
                "Salary ($10k)",
                "Department",
                "Location",
            ]
        ].rename(columns={"Perf_Rating": "Performance rating", "Tenure_Years": "Tenure years", "Training_Hours": "Training hours"}),
        columns=["Department", "Location"],
        drop_first=True,
        dtype=float,
    )
    predictors = predictors.rename(
        columns=lambda value: value.replace("Department_", "Dept: ").replace("Location_", "Loc: ")
    )
    x = sm.add_constant(predictors, has_constant="add")
    params = summary_table.set_index("Variable")["coef"]
    scores = np.dot(x[params.index], params)
    model_frame["Predicted_Promotion_Chance"] = (1 / (1 + np.exp(-scores))) * 100

    def recommend_action(chance: float) -> str:
        if chance >= 50:
            return "Promotion panel review"
        if chance >= 30:
            return "Stretch assignment / succession discussion"
        if chance >= 15:
            return "Targeted development plan"
        return "Continue monitoring"

    model_frame["Recommended_Action"] = model_frame["Predicted_Promotion_Chance"].map(recommend_action)
    model_frame["HR_Rationale"] = np.select(
        [
            model_frame["Recommended_Action"].eq("Promotion panel review"),
            model_frame["Recommended_Action"].eq("Stretch assignment / succession discussion"),
            model_frame["Recommended_Action"].eq("Targeted development plan"),
        ],
        [
            "High model readiness signal; validate with promotion panel evidence.",
            "Promising signal; build readiness evidence through stretch scope.",
            "Some readiness signal; focus development before panel review.",
        ],
        default="Lower model signal; continue monitoring and development support.",
    )
    model_frame["Required_Checks"] = "Manager validation; role readiness; business need; fairness review"
    recommendation_pool = model_frame[model_frame["Left"].eq(0)].copy()
    if recommendation_pool.empty:
        return {
            "recommendations": pd.DataFrame(columns=recommendation_columns),
            "action_summary": pd.DataFrame(columns=action_columns),
            "fairness_summary": pd.DataFrame(columns=fairness_columns),
            "capacity_check": pd.DataFrame(columns=capacity_columns),
            "business_constraints": constraints,
            "missing_evidence": pd.DataFrame(columns=evidence_columns),
            "bias_audit": pd.DataFrame(columns=bias_columns),
            "business_priority": pd.DataFrame(columns=priority_columns),
            "priority_deep_dive": pd.DataFrame(columns=priority_deep_dive_columns),
            "priority_candidate_ranking": pd.DataFrame(columns=priority_candidate_columns),
            "priority_case_studies": pd.DataFrame(columns=case_study_columns),
        }
    recommendations = recommendation_pool.sort_values("Predicted_Promotion_Chance", ascending=False)[recommendation_columns]

    action_summary = (
        recommendations.groupby("Recommended_Action", observed=False)
        .agg(
            Employees=("Employee_ID", "size"),
            Avg_Predicted_Promotion_Chance=("Predicted_Promotion_Chance", "mean"),
        )
        .reset_index()
        .sort_values("Employees", ascending=False)
    )
    fairness_summary = (
        recommendations.groupby("Gender", observed=False)
        .agg(
            Employees=("Employee_ID", "size"),
            Panel_Review_Count=("Recommended_Action", lambda values: values.eq("Promotion panel review").sum()),
        )
        .reset_index()
    )
    fairness_summary["Panel_Review_Rate"] = (
        fairness_summary["Panel_Review_Count"] / fairness_summary["Employees"] * 100
    )
    panel_count = int((recommendations["Recommended_Action"] == "Promotion panel review").sum())
    stretch_count = int(
        (recommendations["Recommended_Action"] == "Stretch assignment / succession discussion").sum()
    )
    review_capacity = max(5, int(np.ceil(len(recommendations) * 0.03)))
    capacity_status = "Within capacity" if panel_count <= review_capacity else "Over capacity"
    capacity_response = (
        "Proceed with full panel-review list."
        if panel_count <= review_capacity
        else "Prioritize highest scores first and move remaining cases into stretch/succession discussion."
    )
    capacity_check = pd.DataFrame(
        [
            {
                "Constraint": "Promotion review capacity",
                "Current_Value": f"{panel_count} panel-review candidates",
                "Guideline": f"Review capacity: about {review_capacity} cases this cycle",
                "Status": capacity_status,
                "Recommended_Response": capacity_response,
            },
            {
                "Constraint": "Near-ready development capacity",
                "Current_Value": f"{stretch_count} stretch/succession candidates",
                "Guideline": "Managers should confirm stretch scope and support before assignment.",
                "Status": "Needs manager planning" if stretch_count else "No immediate capacity pressure",
                "Recommended_Response": "Use business priorities to sequence stretch opportunities.",
            },
        ],
        columns=capacity_columns,
    )
    action_needed_count = int(recommendations["Recommended_Action"].ne("Continue monitoring").sum())
    panel_or_stretch_count = panel_count + stretch_count
    high_potential_mask = (df["Perf_Rating"] >= 4) & (df["Promoted"].eq(0))
    high_potential_missed = int(
        recommendations.loc[high_potential_mask, "Recommended_Action"].ne("Promotion panel review").sum()
    )
    missing_evidence = pd.DataFrame(
        [
            {
                "Evidence_Needed": "Manager feedback",
                "Seen_By_Model": "No",
                "Employees_Needing_Check": action_needed_count,
                "Example_HR_Question": "Does the manager's evidence support the model's readiness signal?",
            },
            {
                "Evidence_Needed": "Role scope",
                "Seen_By_Model": "No",
                "Employees_Needing_Check": panel_or_stretch_count,
                "Example_HR_Question": "Has the employee already performed work at the next role level?",
            },
            {
                "Evidence_Needed": "Business need",
                "Seen_By_Model": "Partly",
                "Employees_Needing_Check": panel_count,
                "Example_HR_Question": "Is there a current or near-term role where this promotion creates business value?",
            },
            {
                "Evidence_Needed": "Leadership behavior",
                "Seen_By_Model": "No",
                "Employees_Needing_Check": panel_or_stretch_count,
                "Example_HR_Question": "Has the employee demonstrated leadership behaviors expected at the next level?",
            },
            {
                "Evidence_Needed": "Critical skills",
                "Seen_By_Model": "No",
                "Employees_Needing_Check": panel_or_stretch_count,
                "Example_HR_Question": "Does the employee have skills needed in scarce or growth-critical areas?",
            },
            {
                "Evidence_Needed": "Mobility preference",
                "Seen_By_Model": "No",
                "Employees_Needing_Check": panel_or_stretch_count,
                "Example_HR_Question": "Is the employee willing to move roles, teams, or locations if needed?",
            },
            {
                "Evidence_Needed": "Performance consistency",
                "Seen_By_Model": "Partly",
                "Employees_Needing_Check": panel_or_stretch_count,
                "Example_HR_Question": "Is the current performance rating consistent over several cycles?",
            },
            {
                "Evidence_Needed": "Promotion budget / headcount availability",
                "Seen_By_Model": "No",
                "Employees_Needing_Check": panel_count,
                "Example_HR_Question": "Can this cycle support the number of recommended promotions?",
            },
        ],
        columns=evidence_columns,
    )

    dept_recommendation = (
        recommendations.groupby("Department", observed=False)
        .agg(
            Employees=("Employee_ID", "size"),
            Panel_Review_Count=("Recommended_Action", lambda values: values.eq("Promotion panel review").sum()),
        )
        .reset_index()
    )
    dept_recommendation["Panel_Review_Rate"] = (
        dept_recommendation["Panel_Review_Count"] / dept_recommendation["Employees"] * 100
    )
    top_dept = dept_recommendation.sort_values("Panel_Review_Rate", ascending=False).iloc[0]
    overall_panel_rate = panel_count / len(recommendations) * 100
    women_row = fairness_summary[fairness_summary["Gender"].eq("Women")]
    women_panel_rate = float(women_row["Panel_Review_Rate"].iloc[0]) if not women_row.empty else 0.0
    lowest_gender = fairness_summary.sort_values("Panel_Review_Rate").iloc[0]
    historical_gender_rates = df.groupby("Gender", observed=False)["Promoted"].mean() * 100
    promotion_bias_spread = float(historical_gender_rates.max() - historical_gender_rates.min())
    high_potential_total = int(high_potential_mask.sum())
    high_potential_missed_rate = (
        high_potential_missed / high_potential_total * 100 if high_potential_total else 0.0
    )
    bias_audit = pd.DataFrame(
        [
            {
                "Check": "Departments over-recommended",
                "Group": str(top_dept["Department"]),
                "Current_Value": f"{top_dept['Panel_Review_Rate']:.1f}% panel-review rate",
                "Comparison": f"Overall panel-review rate: {overall_panel_rate:.1f}%",
                "HR_Interpretation": "If one department is much higher, HR should check whether this reflects true readiness or different manager rating practices.",
            },
            {
                "Check": "Women or minority groups under-recommended",
                "Group": f"Women: {women_panel_rate:.1f}% | Lowest group: {lowest_gender['Gender']}",
                "Current_Value": f"{lowest_gender['Panel_Review_Rate']:.1f}% panel-review rate",
                "Comparison": f"Overall panel-review rate: {overall_panel_rate:.1f}%",
                "HR_Interpretation": "This demo only has gender data. If race, ethnicity, disability, or other minority data is available, HR should repeat the same under-recommendation check for those groups.",
            },
            {
                "Check": "Does the model reproduce old promotion bias?",
                "Group": "Historical promotions by gender",
                "Current_Value": f"{promotion_bias_spread:.1f} percentage-point spread",
                "Comparison": "Compare historical promotion rates before using model recommendations.",
                "HR_Interpretation": "A large historical spread can mean the model is learning past promotion patterns that may include bias.",
            },
            {
                "Check": "Are high-potential employees being missed?",
                "Group": "Performance rating 4+ and not previously promoted",
                "Current_Value": f"{high_potential_missed} of {high_potential_total} missed ({high_potential_missed_rate:.1f}%)",
                "Comparison": "High-potential employees should be reviewed even if their model score is not high.",
                "HR_Interpretation": "This highlights people HR may want to discuss even when the algorithm does not flag them for panel review.",
            },
        ],
        columns=bias_columns,
    )

    enriched = recommendation_pool.sort_values("Predicted_Promotion_Chance", ascending=False).copy()

    def summarize_priority(label: str, mask: pd.Series, hr_use: str) -> dict[str, str | int | float]:
        segment = enriched.loc[mask.reindex(enriched.index, fill_value=False)]
        return {
            "Business_Priority": label,
            "Employees": int(len(segment)),
            "Panel_Review_Count": int(segment["Recommended_Action"].eq("Promotion panel review").sum()),
            "Stretch_Count": int(segment["Recommended_Action"].eq("Stretch assignment / succession discussion").sum()),
            "Attrition_Rate": float(segment["Exit_Prob"].mean() * 100) if not segment.empty else 0.0,
            "HR_Use": hr_use,
        }

    current_employees = enriched[enriched["Left"].eq(0)]
    high_exit_risk_cutoff = current_employees["Exit_Prob"].quantile(0.75) if not current_employees.empty else 1.0
    priority_masks = {
        "Critical roles": enriched["Department"].isin(["R&D", "Sales"]),
        "Succession risk": (enriched["Perf_Rating"] >= 4) & (enriched["Tenure_Years"] >= 5),
        "Retention risk": enriched["Exit_Prob"].ge(high_exit_risk_cutoff) & enriched["Left"].eq(0),
        "Business growth areas": enriched["Location"].isin(["Singapore", "New York"]),
        "Scarce skills": enriched["Department"].eq("R&D"),
        "Leadership pipeline gaps": (enriched["Perf_Rating"] >= 4) & enriched["Promoted"].eq(0),
    }
    priority_definitions = {
        "Critical roles": (
            "Employees in R&D or Sales, used here as roles closest to product, revenue, and customer continuity.",
            "Start with ready-now candidates in critical roles because promotion can protect continuity in roles that are costly to backfill.",
        ),
        "Succession risk": (
            "Employees with performance rating 4+ and tenure of at least 5 years.",
            "Use this group to identify people who may be ready to cover senior or hard-to-backfill roles.",
        ),
        "Retention risk": (
            "Current employees in the top quartile of forward-looking exit probability.",
            "Check whether promotion, stretch scope, or targeted development could reduce regrettable loss risk.",
        ),
        "Business growth areas": (
            "Employees in Singapore or New York, used here as growth-market locations.",
            "Align promotion advice with locations where leadership depth is needed for growth.",
        ),
        "Scarce skills": (
            "R&D employees, used here as a proxy for scarce technical capability.",
            "Protect scarce skills by checking whether high-readiness technical employees need faster career action.",
        ),
        "Leadership pipeline gaps": (
            "Performance rating 4+ employees who have not previously been promoted.",
            "Use this group to find strong performers who may need sponsorship, role-scope evidence, or succession discussion.",
        ),
    }
    business_priority = pd.DataFrame(
        [
            summarize_priority("Critical roles", priority_masks["Critical roles"], "Prioritize review for roles closest to revenue, product, and customer continuity."),
            summarize_priority("Succession risk", priority_masks["Succession risk"], "Use these names to prepare successors for senior or hard-to-backfill roles."),
            summarize_priority("Retention risk", priority_masks["Retention risk"], "Check whether promotion or development action could reduce regrettable loss."),
            summarize_priority("Business growth areas", priority_masks["Business growth areas"], "Align promotion advice with locations where growth requires stronger leadership depth."),
            summarize_priority("Scarce skills", priority_masks["Scarce skills"], "Protect scarce technical capability and avoid losing ready-now specialists."),
            summarize_priority("Leadership pipeline gaps", priority_masks["Leadership pipeline gaps"], "Identify strong performers who may need sponsorship or succession discussion."),
        ],
        columns=priority_columns,
    )
    priority_deep_dive_rows = []
    for priority, mask in priority_masks.items():
        segment = enriched.loc[mask]
        top_department = segment["Department"].mode().iloc[0] if not segment.empty else "No employees"
        top_location = segment["Location"].mode().iloc[0] if not segment.empty else "No employees"
        segment_definition, conclusion = priority_definitions[priority]
        priority_deep_dive_rows.append(
            {
                "Business_Priority": priority,
                "Segment_Definition": segment_definition,
                "Employees": int(len(segment)),
                "Avg_Promotion_Chance": float(segment["Predicted_Promotion_Chance"].mean()) if not segment.empty else 0.0,
                "Avg_Exit_Risk": float(segment["Exit_Prob"].mean() * 100) if not segment.empty else 0.0,
                "Panel_Review_Count": int(segment["Recommended_Action"].eq("Promotion panel review").sum()),
                "Stretch_Count": int(segment["Recommended_Action"].eq("Stretch assignment / succession discussion").sum()),
                "Top_Department": str(top_department),
                "Top_Location": str(top_location),
                "HR_Conclusion": conclusion,
            }
        )
        enriched[priority] = mask.astype(int)
    priority_deep_dive = pd.DataFrame(priority_deep_dive_rows, columns=priority_deep_dive_columns)

    priority_names = list(priority_masks)
    enriched["Priority_Fit_Score"] = enriched[priority_names].sum(axis=1)
    enriched["Matched_Priorities"] = enriched.apply(
        lambda row: ", ".join(priority for priority in priority_names if int(row[priority]) == 1),
        axis=1,
    )
    enriched["Promotion_Suggestion"] = np.select(
        [
            enriched["Recommended_Action"].eq("Promotion panel review") & (enriched["Priority_Fit_Score"] >= 3),
            enriched["Recommended_Action"].eq("Promotion panel review"),
            enriched["Recommended_Action"].eq("Stretch assignment / succession discussion") & (enriched["Priority_Fit_Score"] >= 2),
        ],
        [
            "Strongest business-aligned panel review candidate",
            "Panel review candidate; confirm business need and evidence",
            "Near-ready candidate; use stretch scope to build promotion evidence",
        ],
        default="Development or monitoring before promotion discussion",
    )
    action_rank = {
        "Promotion panel review": 0,
        "Stretch assignment / succession discussion": 1,
        "Targeted development plan": 2,
        "Continue monitoring": 3,
    }
    enriched["Action_Rank"] = enriched["Recommended_Action"].map(action_rank).fillna(4)
    priority_candidate_ranking = (
        enriched[enriched["Priority_Fit_Score"] > 0]
        .sort_values(
            ["Action_Rank", "Priority_Fit_Score", "Predicted_Promotion_Chance"],
            ascending=[True, False, False],
        )
        .head(12)[priority_candidate_columns]
    )
    priority_case_studies = pd.DataFrame(
        [
            {
                "Employee_ID": row["Employee_ID"],
                "Matched_Priorities": row["Matched_Priorities"],
                "Evidence_To_Check": "Manager feedback; next-level role scope; business need; fairness review; promotion capacity.",
                "Suggested_HR_Wording": (
                    f"Employee {row['Employee_ID']} has a {row['Predicted_Promotion_Chance']:.1f}% predicted promotion chance "
                    f"and matches {int(row['Priority_Fit_Score'])} business priorities. HR should not recommend promotion automatically, "
                    "but should bring this case to talent review with manager evidence and workforce-plan context."
                ),
            }
            for _, row in priority_candidate_ranking.head(3).iterrows()
        ],
        columns=case_study_columns,
    )

    return {
        "recommendations": recommendations,
        "action_summary": action_summary[action_columns],
        "fairness_summary": fairness_summary[fairness_columns],
        "capacity_check": capacity_check,
        "business_constraints": constraints,
        "missing_evidence": missing_evidence,
        "bias_audit": bias_audit,
        "business_priority": business_priority,
        "priority_deep_dive": priority_deep_dive,
        "priority_candidate_ranking": priority_candidate_ranking,
        "priority_case_studies": priority_case_studies,
    }


def forecast_retention_scenarios(df: pd.DataFrame, budget: int) -> pd.DataFrame:
    budget = max(int(budget), 0)
    if df.empty:
        return pd.DataFrame(
            [
                {
                    "Scenario": "Targeted Market Adjustment",
                    "Target_Group": "No employees in current filter",
                    "Investment": budget * 0.45,
                    "Estimated_Exits_Avoided": 0.0,
                    "Retention_Lift_Pct_Pts": 0.0,
                    "Estimated_Savings": 0.0,
                    "ROI": 0.0,
                },
                {
                    "Scenario": "Pay Equity Correction",
                    "Target_Group": "No employees in current filter",
                    "Investment": budget * 0.25,
                    "Estimated_Exits_Avoided": 0.0,
                    "Retention_Lift_Pct_Pts": 0.0,
                    "Estimated_Savings": 0.0,
                    "ROI": 0.0,
                },
                {
                    "Scenario": "Balanced C&B Portfolio",
                    "Target_Group": "No employees in current filter",
                    "Investment": budget * 0.30,
                    "Estimated_Exits_Avoided": 0.0,
                    "Retention_Lift_Pct_Pts": 0.0,
                    "Estimated_Savings": 0.0,
                    "ROI": 0.0,
                },
            ]
        )[SCENARIO_COLUMNS]

    pay_summary = prepare_pay_segment_summary(df)
    equity = prepare_pay_equity_summary(df)

    critical_pool = pay_summary[pay_summary["Talent_Segment"] == "Critical Talent"].copy()
    if critical_pool.empty:
        critical_pool = pay_summary.copy()
    market_target = critical_pool.sort_values("Flight_Risk_Index", ascending=False).iloc[0]
    market_investment = budget * 0.45
    market_pay_pressure = max(-market_target["Pay_Gap_Pct"], 0) / 100
    market_effect = min(0.10 + market_pay_pressure * 0.9, 0.28)
    market_exits_avoided = market_target["Employees"] * (market_target["Attrition_Rate"] / 100) * market_effect
    market_retention_lift = (market_exits_avoided / market_target["Employees"]) * 100 if market_target["Employees"] else 0.0

    if equity.empty:
        equity_target = "Women in under-market roles"
        equity_investment = budget * 0.25
        equity_exits_avoided = 0.0
        equity_retention_lift = 0.0
    else:
        worst_gap = equity.sort_values("Gap_Pct").iloc[0]
        equity_population = df[
            (df["Department"] == worst_gap["Department"])
            & (df["Perf_Rating"] == worst_gap["Perf_Rating"])
            & (df["Gender"] == "Women")
        ]
        equity_investment = budget * 0.25
        gap_effect = min(abs(worst_gap["Gap_Pct"]) / 100, 0.12)
        equity_exits_avoided = len(equity_population) * equity_population["Left"].mean() * (0.06 + gap_effect)
        equity_retention_lift = (equity_exits_avoided / len(equity_population)) * 100 if len(equity_population) else 0.0
        equity_target = f"{worst_gap['Department']} | Perf {int(worst_gap['Perf_Rating'])} women"

    top_three = pay_summary.sort_values("Flight_Risk_Index", ascending=False).head(3)
    blended_investment = budget * 0.30
    blended_population = float(top_three["Employees"].sum())
    blended_attrition = (top_three["Attrition_Rate"] / 100).mean() if not top_three.empty else 0.0
    blended_gap = np.maximum(-top_three["Pay_Gap_Pct"], 0).mean() / 100 if not top_three.empty else 0.0
    blended_effect = min(0.08 + blended_gap * 0.8, 0.22)
    blended_exits_avoided = blended_population * blended_attrition * blended_effect
    blended_retention_lift = (blended_exits_avoided / blended_population) * 100 if blended_population else 0.0

    scenarios = pd.DataFrame(
        [
            {
                "Scenario": "Targeted Market Adjustment",
                "Target_Group": f"{market_target['Department']} | {market_target['Location']} | {market_target['Talent_Segment']}",
                "Investment": market_investment,
                "Estimated_Exits_Avoided": market_exits_avoided,
                "Retention_Lift_Pct_Pts": market_retention_lift,
                "Estimated_Savings": market_exits_avoided * REPLACEMENT_COST,
            },
            {
                "Scenario": "Pay Equity Correction",
                "Target_Group": equity_target,
                "Investment": equity_investment,
                "Estimated_Exits_Avoided": equity_exits_avoided,
                "Retention_Lift_Pct_Pts": equity_retention_lift,
                "Estimated_Savings": equity_exits_avoided * REPLACEMENT_COST,
            },
            {
                "Scenario": "Balanced C&B Portfolio",
                "Target_Group": "Top three risk pockets combined",
                "Investment": blended_investment,
                "Estimated_Exits_Avoided": blended_exits_avoided,
                "Retention_Lift_Pct_Pts": blended_retention_lift,
                "Estimated_Savings": blended_exits_avoided * REPLACEMENT_COST,
            },
        ]
    )
    scenarios["ROI"] = np.where(
        scenarios["Investment"] > 0,
        scenarios["Estimated_Savings"] / scenarios["Investment"],
        0.0,
    )
    scenarios[["Investment", "Estimated_Exits_Avoided", "Retention_Lift_Pct_Pts", "Estimated_Savings", "ROI"]] = (
        scenarios[["Investment", "Estimated_Exits_Avoided", "Retention_Lift_Pct_Pts", "Estimated_Savings", "ROI"]].round(2)
    )
    return scenarios[SCENARIO_COLUMNS].sort_values("Estimated_Exits_Avoided", ascending=False).reset_index(drop=True)


def recommend_cb_action(scenarios: pd.DataFrame) -> pd.Series:
    if scenarios.empty:
        return pd.Series(
            {
                "Scenario": "No scenario available",
                "Target_Group": "No employees in current filter",
                "Investment": 0.0,
                "Estimated_Exits_Avoided": 0.0,
                "Retention_Lift_Pct_Pts": 0.0,
                "Estimated_Savings": 0.0,
                "ROI": 0.0,
            }
        )
    ordered = scenarios.sort_values(["Estimated_Exits_Avoided", "ROI"], ascending=[False, False]).reset_index(drop=True)
    return ordered.iloc[0]


def summarize_descriptive_metrics(df: pd.DataFrame) -> dict[str, float]:
    if df.empty:
        return {
            "headcount": 0,
            "turnover_rate": 0.0,
            "avg_salary": 0.0,
            "avg_tenure": 0.0,
            "female_share": 0.0,
            "promotion_rate": 0.0,
            "median_age": 0.0,
        }

    women_share = (df["Gender"].eq("Women").mean() * 100) if "Gender" in df else 0.0
    return {
        "headcount": float(len(df)),
        "turnover_rate": float(df["Left"].mean() * 100),
        "avg_salary": float(df["Salary"].mean()),
        "avg_tenure": float(df["Tenure_Years"].mean()),
        "female_share": float(women_share),
        "promotion_rate": float(df["Promoted"].mean() * 100),
        "median_age": float(df["Age"].median()),
    }


def prepare_workforce_flow(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(
            {
                "Report_Month_Label": REPORTING_MONTHS.strftime("%b %Y"),
                "Hires": np.zeros(len(REPORTING_MONTHS), dtype=int),
                "Exits": np.zeros(len(REPORTING_MONTHS), dtype=int),
            }
        )

    monthly = (
        df.groupby("Report_Month")[["Hire_Event", "Exit_Event"]]
        .sum()
        .reindex(REPORTING_MONTHS, fill_value=0)
        .rename(columns={"Hire_Event": "Hires", "Exit_Event": "Exits"})
        .reset_index(names="Report_Month")
    )
    monthly["Report_Month_Label"] = monthly["Report_Month"].dt.strftime("%b %Y")
    return monthly[["Report_Month_Label", "Hires", "Exits"]]


def prepare_salary_attrition_hypothesis_test(df: pd.DataFrame) -> dict[str, float | int | str]:
    if df.empty:
        return {
            "test_name": "Welch's unequal-variance t-test",
            "null_hypothesis": "Stayed and exited employees have the same average salary.",
            "alternative_hypothesis": "Exited employees have a lower average salary than stayed employees.",
            "stayed_n": 0,
            "exited_n": 0,
            "stayed_mean": 0.0,
            "exited_mean": 0.0,
            "stayed_median": 0.0,
            "exited_median": 0.0,
            "stayed_var": 0.0,
            "exited_var": 0.0,
            "mean_gap": 0.0,
            "standard_error": 0.0,
            "t_stat": 0.0,
            "p_value": 1.0,
            "alpha": 0.05,
            "decision": "Not enough data",
            "interpretation": "No employees are available in the current filter, so the hypothesis test cannot be evaluated.",
        }

    stayed = df.loc[df["Left"] == 0, "Salary"].dropna().astype(float)
    exited = df.loc[df["Left"] == 1, "Salary"].dropna().astype(float)
    stayed_n = int(len(stayed))
    exited_n = int(len(exited))
    stayed_mean = float(stayed.mean()) if stayed_n else 0.0
    exited_mean = float(exited.mean()) if exited_n else 0.0
    stayed_median = float(stayed.median()) if stayed_n else 0.0
    exited_median = float(exited.median()) if exited_n else 0.0
    mean_gap = stayed_mean - exited_mean

    if stayed_n < 2 or exited_n < 2:
        return {
            "test_name": "Welch's unequal-variance t-test",
            "null_hypothesis": "Stayed and exited employees have the same average salary.",
            "alternative_hypothesis": "Exited employees have a lower average salary than stayed employees.",
            "stayed_n": stayed_n,
            "exited_n": exited_n,
            "stayed_mean": stayed_mean,
            "exited_mean": exited_mean,
            "stayed_median": stayed_median,
            "exited_median": exited_median,
            "stayed_var": 0.0,
            "exited_var": 0.0,
            "mean_gap": mean_gap,
            "standard_error": 0.0,
            "t_stat": 0.0,
            "p_value": 1.0,
            "alpha": 0.05,
            "decision": "Not enough data",
            "interpretation": "At least two observations are needed in both groups before testing whether salary differs by attrition status.",
        }

    stayed_var = float(stayed.var(ddof=1))
    exited_var = float(exited.var(ddof=1))
    standard_error = math.sqrt((stayed_var / stayed_n) + (exited_var / exited_n))
    t_stat = (mean_gap / standard_error) if standard_error else 0.0
    p_value = 0.5 * math.erfc(t_stat / math.sqrt(2)) if standard_error else 1.0
    alpha = 0.05
    decision = "Reject H0" if p_value < alpha else "Fail to reject H0"

    if p_value < alpha and mean_gap > 0:
        interpretation = (
            "The salary gap is statistically significant at the 5% level, so exited employees appear to earn less than stayed employees in the current filter."
        )
    elif p_value < alpha:
        interpretation = (
            "The salary gap is statistically significant at the 5% level, but the direction is opposite to the expected pattern in this filter."
        )
    else:
        interpretation = (
            "The observed salary gap is not statistically significant at the 5% level, so this filter does not provide strong evidence that pay differs by attrition status."
        )

    return {
        "test_name": "Welch's unequal-variance t-test",
        "null_hypothesis": "Stayed and exited employees have the same average salary.",
        "alternative_hypothesis": "Exited employees have a lower average salary than stayed employees.",
        "stayed_n": stayed_n,
        "exited_n": exited_n,
        "stayed_mean": stayed_mean,
        "exited_mean": exited_mean,
        "stayed_median": stayed_median,
        "exited_median": exited_median,
        "stayed_var": stayed_var,
        "exited_var": exited_var,
        "mean_gap": mean_gap,
        "standard_error": standard_error,
        "t_stat": float(t_stat),
        "p_value": float(p_value),
        "alpha": alpha,
        "decision": decision,
        "interpretation": interpretation,
    }


def prepare_diagnostic_teaching_examples() -> tuple[pd.DataFrame, pd.DataFrame]:
    turnover_demo = pd.DataFrame(
        [
            {"Department": "HR", "Turnover_Rate": 18.0, "Headcount": 18, "Exits": 3},
            {"Department": "Sales", "Turnover_Rate": 12.0, "Headcount": 150, "Exits": 18},
            {"Department": "Engineering", "Turnover_Rate": 8.0, "Headcount": 210, "Exits": 17},
            {"Department": "Marketing", "Turnover_Rate": 10.0, "Headcount": 60, "Exits": 6},
        ]
    )
    turnover_demo["Label"] = turnover_demo["Turnover_Rate"].map(lambda value: f"{value:.0f}%")

    hiring_demo = pd.DataFrame(
        [
            {"Hiring_Source": "Employee Referral", "Role_Family": "Corporate", "Job_Level": "Entry", "Applicants": 25, "Offers": 7},
            {"Hiring_Source": "Employee Referral", "Role_Family": "Corporate", "Job_Level": "Senior", "Applicants": 15, "Offers": 4},
            {"Hiring_Source": "Employee Referral", "Role_Family": "Technical", "Job_Level": "Entry", "Applicants": 20, "Offers": 5},
            {"Hiring_Source": "Employee Referral", "Role_Family": "Technical", "Job_Level": "Senior", "Applicants": 20, "Offers": 4},
            {"Hiring_Source": "Job Board", "Role_Family": "Corporate", "Job_Level": "Entry", "Applicants": 40, "Offers": 8},
            {"Hiring_Source": "Job Board", "Role_Family": "Corporate", "Job_Level": "Senior", "Applicants": 20, "Offers": 4},
            {"Hiring_Source": "Job Board", "Role_Family": "Technical", "Job_Level": "Entry", "Applicants": 120, "Offers": 18},
            {"Hiring_Source": "Job Board", "Role_Family": "Technical", "Job_Level": "Senior", "Applicants": 60, "Offers": 6},
            {"Hiring_Source": "Campus", "Role_Family": "Corporate", "Job_Level": "Entry", "Applicants": 60, "Offers": 12},
            {"Hiring_Source": "Campus", "Role_Family": "Corporate", "Job_Level": "Senior", "Applicants": 10, "Offers": 2},
            {"Hiring_Source": "Campus", "Role_Family": "Technical", "Job_Level": "Entry", "Applicants": 40, "Offers": 3},
            {"Hiring_Source": "Campus", "Role_Family": "Technical", "Job_Level": "Senior", "Applicants": 10, "Offers": 1},
            {"Hiring_Source": "Agency", "Role_Family": "Corporate", "Job_Level": "Entry", "Applicants": 15, "Offers": 3},
            {"Hiring_Source": "Agency", "Role_Family": "Corporate", "Job_Level": "Senior", "Applicants": 15, "Offers": 4},
            {"Hiring_Source": "Agency", "Role_Family": "Technical", "Job_Level": "Entry", "Applicants": 20, "Offers": 3},
            {"Hiring_Source": "Agency", "Role_Family": "Technical", "Job_Level": "Senior", "Applicants": 10, "Offers": 2},
        ]
    )
    hiring_demo["Offer_Rate"] = hiring_demo["Offers"] / hiring_demo["Applicants"]

    return turnover_demo, hiring_demo


def prepare_turnover_rate_analysis(turnover_demo: pd.DataFrame) -> dict[str, float | str]:
    hr = turnover_demo.loc[turnover_demo["Department"] == "HR"].iloc[0]
    sales = turnover_demo.loc[turnover_demo["Department"] == "Sales"].iloc[0]
    p1 = float(hr["Exits"]) / float(hr["Headcount"])
    p2 = float(sales["Exits"]) / float(sales["Headcount"])
    pooled = float(hr["Exits"] + sales["Exits"]) / float(hr["Headcount"] + sales["Headcount"])
    standard_error = math.sqrt(pooled * (1 - pooled) * ((1 / float(hr["Headcount"])) + (1 / float(sales["Headcount"]))))
    z_stat = ((p1 - p2) / standard_error) if standard_error else 0.0
    p_value = math.erfc(abs(z_stat) / math.sqrt(2))
    decision = "Reject H0" if p_value < 0.05 else "Fail to reject H0"
    interpretation = (
        "The visual rate difference is not enough by itself. Because HR is tiny, the two-proportion test is the better way to judge whether HR vs Sales differs meaningfully."
        if p_value >= 0.05
        else "The turnover-rate difference is statistically significant even after accounting for sample size, so HR vs Sales likely differs beyond random noise."
    )

    return {
        "hr_rate": p1 * 100,
        "sales_rate": p2 * 100,
        "z_stat": float(z_stat),
        "p_value": float(p_value),
        "decision": decision,
        "interpretation": interpretation,
    }


def _betacf(a: float, b: float, x: float) -> float:
    max_iter = 200
    eps = 3.0e-7
    fpmin = 1.0e-30
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d

    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        h *= d * c

        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < fpmin:
            d = fpmin
        c = 1.0 + aa / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def _regularized_incomplete_beta(a: float, b: float, x: float) -> float:
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0

    log_bt = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x)
    bt = math.exp(log_bt)

    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - (bt * _betacf(b, a, 1.0 - x) / b)


def _f_survival(f_stat: float, df1: int, df2: int) -> float:
    if f_stat <= 0:
        return 1.0
    x = (df1 * f_stat) / ((df1 * f_stat) + df2)
    cdf = _regularized_incomplete_beta(df1 / 2.0, df2 / 2.0, x)
    return max(0.0, min(1.0, 1.0 - cdf))


def _regularized_gamma_q(a: float, x: float) -> float:
    if x <= 0:
        return 1.0

    eps = 3.0e-7
    fpmin = 1.0e-30
    max_iter = 200
    b = x + 1.0 - a
    c = 1.0 / fpmin
    d = 1.0 / b
    h = d

    for i in range(1, max_iter + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < fpmin:
            d = fpmin
        c = b + an / c
        if abs(c) < fpmin:
            c = fpmin
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break

    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


def _chi_square_survival(chi_square_stat: float, degrees_of_freedom: int) -> float:
    if chi_square_stat <= 0:
        return 1.0
    return _regularized_gamma_q(degrees_of_freedom / 2.0, chi_square_stat / 2.0)


def _fit_grouped_logistic_regression(hiring_demo: pd.DataFrame) -> pd.DataFrame:
    design = pd.DataFrame(
        {
            "Intercept": 1.0,
            "Job Board": (hiring_demo["Hiring_Source"] == "Job Board").astype(float),
            "Campus": (hiring_demo["Hiring_Source"] == "Campus").astype(float),
            "Agency": (hiring_demo["Hiring_Source"] == "Agency").astype(float),
            "Technical": (hiring_demo["Role_Family"] == "Technical").astype(float),
            "Senior": (hiring_demo["Job_Level"] == "Senior").astype(float),
        }
    )
    x = design.to_numpy(dtype=float)
    applicants = hiring_demo["Applicants"].to_numpy(dtype=float)
    observed_rate = (hiring_demo["Offers"] / hiring_demo["Applicants"]).to_numpy(dtype=float)
    beta = np.zeros(x.shape[1], dtype=float)

    for _ in range(100):
        eta = x @ beta
        mean = 1.0 / (1.0 + np.exp(-eta))
        mean = np.clip(mean, 1.0e-6, 1.0 - 1.0e-6)
        weights = applicants * mean * (1.0 - mean)
        z = eta + (observed_rate - mean) / (mean * (1.0 - mean))
        xtw = x.T * weights
        beta_next = np.linalg.solve(xtw @ x, xtw @ z)
        if np.max(np.abs(beta_next - beta)) < 1.0e-10:
            beta = beta_next
            break
        beta = beta_next

    eta = x @ beta
    mean = 1.0 / (1.0 + np.exp(-eta))
    weights = applicants * mean * (1.0 - mean)
    covariance = np.linalg.inv((x.T * weights) @ x)
    standard_errors = np.sqrt(np.diag(covariance))
    z_scores = beta / standard_errors
    p_values = [math.erfc(abs(value) / math.sqrt(2.0)) for value in z_scores]
    meanings = {
        "Intercept": "Baseline odds for Employee Referral, Corporate, Entry roles.",
        "Job Board": "Difference versus Employee Referral, holding role mix and job level constant.",
        "Campus": "Difference versus Employee Referral, holding role mix and job level constant.",
        "Agency": "Difference versus Employee Referral, holding role mix and job level constant.",
        "Technical": "Shift in odds for technical roles versus corporate roles.",
        "Senior": "Shift in odds for senior roles versus entry roles.",
    }

    regression_table = pd.DataFrame(
        {
            "Term": design.columns,
            "Coefficient": np.round(beta, 3),
            "Odds Ratio": np.round(np.exp(beta), 3),
            "p-value": [round(value, 4) for value in p_values],
            "Meaning": [meanings[column] for column in design.columns],
        }
    )

    return regression_table


def prepare_hiring_offer_rate_analysis(hiring_demo: pd.DataFrame) -> dict[str, object]:
    source_summary = (
        hiring_demo.groupby("Hiring_Source", as_index=False)[["Applicants", "Offers"]]
        .sum()
        .sort_values("Offers", ascending=False)
        .reset_index(drop=True)
    )
    source_summary["Offer_Rate"] = source_summary["Offers"] / source_summary["Applicants"]
    source_summary["Offers_Label"] = source_summary["Offers"].astype(int).astype(str)
    source_summary["Applicants_Label"] = source_summary["Applicants"].map(lambda value: f"{value} applicants")
    source_summary["Offer_Rate_Label"] = source_summary["Offer_Rate"].map(lambda value: f"{value:.1%}")
    job_board = source_summary.loc[source_summary["Hiring_Source"] == "Job Board"].iloc[0]
    referral = source_summary.loc[source_summary["Hiring_Source"] == "Employee Referral"].iloc[0]
    p1 = float(job_board["Offers"]) / float(job_board["Applicants"])
    p2 = float(referral["Offers"]) / float(referral["Applicants"])
    pooled = float(job_board["Offers"] + referral["Offers"]) / float(job_board["Applicants"] + referral["Applicants"])
    standard_error = math.sqrt(
        pooled * (1 - pooled) * ((1 / float(job_board["Applicants"])) + (1 / float(referral["Applicants"])))
    )
    observed_difference = p1 - p2
    z_stat = (observed_difference / standard_error) if standard_error else 0.0
    p_value = math.erfc(abs(z_stat) / math.sqrt(2))
    decision = "Reject H0" if p_value < 0.05 else "Fail to reject H0"
    interpretation = (
        "Job Board creates the most offers in raw volume, but its offer conversion rate is significantly lower than Employee Referral after adjusting for applicant volume."
        if p_value < 0.05
        else "The raw offer-count gap does not prove one source converts candidates better once applicant volume is taken into account."
    )
    observed = np.column_stack(
        [
            source_summary["Offers"].to_numpy(dtype=float),
            (source_summary["Applicants"] - source_summary["Offers"]).to_numpy(dtype=float),
        ]
    )
    row_totals = observed.sum(axis=1, keepdims=True)
    column_totals = observed.sum(axis=0, keepdims=True)
    grand_total = observed.sum()
    expected = row_totals @ column_totals / grand_total
    chi_square_steps = []
    for row_index, source in enumerate(source_summary["Hiring_Source"]):
        for col_index, outcome in enumerate(["Offer", "No offer"]):
            observed_value = observed[row_index, col_index]
            expected_value = expected[row_index, col_index]
            contribution = ((observed_value - expected_value) ** 2) / expected_value
            chi_square_steps.append(
                {
                    "Hiring Source": source,
                    "Outcome": outcome,
                    "Observed": int(observed_value),
                    "Expected": round(float(expected_value), 2),
                    "Contribution to chi-square": round(float(contribution), 3),
                }
            )
    chi_square_stat = float(((observed - expected) ** 2 / expected).sum())
    chi_square_df = int((observed.shape[0] - 1) * (observed.shape[1] - 1))
    chi_square_p_value = float(_chi_square_survival(chi_square_stat, chi_square_df))
    chi_square_decision = "Reject H0" if chi_square_p_value < 0.05 else "Fail to reject H0"
    chi_square_interpretation = (
        "At least one hiring source appears to convert applicants to offers differently overall, so HR should inspect source-level rates instead of raw counts."
        if chi_square_p_value < 0.05
        else "The overall source-to-offer relationship is not strong enough to call one channel meaningfully different based on this demo alone."
    )
    source_summary["Expected_Offers"] = np.round(expected[:, 0], 2)
    regression_table = _fit_grouped_logistic_regression(hiring_demo)
    regression_interpretation = (
        "Once role mix and job level are controlled for, the Job Board penalty shrinks and technical roles remain the clearest drag on offer conversion. That tells HR some of the raw gap is really a mix effect."
    )

    return {
        "source_summary": source_summary,
        "job_board_offers": int(job_board["Offers"]),
        "employee_referral_offers": int(referral["Offers"]),
        "job_board_rate": p1,
        "employee_referral_rate": p2,
        "pooled_rate": pooled,
        "standard_error": float(standard_error),
        "observed_difference": float(observed_difference),
        "z_stat": float(z_stat),
        "p_value": float(p_value),
        "decision": decision,
        "interpretation": interpretation,
        "chi_square_stat": chi_square_stat,
        "chi_square_steps": pd.DataFrame(chi_square_steps),
        "chi_square_df": chi_square_df,
        "chi_square_p_value": chi_square_p_value,
        "chi_square_decision": chi_square_decision,
        "chi_square_interpretation": chi_square_interpretation,
        "regression_formula": "logit(P(Offer)) = beta0 + beta1[Job Board] + beta2[Campus] + beta3[Agency] + beta4[Technical] + beta5[Senior]",
        "regression_reference": "Reference group = Employee Referral, Corporate, Entry roles.",
        "regression_table": regression_table,
        "regression_interpretation": regression_interpretation,
    }


def summarize_business_findings(df: pd.DataFrame, budget: int = 450000) -> dict[str, float | str]:
    pay_summary = prepare_pay_segment_summary(df)
    equity = prepare_pay_equity_summary(df)
    scenarios = forecast_retention_scenarios(df, budget)

    critical = pay_summary[pay_summary["Talent_Segment"] == "Critical Talent"]
    critical_employees = critical["Employees"].sum()
    critical_below_market = critical.loc[critical["Pay_Gap_Pct"] < 0, "Employees"].sum()
    critical_below_market_share = (critical_below_market / critical_employees * 100) if critical_employees else 0.0
    critical_attrition = critical["Attrition_Rate"].mean() if not critical.empty else 0.0

    top_pocket = pay_summary.iloc[0] if not pay_summary.empty else None
    worst_gap = equity.iloc[0] if not equity.empty else None
    best_scenario = recommend_cb_action(scenarios)

    return {
        "critical_below_market_share": critical_below_market_share,
        "critical_attrition": critical_attrition,
        "top_pocket_label": (
            f"{top_pocket['Department']} / {top_pocket['Location']} / {top_pocket['Talent_Segment']}"
            if top_pocket is not None
            else "No risk pocket available"
        ),
        "top_pocket_risk": float(top_pocket["Flight_Risk_Index"]) if top_pocket is not None else 0.0,
        "largest_equity_gap": float(worst_gap["Gap_Pct"]) if worst_gap is not None else 0.0,
        "largest_equity_gap_label": (
            f"{worst_gap['Department']} / Perf {int(worst_gap['Perf_Rating'])}"
            if worst_gap is not None
            else "No equity comparison available"
        ),
        "best_scenario": best_scenario["Scenario"],
        "best_scenario_exits_avoided": float(best_scenario["Estimated_Exits_Avoided"]),
    }


def render_pay_question_board_section(filtered_df: pd.DataFrame):
    if filtered_df.empty:
        st.warning("No employees match the current department and location filters.")
        return

    metrics = summarize_descriptive_metrics(filtered_df)
    flow = prepare_workforce_flow(filtered_df)
    pay_summary = prepare_pay_segment_summary(filtered_df)
    equity = prepare_pay_equity_summary(filtered_df)
    findings = summarize_business_findings(filtered_df)

    st.markdown('<div class="section-kicker">Board Snapshot</div>', unsafe_allow_html=True)
    metric_cols = st.columns(6)
    metric_specs = [
        ("Headcount", f"{int(metrics['headcount']):,}", f"{filtered_df['Department'].nunique()} departments in scope"),
        ("Avg Pay", f"${metrics['avg_salary']:,.0f}", f"Median ${filtered_df['Salary'].median():,.0f}"),
        ("Overall Attrition", f"{metrics['turnover_rate']:.1f}%", f"{int(filtered_df['Left'].sum())} exits in scope"),
        ("Critical Attrition", f"{findings['critical_attrition']:.1f}%", "Average rate for high performers"),
        ("Critical Talent Below Market", f"{findings['critical_below_market_share']:.1f}%", "Share of critical talent paid below market anchor"),
        ("Largest Women Pay Gap", f"{findings['largest_equity_gap']:.1f}%", f"{findings['largest_equity_gap_label']}"),
    ]
    for col, (label, value, caption) in zip(metric_cols, metric_specs):
        col.markdown(build_metric_card(label, value, caption), unsafe_allow_html=True)

    st.markdown('<div class="section-kicker">How The Question Is Answered With Data</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="board-panel">
            <strong>Answering the business issue requires four lenses.</strong>
            <p>We first size the workforce and attrition pressure, then test whether critical talent is being paid below market, check whether pay equity gaps persist within comparable performance groups, and finally estimate which C&B interventions would protect the most talent within budget.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    overview_left, overview_right = st.columns([1.35, 1.0])
    with overview_left:
        flow_long = flow.melt(id_vars="Report_Month_Label", var_name="Event", value_name="Employees")
        fig_flow = px.bar(
            flow_long,
            x="Report_Month_Label",
            y="Employees",
            color="Event",
            barmode="group",
            title="Workforce Movement Sets The Retention Cost Context",
            color_discrete_map={"Hires": PALETTE[2], "Exits": PALETTE[1]},
        )
        fig_flow.update_xaxes(categoryorder="array", categoryarray=flow["Report_Month_Label"].tolist())
        style_descriptive_figure(fig_flow, height=350)
        st.plotly_chart(fig_flow, width="stretch")
        peak_exit = flow.loc[flow["Exits"].idxmax(), "Report_Month_Label"]
        render_chart_summary(
            f"Exit pressure peaks in {peak_exit}, which shows why improving retention economics matters before adding more external hiring spend."
        )

    with overview_right:
        dept_pressure = (
            pay_summary.assign(
                Weighted_Pay_Gap=pay_summary["Pay_Gap_Pct"] * pay_summary["Employees"],
                Weighted_Attrition=pay_summary["Attrition_Rate"] * pay_summary["Employees"],
            )
            .groupby("Department", observed=False)
            .agg(
                Employees=("Employees", "sum"),
                Weighted_Pay_Gap=("Weighted_Pay_Gap", "sum"),
                Weighted_Attrition=("Weighted_Attrition", "sum"),
            )
            .reset_index()
        )
        dept_pressure["Weighted_Pay_Gap_Pct"] = dept_pressure["Weighted_Pay_Gap"] / dept_pressure["Employees"]
        dept_pressure["Attrition_Rate"] = dept_pressure["Weighted_Attrition"] / dept_pressure["Employees"]
        dept_pressure = dept_pressure[["Department", "Weighted_Pay_Gap_Pct", "Attrition_Rate"]].sort_values(
            "Weighted_Pay_Gap_Pct"
        )
        fig_pressure = px.bar(
            dept_pressure,
            x="Weighted_Pay_Gap_Pct",
            y="Department",
            color="Attrition_Rate",
            orientation="h",
            text="Weighted_Pay_Gap_Pct",
            title="Departments Most Exposed To Pay Competitiveness Pressure",
            color_continuous_scale=[PALETTE[2], PALETTE[1]],
        )
        fig_pressure.update_traces(texttemplate="%{text:.1f}%")
        style_descriptive_figure(fig_pressure, height=350, show_legend=False)
        st.plotly_chart(fig_pressure, width="stretch")
        most_exposed = dept_pressure.iloc[0]
        render_chart_summary(
            f"{most_exposed['Department']} has the deepest weighted pay gap versus the internal market anchor, making it the first place to test pay competitiveness fixes."
        )

    context_left, context_right = st.columns(2)
    with context_left:
        risk_by_salary = (
            filtered_df.groupby("Salary_Band", observed=False)
            .agg(Attrition_Rate=("Left", lambda s: s.mean() * 100), Employees=("Employee_ID", "count"))
            .reset_index()
        )
        fig_salary_risk = px.bar(
            risk_by_salary,
            x="Salary_Band",
            y="Attrition_Rate",
            color="Employees",
            title="Retention Risk Is Strongest In Lower Salary Bands",
            color_continuous_scale=[PALETTE[3], PALETTE[1]],
        )
        style_descriptive_figure(fig_salary_risk, height=320, show_legend=False)
        fig_salary_risk.update_coloraxes(showscale=False)
        st.plotly_chart(fig_salary_risk, width="stretch")
        riskiest_band = risk_by_salary.sort_values("Attrition_Rate", ascending=False).iloc[0]
        render_chart_summary(
            f"The {riskiest_band['Salary_Band']} band has the highest attrition rate, which reinforces the link between lower relative pay and exit risk."
        )

    with context_right:
        if equity.empty:
            st.info("Not enough comparable women/men records remain in the current filter to display a pay-equity comparison.")
        else:
            fig_equity = px.bar(
                equity.head(8).sort_values("Gap_Pct"),
                x="Gap_Pct",
                y="Department",
                color="Perf_Rating",
                orientation="h",
                text="Gap_Pct",
                title="Comparable Pay Gaps Show Where Equity Pressure Persists",
                color_continuous_scale=[PALETTE[0], PALETTE[1]],
            )
            fig_equity.update_traces(texttemplate="%{text:.1f}%")
            style_descriptive_figure(fig_equity, height=320)
            st.plotly_chart(fig_equity, width="stretch")
            worst_gap = equity.iloc[0]
            render_chart_summary(
                f"The widest women-versus-men gap appears in {worst_gap['Department']} at performance level {int(worst_gap['Perf_Rating'])}, pointing to a targeted equity review rather than a blanket pay change."
            )


def render_descriptive_tab(filtered_df: pd.DataFrame):
    st.header("Phase 1: Descriptive - Workforce Snapshot")
    st.markdown(
        '<div class="dashboard-intro">A denser executive view of workforce composition, mobility, and demographic mix for the currently filtered population.</div>',
        unsafe_allow_html=True,
    )

    if filtered_df.empty:
        st.warning("No employees match the current department and location filters.")
        return

    metrics = summarize_descriptive_metrics(filtered_df)
    flow = prepare_workforce_flow(filtered_df)
    company_salary = filtered_df["Salary"].median()
    attrition_cases = int(filtered_df["Left"].sum())
    men_share = filtered_df["Gender"].eq("Men").mean() * 100
    high_perf_share = (filtered_df["Perf_Rating"] >= 4).mean() * 100

    st.markdown('<div class="section-kicker">Executive Overview</div>', unsafe_allow_html=True)
    metric_cols = st.columns(6)
    metric_specs = [
        ("Headcount", f"{int(metrics['headcount']):,}", f"{filtered_df['Department'].nunique()} departments in scope"),
        ("Avg Salary", f"${metrics['avg_salary']:,.0f}", f"Median ${company_salary:,.0f}"),
        ("Turnover Rate", f"{metrics['turnover_rate']:.1f}%", f"{attrition_cases} exit records"),
        ("Avg Tenure", f"{metrics['avg_tenure']:.1f} yrs", f"Median age {metrics['median_age']:.0f}"),
        ("Women Representation", f"{metrics['female_share']:.1f}%", f"Men {men_share:.1f}%"),
        ("Promotion Rate", f"{metrics['promotion_rate']:.1f}%", f"{high_perf_share:.1f}% high performers"),
    ]
    for col, (label, value, caption) in zip(metric_cols, metric_specs):
        col.markdown(build_metric_card(label, value, caption), unsafe_allow_html=True)

    st.markdown('<div class="section-kicker">Workforce Flow</div>', unsafe_allow_html=True)
    top_left, top_right = st.columns([1.45, 1.0])

    with top_left:
        flow_long = flow.melt(id_vars="Report_Month_Label", var_name="Event", value_name="Employees")
        fig_flow = px.bar(
            flow_long,
            x="Report_Month_Label",
            y="Employees",
            color="Event",
            barmode="group",
            title="Monthly Hires vs Exits",
            color_discrete_map={"Hires": PALETTE[0], "Exits": PALETTE[1]},
        )
        fig_flow.update_xaxes(categoryorder="array", categoryarray=flow["Report_Month_Label"].tolist())
        style_descriptive_figure(fig_flow, height=360)
        st.plotly_chart(fig_flow, width="stretch")

    with top_right:
        dept_mix = (
            filtered_df.groupby("Department")
            .agg(Headcount=("Employee_ID", "count"), Avg_Salary=("Salary", "mean"))
            .reset_index()
            .sort_values("Headcount", ascending=True)
        )
        fig_dept = px.bar(
            dept_mix,
            x="Headcount",
            y="Department",
            color="Avg_Salary",
            orientation="h",
            text="Headcount",
            title="Department Mix",
            color_continuous_scale=[PALETTE[2], PALETTE[0]],
        )
        fig_dept.update_traces(textposition="outside")
        style_descriptive_figure(fig_dept, height=360, show_legend=False)
        fig_dept.update_coloraxes(showscale=False)
        st.plotly_chart(fig_dept, width="stretch")

    st.markdown('<div class="section-kicker">Demographic Composition</div>', unsafe_allow_html=True)
    comp_left, comp_mid, comp_right = st.columns(3)

    with comp_left:
        gender_mix = filtered_df["Gender"].value_counts().rename_axis("Gender").reset_index(name="Employees")
        fig_gender = px.pie(
            gender_mix,
            names="Gender",
            values="Employees",
            hole=0.62,
            title="Gender Split",
            color="Gender",
            color_discrete_sequence=PALETTE,
        )
        style_descriptive_figure(fig_gender, height=320)
        st.plotly_chart(fig_gender, width="stretch")

    with comp_mid:
        age_mix = (
            filtered_df["Age_Band"]
            .value_counts(sort=False)
            .rename_axis("Age_Band")
            .reset_index(name="Employees")
        )
        fig_age = px.bar(
            age_mix,
            x="Age_Band",
            y="Employees",
            title="Age Band Composition",
            color="Employees",
            color_continuous_scale=[PALETTE[3], PALETTE[0]],
        )
        style_descriptive_figure(fig_age, height=320, show_legend=False)
        fig_age.update_coloraxes(showscale=False)
        st.plotly_chart(fig_age, width="stretch")

    with comp_right:
        location_mix = filtered_df["Location"].value_counts().rename_axis("Location").reset_index(name="Employees")
        fig_location = px.pie(
            location_mix,
            names="Location",
            values="Employees",
            hole=0.55,
            title="Location Mix",
            color_discrete_sequence=PALETTE,
        )
        style_descriptive_figure(fig_location, height=320)
        st.plotly_chart(fig_location, width="stretch")

    st.markdown('<div class="section-kicker">Distribution Detail</div>', unsafe_allow_html=True)
    dist_left, dist_right = st.columns([1.0, 1.2])

    with dist_left:
        tenure_mix = (
            filtered_df.groupby(["Tenure_Band", "Gender"], observed=False)
            .size()
            .reset_index(name="Employees")
        )
        fig_tenure = px.bar(
            tenure_mix,
            x="Tenure_Band",
            y="Employees",
            color="Gender",
            barmode="stack",
            title="Tenure Bands by Gender",
            color_discrete_sequence=PALETTE,
        )
        style_descriptive_figure(fig_tenure, height=340)
        st.plotly_chart(fig_tenure, width="stretch")

    with dist_right:
        salary_mix = (
            filtered_df.groupby(["Department", "Salary_Band"], observed=False)
            .size()
            .reset_index(name="Employees")
        )
        fig_salary = px.bar(
            salary_mix,
            x="Salary_Band",
            y="Employees",
            color="Department",
            barmode="group",
            title="Salary Distribution by Department",
            color_discrete_sequence=PALETTE,
        )
        style_descriptive_figure(fig_salary, height=340)
        st.plotly_chart(fig_salary, width="stretch")


def render_diagnostic_tab(filtered_df: pd.DataFrame):
    st.header("Phase 2: Diagnostic - Why is retention risk happening?")
    st.markdown(
        '<div class="dashboard-intro">These diagnostics connect pay levels and performance to attrition patterns, then cross-check whether the story holds within talent segments, tenure, and performance.</div>',
        unsafe_allow_html=True,
    )

    if filtered_df.empty:
        st.warning("No employees match the current department and location filters.")
        return

    hypothesis_test = prepare_salary_attrition_hypothesis_test(filtered_df)
    turnover_demo, hiring_demo = prepare_diagnostic_teaching_examples()
    turnover_analysis = prepare_turnover_rate_analysis(turnover_demo)
    hiring_analysis = prepare_hiring_offer_rate_analysis(hiring_demo)

    salary_attrition = filtered_df.copy()
    salary_attrition["Attrition_Status"] = salary_attrition["Left"].map({0: "Stayed", 1: "Exited"})
    fig_box = px.box(
        salary_attrition,
        x="Department",
        y="Salary",
        color="Attrition_Status",
        title="Departed Employees Skew Lower-Paid In Several Functions",
        color_discrete_map={"Stayed": PALETTE[2], "Exited": PALETTE[1]},
    )
    style_descriptive_figure(fig_box, height=350)
    st.plotly_chart(fig_box, width="stretch")
    stayed_pay = salary_attrition.loc[salary_attrition["Attrition_Status"] == "Stayed", "Salary"].median()
    exited_pay = salary_attrition.loc[salary_attrition["Attrition_Status"] == "Exited", "Salary"].median()
    render_chart_summary(
        f"Employees who exited earn about ${stayed_pay - exited_pay:,.0f} less at the median than employees who stayed, signaling that pay competitiveness is part of the retention story."
    )

    st.markdown("#### Hypothesis test spotlight")
    spotlight_left, spotlight_right = st.columns([1.2, 1.0])
    with spotlight_left:
        st.markdown(
            "\n\n".join(
                [
                    f"**Business question:** Do employees who exited earn significantly less than employees who stayed?",
                    f"**Test used:** {hypothesis_test['test_name']}",
                    f"**Null hypothesis:** {hypothesis_test['null_hypothesis']}",
                    f"**Alternative hypothesis:** {hypothesis_test['alternative_hypothesis']}",
                    f"**Decision:** {hypothesis_test['decision']}",
                ]
            )
        )
    with spotlight_right:
        st.markdown(
            "\n\n".join(
                [
                    f"**Stayed (n):** {hypothesis_test['stayed_n']}",
                    f"**Exited (n):** {hypothesis_test['exited_n']}",
                    f"**Mean salary gap:** ${hypothesis_test['mean_gap']:,.0f}",
                    f"**Standard error:** ${hypothesis_test['standard_error']:,.0f}",
                    f"**t-statistic:** {hypothesis_test['t_stat']:.2f}",
                    f"**p-value:** {hypothesis_test['p_value']:.4f}",
                ]
            )
        )
    st.markdown("**Formulas used in this test**")
    st.latex(r"\bar{x}_{stay} = \frac{1}{n_{stay}} \sum_{i=1}^{n_{stay}} x_i \qquad \bar{x}_{exit} = \frac{1}{n_{exit}} \sum_{i=1}^{n_{exit}} x_i")
    st.latex(r"\text{Mean gap} = \bar{x}_{stay} - \bar{x}_{exit}")
    st.latex(r"SE = \sqrt{\frac{s_{stay}^{2}}{n_{stay}} + \frac{s_{exit}^{2}}{n_{exit}}}")
    st.latex(r"t = \frac{(\bar{x}_{stay} - \bar{x}_{exit}) - 0}{SE}")
    st.latex(r"p \approx P(Z \ge t) = \frac{1}{2}\operatorname{erfc}\left(\frac{t}{\sqrt{2}}\right)")
    st.markdown(
        "\n\n".join(
            [
                "**Using for this dashboard:** We compare the average salary of employees who stayed with the average salary of employees who exited.",
                "**Decision rule:** Reject H0 when the one-sided p-value is below 0.05 and the exited mean salary is lower than the stayed mean salary.",
                "**Interpretation note:** This supports a statistically significant salary difference in the current filter, but it does not prove salary caused attrition.",
            ]
        )
    )
    render_chart_summary(hypothesis_test["interpretation"])

    st.markdown("#### Cross-check the salary story")
    cross_left, cross_right = st.columns(2)
    with cross_left:
        segment_scatter = prepare_salary_risk_by_talent_segment(filtered_df)
        if segment_scatter.empty:
            st.info("Not enough records remain in the current filter to compare salary and exit risk within talent segments.")
        else:
            fig_segment_scatter = px.scatter(
                segment_scatter,
                x="Salary",
                y="Risk_Pct",
                color="Talent_Segment",
                size="Tenure_Years",
                hover_data=["Department", "Location", "Gender"],
                title="Salary vs Exit Risk Within Talent Segments",
                color_discrete_sequence=PALETTE,
            )
            style_descriptive_figure(fig_segment_scatter, height=350)
            st.plotly_chart(fig_segment_scatter, width="stretch")
            segment_corr = segment_scatter[["Salary", "Exit_Prob"]].corr().iloc[0, 1]
            riskiest_segment = (
                segment_scatter.groupby("Talent_Segment", observed=False)["Risk_Pct"]
                .mean()
                .sort_values(ascending=False)
                .index[0]
            )
            render_chart_summary(
                f"Even after comparing employees within talent segments, the salary-risk relationship stays negative ({segment_corr:.2f}). {riskiest_segment} still carries the highest average exit risk, so the pay story is not only a mix-of-roles effect."
            )

    with cross_right:
        tenure_perf_attrition = prepare_attrition_by_tenure_performance(filtered_df)
        if tenure_perf_attrition.empty:
            st.info("Not enough records remain in the current filter to render the tenure and performance attrition heatmap.")
        else:
            tenure_perf_matrix = tenure_perf_attrition.pivot(
                index="Perf_Rating",
                columns="Tenure_Band",
                values="Attrition_Rate",
            ).sort_index()
            fig_tenure_perf_heatmap = px.imshow(
                tenure_perf_matrix,
                text_auto=".1f",
                aspect="auto",
                color_continuous_scale="YlOrRd",
                title="Attrition Hotspots By Tenure And Performance",
            )
            fig_tenure_perf_heatmap.update_layout(xaxis_title="Tenure Band", yaxis_title="Performance Rating")
            style_descriptive_figure(fig_tenure_perf_heatmap, height=350, show_legend=False)
            st.plotly_chart(fig_tenure_perf_heatmap, width="stretch")
            hottest_tenure_perf = tenure_perf_attrition.sort_values("Attrition_Rate", ascending=False).iloc[0]
            render_chart_summary(
                f"The hottest exit pocket sits at performance level {int(hottest_tenure_perf['Perf_Rating'])} in the {hottest_tenure_perf['Tenure_Band']} group. That means tenure and performance matter too, so HR should treat pay as one driver within a broader retention pattern."
            )

    segment_gap = prepare_salary_gap_by_talent_segment(filtered_df)
    if segment_gap.empty:
        st.info("Not enough records remain in the current filter to compare stayed versus exited pay within talent segments.")
    else:
        fig_segment_gap = px.bar(
            segment_gap,
            x="Talent_Segment",
            y="Median_Salary",
            color="Attrition_Status",
            barmode="group",
            title="Stayed vs Exited Salary Gap By Talent Segment",
            color_discrete_map={"Stayed": PALETTE[2], "Exited": PALETTE[1]},
        )
        style_descriptive_figure(fig_segment_gap, height=350)
        st.plotly_chart(fig_segment_gap, width="stretch")
        segment_pivot = (
            segment_gap.pivot(index="Talent_Segment", columns="Attrition_Status", values="Median_Salary")
            .dropna()
        )
        if segment_pivot.empty:
            render_chart_summary(
                "The current filter does not leave enough stayed and exited records inside the same talent segment to confirm a stable within-segment pay gap."
            )
        else:
            segment_pivot["Median_Gap"] = segment_pivot["Stayed"] - segment_pivot["Exited"]
            widest_gap_segment = segment_pivot["Median_Gap"].idxmax()
            widest_gap_value = segment_pivot.loc[widest_gap_segment, "Median_Gap"]
            broad_pattern = (segment_pivot["Median_Gap"] > 0).sum()
            render_chart_summary(
                f"The largest within-segment pay gap appears in {widest_gap_segment}, where exited employees sit about ${widest_gap_value:,.0f} below stayed employees at the median. The lower-pay exit pattern appears in {broad_pattern} talent segment(s), so it is broader than one isolated pocket."
            )

    st.markdown("#### Common interpretation mistakes")
    st.caption("Teaching-demo examples: these two mini charts are intentionally designed to show how HR can over-interpret visuals without checking sample size, denominators, and the right test.")

    mistake_left, mistake_right = st.columns(2)
    with mistake_left:
        fig_turnover_demo = px.bar(
            turnover_demo.sort_values("Turnover_Rate", ascending=False),
            x="Department",
            y="Turnover_Rate",
            color="Headcount",
            text="Label",
            title="Mistake Demo 1: Highest Turnover Rate Must Mean Worst Problem",
            color_continuous_scale=[PALETTE[3], PALETTE[0]],
        )
        fig_turnover_demo.update_traces(textposition="outside")
        style_descriptive_figure(fig_turnover_demo, height=320, show_legend=False)
        fig_turnover_demo.update_coloraxes(showscale=False)
        st.plotly_chart(fig_turnover_demo, width="stretch")
        st.markdown("**Step 1: Read the diagnostic pattern.**")
        st.markdown(
            f"HR has the highest percentage, but Sales has many more actual exits. HR = 3/18 ({turnover_analysis['hr_rate']:.1f}%) vs Sales = 18/150 ({turnover_analysis['sales_rate']:.1f}%)."
        )

        st.markdown("**Step 2: Name the common mistake.**")
        st.markdown(
            '"HR has the worst turnover problem because it has the highest rate." This is risky because HR is tiny here, so 3 exits create an eye-catching percentage even though Sales lost many more people.'
        )

        st.markdown("**Step 3: Check numerator and denominator.**")
        st.markdown(
            "HR has a small denominator, so always read both the exit count and the total headcount before judging the rate."
        )

        st.markdown("**Step 4: Test whether the difference is meaningful.**")
        st.markdown(
            "Correct statistical approach: run a two-proportion test after checking both the numerator and denominator."
        )
        st.markdown(
            "**What is a two-proportion test?** It is a test used to compare two percentages. Here, it asks whether HR's 16.7% turnover and Sales' 12.0% turnover are meaningfully different, or whether the gap could just be random noise from different group sizes."
        )
        st.markdown("**Null hypothesis:** HR and Sales have the same underlying turnover rate.")

        st.markdown("**Step 5: Build the baseline with p-hat.**")
        st.markdown(
            "**What is p-hat?** It is the combined turnover rate used when the null hypothesis says both groups share the same underlying rate."
        )
        st.markdown(
            "**Pooled proportion:** p-hat = (3 + 18) / (18 + 150) = 21 / 168 = 0.125, meaning 12.5% turnover across HR and Sales combined."
        )

        st.markdown("**Step 6: Calculate the test statistic.**")
        st.markdown(
            "  \n".join(
                [
                    "**Formula:** z = (p1 - p2) / SE",
                    "**Observed difference:** p1 - p2 = 0.167 - 0.120 = 0.047",
                    "**Standard error formula:** SE = sqrt( p-hat * (1 - p-hat) * (1/n1 + 1/n2) )",
                    "**Standard error calculation:** SE = sqrt(0.125 * 0.875 * (1/18 + 1/150)) = 0.0825",
                    f"**Z-test calculation:** z = 0.047 / 0.0825 = {turnover_analysis['z_stat']:.2f}",
                ]
            )
        )

        st.markdown("**Step 7: Read the result.**")
        st.markdown(
            f"Two-proportion result: z = {turnover_analysis['z_stat']:.2f}, p = {turnover_analysis['p_value']:.4f}, decision = {turnover_analysis['decision']}."
        )
        st.markdown(f"**Interpretation:** {turnover_analysis['interpretation']}")

    with mistake_right:
        hiring_summary = hiring_analysis["source_summary"]
        fig_hiring_demo = px.bar(
            hiring_summary,
            x="Hiring_Source",
            y="Offers",
            color="Hiring_Source",
            text="Offers_Label",
            title="Mistake Demo 2: Most Offers Means Best Hiring Source",
            color_discrete_sequence=PALETTE,
            hover_data={
                "Applicants": True,
                "Offers": True,
                "Offer_Rate": ":.1%",
                "Offers_Label": False,
            },
        )
        style_descriptive_figure(fig_hiring_demo, height=320, show_legend=False)
        st.plotly_chart(fig_hiring_demo, width="stretch")
        st.markdown(
            "  \n".join(
                [
                    "**Step 1: Read the diagnostic pattern.** The bar chart shows number of offers by hiring source. Job Board creates the tallest offer bar.",
                    "**Step 2: Name the common mistake.** \"Job Board is clearly the best source because it generated the most offers.\"",
                    "**Why that is risky:** Offer count mostly reflects volume. A source with more applicants can generate more offers even if it is less effective at converting candidates.",
                    "**Step 3: Choose the correct statistical approach.** Normalize first, then test the overall source-to-offer relationship, then control for role mix and job level with regression.",
                ]
            )
        )
        st.markdown("**Step 4: Normalize by exposure**")
        st.markdown(
            "Offer conversion rate = offers / applicants. A large offer bar can still hide a weak conversion rate if that source processed much more volume."
        )
        st.dataframe(
            hiring_summary[["Hiring_Source", "Applicants", "Offers", "Offer_Rate_Label"]].rename(
                columns={"Hiring_Source": "Hiring Source", "Offer_Rate_Label": "Offer Rate"}
            ),
            width="stretch",
            hide_index=True,
        )
        st.markdown(
            "  \n".join(
                [
                    f"**Job Board vs Employee Referral:** Job Board = 36 / 240 offers ({hiring_analysis['job_board_rate']:.1%}) vs Employee Referral = 20 / 80 offers ({hiring_analysis['employee_referral_rate']:.1%}).",
                    f"**Pairwise rate takeaway:** {hiring_analysis['interpretation']}",
                ]
            )
        )
        st.markdown("**Step 5: Chi-square test across all sources**")
        st.markdown(
            "Use a chi-square test when you want to compare the offer / no-offer pattern across all sources at once instead of only comparing two channels. In plain English, a chi-square test checks whether the observed pattern is far enough from the expected pattern to treat the relationship as meaningful."
        )
        offer_no_offer_table = hiring_summary.assign(
            No_Offer=lambda frame: frame["Applicants"] - frame["Offers"],
        )[["Hiring_Source", "Offers", "No_Offer", "Applicants", "Offer_Rate_Label"]].rename(
            columns={
                "Hiring_Source": "Hiring Source",
                "Offers": "Offer",
                "No_Offer": "No offer",
                "Applicants": "Total applicants",
                "Offer_Rate_Label": "Offer rate",
            }
        )
        st.markdown("**Observed offer / no-offer table used for the chi-square test**")
        st.dataframe(offer_no_offer_table, width="stretch", hide_index=True)
        st.markdown("**Chi-square calculation steps**")
        st.markdown(
            "Expected = row total * column total / grand total. Each cell then contributes (Observed - Expected)^2 / Expected, and the chi-square statistic is the sum of all cell contributions."
        )
        st.dataframe(hiring_analysis["chi_square_steps"], width="stretch", hide_index=True)
        st.markdown(
            "  \n".join(
                [
                    "**Null hypothesis:** Hiring source and offer outcome are independent.",
                    "**Formula:** chi-square = sum( (Observed - Expected)^2 / Expected )",
                    f"**Degrees of freedom:** (4 - 1) * (2 - 1) = {hiring_analysis['chi_square_df']}. In plain English, degrees of freedom describe how many parts of the table can vary after the row and column totals are fixed.",
                    f"**Chi-square result:** chi-square = {hiring_analysis['chi_square_stat']:.2f}, p = {hiring_analysis['chi_square_p_value']:.4f}, decision = {hiring_analysis['chi_square_decision']}.",
                    f"**Interpretation:** {hiring_analysis['chi_square_interpretation']}",
                ]
            )
        )
        st.markdown("**Step 6: Regression with controls**")
        st.markdown(
            "Regression lets HR ask whether a source still looks better or worse after controlling for role mix and job level."
        )
        st.markdown(
            "  \n".join(
                [
                    f"**Model:** {hiring_analysis['regression_formula']}",
                    f"**Reference group:** {hiring_analysis['regression_reference']}",
                    "**Odds ratio:** Values below 1.00 mean lower offer odds than the reference after controls; values above 1.00 mean higher odds.",
                ]
            )
        )
        st.dataframe(hiring_analysis["regression_table"], width="stretch", hide_index=True)
        st.markdown(f"**Regression interpretation:** {hiring_analysis['regression_interpretation']}")


def render_predictive_tab(filtered_df: pd.DataFrame):
    st.header("Phase 3: Predictive - Promotion Readiness With Logistic Regression")
    st.markdown(
        '<div class="dashboard-intro">This walkthrough shows how HR can use logistic regression to estimate predicted promotion chance while considering several factors together. It is a decision-support demo, not an automatic promotion rule.</div>',
        unsafe_allow_html=True,
    )

    if filtered_df.empty:
        st.warning("No employees match the current department and location filters.")
        return

    logit_demo = prepare_promotion_logit_demo(filtered_df)
    model_stats = logit_demo["model_stats"]
    interpretation = logit_demo["interpretation"]

    st.markdown("## Promotion Readiness With Logistic Regression")
    st.markdown("## Business question")
    st.markdown(
        "Which employees appear more promotion-ready when HR considers multiple factors together, such as performance, tenure, training, salary, department, and location?"
    )
    st.markdown(
        '<div class="chart-summary"><strong>Important framing.</strong><br/>The model estimates predicted promotion chance. It should support talent review and succession discussion, not decide who gets promoted automatically.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("## Common HR shortcut that can go wrong")
    st.markdown(
        "\n".join(
            [
                "- A common shortcut is to rely on one signal only, such as the latest performance rating or a manager nomination.",
                "- That can miss people who have strong readiness signals across several factors, or overstate readiness when one strong signal hides weaker context elsewhere.",
                "- Logistic regression gives HR a structured way to consider several signals at the same time.",
            ]
        )
    )

    st.markdown("## What is logistic regression?")
    st.markdown(
        "\n".join(
            [
                "**Logistic regression vs. linear regression**",
                "- Linear regression predicts a continuous number, such as salary, engagement score, or time to fill.",
                "- Logistic regression is used when the outcome is categorical, especially a yes/no outcome.",
                "- Instead of drawing a straight line that can go below 0 or above 1, logistic regression maps the model score into a probability bounded between 0 and 1.",
                "",
                "**Logistic regression under the hood**",
                "- The model first creates a linear score from the input variables.",
                "- That score is passed through a sigmoid function, which creates the traditional S-curve.",
                "- Low scores are pushed toward probabilities near 0, high scores are pushed toward probabilities near 1, and scores around the middle change most quickly.",
            ]
        )
    )
    linear_example = pd.DataFrame(
        {
            "Tenure (Years)": [0.5, 1.2, 2.0, 2.8, 3.6, 4.4, 5.2, 6.0, 6.8, 7.6],
            "Salary": [52000, 56500, 61000, 65500, 70000, 73500, 79000, 83500, 87500, 93000],
        }
    )
    linear_coef = np.polyfit(linear_example["Tenure (Years)"], linear_example["Salary"], 1)
    linear_fit = pd.DataFrame(
        {
            "Tenure (Years)": linear_example["Tenure (Years)"],
            "Predicted Salary": np.polyval(linear_coef, linear_example["Tenure (Years)"]),
        }
    )
    fig_linear_intro = px.scatter(
        linear_example,
        x="Tenure (Years)",
        y="Salary",
        title="Linear Regression Concept: Tenure To Salary",
    )
    fig_linear_intro.update_traces(marker=dict(color=PALETTE[2], size=9), name="Observed employees", showlegend=True)
    fig_linear_intro.add_scatter(
        x=linear_fit["Tenure (Years)"],
        y=linear_fit["Predicted Salary"],
        mode="lines",
        line=dict(color=PALETTE[0], width=4),
        name="Linear prediction line",
        hovertemplate="Tenure: %{x:.1f} years<br>Predicted salary: $%{y:,.0f}<extra></extra>",
    )
    fig_linear_intro.update_layout(
        xaxis_title="Tenure (Years)",
        yaxis_title="Salary",
        yaxis=dict(tickprefix="$", separatethousands=True),
    )
    style_descriptive_figure(fig_linear_intro, height=340)
    linear_chart_col, linear_formula_col = st.columns([2, 1])
    with linear_chart_col:
        st.plotly_chart(fig_linear_intro, width="stretch")
    with linear_formula_col:
        slope, intercept = linear_coef
        st.markdown("**Linear regression equation**")
        st.markdown("`Salary = intercept + slope × tenure`")
        st.latex(r"\text{Salary} = b_0 + b_1(\text{Tenure})")
        st.latex(rf"\text{{Salary}} = {intercept:,.0f} + {slope:,.0f}(\text{{Tenure}})")
        st.markdown(
            f"If tenure increases by 1 year, the line estimates salary increases by about `${slope:,.0f}` in this simple example."
        )
    render_chart_summary(
        "When tenure and salary move in a roughly linear pattern, linear regression can draw a straight prediction line and estimate a continuous number such as salary."
    )

    score_range = np.linspace(-8, 8, 200)
    logistic_curve = pd.DataFrame(
        {
            "Model Score": score_range,
            "Predicted Probability": 1 / (1 + np.exp(-score_range)),
        }
    )
    fig_logit_intro = px.line(
        logistic_curve,
        x="Model Score",
        y="Predicted Probability",
        title="Traditional Logistic S-Curve: Model Score To Probability",
    )
    fig_logit_intro.update_traces(line=dict(color=PALETTE[0], width=4), name="Logistic curve", showlegend=True)
    fig_logit_intro.add_hline(
        y=0.5,
        line_dash="dash",
        line_color=GRID,
        annotation_text="0.5 probability reference line",
        annotation_position="top left",
    )
    fig_logit_intro.update_layout(
        xaxis_title="Promotion Readiness Score (model score)",
        yaxis_title="Predicted Promotion Chance",
        yaxis=dict(tickformat=".0%"),
    )
    style_descriptive_figure(fig_logit_intro, height=360)
    st.plotly_chart(fig_logit_intro, width="stretch")
    render_chart_summary(
        "The S-curve is the classic logistic regression shape. In this promotion example, the x-axis can be read as the model's promotion readiness score, and the y-axis translates that score into predicted promotion chance."
    )

    st.markdown("## Why logistic regression fits this problem")
    st.markdown(
        "\n".join(
            [
                "- Promotion is a yes/no historical outcome: an employee was promoted or was not promoted.",
                "- Logistic regression is designed for this kind of binary outcome.",
                "- The output can be translated into predicted promotion chance, which is easier for HR to discuss than technical model coefficients.",
            ]
        )
    )

    st.markdown("## Prepare the model")
    st.markdown(
        "To run this analysis, HR starts with an ordinary employee-level dataset, then cleans it into a model-ready dataset. The important change is that text categories such as department and region/location must be converted into numeric comparison flags before logistic regression can use them."
    )
    st.markdown("**Original HR dataset**")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Employee": "A",
                    "Promoted before": "Yes",
                    "Performance rating": 5,
                    "Tenure years": 4.8,
                    "Training hours": 36,
                    "Salary": "$92k",
                    "Department": "Engineering",
                    "Region": "New York",
                },
                {
                    "Employee": "B",
                    "Promoted before": "No",
                    "Performance rating": 4,
                    "Tenure years": 1.2,
                    "Training hours": 14,
                    "Salary": "$68k",
                    "Department": "Sales",
                    "Region": "Singapore",
                },
                {
                    "Employee": "C",
                    "Promoted before": "Yes",
                    "Performance rating": 4,
                    "Tenure years": 5.6,
                    "Training hours": 28,
                    "Salary": "$81k",
                    "Department": "Marketing",
                    "Region": "London",
                },
                {
                    "Employee": "D",
                    "Promoted before": "No",
                    "Performance rating": 3,
                    "Tenure years": 2.4,
                    "Training hours": 18,
                    "Salary": "$74k",
                    "Department": "R&D",
                    "Region": "Tokyo",
                },
            ]
        ),
        width="stretch",
        hide_index=True,
    )
    st.markdown("**Cleaned dataset ready for logistic regression**")
    st.dataframe(
        pd.DataFrame(
            [
                {
                    "Employee": "A",
                    "Promoted": 1,
                    "Performance": 5,
                    "Tenure": 4.8,
                    "Training": 36,
                    "Salary_10k": 9.2,
                    "Dept_Engineering": 1,
                    "Dept_Sales": 0,
                    "Region_New_York": 1,
                    "Region_Singapore": 0,
                },
                {
                    "Employee": "B",
                    "Promoted": 0,
                    "Performance": 4,
                    "Tenure": 1.2,
                    "Training": 14,
                    "Salary_10k": 6.8,
                    "Dept_Engineering": 0,
                    "Dept_Sales": 1,
                    "Region_New_York": 0,
                    "Region_Singapore": 1,
                },
                {
                    "Employee": "C",
                    "Promoted": 1,
                    "Performance": 4,
                    "Tenure": 5.6,
                    "Training": 28,
                    "Salary_10k": 8.1,
                    "Dept_Engineering": 0,
                    "Dept_Sales": 0,
                    "Region_New_York": 0,
                    "Region_Singapore": 0,
                },
                {
                    "Employee": "D",
                    "Promoted": 0,
                    "Performance": 3,
                    "Tenure": 2.4,
                    "Training": 18,
                    "Salary_10k": 7.4,
                    "Dept_Engineering": 0,
                    "Dept_Sales": 0,
                    "Region_New_York": 0,
                    "Region_Singapore": 0,
                },
            ]
        ),
        width="stretch",
        hide_index=True,
    )
    st.markdown(
        "\n".join(
            [
                "- The original table is easy for HR to read, but the model cannot directly use text such as `Engineering`, `Sales`, or `New York`.",
                "- The cleaned table converts `Promoted before` into `1` and `0`, where 1 means promoted and 0 means not promoted.",
                "- Department and region are converted into dummy variables, where 1 means the employee belongs to that group and 0 means they do not.",
                "- The remaining numeric columns become the predictors: the factors HR wants to consider together.",
                "- After learning from the historical rows, the model estimates each employee's predicted promotion chance.",
            ]
        )
    )

    st.markdown("## How to run the regression")
    st.markdown(
        "After preparing the dataset, the analysis turns the HR question into a model formula and asks the computer to estimate the relationship between each factor and promotion."
    )
    st.markdown("**Step 1: Separate what we want to predict from what we use to predict it**")
    st.latex(
        r"\text{Promoted before} \leftarrow \text{Performance} + \text{Tenure} + \text{Training} + \text{Salary} + \text{Department} + \text{Location}"
    )
    st.markdown(
        "The left side is what HR wants to predict. The right side is the set of employee signals the model uses to make that prediction."
    )
    st.markdown("**Step 2: Write the model formula in HR language**")
    st.markdown(
        "`Predicted promotion chance = performance + tenure + training + salary + department + location`"
    )
    st.markdown("**The model first creates a promotion readiness score:**")
    st.latex(
        r"\text{Score} = b_0 + b_1(\text{Performance}) + b_2(\text{Tenure}) + b_3(\text{Training}) + b_4(\text{Salary}) + b_5(\text{Dept}) + b_6(\text{Region})"
    )
    st.markdown("**Where do `b0`, `b1`, `b2` come from?**")
    st.markdown(
        "They are learned from the historical dataset. The regression tries many possible coefficient values and keeps the set that best separates employees who were promoted from employees who were not promoted."
    )
    st.latex(
        r"\text{Historical data} \rightarrow \text{fit logistic regression} \rightarrow b_0, b_1, b_2, b_3, \ldots"
    )
    st.markdown(
        "In the summary table below, the `coef` column is where those learned values appear. For example, the intercept is `b0`, the performance coefficient is `b1`, the tenure coefficient is `b2`, and so on."
    )
    st.markdown("**Step 3: Let the model learn the pattern from historical employees**")
    st.markdown(
        "This is the fitting step. The computer compares each historical employee's input signals with whether they were promoted before, then estimates the coefficient values that best separate promoted and not-promoted cases."
    )
    sklearn_demo = logit_demo["sklearn_demo"]
    st.code(sklearn_demo["code"], language="python")
    st.markdown("## Run the model and read the summary table")
    summary_table = logit_demo["summary_table"].copy()
    statsmodels_summary = logit_demo["statsmodels_summary"]
    st.markdown("**Statsmodels script using the same model-ready dataset**")
    st.code(statsmodels_summary["code"], language="python")
    st.markdown("**Raw `result.summary()` output**")
    st.code(statsmodels_summary["output"])
    st.markdown("**Step 4: Use the learned pattern to estimate promotion chance**")
    st.markdown(
        "After reading the `coef` column in `result.summary()`, HR can plug those learned coefficients into the score equation with one employee's model-ready values, then convert that score into a predicted promotion chance."
    )
    st.markdown("**Major indicators to notice in `result.summary()`**")
    st.markdown(
        "\n".join(
            [
                "- **No. Observations:** how many historical employee records were used.",
                "- **Pseudo R-squ.:** a model-fit indicator. Higher means the model separates promoted and not-promoted cases better, but it is not interpreted like ordinary linear regression R-squared.",
                "- **LLR p-value:** whether the model as a whole adds useful explanatory power compared with an empty model.",
                "- **coef:** the learned coefficient for each factor. These values become `b0`, `b1`, `b2`, and so on in the score equation.",
                "- **P>|z|:** whether each factor has strong statistical evidence in this model. Smaller values suggest stronger evidence.",
                "- **[0.025, 0.975]:** the confidence interval. If the range crosses zero, HR should be cautious about over-reading that factor.",
            ]
        )
    )
    clear_positive = summary_table[
        (summary_table["Variable"].isin(["Performance rating", "Tenure years"]))
        & (summary_table["coef"] > 0)
        & (summary_table["P>|z|"] < 0.05)
    ]["Variable"].tolist()
    unclear_factors = summary_table[
        (summary_table["Variable"] != "const")
        & (summary_table["[0.025"] <= 0)
        & (summary_table["0.975]"] >= 0)
    ]["Variable"].tolist()
    st.markdown("**How to interpret the current values**")
    st.markdown(
        "\n".join(
            [
                f"- The model used **{model_stats['nobs']:,} employee records**. This is the historical sample behind the coefficient estimates.",
                f"- The **Pseudo R-squared is {model_stats['pseudo_r2']:.3f}**. This suggests the model has some separation power, but promotion is still influenced by factors outside this dataset.",
                f"- The **LLR p-value is {model_stats['llr_pvalue']:.2e}**, so the predictors as a group add meaningful explanatory power compared with an empty model.",
                f"- **Performance rating and tenure are the clearest positive predictors** in this sample: {', '.join(clear_positive)}.",
                f"- For HR interpretation, do not over-interpret variables whose confidence interval crosses zero, such as {', '.join(unclear_factors[:5])}.",
                "- A statistically strong coefficient shows association in the model. It does not prove that the factor alone causes promotion.",
            ]
        )
    )
    learned_equation_terms = []
    for _, row in summary_table.iterrows():
        variable = str(row["Variable"])
        coefficient = float(row["coef"])
        if variable == "const":
            learned_equation_terms.append(f"{coefficient:.3f}")
        else:
            learned_equation_terms.append(f"{coefficient:.3f}({variable})")
    st.markdown("**Score equation using the `coef` column**")
    st.code("Score = " + " + ".join(learned_equation_terms))
    st.markdown("**Meaningful shorthand equation**")
    clear_predictor_labels = {
        "Performance rating": "Performance",
        "Tenure years": "Tenure",
        "Training hours": "Training",
        "Salary ($10k)": "Salary",
    }
    clear_predictors = summary_table[
        (summary_table["Variable"] != "const")
        & (summary_table["coef"] > 0)
        & (summary_table["P>|z|"] < 0.05)
        & (summary_table["[0.025"] > 0)
        & (summary_table["0.975]"] > 0)
    ].copy()
    shorthand_terms = [
        f"{float(row['coef']):.3f}({clear_predictor_labels.get(str(row['Variable']), str(row['Variable']))})"
        for _, row in clear_predictors.iterrows()
    ]
    st.code(
        "Score = "
        + f"{float(summary_table.loc[summary_table['Variable'] == 'const', 'coef'].iloc[0]):.3f}"
        + " + "
        + " + ".join(shorthand_terms)
    )
    st.markdown(
        "This shorthand keeps only the clearest positive predictors from the summary table, so it is easier to explain to HR."
    )
    calculation_example = logit_demo["calculation_example"].copy()
    shorthand_values = {
        str(row["Variable"]): float(row["Employee_Value"])
        for _, row in calculation_example.iterrows()
        if str(row["Variable"]) in {"Performance rating", "Tenure years"}
    }
    shorthand_score = float(summary_table.loc[summary_table["Variable"] == "const", "coef"].iloc[0])
    shorthand_rows = []
    for _, row in clear_predictors.iterrows():
        variable = str(row["Variable"])
        label = clear_predictor_labels.get(variable, variable)
        coefficient = float(row["coef"])
        employee_value = shorthand_values.get(variable, 0.0)
        contribution = coefficient * employee_value
        shorthand_score += contribution
        shorthand_rows.append(
            {
                "Step": f"{label} contribution",
                "Calculation": f"{coefficient:.3f} x {employee_value:.2f}",
                "Value": contribution,
            }
        )
    shorthand_probability = 1 / (1 + np.exp(-shorthand_score))
    shorthand_demo = pd.DataFrame(
        [
            {
                "Step": "Employee inputs",
                "Calculation": f"Performance = {shorthand_values.get('Performance rating', 0.0):.2f}; Tenure = {shorthand_values.get('Tenure years', 0.0):.2f}",
                "Value": np.nan,
            },
            {
                "Step": "Starting point",
                "Calculation": "Intercept",
                "Value": float(summary_table.loc[summary_table["Variable"] == "const", "coef"].iloc[0]),
            },
            *shorthand_rows,
            {
                "Step": "Shorthand score",
                "Calculation": "Intercept + clear predictor contributions",
                "Value": shorthand_score,
            },
            {
                "Step": "Predicted promotion chance",
                "Calculation": "1 / (1 + e^(-score))",
                "Value": shorthand_probability,
            },
        ]
    )
    st.markdown("**How HR can use this equation for promotion advice**")
    st.markdown(
        "\n".join(
            [
                "1. **Collect the employee inputs.** Confirm the employee's current performance rating and tenure.",
                "2. **Calculate a readiness score.** Substitute the employee's values into the shorthand equation.",
                "3. **Convert the score into a probability.** Use the logistic curve formula to translate the score into predicted promotion chance.",
                "4. **Compare employees in context.** Use the result to identify who may need deeper talent-review discussion, not to make an automatic decision.",
                "5. **Add manager and business judgment.** Check role readiness, business need, critical skills, mobility, fairness, and succession context before giving advice.",
            ]
        )
    )
    st.markdown("**What do the score and predicted promotion chance mean?**")
    st.markdown(
        "\n".join(
            [
                "- The **score** is the model's internal promotion-readiness signal. It is not a percentage.",
                "- A higher score means the employee looks more similar to employees who were promoted before, based on the factors included in this model.",
                "- The **predicted promotion chance** converts that score into a percentage using the logistic curve.",
                "- If HR scores all employees, use higher scores to prioritize review, not to automatically decide promotion.",
                "- The final advice still needs manager evidence, role readiness, business need, fairness review, and succession context.",
            ]
        )
    )
    st.markdown("**Numeric demonstration using the current sample employee**")
    st.dataframe(
        shorthand_demo.assign(
            Value=shorthand_demo["Value"].map(lambda value: "" if pd.isna(value) else f"{value:.3f}")
        ),
        width="stretch",
        hide_index=True,
    )
    st.code(
        f"Score = {float(summary_table.loc[summary_table['Variable'] == 'const', 'coef'].iloc[0]):.3f}"
        + "".join(
            f" + {float(row['coef']):.3f}({shorthand_values.get(str(row['Variable']), 0.0):.2f})"
            for _, row in clear_predictors.iterrows()
        )
        + f" = {shorthand_score:.3f}\n"
        + f"Predicted promotion chance = 1 / (1 + e^(-{shorthand_score:.3f})) = {shorthand_probability:.3f} = {shorthand_probability * 100:.0f}%"
    )
    st.markdown("**Promotion advice from the numeric result**")
    st.markdown(
        f"This sample employee's shorthand promotion chance is about **{shorthand_probability * 100:.0f}%** based on the clearest signals in this model. HR can use this as a prompt to review promotion readiness, development evidence, role scope, and manager feedback."
    )
    st.markdown("**Use the score to structure a talent-review conversation**")
    st.markdown(
        "The equation is most useful as a discussion guide: it shows that, in this sample, stronger performance and longer tenure are the clearest historical signals linked with promotion."
    )
    st.markdown("**Presentation wording**")
    st.markdown(
        "> The model suggests this employee has stronger promotion-readiness signals because their performance and tenure look similar to employees who were promoted before. This does not mean the employee should automatically be promoted; it means HR should include them in a more detailed talent-review discussion."
    )

    st.markdown("## Interpretation and action")
    st.markdown(
        "\n".join(
            [
                "- Use the model to identify employees or groups that deserve closer talent-review discussion.",
                "- Review the high-readiness band for succession planning, development planning, and promotion panel preparation.",
                "- Check whether the model is reproducing old bias before using it in any real promotion process.",
                "- Treat predicted promotion chance as decision support, not a decision.",
            ]
        )
    )
    st.dataframe(
        logit_demo["employee_sample"].assign(
            Predicted_Promotion_Chance=lambda frame: frame["Predicted_Promotion_Chance"].map(lambda value: f"{value:.1f}%"),
            Tenure_Years=lambda frame: frame["Tenure_Years"].map(lambda value: f"{value:.1f}"),
        ),
        width="stretch",
        hide_index=True,
    )


def render_prescriptive_tab(filtered_df: pd.DataFrame):
    st.header("Phase 4: Prescriptive - Promotion Action Recommendations")
    st.markdown(
        '<div class="dashboard-intro">This tab turns the promotion-readiness prediction into recommended HR actions, review safeguards, and decision rules. It shows how prescriptive analytics moves from who may need attention to what HR should consider next.</div>',
        unsafe_allow_html=True,
    )

    if filtered_df.empty:
        st.warning("No employees match the current department and location filters.")
        return

    prescriptive = prepare_promotion_prescriptive_actions(filtered_df)
    recommendations = prescriptive["recommendations"]
    action_summary = prescriptive["action_summary"]
    fairness_summary = prescriptive["fairness_summary"]
    capacity_check = prescriptive["capacity_check"]
    constraints = prescriptive["business_constraints"]
    missing_evidence = prescriptive["missing_evidence"]
    bias_audit = prescriptive["bias_audit"]
    business_priority = prescriptive["business_priority"]
    priority_deep_dive = prescriptive["priority_deep_dive"]
    priority_candidate_ranking = prescriptive["priority_candidate_ranking"]
    priority_case_studies = prescriptive["priority_case_studies"]

    panel_count = int((recommendations["Recommended_Action"] == "Promotion panel review").sum())
    stretch_count = int((recommendations["Recommended_Action"] == "Stretch assignment / succession discussion").sum())
    top_chance = float(recommendations["Predicted_Promotion_Chance"].max()) if not recommendations.empty else 0.0

    metric_cols = st.columns(4)
    metric_specs = [
        ("Employees In Scope", f"{len(recommendations):,}", "Filtered population"),
        ("Panel Review Candidates", f"{panel_count:,}", "Ready-now review triggers"),
        ("Stretch / Succession", f"{stretch_count:,}", "Near-ready development moves"),
        ("Highest Predicted Chance", f"{top_chance:.1f}%", "Top individual signal"),
    ]
    for col, (label, value, caption) in zip(metric_cols, metric_specs):
        col.markdown(build_metric_card(label, value, caption), unsafe_allow_html=True)

    st.markdown("## From prediction to recommendation")
    st.markdown(
        "The predictive model estimates promotion-readiness signals. The prescriptive stage turns those signals into recommended next actions, required checks, and safeguards for HR."
    )

    st.markdown("## Recommended action table")
    st.markdown(
        "This table is a review list, not an automatic promotion list. HR should use it to decide who needs panel discussion, stretch scope, development planning, or monitoring."
    )
    st.dataframe(
        recommendations.head(12).assign(
            Predicted_Promotion_Chance=lambda frame: frame["Predicted_Promotion_Chance"].map(lambda value: f"{value:.1f}%"),
            Tenure_Years=lambda frame: frame["Tenure_Years"].map(lambda value: f"{value:.1f}"),
        ),
        width="stretch",
        hide_index=True,
    )

    st.markdown("## Action rules")
    st.markdown(
        "\n".join(
            [
                "- **50% or above:** promotion panel review.",
                "- **30% to 49%:** stretch assignment or succession discussion.",
                "- **15% to 29%:** targeted development plan.",
                "- **Below 15%:** continue monitoring and development support.",
                "- These thresholds are review triggers and should be calibrated by HR, not treated as hard policy.",
            ]
        )
    )

    chart_left, chart_right = st.columns(2)
    with chart_left:
        fig_actions = px.bar(
            action_summary.sort_values("Employees"),
            x="Employees",
            y="Recommended_Action",
            orientation="h",
            color="Avg_Predicted_Promotion_Chance",
            title="Recommended Action Distribution",
            color_continuous_scale=[PALETTE[3], PALETTE[0]],
        )
        style_descriptive_figure(fig_actions, height=340, show_legend=False)
        st.plotly_chart(fig_actions, width="stretch")
        render_chart_summary(
            "The action distribution shows whether the model is creating a manageable review list or too many recommendations for HR capacity."
        )

    with chart_right:
        fig_fairness = px.bar(
            fairness_summary,
            x="Gender",
            y="Panel_Review_Rate",
            color="Gender",
            text="Panel_Review_Rate",
            title="Fairness Check: Panel Review Rate By Gender",
            color_discrete_sequence=PALETTE,
        )
        fig_fairness.update_traces(texttemplate="%{text:.1f}%")
        style_descriptive_figure(fig_fairness, height=340)
        st.plotly_chart(fig_fairness, width="stretch")
        render_chart_summary(
            "Fairness check: HR should investigate large representation gaps before using the recommendation list in a real promotion process."
        )

    st.markdown("## Fairness check")
    st.dataframe(
        fairness_summary.assign(Panel_Review_Rate=lambda frame: frame["Panel_Review_Rate"].map(lambda value: f"{value:.1f}%")),
        width="stretch",
        hide_index=True,
    )

    st.markdown("## What evidence is missing?")
    st.markdown(
        "The model only sees structured data such as performance, tenure, training, salary, department, and location. HR still needs qualitative and business evidence before recommending action."
    )
    st.dataframe(missing_evidence, width="stretch", hide_index=True)

    st.markdown("## Fairness and bias concerns")
    st.markdown(
        "\n".join(
            [
                "- **Are some departments over-recommended?** Compare each department's panel-review rate against the overall rate.",
                "- **Are women or minority groups under-recommended?** This demo has gender data, so it checks women and the lowest-recommended gender group; HR should repeat the same check for race, ethnicity, disability, or other minority data if available.",
                "- **Does the model reproduce old promotion bias?** Compare recommendation patterns with historical promotion-rate gaps.",
                "- **Are high-potential employees being missed?** Look for strong performers who are not flagged for panel review.",
            ]
        )
    )
    st.dataframe(bias_audit, width="stretch", hide_index=True)

    st.markdown("## Business priority alignment")
    st.markdown(
        "Promotion advice should connect to workforce planning, not just individual model scores. The table below shows where recommendations overlap with critical roles, succession risk, retention risk, growth areas, scarce skills, and leadership pipeline gaps."
    )
    st.dataframe(
        business_priority.assign(Attrition_Rate=lambda frame: frame["Attrition_Rate"].map(lambda value: f"{value:.1f}%")),
        width="stretch",
        hide_index=True,
    )
    st.markdown("### How HR combines the business-priority data")
    st.markdown(
        "\n".join(
            [
                "1. **Start with the model recommendation.** Identify employees flagged for panel review or stretch/succession discussion.",
                "2. **Overlay workforce priorities.** Check whether each candidate sits in a critical role, succession-risk group, retention-risk group, growth area, scarce-skill group, or leadership-pipeline gap.",
                "3. **Compare business value and risk.** Prioritize employees where promotion readiness, business need, and risk exposure overlap.",
                "4. **Check missing evidence and fairness.** Validate manager feedback, role scope, leadership behavior, mobility, budget, and representation before making a recommendation.",
                "5. **Turn the analysis into advice.** Use the ranked list and case examples to decide who should go to panel review, stretch assignment, development plan, or monitoring.",
            ]
        )
    )

    priority_chart_data = priority_deep_dive.sort_values("Panel_Review_Count", ascending=False)
    fig_priority_actions = px.bar(
        priority_chart_data,
        x="Business_Priority",
        y=["Panel_Review_Count", "Stretch_Count"],
        barmode="group",
        title="Business Priorities: Panel Review And Stretch Candidates",
        color_discrete_sequence=PALETTE,
    )
    style_descriptive_figure(fig_priority_actions, height=380)
    st.plotly_chart(fig_priority_actions, width="stretch")
    render_chart_summary(
        "This chart shows where promotion-ready and near-ready employees overlap with workforce priorities, helping HR sequence which groups deserve immediate review."
    )

    heatmap_metrics = priority_deep_dive.set_index("Business_Priority")[
        ["Avg_Promotion_Chance", "Avg_Exit_Risk", "Panel_Review_Count", "Stretch_Count"]
    ]
    heatmap_metrics = heatmap_metrics.divide(heatmap_metrics.max().replace(0, 1), axis=1) * 100
    heatmap_metrics = heatmap_metrics.rename(
        columns={
            "Avg_Promotion_Chance": "Readiness Index",
            "Avg_Exit_Risk": "Exit Risk Index",
            "Panel_Review_Count": "Panel Volume Index",
            "Stretch_Count": "Stretch Volume Index",
        }
    )
    fig_priority_heatmap = px.imshow(
        heatmap_metrics,
        text_auto=".1f",
        aspect="auto",
        color_continuous_scale="Blues",
        title="Business Priority Heatmap: Normalized Readiness, Risk, And Action Volume",
    )
    style_descriptive_figure(fig_priority_heatmap, height=430)
    st.plotly_chart(fig_priority_heatmap, width="stretch")
    render_chart_summary(
        "The heatmap normalizes each metric to a 0-100 index, so HR can compare readiness, exit risk, and action volume without raw counts overpowering percentages."
    )

    st.markdown("### Deep dive by business priority")
    for _, priority_row in priority_deep_dive.iterrows():
        priority = str(priority_row["Business_Priority"])
        st.markdown(f"#### {priority}")
        st.markdown(
            "\n".join(
                [
                    f"- **Define the segment:** {priority_row['Segment_Definition']}",
                    f"- **Size the opportunity:** {int(priority_row['Employees']):,} employees are in this priority group.",
                    f"- **Combine model and workforce risk:** average predicted promotion chance is **{priority_row['Avg_Promotion_Chance']:.1f}%** and average forward-looking exit risk is **{priority_row['Avg_Exit_Risk']:.1f}%**.",
                    f"- **Translate into action:** {int(priority_row['Panel_Review_Count']):,} employees are panel-review candidates and {int(priority_row['Stretch_Count']):,} are stretch/succession candidates.",
                    f"- **HR conclusion:** {priority_row['HR_Conclusion']}",
                ]
            )
        )
        single_priority_chart = pd.DataFrame(
            {
                "Measure": ["Employees", "Panel review", "Stretch / succession"],
                "Count": [
                    int(priority_row["Employees"]),
                    int(priority_row["Panel_Review_Count"]),
                    int(priority_row["Stretch_Count"]),
                ],
            }
        )
        fig_single_priority = px.bar(
            single_priority_chart,
            x="Measure",
            y="Count",
            text="Count",
            title=f"{priority}: Segment Size And Promotion Actions",
            color="Measure",
            color_discrete_sequence=PALETTE,
        )
        style_descriptive_figure(fig_single_priority, height=310)
        st.plotly_chart(fig_single_priority, width="stretch")

    st.markdown("### Final ranked promotion suggestion")
    st.markdown(
        "The final ranking combines the model's promotion-readiness score with business-priority fit. Higher priority-fit means the employee connects to more workforce-planning needs, not that promotion is automatic."
    )
    st.dataframe(
        priority_candidate_ranking.assign(
            Predicted_Promotion_Chance=lambda frame: frame["Predicted_Promotion_Chance"].map(lambda value: f"{value:.1f}%"),
            Tenure_Years=lambda frame: frame["Tenure_Years"].map(lambda value: f"{value:.1f}"),
        ),
        width="stretch",
        hide_index=True,
    )

    st.markdown("### Employee case study examples")
    st.markdown(
        "These examples show how HR can turn the ranking into presentation language for a talent-review meeting."
    )
    st.dataframe(priority_case_studies, width="stretch", hide_index=True)

    st.markdown("## Business constraint check")
    st.markdown(
        "Before HR acts on the recommendation list, check whether the promotion panel and managers have enough capacity to review the suggested cases this cycle."
    )
    st.dataframe(capacity_check, width="stretch", hide_index=True)
    st.dataframe(constraints, width="stretch", hide_index=True)

    st.markdown("## Final HR recommendation")
    st.markdown(
        f"""
        <div class="board-panel">
            <strong>Recommended action.</strong>
            <p>Start with the <strong>{panel_count}</strong> employees flagged for promotion panel review, then validate each case against manager evidence, role readiness, business need, fairness, and succession context. Employees in the stretch/succession group should receive near-term development actions rather than an immediate promotion recommendation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ai_adaptation_strategy_tab():
    st.header("AI Adaptation Strategy")
    st.markdown(
        '<div class="dashboard-intro">A privacy-first 4-layer AI adoption strategy for HR analytics. The goal is to use AI as an analytics co-pilot without uploading raw employee-level data into external tools.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="board-panel">
            <strong>Core principle.</strong>
            <p><strong>Do not upload raw employee-level data</strong> into AI unless the tool is approved, governed, and secured by the company. A safer approach is to let AI help with questions, code, interpretation, and reporting style while sensitive data stays inside the company environment.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    layer_cards = [
        {
            "title": "Layer 1: Give AI the business question",
            "purpose": "Use AI to design the analysis before touching sensitive data.",
            "example": "Business question: Are lower-paid employees leaving at a higher rate, and is the pattern still visible after checking department, tenure, performance, and location?",
            "prompt": "Example prompt: We want to understand whether low salary is linked to higher attrition. What analyses, charts, statistical tests, and control variables should HR use?",
            "output": "Expected AI output: box plots, t-test, segment checks, tenure/performance heatmap, caveats about causation, and a checklist of extra evidence HR needs.",
        },
        {
            "title": "Layer 2: Let AI generate the Python dashboard script",
            "purpose": "Ask AI to turn the HR question into a repeatable dashboard workflow. This can be Python, Excel, Power BI, Tableau, or another approved reporting tool.",
            "example": "Example request: Create a dashboard workflow that compares attrition by salary band, department, tenure, performance, and location.",
            "prompt": "Example prompt: Using placeholder columns named Salary, Left, Department, Tenure_Years, Perf_Rating, and Location, show how to build this analysis in Python, Excel, Power BI, Tableau, or an approved low-code tool. Do not use real employee data.",
            "output": "Expected AI output: tool-specific formulas, calculated fields, dashboard layout ideas, chart choices, and step-by-step build instructions that HR or the analytics team can run inside the secure company environment.",
        },
        {
            "title": "Layer 3: Use AI to interpret aggregated patterns",
            "purpose": "Share only aggregated or anonymized results with AI, then ask for safe HR interpretation.",
            "example": "Example input: Exited employees average $82k, stayed employees average $91k, p-value = 0.01, and the gap is strongest in Sales and Marketing.",
            "prompt": "Example prompt: Interpret these aggregated findings for HR. What can we conclude, what can we not conclude, and what follow-up checks are needed?",
            "output": "Expected AI output: plain-English interpretation, warnings about causation, recommended cross-checks, and leadership-ready wording.",
        },
        {
            "title": "Layer 4: Summarise a skill for consistent HR reports",
            "purpose": "Use AI to create a repeatable reporting style so HR analytics outputs are consistent across topics.",
            "example": "Example report structure: business question, data used, method, key finding, interpretation, HR action, fairness check, limitation, next step.",
            "prompt": "Example prompt: Create a reusable HR analytics reporting skill that always writes findings in a cautious, evidence-based, business-friendly style.",
            "output": "Expected AI output: a standard report template, approved wording patterns, fairness reminders, and a checklist for responsible recommendations.",
        },
    ]

    st.markdown("## 4-layer AI adoption strategy")
    for layer in layer_cards:
        st.markdown(f"### {layer['title']}")
        left_col, right_col = st.columns([1.0, 1.2])
        with left_col:
            st.markdown(
                f"""
                <div class="chart-summary">
                    <strong>Purpose.</strong><br/>
                    {layer['purpose']}<br/><br/>
                    <strong>HR example.</strong><br/>
                    {layer['example']}
                </div>
                """,
                unsafe_allow_html=True,
            )
        with right_col:
            st.markdown(f"**{layer['prompt']}**")
            st.markdown(f"**{layer['output']}**")
            if layer["title"] == "Layer 2: Let AI generate the Python dashboard script":
                st.markdown("**Expected output by tool**")
                st.markdown(
                    "Tool options included: Excel or Google Sheets; Power BI; Tableau; Streamlit / Python handled by analytics team; No-code / low-code BI tools."
                )
                st.dataframe(
                    pd.DataFrame(
                        [
                            {
                                "Tool / method": "Excel or Google Sheets",
                                "How AI helps": "Generate formulas, pivot table logic, calculated columns, chart ideas, and step-by-step analysis instructions.",
                                "Related output": "Formula examples, pivot setup, calculated salary bands, attrition-rate charts, and a worksheet build checklist.",
                            },
                            {
                                "Tool / method": "Power BI",
                                "How AI helps": "Write DAX measures, suggest dashboard layouts, create calculated fields, and explain page structure for HR insights.",
                                "Related output": "DAX measures, Power Query steps, slicer suggestions, KPI cards, and page-by-page dashboard design.",
                            },
                            {
                                "Tool / method": "Tableau",
                                "How AI helps": "Suggest calculated fields, dashboard structure, filters, chart choices, and storytelling flow.",
                                "Related output": "Calculated-field logic, worksheet list, filter plan, recommended views, and a presentation storyline.",
                            },
                            {
                                "Tool / method": "Streamlit / Python handled by analytics team",
                                "How AI helps": "Generate reusable Python or Streamlit code while HR reviews the business question, assumptions, and interpretation.",
                                "Related output": "Data-cleaning logic, Plotly charts, statistical-test code, dashboard sections, and interpretation notes.",
                            },
                            {
                                "Tool / method": "No-code / low-code BI tools",
                                "How AI helps": "Translate the analysis into steps for approved internal HR analytics platforms, Power Query, Airtable, or similar tools.",
                                "Related output": "Workflow steps, field-mapping guidance, filter rules, chart recommendations, and governance reminders.",
                            },
                        ]
                    ),
                    width="stretch",
                    hide_index=True,
                )

    st.markdown("## What data is safe to share with AI?")
    safe_data = pd.DataFrame(
        [
            {
                "AI Use": "Business question design",
                "Safe Input": "Problem statement, desired decision, possible variables",
                "Avoid": "Names, employee IDs, raw compensation records",
            },
            {
                "AI Use": "Code generation",
                "Safe Input": "Placeholder column names and sample schema",
                "Avoid": "Actual employee-level dataset",
            },
            {
                "AI Use": "Pattern interpretation",
                "Safe Input": "Aggregated tables, anonymized chart findings, p-values, model metrics",
                "Avoid": "Individual employee rows or identifiable comments",
            },
            {
                "AI Use": "Report style",
                "Safe Input": "Writing standard, tone, approved caveat language",
                "Avoid": "Confidential employee cases unless approved and anonymized",
            },
        ]
    )
    st.dataframe(safe_data, width="stretch", hide_index=True)

    st.markdown("## Presentation wording")
    st.markdown(
        "> We do not need to give AI all employee data to benefit from AI. HR can use AI to frame the analysis, generate code templates, interpret aggregated findings, and standardize reports. Sensitive data stays inside the company environment, while AI improves speed, consistency, and quality of thinking."
    )


def render_app():
    st.set_page_config(page_title="HR Analytics Mastery Demo", layout="wide")
    inject_dashboard_css()
    df = load_data()

    st.sidebar.title("Global Filters")
    dept_filter = st.sidebar.multiselect(
        "Select Department",
        options=sorted(df["Department"].unique()),
        default=sorted(df["Department"].unique()),
    )
    loc_filter = st.sidebar.multiselect(
        "Select Location",
        options=sorted(df["Location"].unique()),
        default=sorted(df["Location"].unique()),
    )

    filtered_df = df[(df["Department"].isin(dept_filter)) & (df["Location"].isin(loc_filter))]

    st.title("HR Analytics: From Data to Business Impact")
    st.markdown("### Introduction Session: The 4 Phases of Analytics")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Descriptive", "Diagnostic", "Predictive", "Prescriptive", "AI Adaptation Strategy"]
    )

    with tab1:
        render_descriptive_tab(filtered_df)
    with tab2:
        render_diagnostic_tab(filtered_df)
    with tab3:
        render_predictive_tab(filtered_df)
    with tab4:
        render_prescriptive_tab(filtered_df)
    with tab5:
        render_ai_adaptation_strategy_tab()


if __name__ == "__main__":
    render_app()
