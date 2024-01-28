### LIBRAIRIES ###
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


### CONFIGURATION ###
st.set_page_config(
    page_title="GetAround dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


## FONCTIONS ##
def has_delay_in_previous(row, df): # Lié à la fonction categorize_state
    if pd.notna(row['previous_ended_rental_id']):
        matching_rows = df[df['rental_id'] == row['previous_ended_rental_id']]
        if not matching_rows.empty:
            previous_row = matching_rows.iloc[0]
            return pd.notna(previous_row['delay_at_checkout_in_minutes']) and previous_row['delay_at_checkout_in_minutes'] > 0
    return False

def categorize_state(row, df): # Nécessite la fonction has_delay_in_previous
    if row['state'] == 'canceled':
        if has_delay_in_previous(row, df):
            return "Annulé causé par retard précédente location"
        else:
            return "Annulation sans motif"
    elif row['state'] == 'ended':
        if row['delay_at_checkout_in_minutes'] > 0:
            if has_delay_in_previous(row, df):
                return "Retard causé par retard précedente location"
            else:
                return "Retard sans motif"
        else:
            return "A l'heure / En avance"
    else:
        return "Etat non reconnu"


## CHARGEMENT DES DONNEES ##
@st.cache_data
def load_delay():
    data = pd.read_excel('src/get_around_delay_analysis.xlsx')
    return data

delay = load_delay()
delay['categorized_state'] = delay.apply(categorize_state, axis=1, df=delay)
percent_outliers = 97.5
lower_quantile = np.percentile(delay['delay_at_checkout_in_minutes'].dropna(), (100 - percent_outliers) / 2)
upper_quantile = np.percentile(delay['delay_at_checkout_in_minutes'].dropna(), 100 - (100 - percent_outliers) / 2)
delay = delay[((delay['delay_at_checkout_in_minutes'] >= lower_quantile) & (delay['delay_at_checkout_in_minutes'] <= upper_quantile)) | (delay['delay_at_checkout_in_minutes'].isnull())]

delay_filtered = delay.copy()

@st.cache_data
def load_price():
    data = pd.read_csv('src/get_around_pricing_project.csv').iloc[:,1:]
    return data
price = load_price()


## SIDE BAR
st.sidebar.image('img/image.jpg', use_column_width="auto")
st.sidebar.title("🔍 Filtres 🔍")

st.sidebar.write('Selectionnez le délai en :')
selection = st.sidebar.radio(label = "Selection délai", options = ['Pourcentage', 'Minutes'], horizontal=True, label_visibility = 'collapsed')
if selection == 'Pourcentage':
    seuil_percent = st.sidebar.slider("délai (%)", min_value=0, max_value=100, value=90, label_visibility = 'collapsed') / 100
    seuil_minutes = np.quantile(delay_filtered['delay_at_checkout_in_minutes'][delay_filtered['delay_at_checkout_in_minutes'] > 0], seuil_percent)

else:
    seuil_minutes = st.sidebar.slider("délai (minutes)", min_value=0, max_value=720, value=300, step=60, label_visibility = 'collapsed')
    seuil_percent = None

delay_filtered['delay_at_checkout_in_minutes'] = delay_filtered['delay_at_checkout_in_minutes'].apply(lambda x: x - seuil_minutes)
delay_filtered['categorized_state'] = delay_filtered.apply(categorize_state, axis=1, df=delay_filtered)

st.sidebar.write('Selectionnez le(s) type(s) de checkin :')
columns = st.sidebar.columns([1,1])
option_connect = columns[0].checkbox('Connect', value=True, key = 'connect')
option_mobile = columns[1].checkbox('Mobile', value=True, key = 'mobile')
selected_options = []
if option_connect:
    selected_options.append('connect')
if option_mobile:
    selected_options.append('mobile')

if not selected_options:
    st.sidebar.error("Veuillez sélectionner au moins un type de checkin.")
else:
    delay = delay[delay['checkin_type'].isin(selected_options)]
    delay_filtered = delay_filtered[delay_filtered['checkin_type'].isin(selected_options)]


## MODIFICATION DES DONNEES ##


## APPLICATION ##
st.title("📊 GetAround Dashboard 📊")
st.write("Ce dashboard a pour but de visualiser les données de GetAround, d'y sélectionner un délai minimum entre deux locations, puis d'analyser les données avant et après modification du seuil.")
st.write("---")


# TEMPORAIRE : affichage des données
st.dataframe(delay)


columns = st.columns([1,1], gap = 'medium')
with columns[0]:
    st.subheader("📈 Analyse initiale 📈")
    
    
with columns[1]:
    st.subheader("📈 Analyse après modification du seuil 📈")
    st.write('Seuil', seuil_minutes, 'minutes')


# TEMPORAIRE : affichage des données
st.dataframe(delay_filtered)


### FOOTER ###
github_url = 'https://github.com/Clementbroeders/getaround-dashboard'

st.write("---")
st.write(f"Powered by [Streamlit](https://streamlit.io/). Lien vers le [GitHub]({github_url}).")
st.write('© 2024 Clément Broeders.')