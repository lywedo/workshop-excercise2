# Enhanced Streamlit Spotify Data Analysis with Additional Features
import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    """
     Load spotify dataset
    """
    return pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')


# Start of the Streamlit App
def main():
    """
        Function for exploratory data analysis
    """
    # Load the Spotify dataset
    data = load_data()

    # App title and introduction
    st.title("Spotify Data Analysis (2023)")
    st.write("Explore various insights from the Spotify 2023 dataset. Dive deeper using the interactive components.")

    # Sidebar for data filtering
    st.sidebar.header("Filter Data")

    # Year Filter
    selected_year = st.sidebar.slider("Select a Release Year", int(data["released_year"].min()), int(data["released_year"].max()), (int(data["released_year"].min()), int(data["released_year"].max())))
    data = data[(data["released_year"] >= selected_year[0]) & (data["released_year"] <= selected_year[1])]

    # Artist Filter
    unique_artists = sorted(data['artist(s)_name'].unique().tolist())
    selected_artist = st.sidebar.multiselect("Select Artist(s)", unique_artists)
    if selected_artist:
        data = data[data['artist(s)_name'].isin(selected_artist)]

    # Data Overview Button
    if st.button("Show Data Overview"):
        st.subheader("Data Overview")
        st.write(data.head())

    # Track Streams Distribution
    st.subheader("Distribution of Track Streams")
    fig_streams = px.histogram(data, x="streams", title="Streams Distribution", color_discrete_sequence=["#316394"])
    st.plotly_chart(fig_streams)

    # Number of Tracks per Artist
    st.subheader("Top Artists by Track Count")
    top_artists = data['artist(s)_name'].value_counts().head(10)
    fig_artists = px.bar(top_artists, x=top_artists.index, y=top_artists.values, title="Top 10 Artists by Track Count", color_discrete_sequence=["#EF553B"])
    st.plotly_chart(fig_artists)

    # Track Attribute Distribution
    st.subheader("Track Attribute Distribution")
    attribute = st.selectbox("Select an attribute", ["danceability_%", "energy_%", "valence_%", "acousticness_%", "liveness_%", "speechiness_%"])
    fig_attribute = px.histogram(data, x=attribute, title=f"Distribution of {attribute}", color_discrete_sequence=["#00CC96"])
    st.plotly_chart(fig_attribute)

    # BPM Distribution
    st.subheader("BPM (Beats Per Minute) Distribution")
    bpm_range = st.slider("Select a BPM range", int(data["bpm"].min()), int(data["bpm"].max()), (80, 140))
    filtered_data = data[(data["bpm"] >= bpm_range[0]) & (data["bpm"] <= bpm_range[1])]
    fig_bpm = px.histogram(filtered_data, x="bpm", title=f"BPM Distribution ({bpm_range[0]} - {bpm_range[1]})", color_discrete_sequence=["#AB63FA"])
    st.plotly_chart(fig_bpm)

    # Popular Keys Distribution
    st.subheader("Popular Keys Distribution")
    key_counts = data["key"].value_counts()
    fig_keys = px.bar(key_counts, x=key_counts.index, y=key_counts.values, title="Distribution of Tracks by Key", color_discrete_sequence=["#FFA15A"])
    st.plotly_chart(fig_keys)

    # Mode Distribution
    st.subheader("Mode Distribution")
    mode_counts = data["mode"].value_counts()
    fig_mode = px.pie(values=mode_counts.values, names=mode_counts.index, title="Distribution of Tracks by Mode", color_discrete_sequence=["#636EFA", "#FFA15A"])
    st.plotly_chart(fig_mode)

    # Interactive Scatter Plot
    st.subheader("Scatter Plot of Attributes")
    attr_x = st.selectbox("Select attribute for X-axis", ["danceability_%", "energy_%", "valence_%"], index=0)
    attr_y = st.selectbox("Select attribute for Y-axis", ["danceability_%", "energy_%", "valence_%"], index=1)
    fig_scatter = px.scatter(data, x=attr_x, y=attr_y, color="key", title=f"{attr_x} vs. {attr_y} by Key")
    st.plotly_chart(fig_scatter)


if __name__ == "__main__":
    main()
