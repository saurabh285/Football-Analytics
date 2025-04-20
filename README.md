# Football Analytics

As a football player and lifelong fan, this project is a personal exploration that merges my love for the game with the power of data and AI. Using event-level data from StatsBomb, this system analyzes the performances of Liverpool players — currently focusing on Emre Can and James Milner — across 44 historical matches.

## Project Highlights

This project is built to go beyond basic stats, leveraging intelligent tools to extract meaningful performance insights:

### Intelligent Anomaly Detection
- Automatically detects matches where a player performed differently than usual.
- Uses statistical modeling and Isolation Forests to identify outlier games.
- Allows performance evolution tracking throughout the season.

### Natural Language Insights (LLM)
- Integrates Gemini 1.5 Flash to interpret player trends and match anomalies.
- Generates short, readable summaries for every metric and match trend.
- Compares players using natural language that mirrors a football analyst’s commentary.

### Data and Analysis Components
- Modular Python codebase for loading, cleaning, and analyzing StatsBomb event data.
- 44 match CSV files stored under a `matches` folder for direct access.
- Python notebooks demonstrating early experiments and feature explorations.
- Interactive visual analysis interface powered by Streamlit.

## Use Cases

- Identify how and when a midfielder like Emre Can shifts between defensive and creative roles.
- Compare the passing styles and pressure-handling behavior of two different players.
- Generate scouting-style summaries from raw match data.

This project is both a technical deep dive and a fan-driven attempt to bring clarity to what happens on the pitch — one event at a time.


##  Folder Structure

```
football-analytics/
├── app.py                  # Streamlit dashboard
├── analysis.py             # Stats processing and anomaly detection
├── config.py               # Metric list and global constants
├── llm_utils.py            # Gemini API and description generators
├── data_loader.py          # Match data loading utilities
├── matches/                # 44 Liverpool match CSV files
├── notebooks/              # Jupyter notebooks used during exploration
└── .streamlit/             # Local secrets (excluded from GitHub)
```

---

##  Analysis Approach

### Event Types Considered (`type` column):

- `'Pass'`, `'Ball Receipt*'`, `'Carry'`, `'Dribble'`
- `'Duel'`, `'Pressure'`, `'Ball Recovery'`, `'Interception'`
- `'Shot'`, `'Foul Committed'`, `'Foul Won'`, `'Dispossessed'`, etc.

### Key Features Tracked:

- **Pass:**

  - `pass_outcome`: empty = completed
  - `pass_cross`, `pass_goal_assist`, `pass_shot_assist` (True/False)
  - `pass_body_part`, `pass_height`, `pass_length`

- **Carry:**

  - Distance = Euclidean between `location` and `carry_end_location`

- *Ball Receipt**:*\*

  - Count of successful receptions

- **Dribble:**

  - `dribble_outcome`: “Complete” or not

- **Pressure:**

  - `under_pressure`: Boolean

- **Defensive Work:**

  - `Ball Recovery`, `Interception`, `Duel` outcome

- **Receiving:**

  - `pass_recipient` + `ball_receipt_outcome`

---

##  Getting Started

1. Clone the repo:

   ```bash
   git clone https://github.com/your-username/football-analytics.git
   cd football-analytics
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set your Gemini API key: Create `.streamlit/secrets.toml`:

   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```

4. Run the app:

   ```bash
   streamlit run app.py
   ```

---

## Note

- The `.streamlit/secrets.toml` file is excluded via `.gitignore`
- All match data is publicly accessible through the [StatsBomb Open Data](https://github.com/statsbomb/open-data)

---


