# -------------------------------------------------------------------------------------------------------------------- #
"""
App to get insights about ab test on binary outcome leveraging bayesian statistics
"""
# -------------------------------------------------------------------------------------------------------------------- #
# Imports

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# -------------------------------------------------------------------------------------------------------------------- #
# Constants

OUTPUT_SAMPLE_SIZE = 50_000
CENTILES_TO_COMPUTE = np.arange(0, 100 + 1)

# Corresponds to uniform prior
PRIOR_A = 1
PRIOR_B = 1

DEFAULT_INPUT = {
    "nb_a": 100,
    "nb_b": 100,
    "converted_a": 50,
    "converted_b": 45,
}

SEED = 42


# -------------------------------------------------------------------------------------------------------------------- #
# Config

st.set_page_config(page_title="AB Test", layout="wide")
np.random.seed(SEED)
sns.set()


# -------------------------------------------------------------------------------------------------------------------- #
# App

nb_a = st.sidebar.number_input(
    "Number of samples in group A",
    min_value=0,
    value=DEFAULT_INPUT["nb_a"],
    step=1,
)
nb_b = st.sidebar.number_input(
    "Number of samples in group B",
    min_value=0,
    value=DEFAULT_INPUT["nb_b"],
    step=1,
)

converted_a = st.sidebar.number_input(
    "Number of samples converted in group A",
    min_value=0,
    max_value=nb_a,
    value=DEFAULT_INPUT["converted_a"],
)
converted_b = st.sidebar.number_input(
    "Number of samples converted in group B",
    min_value=0,
    max_value=nb_a,
    value=DEFAULT_INPUT["converted_b"],
)

# Simulate draws
samples_conversion_rate_a = np.random.beta(
    a=PRIOR_A + converted_a,
    b=PRIOR_B + nb_a - converted_a,
    size=OUTPUT_SAMPLE_SIZE,
)

samples_conversion_rate_b = np.random.beta(
    a=PRIOR_B + converted_b,
    b=PRIOR_B + nb_b - converted_b,
    size=OUTPUT_SAMPLE_SIZE,
)

diff = samples_conversion_rate_a - samples_conversion_rate_b

# Convert in percentage
samples_conversion_rate_a *= 100
samples_conversion_rate_b *= 100
diff *= 100


# Plot results
fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(12, 8))

sns.histplot(samples_conversion_rate_a, stat="percent", alpha=0.5, kde=True, ax=axs[0])
sns.histplot(samples_conversion_rate_b, stat="percent", alpha=0.5, kde=True, ax=axs[0])

axs[0].set_xlabel("Conversion rate (%)")
axs[0].set_ylabel("Probability density (%)")
axs[0].set_title("Distribution of conversion rate between A and B groups")
axs[0].legend(["A", "B"])

sns.histplot(diff, stat="percent", alpha=0.5, kde=True, ax=axs[1])

axs[1].set_xlabel("Absolute difference in conversion rate (%)")
axs[1].set_ylabel("Probability density (%)")
axs[1].set_title("Distribution of the difference in conversion rate between A and B groups")

plt.tight_layout()


df_repartitions = pd.DataFrame(
    {
        "centile": CENTILES_TO_COMPUTE,
        "conversion_rate_a": np.percentile(samples_conversion_rate_a, CENTILES_TO_COMPUTE),
        "conversion_rate_b": np.percentile(samples_conversion_rate_b, CENTILES_TO_COMPUTE),
        "diff_conversion_rate_a_minus_b": np.percentile(diff, CENTILES_TO_COMPUTE),
    }
)

# Layouts
st.header("AB Test result")

summary = f"""
## Results summary

#### Observed:
- Conversion rate (group A): {converted_a / nb_a:.1%}
- Conversion rate (group B): {converted_b / nb_b:.1%}
- Difference in conversion rate: {converted_a / nb_a - converted_b / nb_b:.1%} 

#### Estimation of variability
- Probability of group A's conversion rate being higher than group B's conversion rate: {(diff > 0).mean():.1f}%
- There is 90% chances that group A's conversion rate minus groupb B's conversion high is higher than {np.percentile(diff, 10):.1f}%
- There is 95% chances that group A's conversion rate minus groupb B's conversion high is higher than {np.percentile(diff, 5):.1f}%
- There is 99% chances that group A's conversion rate minus groupb B's conversion high is higher than {np.percentile(diff, 1):.1f}%
"""

st.markdown(summary)
st.subheader("Conversion rates by centile")
st.dataframe(df_repartitions.round(1))
st.subheader("Parameters' distribution")
st.pyplot(fig)
