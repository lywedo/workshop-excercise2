import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
import pandas as pd


@st.cache
def load_data():
    """
    Load the California housing dataset and convert to DataFrame.

    """
    data = fetch_california_housing()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df["MedianHouseValue"] = data.target
    return df


def filter_data_by_median_income(df, low_income, high_income):
    """
    Filter the dataset based on a range of median incomes.
    """
    return df[(df["MedInc"] >= low_income) & (df["MedInc"] <= high_income)]


def main():
    """
    Setting up streamlit page configurations.
    """
    st.set_page_config(page_title="California Housing Analysis", layout="wide")
    st.title("California Housing Data Analysis")
    # Load data
    df = load_data()

    # Sidebar controls
    st.sidebar.header("Filters")
    min_income = float(np.min(df["MedInc"]))
    max_income = float(np.max(df["MedInc"]))
    low_income = st.sidebar.slider(
        "Minimum Median Income", min_income, max_income, min_income, 0.1
    )
    high_income = st.sidebar.slider(
        "Maximum Median Income", min_income, max_income, max_income, 0.1
    )
    filtered_df = filter_data_by_median_income(df, low_income, high_income)

    # Button to toggle between map and histograms
    map_button = st.sidebar.button("Show Map")
    if map_button:
        # Display houses on a map of California
        st.map(filtered_df.rename(columns={"Latitude": "lat",
                                           "Longitude": "lon"}))
    else:
        # Display histograms for house values and median incomes
        fig, ax = plt.subplots(1, 2, figsize=(15, 5))

        # Median House Value Histogram
        ax[0].hist(filtered_df["MedianHouseValue"], bins=20, alpha=0.6, color="b")
        ax[0].set_title("Distribution of Median House Values")
        ax[0].set_xlabel("Median House Value (in $1000s)")
        ax[0].set_ylabel("Number of Houses")
        # Median Income Histogram
        ax[1].hist(filtered_df["MedInc"], bins=20, alpha=0.6, color="r")
        ax[1].set_title("Distribution of Median Income")
        ax[1].set_xlabel("Median Income")
        ax[1].set_ylabel("Number of Houses")

        st.pyplot(fig)


if __name__ == "__main__":
    main()
