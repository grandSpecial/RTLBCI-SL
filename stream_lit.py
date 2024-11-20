import streamlit as st
import pandas as pd
import json
import requests

class StatCan:
    """Given a PID, Coordinate and number of periods
    request data from statcan and return a dataframe"""
    def __init__(self, pid, coord, periods=100):
        self.pid = pid
        self.coord = coord
        self.periods = periods

    def get_data(self):
        url = "https://www150.statcan.gc.ca/t1/wds/rest/getDataFromCubePidCoordAndLatestNPeriods"
        r = requests.post(url, json=[{"productId": self.pid, "coordinate": self.coord, "latestN": self.periods}])
        return json.loads(r.text)

    def make_table(self):
        data = self.get_data()
        hold = {"date": [], "value": []}
        points = data[0]['object']['vectorDataPoint']
        for p in points:
            hold['date'].append(p['refPer'])
            hold['value'].append(p['value'])
        df = pd.DataFrame(hold)
        return df


# Mapping of regions and their respective coordinates
regions = {
    "St. John's, Newfoundland": {"coord": "16.0.0.0.0.0.0.0.0.0"},
    "Halifax, Nova Scotia": {"coord": "8.0.0.0.0.0.0.0.0.0"},
    "Moncton, New Brunswick": {"coord": "29.0.0.0.0.0.0.0.0.0"},
    "Quebec, Quebec": {"coord": "9.0.0.0.0.0.0.0.0.0"},
    "Trois-Rivieres, Quebec": {"coord": "26.0.0.0.0.0.0.0.0.0"},
    "Sherbrooke, Quebec": {"coord": "21.0.0.0.0.0.0.0.0.0"},
    "Montreal, Quebec": {"coord": "1.0.0.0.0.0.0.0.0.0"},
    "Ottawa, Ontario": {"coord": "2.0.0.0.0.0.0.0.0.0"},
    "Hamilton, Ontario": {"coord": "10.0.0.0.0.0.0.0.0.0"},
    "Kitchener, Ontario": {"coord": "11.0.0.0.0.0.0.0.0.0"},
    "St. Catharines - Niagara Falls, Ontario": {"coord": "17.0.0.0.0.0.0.0.0.0"},
    "Barrie, Ontario": {"coord": "22.0.0.0.0.0.0.0.0.0"},
    "London, Ontario": {"coord": "12.0.0.0.0.0.0.0.0.0"},
    "Milton, Ontario": {"coord": "28.0.0.0.0.0.0.0.0.0"},
    "Toronto, Ontario": {"coord": "3.0.0.0.0.0.0.0.0.0"},
    "Kingston, Ontario": {"coord": "27.0.0.0.0.0.0.0.0.0"},
    "Kanata, Ontario": {"coord": "23.0.0.0.0.0.0.0.0.0"},
    "Guelph, Ontario": {"coord": "24.0.0.0.0.0.0.0.0.0"},
    "Oshawa, Ontario": {"coord": "13.0.0.0.0.0.0.0.0.0"},
    "Windsor, Ontario": {"coord": "14.0.0.0.0.0.0.0.0.0"},
    "Winnipeg, Manitoba": {"coord": "4.0.0.0.0.0.0.0.0.0"},
    "Saskatoon, Saskatchewan": {"coord": "18.0.0.0.0.0.0.0.0.0"},
    "Regina, Saskatchewan": {"coord": "19.0.0.0.0.0.0.0.0.0"},
    "Calgary, Alberta": {"coord": "5.0.0.0.0.0.0.0.0.0"},
    "Edmonton, Alberta": {"coord": "6.0.0.0.0.0.0.0.0.0"},
    "Abbotsford, British Columbia": {"coord": "25.0.0.0.0.0.0.0.0.0"},
    "Kelowna, British Columbia": {"coord": "20.0.0.0.0.0.0.0.0.0"},
    "White Rock, British Columbia": {"coord": "30.0.0.0.0.0.0.0.0.0"},
    "Vancouver, British Columbia": {"coord": "7.0.0.0.0.0.0.0.0.0"},
    "Victoria, British Columbia": {"coord": "15.0.0.0.0.0.0.0.0.0"}
}

# Set page configuration
st.set_page_config(
    page_title="RTLBCI Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar navigation
st.sidebar.title("Navigation")
city = st.sidebar.selectbox("Select a Region", list(regions.keys()))

# Fetch and display data for the selected region
st.title(f"📊 Real-time Local Business Condition Index (RTLBCI)")
st.subheader(city)

st.write(f"""
The **Real-time Local Business Condition Index (RTLBCI)** for **{city}** provides a high-level snapshot of recent business conditions in the area. 
This index is calculated based on various economic factors to reflect the health and activity of local businesses over time.

While the data is limited and consists solely of the index values over the selected time period, it can still serve as a useful trend indicator for 
business professionals, analysts, and decision-makers. By observing how the index changes over time, you can get a sense of the overall direction 
of the local economy, whether it is improving, declining, or remaining stable.

Keep in mind:
- The values represent an abstract measure of local business conditions and do not provide granular details.
- Use this as a **supplemental tool** alongside other economic or business insights.
""")

region_info = regions[city]
s = StatCan(33100398, region_info["coord"])

try:
    df = s.make_table()

    # Display metrics and table
    st.header("Recent Business Conditions")
    st.write(f"""
        Below is a table and chart showing the index's performance over the **last {len(df)} periods** for **{city}**. 
        Keep in mind that this is a trend-based index and not an exhaustive analysis of the local business environment.
      """)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Most Recent Value", value=f"{df['value'].iloc[-1]:,.2f}")
    with col2:
        st.metric(label="Oldest Value", value=f"{df['value'].iloc[0]:,.2f}")

    # Display trendline chart
    st.markdown("### Trend Overview")
    st.line_chart(data=df, x="date", y="value", use_container_width=True)

    st.markdown("### Trend Table")
    st.dataframe(df, use_container_width=True, height=300)  # Adjust the height as needed

except Exception as e:
    st.error("Could not retrieve the data. Please check the API and try again.")

# Footer information
st.sidebar.markdown("---")
st.sidebar.write(f"""
Developed using Streamlit for seamless, real-time insights.  
📍 **{city}**
""")

