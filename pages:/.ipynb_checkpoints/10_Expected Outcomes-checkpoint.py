import streamlit as st
import numpy as np
import pandas as pd

# ---------------------------------------------
# Page setup
# ---------------------------------------------
st.set_page_config(
    page_title="Buying vs Renting in Kuala Lumpur: 30-Year Wealth Simulation",
    page_icon="🏠",
    layout="wide",
)

st.title("🏠 Buying vs Renting in Kuala Lumpur: 30-Year Wealth Simulation")

# ---------------------------------------------
# Core financial functions (aligned to the docx assumptions)
# ---------------------------------------------

def monthly_mortgage_payment(principal: float, annual_rate: float, years: int) -> float:
    r = annual_rate / 12.0
    n = years * 12
    if annual_rate == 0:
        return principal / n
    return principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

def fv_lump_sum(pv: float, annual_rate: float, years: int) -> float:
    return pv * ((1 + annual_rate) ** years)

def fv_monthly_annuity(pmt: float, annual_rate: float, years: int) -> float:
    r = annual_rate / 12.0
    n = years * 12
    if annual_rate == 0:
        return pmt * n
    return pmt * (((1 + r) ** n - 1) / r)

def buy_vs_rent_wealth(
    house_price: float = 800_000.0,
    down_pct: float = 0.10,
    mortgage_rate: float = 0.04,
    term_years: int = 30,
    rent_yield: float = 0.045,
    invest_return: float = 0.06,
    home_appreciation: float = 0.02,
):
    loan = house_price * (1 - down_pct)
    down = house_price * down_pct

    m_mort = monthly_mortgage_payment(loan, mortgage_rate, term_years)
    monthly_rent = (house_price * rent_yield) / 12.0
    monthly_contribution = m_mort - monthly_rent

    buy_wealth = fv_lump_sum(house_price, home_appreciation, term_years)
    rent_wealth = fv_lump_sum(down, invest_return, term_years) + fv_monthly_annuity(monthly_contribution, invest_return, term_years)
    diff = buy_wealth - rent_wealth
    return buy_wealth, rent_wealth, diff

# ---------------------------------------------
# Sidebar — Inputs
# ---------------------------------------------
st.sidebar.header("Inputs")
house_price = st.sidebar.number_input("House Price (RM)", min_value=100000, max_value=5_000_000, value=800_000, step=10_000, format="%d")
down_pct = st.sidebar.slider("Down Payment (%)", 0.0, 0.9, 0.10, 0.01)
mortgage_rate = st.sidebar.slider("Mortgage Rate (%)", 0.0, 10.0, 4.0, 0.1) / 100.0
term_years = st.sidebar.slider("Loan Term (years)", 5, 40, 30, 1)
rent_yield = st.sidebar.slider("Rent Yield (% of property / year)", 0.0, 10.0, 4.5, 0.1) / 100.0
invest_return = st.sidebar.slider("Investment Return (%)", 0.0, 15.0, 6.0, 0.1) / 100.0
home_appreciation = st.sidebar.slider("Home Appreciation (%)", 0.0, 10.0, 2.0, 0.1) / 100.0

# Compute base case result
buy_wealth, rent_wealth, diff = buy_vs_rent_wealth(
    house_price=house_price,
    down_pct=down_pct,
    mortgage_rate=mortgage_rate,
    term_years=term_years,
    rent_yield=rent_yield,
    invest_return=invest_return,
    home_appreciation=home_appreciation,
)

col1, col2, col3 = st.columns(3)
col1.metric("Buying Wealth (RM)", f"RM {buy_wealth:,.0f}")
col2.metric("Renting Wealth (RM)", f"RM {rent_wealth:,.0f}")
col3.metric("Buy − Rent (RM)", f"RM {diff:,.0f}", help="Positive means buying leads; negative means renting + investing leads.")

st.divider()

# ---------------------------------------------
# Expected Outcomes — Simple view
# ---------------------------------------------
st.subheader("Simple Expected Outcomes")

exp_cols = st.columns(2)
with exp_cols[0]:
    st.markdown("""
    **When Buying Wins**
    - Mortgage rates are **low (≤ 4%)**
    - Property appreciation is **steady (≥ 2%/yr)**
    - Rent is **expensive (≥ 4.5% of price)**
    - Over **long horizons (≈30 yrs)**
    """)

with exp_cols[1]:
    st.markdown("""
    **When Renting Wins**
    - Mortgage rates are **high (≥ 5.5%)**
    - Property prices **stagnate (~0%)**
    - Investments return **≥ 7–8%**
    - Rent is **cheap (≤ 3.5% of price)**
    """)

st.info("These summaries align with the uploaded report's base-case logic for Kuala Lumpur and are meant as quick decision cues.")

st.divider()

# ---------------------------------------------
# Sensitivity Tables with RM formatting + color coding
# ---------------------------------------------
st.subheader("Sensitivity Tables — Buy − Rent after 30 years (RM)")

def format_rm(val):
    return f"RM {val:,.0f}"

def color_positive_negative(val):
    try:
        numeric = float(val.replace("RM", "").replace(",", "").strip())
    except:
        return ""
    color = "green" if numeric > 0 else "red" if numeric < 0 else "black"
    return f"color: {color}"

# A) Mortgage Rate vs Investment Return
st.markdown("**A) Mortgage Rate (%) × Investment Return (%)**")
mr_grid = np.arange(0.03, 0.0601, 0.005)
ir_grid = np.arange(0.04, 0.1001, 0.01)

data_A = []
for ir in ir_grid:
    row = []
    for mr in mr_grid:
        _, _, d = buy_vs_rent_wealth(
            house_price=house_price,
            down_pct=down_pct,
            mortgage_rate=mr,
            term_years=term_years,
            rent_yield=rent_yield,
            invest_return=ir,
            home_appreciation=home_appreciation,
        )
        row.append(format_rm(d))
    data_A.append(row)

table_A = pd.DataFrame(
    data_A,
    index=[f"{int(x*100)}%" for x in ir_grid],
    columns=[f"{x*100:.1f}%" for x in mr_grid],
)
table_A.index.name = "Investment Return"
table_A.columns.name = "Mortgage Rate"
st.dataframe(table_A.style.applymap(color_positive_negative), use_container_width=True)
st.caption("Green = Buying wins, Red = Renting wins")

# B) Property Appreciation vs Investment Return
st.markdown("**B) Property Appreciation (%) × Investment Return (%)**")
ap_grid = np.arange(0.00, 0.0501, 0.005)

data_B = []
for ir in ir_grid:
    row = []
    for ap in ap_grid:
        _, _, d = buy_vs_rent_wealth(
            house_price=house_price,
            down_pct=down_pct,
            mortgage_rate=mortgage_rate,
            term_years=term_years,
            rent_yield=rent_yield,
            invest_return=ir,
            home_appreciation=ap,
        )
        row.append(format_rm(d))
    data_B.append(row)

table_B = pd.DataFrame(
    data_B,
    index=[f"{int(x*100)}%" for x in ir_grid],
    columns=[f"{x*100:.1f}%" for x in ap_grid],
)
table_B.index.name = "Investment Return"
table_B.columns.name = "Property Appreciation"
st.dataframe(table_B.style.applymap(color_positive_negative), use_container_width=True)
st.caption("Green = Buying wins, Red = Renting wins")

# C) Rent Yield vs Mortgage Rate
st.markdown("**C) Rent Yield (%) × Mortgage Rate (%)**")
ry_grid = np.arange(0.03, 0.0601, 0.005)

data_C = []
for mr in mr_grid:
    row = []
    for ry in ry_grid:
        _, _, d = buy_vs_rent_wealth(
            house_price=house_price,
            down_pct=down_pct,
            mortgage_rate=mr,
            term_years=term_years,
            rent_yield=ry,
            invest_return=invest_return,
            home_appreciation=home_appreciation,
        )
        row.append(format_rm(d))
    data_C.append(row)

table_C = pd.DataFrame(
    data_C,
    index=[f"{x*100:.1f}%" for x in mr_grid],
    columns=[f"{x*100:.1f}%" for x in ry_grid],
)
table_C.index.name = "Mortgage Rate"
table_C.columns.name = "Rent Yield"
st.dataframe(table_C.style.applymap(color_positive_negative), use_container_width=True)
st.caption("Green = Buying wins, Red = Renting wins")

# ---------------------------------------------
# Sources (from the uploaded docx)
# ---------------------------------------------
st.subheader("Sources (from the document)")
SOURCES = [
    ("[1] Malaysia's Residential Property Market Analysis 2025 — Global Property Guide",
     "https://www.globalpropertyguide.com/asia/malaysia/price-history"),
    ("[2] Rental Yields in Malaysia in 2025, Q1 — Global Property Guide",
     "https://www.globalpropertyguide.com/asia/malaysia/rental-yields"),
    ("[3] Base Lending Rates — Maybank Malaysia",
     "https://www.maybank2u.com.my/maybank2u/malaysia/en/personal/rates/blr_rates.page"),
    ("[4] Malaysia c.bank lowers key rate to 2.75% — Reuters",
     "https://www.reuters.com/world/asia-pacific/malaysia-cbank-lowers-key-rate-275-2025-07-09/"),
    ("[5] Malaysia Inflation (CPI) — FocusEconomics",
     "https://www.focus-economics.com/country-indicator/malaysia/inflation/"),
    ("[6] EPF Dividend 2024 — KWSP Malaysia",
     "https://www.kwsp.gov.my/en/others/resource-centre/dividend"),
    ("[7] Buy vs Rent in Malaysia — KWSP Malaysia",
     "https://www.kwsp.gov.my/en/w/article/buy-vs-rent-malaysia"),
]

for label, url in SOURCES:
    st.markdown(f"- {label}  \\\n        <small><a href='{url}' target='_blank'>{url}</a></small>", unsafe_allow_html=True)

# Professional note for transparency
st.caption("*App logic is based on the assumptions in the uploaded report for comparability.*")
