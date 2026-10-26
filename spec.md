# Technical Specification (Spec) - Atlas

## Architecture & Tech Stack
- **Frontend & Interface:** Streamlit (Python framework)
- **Data Manipulation:** Pandas (Dataframe merging on country names)
- **Data Visualization:** Plotly Express (Interactive scatter/bar plots)
- **LLM Engine:** Groq Console API (Utilizing open-weights models for low-latency generation)
- **Data Layer:** Static `safety_data.csv` combined with `kagglehub` automated package retrieval.

## System Data Flow
1. User selects a country -> App filters merged pandas dataframe.
2. App passes structural data (Safety + Cost index metrics) to Plotly -> Renders dynamic dashboard charts.
3. User triggers AI Summary -> Prompt constructed with specific indices -> Dispatched to Groq API -> Text response rendered inside Streamlit app window.
