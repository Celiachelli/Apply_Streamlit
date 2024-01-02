import streamlit as st
from functions import scraping_bdm
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title='Scraping Blog du Modérateur', layout='wide')

# CSS pour personnaliser l'apparence
st.markdown(""" <style> ... </style> """, unsafe_allow_html=True)

# En-tête avec icône
st.title(':mag: Explorateur d\'Articles du Blog du Modérateur')

# Création des onglets
tab1, tab2 = st.tabs(["Recherche", "Résultats"])

# Onglet de recherche
with tab1:
    with st.sidebar:
        st.write("## :wrench: Paramètres de Recherche")
        keywords = st.text_input(":key: Entrez les mots-clés")

    if st.button('🔍 Lancer la recherche'):
        if keywords:
            search_url = f'https://www.blogdumoderateur.com/?s={keywords}'
            data = scraping_bdm(search_url)

            # Stocker les données dans la session pour les utiliser dans l'autre onglet
            st.session_state['data'] = data

# Onglet des résultats
with tab2:
    if 'data' in st.session_state and st.session_state['data']:
        df = pd.DataFrame.from_dict(st.session_state['data'], orient='index')
        st.write("### :bar_chart: Résultats de la Recherche")
        st.dataframe(df)

        # Graphique interactif (si pertinent)
        fig = px.bar(df, x='label', y='time', color='label', title="Répartition des Articles par Catégorie")
        st.plotly_chart(fig)

        # Bouton de téléchargement CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label=":arrow_down: Télécharger les données en CSV",
            data=csv,
            file_name='articles_bdm.csv',
            mime='text/csv',
        )
    else:
        st.write("Aucune donnée à afficher. Veuillez effectuer une recherche dans l'onglet 'Recherche'.")
