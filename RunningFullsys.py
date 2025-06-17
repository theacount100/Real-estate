# Real Estate Data Dashboard using Streamlit
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Load Data
@st.cache_data
def load_data():
    file_path = "cleaned_corrected_real_estate.parquet"
    files = os.listdir(".")
    st.write("Files in current directory:", files)  # Debugging help
    #file_path = r"D:\Projects\realeastae\omanreal_outputs\filtered_real_estate_data.parquet"
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

governorate_options = ["All"] + sorted(df["Governorate"].dropna().unique().tolist())
selected_governorate = st.sidebar.selectbox("Governorate", options=governorate_options)

if selected_governorate != "All":
    wilayat_options = df[df["Governorate"] == selected_governorate]["Wilayat"].dropna().unique()
else:
    wilayat_options = df["Wilayat"].dropna().unique()
wilayat_options = ["All"] + sorted(wilayat_options.tolist())
selected_wilayat = st.sidebar.selectbox("Wilayat", options=wilayat_options)

if selected_wilayat != "All":
    area_options = df[df["Wilayat"] == selected_wilayat]["Area"].dropna().unique()
else:
    area_options = df["Area"].dropna().unique()
area_options = ["All"] + sorted(area_options.tolist())
selected_area = st.sidebar.selectbox("Area", options=area_options)

cat1_options = ["All"] + sorted(df["Category Level 1"].dropna().unique().tolist())
selected_cat1 = st.sidebar.selectbox("Sale / Rent", options=cat1_options)

if selected_cat1 != "All":
    cat2_options = df[df["Category Level 1"] == selected_cat1]["Category Level 2"].dropna().unique()
else:
    cat2_options = df["Category Level 2"].dropna().unique()
cat2_options = ["All"] + sorted(cat2_options.tolist())
selected_cat2 = st.sidebar.selectbox("Land Type", options=cat2_options)

if selected_cat2 != "All":
    cat3_options = df[df["Category Level 2"] == selected_cat2]["Category Level 3"].dropna().unique()
else:
    cat3_options = df["Category Level 3"].dropna().unique()
cat3_options = ["All"] + sorted(cat3_options.tolist())
selected_cat3 = st.sidebar.selectbox("Subcategory", options=cat3_options)

selected_month = st.sidebar.slider("Month", min_value=1, max_value=12, value=(1, 12))

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
df_filtered = df_filtered[df_filtered["Month"].between(*selected_month)]


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

# Get current page data
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



# Price Trends
st.subheader("📈 Price Trend Over Time")

def plot_trend(df, location_name):
    # Group by month and calculate mean price
    trend_df = df.groupby("Month")["Price_per_m2"].mean().reset_index()
    
    # Only plot if we have data
    if not trend_df.empty:
        # Find first and last month with data
        min_month = trend_df["Month"].min()
        max_month = trend_df["Month"].max()
        
        # Create plot with dynamic range
        fig = px.line(
            trend_df,
            x="Month",
            y="Price_per_m2",
            title=f"Price Trend in {location_name}",
            range_x=[min_month-0.5, max_month+0.5]  # Add small padding
        )
        
        # Format x-axis to show only whole months
        fig.update_xaxes(
            tickmode='linear',
            dtick=1,
            range=[min_month-0.5, max_month+0.5]
        )
        
        # Format y-axis to start from sensible value
        min_price = trend_df["Price_per_m2"].min()
        fig.update_yaxes(range=[min_price*0.9, trend_df["Price_per_m2"].max()*1.1])
        
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


st.caption("Created by Abdullah | Powered by Streamlit")
