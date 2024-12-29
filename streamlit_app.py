import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Title and Introduction
st.title("🎈 Dashboard")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# Function to assign Date Buckets
def dateAge(x):
    a = (x - np.datetime64("today", "D")) / np.timedelta64(1, "D")
    if a <= 0:
        return "0 or Less"
    elif a <= 5:
        return "5 days"
    elif a <= 14:
        return "6 to 14 days"
    elif a <= 30:
        return "15 to 30 days"
    else:
        return "over 30 days"

# Function to get data with file uploader
@st.cache_data
def getData():
    uploaded_file = st.file_uploader("Upload a CSV file")
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    else:
        st.stop()

# Load the data
df = getData()

# Set Org Level and Role Title
org_level = ["6", "7", "8"]
role_title = "Data"

# Convert dates
df["Resource Start Date"] = pd.to_datetime(df["Resource Start Date"], format="%d-%b-%y")
df["Resource End Date"] = pd.to_datetime(df["Resource End Date"], format="%d-%b-%y")

# Define Date Bucket column
df["Date Bucket"] = df["Resource Start Date"].apply(dateAge)

# Standardize Location Names
df["Role Work Location"] = df["Role Work Location"].str.title()

# Rename columns for clarity
df.rename(
    columns={
        "Project Has Security/ Nationality Restriction": "Clearance Required",
        "Resource Start Date": "Start Date",
        "Resource End Date": "End Date",
        "Role ID": "ID",
        "Role Title": "Title",
        "Role Description": "Description",
        "Role Talent Segment": "Talent Segment",
        "Role Career Level From": "Career Level From",
        "Role Career Level To": "Career Level To",
        "Role Work Location": "Work Location",
        "Role Location Type": "Location Type",
        "Role Fulfillment Entity L3": "Fulfillment Entity L3",
    },
    inplace=True,
)

# Filter relevant columns
df_sub = df[
    [
        "ID",
        "Clearance Required",
        "Start Date",
        "End Date",
        "Date Bucket",
        "Title",
        "Description",
        "Talent Segment",
        "Assigned Role",
        "Career Level To",
        "Work Location",
        "Location Type",
        "Role Primary Contact",
        "Role Primary Contact\n(Email ID)",
    ]
]

# Apply filters based on Org Level and Role Title
df_filter = df_sub[
    df_sub["Assigned Role"].str.contains(role_title, case=False, na=False)
    & df_sub["Career Level To"].isin(org_level)
]

# Sidebar Filters
st.sidebar.header("Filters:")
location = st.sidebar.multiselect(
    "Select Location:", options=df_filter["Work Location"].unique(), default=df_filter["Work Location"].unique()
)
work_type = st.sidebar.multiselect(
    "Select Work Type:", options=df_filter["Location Type"].unique(), default=df_filter["Location Type"].unique()
)

# Apply sidebar filters
df_selection = df_filter.query("`Work Location` == @location & `Location Type` == @work_type")

# Metrics Calculations
total_roles = df_selection["ID"].nunique()
bucket_0 = df_selection[df_selection["Date Bucket"] == "0 or Less"].shape[0]
bucket_5 = df_selection[df_selection["Date Bucket"] == "5 days"].shape[0]
bucket_14 = df_selection[df_selection["Date Bucket"] == "6 to 14 days"].shape[0]
bucket_30 = df_selection[df_selection["Date Bucket"] == "15 to 30 days"].shape[0]
bucket_31 = df_selection[df_selection["Date Bucket"] == "over 30 days"].shape[0]

# Display Metrics
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric(label="No. Roles", value=total_roles)
col2.metric(label="Already Started", value=bucket_0)
col3.metric(label="In 5 Days", value=bucket_5)
col4.metric(label="In 14 Days", value=bucket_14)
col5.metric(label="In 30 Days", value=bucket_30)
col6.metric(label="Over 30 Days", value=bucket_31)

st.divider()

# Prepare data for Plotly chart
df_1 = df_selection.groupby(["Work Location", "Location Type"]).size().reset_index(name="count")

# Plotly Bar Chart
fig_count_location_type = px.bar(
    df_1,
    x="Work Location",
    y="count",
    color="Location Type",
    title="Role by Location and Type - Plotly",
)
st.plotly_chart(fig_count_location_type, use_container_width=True)

st.divider()

# Display DataFrame with configurations
st.dataframe(
    df_selection,
    hide_index=True,
    column_config={
        "ID": st.column_config.NumberColumn(format="%d"),
        "Start Date": st.column_config.DateColumn(format="DD-MMM-YYYY"),
        "End Date": st.column_config.DateColumn(format="DD-MMM-YYYY"),
        "Title": st.column_config.TextColumn(width="medium"),
        "Description": st.column_config.TextColumn(width="medium"),
    },
)
