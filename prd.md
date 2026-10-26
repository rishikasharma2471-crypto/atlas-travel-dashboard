# Product Requirement Document (PRD) - Atlas

## Project Overview
Atlas is designed to solve a major problem for budget-conscious travelers: understanding if a destination is both safe and affordable. It acts as an AI-powered analytic helper for smart trip planning.

## Key Requirements
1. **Data Blending:** Seamlessly merge global safety indices with Kaggle cost of living datasets on the fly.
2. **Interactive UI:** A clean Streamlit interface with dropdown search and dynamic charts for top safe destinations.
3. **AI Summarization:** A dedicated button that takes context numbers and invokes Groq LLMs to give a quick, readable travel advice text.
4. **Local Configuration:** Allow secure local API configurations via Streamlit secrets to protect user access.
