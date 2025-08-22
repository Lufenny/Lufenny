import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------
# Page Setup
# ---------------------------------------------
st.set_page_config(page_title="📊 Modelling", page_icon="📊", layout="wide")

# ---- Sidebar Navigation ----
def navigation_guide(current_page: str):
    pages = [
        "Expected Outcomes",
        "📑 Analysis",
        "📊 EDA",
        "⚙️ Data Process",
        "📊 Modelling",
        "📑 Results and Interpretation",
        "🚀 Deployment"
    ]
    with st.sidebar:
        st.markdown("## 📌 Navigation Guide")
        for page in pages:
            if page == current_page:
                st.markdown(f"🔵 **{page}**")
            else:
                st.markdown(page)

navigation_guide("📊 Modelling")

# ---------------------------------------------
# Modelling Content
# ---------------------------------------------
st.title("📊 Modelling")

st.markdown("### 📈 Sensitivity Analysis")
with st.expander("ℹ️ Description", expanded=False):
    st.write("""
    Sensitivity analysis investigates how variations in key parameters—such as 
    contribution rates, return assumptions, and inflation—affect long-term 
    investment outcomes.
    """)

# --- Example Data ---
contrib_rates = [200, 400, 600]
returns = [0.05, 0.07, 0.09]
years = np.arange(2025, 2046)

results = []
for c in contrib_rates:
    for r in returns:
        values = np.cumsum([c * ((1 + r)**i) for i in range(len(years))])
        results.append(pd.DataFrame({
            "Year": years,
            "Contribution": c,
            "Return": r,
            "Value": values
        }))

df_sens = pd.concat(results)

# --- Chart ---
fig, ax = plt.subplots()
for (c, r), group in df_sens.groupby(["Contribution", "Return"]):
    ax.plot(group["Year"], group["Value"], label=f"RM{c}/m @ {int(r*100)}%")
ax.set_title("Sensitivity of Contributions & Returns")
ax.set_xlabel("Year")
ax.set_ylabel("Portfolio Value (RM)")
ax.legend()
st.pyplot(fig)

# --- Download ---
csv = df_sens.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Sensitivity Results (CSV)",
    data=csv,
    file_name="sensitivity_analysis.csv",
    mime="text/csv"
)
