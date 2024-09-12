import streamlit as st

st.title("Prédictions de matchs de football")
st.write("Voici les résultats des prédictions du modèle de machine learning !")

# Exemple de prédiction affichée
prediction = {"Match": "Team A vs Team B", "Prédiction": "2-1"}
st.write(prediction)
