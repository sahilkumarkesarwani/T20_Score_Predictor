# T20 Score Predictor

A machine learning web app that predicts the final first-innings score of a T20 cricket match in real time, based on the current match state — teams, venue, overs played, runs, wickets, and recent scoring momentum.

## Demo
>https://t20sscorepredictor.streamlit.app/

## Overview

Predicting a T20 innings' final score is a live, dynamic problem — the right prediction at over 5 looks very different from the right prediction at over 15, even with the same run rate, because match situation (wickets in hand, momentum, venue tendencies) changes everything. This project builds a regression model that takes a live match snapshot and estimates the final first-innings total, deployed as an interactive Streamlit app for real-time predictions.

## Approach

1. **Data Extraction** (`data_extraction.ipynb`) — Collected and parsed ball-by-ball / match-level T20 data across international teams and venues into a structured dataset.
2. **Feature Engineering** (`feature_engineering.ipynb`)
   - **Balls left** = `120 - (overs bowled × 6)` — converts the more intuitive "overs" into a precise countdown of the resource that matters most.
   - **Wickets left** = `10 - wickets fallen` — reframes wickets lost as batting resource remaining, which correlates more directly with scoring potential than a raw wicket count.
   - **Current Run Rate (CRR)** = `runs / overs` — captures the innings' overall scoring pace.
   - **Last-5-overs score** — a momentum feature capturing recent scoring rate, which reflects live conditions (pitch behavior, bowling changes, batter form) better than the innings-long average alone.
   - Encoded categorical context: batting team, bowling team, and venue (city).
3. **Model Training** — Trained and evaluated regression models on the engineered feature set; **XGBoost** was selected as the final model.
4. **Deployment** — Serialized the trained model and reference dataframe with `pickle`, then built a **Streamlit** app that takes a live match snapshot as input and returns a predicted final score.

## Model Performance

| Metric | Score |
|---|---|
| Algorithm | XGBoost Regressor |
| R² Score | 0.985 |
| MAE | ±1.95 runs |

On average, predictions are within **~2 runs** of the actual first-innings score.

## Tech Stack

- **Python** — Pandas, NumPy
- **Scikit-learn** — preprocessing, pipeline, train/test split
- **XGBoost** — final regression model
- **Streamlit** — web app / UI
- **Jupyter Notebook** — data extraction, feature engineering, model development

## Project Structure

```
├── data_extraction.ipynb      # Collecting and parsing raw match data
├── feature_engineering.ipynb  # Building CRR, balls/wickets left, momentum features
├── app.py                     # Streamlit web app
├── dataset.pkl                # Extracted raw/intermediate dataset
├── df.pkl                     # Preprocessed dataframe (used by app.py)
├── model.pkl                  # Trained XGBoost model
├── requirements.txt           # Python dependencies
```

## Running Locally

```bash
# Clone the repo
git clone https://github.com/sahilkumarkesarwani/T20_Score_Predictor.git
cd T20_Score_Predictor

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Inputs Used for Prediction

- Batting team & Bowling team
- Venue (city)
- Overs played, runs scored, wickets lost
- Runs scored in the last 5 overs (momentum)

## Future Improvements

- Validate on unseen matches/venues to confirm the model isn't overfitting to specific team/venue combinations
- Add cross-validation and hyperparameter tuning with logged results
- Add feature importance (SHAP) to show which factors drive the prediction most
- Handle the all-out edge case (10 wickets lost) more explicitly in the app logic
- Deploy publicly and link demo above

## Author

**Sahil Kumar Kesarwani**
[GitHub](https://github.com/sahilkumarkesarwani)