# Atlas: Travel Risk & Cost Intelligence Dashboard

Atlas helps travelers compare destinations by **safety** and **cost** in one place, and adds a short AI-written summary for the selected country.

Built for **WarriorHack 2.0**.

## What it does

- Lets you search and select a destination country
- Shows three key numbers: Safety Index, Cost of Living Index, and Local Purchasing Power
- Compares safety vs cost for the top 20 safest countries in an interactive chart
- Generates a short AI travel risk and cost summary using Groq

## How it works

1. Cost of living data is downloaded from Kaggle.
2. Safety index data is loaded from `safety_data.csv`.
3. Both datasets are cleaned and merged on the country name.
4. Streamlit shows the dashboard and Plotly draws the chart.
5. When you click **Generate AI Summary**, the country's numbers are sent to a Groq-hosted model, which writes a simple summary.

## Tech stack

Python, Streamlit, Pandas, Plotly, KaggleHub, Groq API

## How to run

1. Install the libraries:

```
   pip install -r requirements.txt
```

2. Get a free API key from [Groq Console](https://console.groq.com/keys). Then create a file named `.streamlit/secrets.toml` in the project folder and add your key:

```toml
   GROQ_API_KEY = "your_key_here"
```

3. Start the app:

```
   python -m streamlit run app.py
```

## Project files

- `app.py`: the dashboard
- `safety_data.csv`: safety index data
- `requirements.txt`: Python libraries needed
- `.streamlit/config.toml`: dashboard theme

## Future ideas

- Show the selected country in the chart next to the top 20
- Add more risk factors (health, weather, political stability)
- Compare two countries side by side
- Add a travel budget calculator

## Notes

- The app needs your own Groq API key to generate the AI summary. The key is not included in this repository.
- Keep your key private and do not share `.streamlit/secrets.toml` publicly.
- The Kaggle dataset is downloaded automatically the first time you run the app, so an internet connection is needed.
- Available Groq models can differ between accounts. If you see a "model not found" error, change the `model=` name in `app.py` to one that is available on your account.
