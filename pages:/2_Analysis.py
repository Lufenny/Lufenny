import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---- Sidebar Navigation ----
def navigation_guide(current_page: str):
    pages = [
        "Expected Outcomes",
        "📑 Analysis",
        "📊 EDA",
        "⚙️ Data Process",
        "📈 Modelling",
        "📖 Interpretation",
        "🚀 Deployment"
    ]
    with st.sidebar:
        st.markdown("## 📌 Navigation Guide")
        for page in pages:
            if page == current_page:
                st.markdown(f"🔵 **{page}**")  # highlight active
            else:
                st.markdown(page)

# Call navigation for this page
navigation_guide("📑 Analysis")

# ---- Page Content ----
st.title("📑 Analysis")

st.markdown("### 🔄 Scenario Comparison")
with st.expander("ℹ️ Description", expanded=False):
    st.write("""
    Scenario analysis evaluates how investment outcomes change under 
    alternative future states, such as optimistic, baseline, and 
    pessimistic conditions. This technique supports robust planning by 
    illustrating potential deviations from the central forecast.
    """)

# --- Define Scenarios ---
years = np.arange(2025, 2046)
baseline = np.cumprod([1.05]*len(years)) * 100
optimistic = np.cumprod([1.08]*len(years)) * 100
pessimistic = np.cumprod([1.03]*len(years)) * 100

df_scen = pd.DataFrame({
    "Year": years.astype(int),
    "Baseline (5%)": baseline,
    "Optimistic (8%)": optimistic,
    "Pessimistic (3%)": pessimistic
})

# --- Chart ---
fig, ax = plt.subplots()
ax.plot(df_scen["Year"], df_scen["Baseline (5%)"], label="Baseline (5%)", color="blue")
ax.plot(df_scen["Year"], df_scen["Optimistic (8%)"], label="Optimistic (8%)", color="green")
ax.plot(df_scen["Year"], df_scen["Pessimistic (3%)"], label="Pessimistic (3%)", color="red")
ax.set_xlabel("Year")
ax.set_ylabel("Index Value (Relative Growth)")
ax.set_title("Scenario Comparison")
ax.legend()
st.pyplot(fig)

# --- Download ---
csv = df_scen.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Scenario Results (CSV)",
    data=csv,
    file_name="scenario_analysis.csv",
    mime="text/csv"
)
