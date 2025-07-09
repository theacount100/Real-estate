# Real Estate Data Dashboard using Streamlit
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from pathlib import Path # for computer use only not githup

st.set_page_config(layout="wide")

# Load Data
@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).resolve().parent.parent # for computer use only not githup
    CLEANED_DIR = BASE_DIR / "data" / "cleaned" # for computer use only not githup
    file_path = CLEANED_DIR / "cleaned_corrected_real_estate.parquet" # for computer use only not githup

    # file_path = "cleaned_corrected_real_estate.parquet" # for githupuse

    df = pd.read_parquet(file_path)
    df["PostDate"] = pd.to_datetime(df["PostDate"])
    df["Month"] = df["PostDate"].dt.month
    df["MonthStr"] = df["PostDate"].dt.to_period("M").astype(str)  # For time trend plots
    df["ListingAge"] = (pd.to_datetime("today") - df["PostDate"]).dt.days
    df["View_per_1k_OMR"] = df["Views"] / (df["Price"] / 1000)
    df["InvestmentScore"] = df["View_per_1k_OMR"] * (df["Price_per_m2"].median() / df["Price_per_m2"])
    return df

df = load_data()


st.title("📊 Oman Real Estate Market Dashboard")

# Sidebar Filters
st.sidebar.header("Filter Listings")

# Dynamic Wilayat options based on Governorate
df_temp = df.copy()

# Time Filter Options
time_filter_options = {
    "All": None,
    "Past 1 Month": 1,
    "Past 2 Months": 2,
    "Past 3 Months": 3,
    "Past 6 Months": 6,
}

selected_time_range = st.sidebar.selectbox("Time Range", list(time_filter_options.keys()))
months_back = time_filter_options[selected_time_range]

governorate_options = ["All"] + sorted(df["Governorate"].dropna().unique().tolist())
selected_governorate = st.sidebar.selectbox("Governorate", options=governorate_options)

if selected_governorate != "All":
    df_temp = df_temp[df_temp["Governorate"] == selected_governorate]
wilayat_options = ["All"] + sorted(df_temp["Wilayat"].dropna().unique().tolist())
selected_wilayat = st.sidebar.selectbox("Wilayat", options=wilayat_options)

# Dynamic Area options based on Wilayat
if selected_wilayat != "All":
    df_temp = df_temp[df_temp["Wilayat"] == selected_wilayat]
area_options = ["All"] + sorted(df_temp["Area"].dropna().unique().tolist())
selected_area = st.sidebar.selectbox("Area", options=area_options)

cat1_options = ["All"] + sorted(df["Category Level 1"].dropna().unique().tolist())
selected_cat1 = st.sidebar.selectbox("Sale / Rent", options=cat1_options)

df_temp = df.copy()
if selected_governorate != "All":
    df_temp = df_temp[df_temp["Governorate"] == selected_governorate]
if selected_wilayat != "All":
    df_temp = df_temp[df_temp["Wilayat"] == selected_wilayat]
if selected_area != "All":
    df_temp = df_temp[df_temp["Area"] == selected_area]
if selected_cat1 != "All":
    df_temp = df_temp[df_temp["Category Level 1"] == selected_cat1]

# Filter out Category Level 2 values with fewer than 20 listings
cat2_counts = df_temp["Category Level 2"].value_counts()
valid_cat2 = cat2_counts[cat2_counts >= 20].index.tolist()

cat2_options = ["All"] + sorted(valid_cat2)
selected_cat2 = st.sidebar.selectbox("Land Type", options=cat2_options)

if selected_cat2 != "All":
    df_temp = df_temp[df_temp["Category Level 2"] == selected_cat2]

cat3_options = ["All"] + sorted(df_temp["Category Level 3"].dropna().unique().tolist())
selected_cat3 = st.sidebar.selectbox("Subcategory", options=cat3_options)

df_filtered = df[df['RepostLabel'].isin(['new', 'unique'])].copy()
if selected_governorate != "All":
    df_filtered = df_filtered[df_filtered["Governorate"] == selected_governorate]
if selected_wilayat != "All":
    df_filtered = df_filtered[df_filtered["Wilayat"] == selected_wilayat]
if selected_area != "All":
    df_filtered = df_filtered[df_filtered["Area"] == selected_area]
if selected_cat1 != "All":
    df_filtered = df_filtered[df_filtered["Category Level 1"] == selected_cat1]
if selected_cat2 != "All":
    df_filtered = df_filtered[df_filtered["Category Level 2"] == selected_cat2]
if selected_cat3 != "All":
    df_filtered = df_filtered[df_filtered["Category Level 3"] == selected_cat3]

# Remove low-frequency Land Types
valid_cat2_filtered = df_filtered["Category Level 2"].value_counts()
valid_cat2_filtered = valid_cat2_filtered[valid_cat2_filtered >= 20].index.tolist()
df_filtered = df_filtered[df_filtered["Category Level 2"].isin(valid_cat2_filtered)]

min_area = int(df_filtered["Area_m2"].min()) if not df_filtered.empty else 0
max_area = int(df_filtered["Area_m2"].max()) if not df_filtered.empty else 1

# Only if df_filtered is not empty
if not df_filtered.empty:
    area_min = int(df_filtered["Area_m2"].min())
    area_max = int(df_filtered["Area_m2"].max())

    st.sidebar.markdown("**Filter by Area Size (m²)**")
    user_min_area = st.sidebar.number_input("Min Area", min_value=area_min, max_value=area_max, value=area_min, step=10)
    user_max_area = st.sidebar.number_input("Max Area", min_value=area_min, max_value=area_max, value=area_max, step=10)

    # Apply filtering only if inputs are valid
    if user_min_area <= user_max_area:
        df_filtered = df_filtered[df_filtered["Area_m2"].between(user_min_area, user_max_area)]
    else:
        st.sidebar.warning("⚠️ Min area must be less than or equal to max area.")


if months_back is not None:
    cutoff_date = pd.to_datetime("today") - pd.DateOffset(months=months_back)
    df_filtered = df_filtered[df_filtered["PostDate"] >= cutoff_date]


# Map
# === Map Section ===
st.subheader("🗺️ Map of Listings")
st.markdown("**Click a point on the map to see listing details below.**")

if not df_filtered.empty:
    df_filtered["ListingLink"] = df_filtered["Listing URL"].apply(lambda x: f"<a href='{x}' target='_blank'>View Listing</a>")

    fig_map = px.scatter_mapbox(
        df_filtered.dropna(subset=["Latitude", "Longitude"]),
        lat="Latitude",
        lon="Longitude",
        color="Price_per_m2",
        size="Price",
        hover_name="Governorate",
        hover_data={
            "Wilayat": True,
            "Area": True,
            "Price": True,
            "Price_per_m2": True,
        },
        zoom=5,
        height=500,
        mapbox_style="open-street-map"
    )

    fig_map.update_traces(marker=dict(opacity=0.7))
    fig_map.update_layout(hovermode='closest')

    # Call plotly_chart ONLY ONCE
    click_event = st.plotly_chart(fig_map, use_container_width=True, key="main_map")

else:
    st.warning("No listings to show on the map.")


# === KPIs ===
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Listings", len(df_filtered), help="Total number of listings matching the selected filters.")
col2.metric("Avg Price (OMR)", f"{df_filtered['Price'].mean():,.0f}", help="Average price of the listings.")
col3.metric("Avg Price per m²", f"{df_filtered['Price_per_m2'].mean():.2f} OMR", help="Average price per square meter of land.")
col4.metric("Median Price per m²", f"{df_filtered['Price_per_m2'].median():.2f} OMR", help="Middle price per square meter. Less affected by extreme values.")


# === Listings Table ===
st.subheader("📋 Listings")

# Add pagination controls
if 'page' not in st.session_state:
    st.session_state.page = 0

# Sort options
sort_option = st.selectbox(
    "Sort listings by:",
    options=["Newest First", "Oldest First", "Highest Price", "Lowest Price", 
             "Highest Price/m²", "Lowest Price/m²"],
    index=0
)

# Apply sorting
if sort_option == "Newest First":
    df_sorted = df_filtered.sort_values("PostDate", ascending=False)
elif sort_option == "Oldest First":
    df_sorted = df_filtered.sort_values("PostDate", ascending=True)
elif sort_option == "Highest Price":
    df_sorted = df_filtered.sort_values("Price", ascending=False)
elif sort_option == "Lowest Price":
    df_sorted = df_filtered.sort_values("Price", ascending=True)
elif sort_option == "Highest Price/m²":
    df_sorted = df_filtered.sort_values("Price_per_m2", ascending=False)
elif sort_option == "Lowest Price/m²":
    df_sorted = df_filtered.sort_values("Price_per_m2", ascending=True)

# ✅ Generate Details column BEFORE slicing for pagination
df_sorted["Details"] = df_sorted["Listing URL"].apply(
    lambda url: f'<a href="{url}" target="_blank">🔗 View</a>'
)
# Columns to display
display_cols = ["PostDate", "Governorate", "Wilayat", "Area", "Area_m2", "Price", 
                "Price_per_m2","Category Level 1", "Category Level 2", "Category Level 3", "Details"]

# Pagination
items_per_page = 10
total_pages = len(df_sorted) // items_per_page + (1 if len(df_sorted) % items_per_page > 0 else 0)

col1, col2, _ = st.columns([1, 1, 3])
with col1:
    if st.button("Previous") and st.session_state.page > 0:
        st.session_state.page -= 1
with col2:
    if st.button("Next") and st.session_state.page < total_pages - 1:
        st.session_state.page += 1

st.write(f"Page {st.session_state.page + 1} of {total_pages}")

# Get current page data
start_idx = st.session_state.page * items_per_page
end_idx = start_idx + items_per_page
current_page_data = df_sorted.iloc[start_idx:end_idx]


# Add repost flag column to df_sorted if missing
if "DuplicateGroup" in df.columns:
    dup_counts = df["DuplicateGroup"].value_counts()
    df_sorted["HasReposts"] = df_sorted["DuplicateGroup"].map(dup_counts).fillna(0).astype(int) > 1
else:
    df_sorted["HasReposts"] = False

# === Enhanced listing display with expandable repost history ===
for idx, row in df_sorted.iloc[start_idx:end_idx].iterrows():
    st.markdown("---")  # Separator line

    st.markdown(f"### 📍 {row['Governorate']} - {row['Wilayat']} - {row['Area']}| **{int(row['Price']):,} OMR**")
    st.markdown(f"[🔗 View Listing]({row['Listing URL']})", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.write(f"**Posted:** {row['PostDate']}")
    col2.write(f"**Price/m²:** {row['Price_per_m2']:.2f}")
    col3.write(f"**Area Size:** {row['Area_m2']:.0f} m²")

    col4, col5, col6= st.columns(3)
    col4.write(f"**Category 1:** {row['Category Level 1']}")
    col5.write(f"**Category 2:** {row['Category Level 2']}")
    col6.write(f"**Category 3:** {row['Category Level 3']}")

    col7, col8 = st.columns(2)
    Publisher = row['Publisher'] if pd.notna(row['Publisher']) else "N/A"
    col7.write(f"**Publisher:** {Publisher}")    
    contact = row['Primary Phone'] if pd.notna(row['Primary Phone']) else "N/A"
    col8.write(f"**📞 Contact:** {contact}")

    if row["HasReposts"]:
        reposts = df[df["DuplicateGroup"] == row["DuplicateGroup"]].sort_values("PostDate", ascending=False)
        with st.expander("🔁 Show Repost History"):
            reposts_display = reposts[["PostDate", "Publisher", "Price", "Area", "Price_per_m2", "Listing URL"]].copy()
            reposts_display["Listing URL"] = reposts_display["Listing URL"].apply(
                lambda x: f'<a href="{x}" target="_blank">🔗 Link</a>' if pd.notna(x) else ""
            )
            st.write(
                reposts_display.to_html(escape=False, index=False),
                unsafe_allow_html=True
            )
# Bottom Pagination Controls
col1, col2, _ = st.columns([1, 1, 3])
with col1:
    if st.button("Previous", key="prev_bottom") and st.session_state.page > 0:
         st.session_state.page -= 1
with col2:
    if st.button("Next", key="next_bottom") and st.session_state.page < total_pages - 1:
        st.session_state.page += 1

    st.write(f"Page {st.session_state.page + 1} of {total_pages}")


# Price Trends
st.subheader("📈 Price Trend Over Time")

def plot_trend(df, location_name):
    # Extract year and month
    df["YearMonth"] = df["PostDate"].dt.to_period("M").astype(str)

    # Group by Year-Month string and calculate mean price
    trend_df = df.groupby("YearMonth")["Price_per_m2"].mean().reset_index()
    trend_df["YearMonth"] = pd.to_datetime(trend_df["YearMonth"])

    if not trend_df.empty:
        fig = px.line(
            trend_df,
            x="YearMonth",
            y="Price_per_m2",
            title=f"Price Trend in {location_name}"
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price per m²",
            xaxis=dict(tickformat="%b %Y"),  # Month Year format
        )

        min_price = trend_df["Price_per_m2"].min()
        max_price = trend_df["Price_per_m2"].max()
        fig.update_yaxes(range=[min_price * 0.9, max_price * 1.1])

        st.plotly_chart(fig, use_container_width=True)


# Plot trends for selected locations
if selected_governorate != "All":
    df_gov = df[df["Governorate"] == selected_governorate].copy()
    plot_trend(df_gov, selected_governorate)

if selected_wilayat != "All":
    df_wil = df[df["Wilayat"] == selected_wilayat].copy()
    plot_trend(df_wil, selected_wilayat)

if selected_area != "All":
    df_ar = df[df["Area"] == selected_area].copy()
    plot_trend(df_ar, selected_area)



# Seller Saturation
st.subheader("🏢 Seller Saturation (Active Ads per Publisher)")
st.markdown("**Concentration of listings per publisher. High means market dominated by few sellers.**")
seller_counts = df_filtered["Publisher"].value_counts().reset_index()
seller_counts.columns = ["Publisher", "Active Listings"]
fig = px.bar(seller_counts.head(10), x="Publisher", y="Active Listings", title="Top 10 Sellers")
st.plotly_chart(fig, use_container_width=True)

