import streamlit as st 
import pickle
import pandas as pd 
import numpy as np


model = pickle.load(open('model.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))


st.title("T20 Score Predictor",text_alignment= 'center')
st.write("This app predicts the score of first innings of T20 cricket matches.")

teams = [
    'Australia',
    'Afghanistan',
    'Bangladesh',
    'England',
    'India',
    'New Zealand',
    'Pakistan',
    'South Africa',
    'Sri Lanka',
    'West Indies',
]



col1, col2 = st.columns(2)

with col1: 
    batting_team = st.selectbox("Select Batting Team", sorted(teams))

with col2:
    bowling_team = st.selectbox("Select Bowling Team", teams)

if batting_team == bowling_team:
    st.error("Batting and Bowling teams cannot be the same. Please select different teams.")
    st.stop()

col3, col4, col5 = st.columns(3)

with col3:
    overs = st.number_input('How many overs have been played', min_value = 1, max_value= 20, step = 1)

with col4:
    runs = st.number_input('How many runs have been scored', max_value= overs * 6, step = 1)

with col5:
    wickets = st.number_input('How many wickets have been lost', max_value= 10, step = 1)


city = st.selectbox('Select Venue', sorted(df['city'].unique()))


if overs >= 5:
    five_over_score = st.number_input('Score in last 5 overs', min_value = 0, max_value = 180)
else: 
    st.write('Wait 5 overs to complete.')
    st.stop()

if st.button('Predict Score'):

    balls_left = 120 - overs * 6
    wickets_left = 10 - wickets
    if overs > 0 :
        crr = runs / overs
    else :
        st.error("Overs played should not be zero or less than zero. Enter valid overs.")
        st.stop()

    query = pd.DataFrame({"batting_team": [batting_team], "bowling_team": [bowling_team],"city": [city], "score": [runs],"balls_left": [balls_left], "wickets_left": [wickets_left], "crr": [crr], "last_five" :[five_over_score]})

    if (wickets < 10) & (overs < 20):

        result =  model.predict(query)
        st.text(f"The Predicted Score {batting_team} is: " + str(round(result[0], 0)))

    else :

        st.text(f'The Predicted Score {batting_team} is: {runs}')

    