import os
import streamlit as st
import pandas as pd
import plotly.express as px
import kagglehub
from groq import Groq

st.set_page_config(page_title="Atlas | Travel Risk & Cost Intelligence", page_icon="🌍", layout="wide")

st.title("Atlas: Travel Risk & Cost Intelligence Dashboard")
st.caption("Cost of living data from Kaggle, safety index from a curated dataset, and an AI summary powered by Groq.")


@st.cache_data(show_spinner="Fetching cost of living data...")
def load_cost_data():
    path = kagglehub.dataset_download("myrios/cost-of-living-index-by-country-by-number-2024")
    csv_name = [f for f in os.listdir(path) if f.endswith(".csv")][0]
    return pd.read_csv(os.path.join(path, csv_name))


@st.cache_data
def load_safety_data():
    return pd.read_csv("safety_data.csv")


cost_df = load_cost_data()
safety_df = load_safety_data()

# removing extra spaces so the names match properly
cost_df["Country"] = cost_df["Country"].str.strip()
safety_df["Country"] = safety_df["Country"].str.strip()

# same country, different spelling in the two files
safety_df["Country"] = safety_df["Country"].replace({
    "USA": "United States",
    "Czechia": "Czech Republic",
})

# only keeping countries that exist in both files
df = pd.merge(cost_df, safety_df, on="Country", how="inner")

if df.empty:
    st.error("Something went wrong merging the two datasets - no matching countries found.")
    st.stop()


# ---------- sidebar ----------
st.sidebar.header("Search Destinations")
search_query = st.sidebar.text_input("Type to filter...")

if search_query:
    filtered_df = df[df["Country"].str.contains(search_query, case=False, na=False, regex=False)]
else:
    filtered_df = df

if filtered_df.empty:
    st.sidebar.warning("No matches found.")
    st.stop()

selected_country = st.sidebar.selectbox("Select a destination", sorted(filtered_df["Country"].unique()))
row = df[df["Country"] == selected_country].iloc[0]

safety_score = row["Safety Index"]
cost_index = row["Cost of Living Index"]
buying_power = row["Local Purchasing Power Index"]


# ---------- metrics ----------
if safety_score >= 80:
    status = "Very Safe"
elif safety_score >= 60:
    status = "Moderately Safe"
else:
    status = "Caution Advised"

c1, c2, c3 = st.columns(3)
c1.metric("Safety Index (out of 100)", f"{safety_score:.1f}", status, delta_color="off")
c2.metric("Cost of Living Index", f"{cost_index:.1f}", help="New York City = 100")
c3.metric("Local Purchasing Power", f"{buying_power:.1f}")

st.divider()


# ---------- chart ----------
st.subheader("Safety vs Cost - Top 20 Safest Countries")

top20 = df.sort_values("Safety Index", ascending=False).head(20)
fig = px.bar(
    top20,
    x="Country",
    y=["Safety Index", "Cost of Living Index"],
    barmode="group",
    template="plotly_dark",
    color_discrete_map={
       "Safety Index": "#F472B6",
        "Cost of Living Index": "#60A5FA",
    },
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    legend_title_text="",
    xaxis_title=None,
    yaxis_title="Index value",
)
fig.update_yaxes(gridcolor="#3B2660")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------- AI summary ----------
st.subheader(f"AI Risk Summary - {selected_country}")

if st.button("Generate AI Summary"):
    api_key = st.secrets.get("GROQ_API_KEY", "")

    if not api_key:
        st.error("GROQ_API_KEY is missing. Add it in .streamlit/secrets.toml")
        st.stop()

    prompt = f"""Give a short 3-4 sentence travel risk and cost summary for {selected_country}.
Safety Index: {safety_score} out of 100.
Cost of Living Index: {cost_index} (New York City = 100).
Tell me if it is generally safe for tourists and whether it is cheap, moderate or expensive.
Keep it simple."""

    with st.spinner("Generating AI travel summary..."):
        try:
            client = Groq(api_key=api_key)
            reply = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.6,
            )
            summary = reply.choices[0].message.content.replace("\n", "<br>")
            st.markdown(f"<div style='background:#2D1A4A; border-left:5px solid #F472B6; padding:16px 20px; border-radius:10px; color:#F5EBFF;'>{summary}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            try:
                names = [m.id for m in client.models.list().data]
                st.info("Models available on your key: " + ", ".join(names))
            except Exception as e2:
                st.warning(f"Could not fetch model list: {e2}")