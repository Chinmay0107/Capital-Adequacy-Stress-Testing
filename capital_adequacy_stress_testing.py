import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Capital Adequacy Stress Testing Model", layout="wide")

# Title and Description
st.title("Capital Adequacy Stress Testing Model")
st.markdown("""
This interactive model allows you to simulate the impact of various stress scenarios on capital adequacy ratios. 
Use the dropdown to select predefined scenarios, run Monte Carlo simulations, and explore what-if analyses dynamically.
""")

# Sidebar for Inputs
st.sidebar.title("Inputs")
st.sidebar.markdown("### Bank Financials")

# Financial Inputs
initial_cet1 = st.sidebar.number_input("Initial CET1 Capital ($M)", min_value=0.0, value=1000.0, step=10.0)
initial_tier1 = st.sidebar.number_input("Initial Tier 1 Capital ($M)", min_value=0.0, value=1200.0, step=10.0)
initial_total_capital = st.sidebar.number_input("Initial Total Capital ($M)", min_value=0.0, value=1500.0, step=10.0)
risk_weighted_assets = st.sidebar.number_input("Risk-Weighted Assets (RWA) ($M)", min_value=0.0, value=12000.0, step=100.0)

# Current Base Rates Inputs
st.sidebar.markdown("### Current Rates")
current_interest_rate = st.sidebar.number_input("Current Interest Rate (%)", min_value=0.0, value=3.0, step=0.1)
current_default_rate = st.sidebar.number_input("Current Default Rate (%)", min_value=0.0, value=2.0, step=0.1)
current_market_shock = st.sidebar.number_input("Current Market Shock (%)", min_value=0.0, value=1.0, step=0.1)

# Dropdown for Scenario Selection
scenario = st.sidebar.selectbox(
    "Select a Stress Scenario",
    [
        "Baseline (No Stress)",
        "Mild Recession",
        "Severe Recession",
        "Interest Rate Shock",
        "Market Crash",
        "Credit Crisis",
        "Inflation Shock",
        "Liquidity Stress",
        "Currency Devaluation",
        "Custom Scenario"
    ]
)

# Set Parameters Based on Scenario
if scenario == "Baseline (No Stress)":
    interest_rate_hike = 0.0
    credit_loss_rate = 0.0
    market_shock = 0.0
elif scenario == "Mild Recession":
    interest_rate_hike = 1.0
    credit_loss_rate = 2.0
    market_shock = 3.0
elif scenario == "Severe Recession":
    interest_rate_hike = 2.5
    credit_loss_rate = 5.0
    market_shock = 8.0
elif scenario == "Interest Rate Shock":
    interest_rate_hike = 3.0
    credit_loss_rate = 0.0
    market_shock = 0.0
elif scenario == "Market Crash":
    interest_rate_hike = 0.0
    credit_loss_rate = 0.0
    market_shock = 10.0
elif scenario == "Credit Crisis":
    interest_rate_hike = 0.5
    credit_loss_rate = 8.0
    market_shock = 3.0
elif scenario == "Inflation Shock":
    interest_rate_hike = 4.0
    credit_loss_rate = 1.0
    market_shock = 2.0
elif scenario == "Liquidity Stress":
    interest_rate_hike = 0.0
    credit_loss_rate = 3.0
    market_shock = 5.0
elif scenario == "Currency Devaluation":
    interest_rate_hike = 1.5
    credit_loss_rate = 2.5
    market_shock = 6.0
elif scenario == "Custom Scenario":
    interest_rate_hike = st.sidebar.slider("Interest Rate Hike (%)", 0.0, 5.0, 1.0)
    credit_loss_rate = st.sidebar.slider("Increase in Default Rates (%)", 0.0, 10.0, 2.0)
    market_shock = st.sidebar.slider("Market Shock (%)", 0.0, 10.0, 5.0)

# Stress Testing Logic
interest_rate_loss = risk_weighted_assets * (interest_rate_hike / 100)
credit_losses = risk_weighted_assets * (credit_loss_rate / 100)
market_shock_loss = initial_tier1 * (market_shock / 100)
total_losses = interest_rate_loss + credit_losses + market_shock_loss

updated_cet1 = initial_cet1 - total_losses
updated_cet1_ratio = (updated_cet1 / risk_weighted_assets) * 100

# Display Results
st.header("Stress Testing Results")
col1, col2 = st.columns(2)

with col1:
    st.metric("Initial CET1 Ratio (%)", f"{(initial_cet1 / risk_weighted_assets) * 100:.2f}")
    st.metric("Updated CET1 Ratio (%)", f"{updated_cet1_ratio:.2f}")

# Monte Carlo Simulation
st.sidebar.markdown("### Monte Carlo Simulation")
num_simulations = st.sidebar.number_input("Number of Simulations", min_value=100, max_value=10000, value=1000, step=100)
run_simulation = st.sidebar.button("Run Monte Carlo Simulation")

if run_simulation:
    simulation_results = []
    for _ in range(num_simulations):
        simulated_interest_rate_hike = np.random.uniform(0, 5)
        simulated_credit_loss_rate = np.random.uniform(0, 10)
        simulated_market_shock = np.random.uniform(0, 10)

        simulated_losses = (
            risk_weighted_assets * (simulated_interest_rate_hike / 100)
            + risk_weighted_assets * (simulated_credit_loss_rate / 100)
            + initial_tier1 * (simulated_market_shock / 100)
        )
        simulated_cet1 = initial_cet1 - simulated_losses
        simulated_cet1_ratio = (simulated_cet1 / risk_weighted_assets) * 100
        simulation_results.append(simulated_cet1_ratio)

    # Display Monte Carlo Results
    st.header("Monte Carlo Simulation Results")
    st.write(f"Mean CET1 Ratio: {np.mean(simulation_results):.2f}%")
    st.write(f"Minimum CET1 Ratio: {np.min(simulation_results):.2f}%")
    st.write(f"Maximum CET1 Ratio: {np.max(simulation_results):.2f}%")

    # Create a histogram for distribution
    fig = px.histogram(
        simulation_results,
        nbins=30,
        title="Monte Carlo Simulation: CET1 Ratios",
        labels={"value": "CET1 Ratio (%)", "count": "Frequency"},
    )
    fig.update_layout(
        xaxis_title="CET1 Ratio (%)",
        yaxis_title="Frequency",
        bargap=0.1,
        template="plotly_white",
    )
    st.plotly_chart(fig)

# What-If Analysis
st.header("What-If Analysis")
what_if_interest_rate_hike = st.slider("What-If: Interest Rate Hike (%)", 0.0, 5.0, 0.0)
what_if_credit_loss_rate = st.slider("What-If: Default Rates (%)", 0.0, 10.0, 0.0)
what_if_market_shock = st.slider("What-If: Market Shock (%)", 0.0, 10.0, 0.0)

# Adjust based on the current rates
total_interest_rate = current_interest_rate + what_if_interest_rate_hike
total_default_rate = current_default_rate + what_if_credit_loss_rate
total_market_shock = current_market_shock + what_if_market_shock

what_if_interest_rate_loss = risk_weighted_assets * (total_interest_rate / 100)
what_if_credit_losses = risk_weighted_assets * (total_default_rate / 100)
what_if_market_shock_loss = initial_tier1 * (total_market_shock / 100)
what_if_total_losses = what_if_interest_rate_loss + what_if_credit_losses + what_if_market_shock_loss

what_if_cet1 = initial_cet1 - what_if_total_losses
what_if_cet1_ratio = (what_if_cet1 / risk_weighted_assets) * 100

st.metric("What-If CET1 Ratio (%)", f"{what_if_cet1_ratio:.2f}")
st.metric("Total Interest Rate (%)", f"{total_interest_rate:.2f}")
st.metric("Total Default Rate (%)", f"{total_default_rate:.2f}")
st.metric("Total Market Shock (%)", f"{total_market_shock:.2f}")

# Scenario Comparison
st.header("Scenario Comparison")

# Select Scenarios for Comparison
scenario_1 = st.sidebar.selectbox(
    "Select Scenario 1",
    [
        "Baseline (No Stress)",
        "Mild Recession",
        "Severe Recession",
        "Interest Rate Shock",
        "Market Crash",
        "Credit Crisis",
        "Inflation Shock",
        "Liquidity Stress",
        "Currency Devaluation",
        "Custom Scenario",
    ],
    key="scenario_1",
)

scenario_2 = st.sidebar.selectbox(
    "Select Scenario 2",
    [
        "Baseline (No Stress)",
        "Mild Recession",
        "Severe Recession",
        "Interest Rate Shock",
        "Market Crash",
        "Credit Crisis",
        "Inflation Shock",
        "Liquidity Stress",
        "Currency Devaluation",
        "Custom Scenario",
    ],
    key="scenario_2",
)

# Define a function to get scenario parameters
def get_scenario_parameters(scenario):
    if scenario == "Baseline (No Stress)":
        return 0.0, 0.0, 0.0
    elif scenario == "Mild Recession":
        return 1.0, 2.0, 3.0
    elif scenario == "Severe Recession":
        return 2.5, 5.0, 8.0
    elif scenario == "Interest Rate Shock":
        return 3.0, 0.0, 0.0
    elif scenario == "Market Crash":
        return 0.0, 0.0, 10.0
    elif scenario == "Credit Crisis":
        return 0.5, 8.0, 3.0
    elif scenario == "Inflation Shock":
        return 4.0, 1.0, 2.0
    elif scenario == "Liquidity Stress":
        return 0.0, 3.0, 5.0
    elif scenario == "Currency Devaluation":
        return 1.5, 2.5, 6.0
    elif scenario == "Custom Scenario":
        interest_rate_hike = st.sidebar.slider("Interest Rate Hike (%) for Custom Scenario", 0.0, 5.0, 1.0, key="custom_hike")
        credit_loss_rate = st.sidebar.slider("Default Rates (%) for Custom Scenario", 0.0, 10.0, 2.0, key="custom_loss")
        market_shock = st.sidebar.slider("Market Shock (%) for Custom Scenario", 0.0, 10.0, 5.0, key="custom_shock")
        return interest_rate_hike, credit_loss_rate, market_shock

# Get parameters for Scenario 1 and Scenario 2
interest_rate_hike_1, credit_loss_rate_1, market_shock_1 = get_scenario_parameters(scenario_1)
interest_rate_hike_2, credit_loss_rate_2, market_shock_2 = get_scenario_parameters(scenario_2)

# Compute Updated CET1 Ratios for Both Scenarios
total_losses_1 = (
    risk_weighted_assets * (interest_rate_hike_1 / 100)
    + risk_weighted_assets * (credit_loss_rate_1 / 100)
    + initial_tier1 * (market_shock_1 / 100)
)
updated_cet1_ratio_scenario_1 = ((initial_cet1 - total_losses_1) / risk_weighted_assets) * 100

total_losses_2 = (
    risk_weighted_assets * (interest_rate_hike_2 / 100)
    + risk_weighted_assets * (credit_loss_rate_2 / 100)
    + initial_tier1 * (market_shock_2 / 100)
)
updated_cet1_ratio_scenario_2 = ((initial_cet1 - total_losses_2) / risk_weighted_assets) * 100

# Display Comparison
st.metric(
    "CET1 Ratio Difference (%)",
    f"{updated_cet1_ratio_scenario_2 - updated_cet1_ratio_scenario_1:.2f}",
)
st.write(f"Scenario 1 Updated CET1 Ratio: **{updated_cet1_ratio_scenario_1:.2f}%**")
st.write(f"Scenario 2 Updated CET1 Ratio: **{updated_cet1_ratio_scenario_2:.2f}%**")


# Disclaimer Section
st.header("Disclaimer: Predefined Parameters")
st.markdown("""
### Stress Scenario Definitions:
- **Baseline (No Stress)**: No changes to interest rate, default rate, or market shock.
- **Mild Recession**: Interest Rate +1%, Default Rate +2%, Market Shock +3%.
- **Severe Recession**: Interest Rate +2.5%, Default Rate +5%, Market Shock +8%.
- **Interest Rate Shock**: Interest Rate +3%, Default Rate 0%, Market Shock 0%.
- **Market Crash**: Interest Rate 0%, Default Rate 0%, Market Shock +10%.
- **Credit Crisis**: Interest Rate +0.5%, Default Rate +8%, Market Shock +3%.
- **Inflation Shock**: Interest Rate +4%, Default Rate +1%, Market Shock +2%.
- **Liquidity Stress**: Interest Rate 0%, Default Rate +3%, Market Shock +5%.
- **Currency Devaluation**: Interest Rate +1.5%, Default Rate +2.5%, Market Shock +6%.
- **Custom Scenario**: User-defined stress parameters.
""")

# Footer with Right Alignment and Enhanced Effects
st.markdown(
    """
    <style>
    .footer {
        position: fixed; 
        bottom: 10px; 
        right: 20px; 
        text-align: right; 
        font-size: 0.9em; 
        color: #6c757d;
        z-index: 1000;
    }
    .footer a {
        text-decoration: none; 
        color: inherit; 
        font-weight: bold;
        transition: color 0.3s ease;
    }
    .footer a:hover { 
        color: #007bff; 
        text-decoration: underline;
    }
    .footer-icons a {
        text-decoration: none; 
        color: #6c757d; 
        margin-left: 10px;
        font-size: 1.2em;
        transition: color 0.3s ease, transform 0.3s ease;
    }
    .footer-icons a:hover {
        color: #007bff; 
        transform: scale(1.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="footer">
        <div>
            Created by <a href="#">Chinmay Yadav</a>
        </div>
        <div class="footer-icons">
            <a href="mailto:chinmay.yadav@uconn.edu" title="Email">
                <i class="fas fa-envelope"></i>
            </a>
            <a href="https://www.linkedin.com/in/chinmayyadav0107/" title="LinkedIn" target="_blank">
                <i class="fab fa-linkedin"></i>
            </a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Add Font Awesome for Icons
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">',
    unsafe_allow_html=True
)

