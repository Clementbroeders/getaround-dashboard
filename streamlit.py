### LIBRAIRIES ###
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests
import joblib


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
            return "Annulation causée par retard précédente location"
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

def predict_rental_price(data): # Fonction pour prédire le prix de location
    input_data = pd.DataFrame([data], columns = pricing.drop("rental_price_per_day", axis=1).columns)
    input_data = preprocessor.transform(input_data)
    prediction = model.predict(input_data)
    return prediction[0]


## HEADER ##

columns = st.columns([1, 0.15, 0.15])
columns[0].title("📊 GetAround Dashboard 📊")
columns[1].link_button('FastAPI', 'https://getaround-fastapi.onrender.com/docs', type = 'primary')
# columns[1].link_button('FastAPI', 'https://getaround-fastapi1-f159113e9f42.herokuapp.com/docs', type = 'primary') # si déploiement Heroku
# columns[1].link_button('FastAPI', 'http://localhost:4000/docs', type = 'primary') # si déploiement local
columns[2].link_button('GitHub', 'https://github.com/Clementbroeders/getaround-dashboard', type = 'primary')


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
def load_pricing():
    data = pd.read_csv('src/get_around_pricing_project.csv').iloc[:,1:]
    return data
pricing = load_pricing()
pricing.loc[pricing['model_key'] == 'Porsche', 'engine_power'] = 500
pricing.loc[pricing.index == 3765, 'engine_power'] = 105

model = joblib.load('src/model.pkl')
preprocessor = joblib.load('src/preprocessor.pkl')


## SIDE BAR
st.sidebar.image('img/image.jpg', use_column_width="auto")
st.sidebar.title("🔍 Filtres 🔍")
st.sidebar.write('Selectionnez le délai en :')
selection = st.sidebar.radio(label = "Selection délai", options = ['Pourcentage', 'Minutes'], horizontal=True, label_visibility = 'collapsed')
if selection == 'Pourcentage':
    seuil_percent = st.sidebar.slider("délai (%)", min_value=0, max_value=100, value=80, label_visibility = 'collapsed') / 100
    seuil_minutes = delay_filtered['delay_at_checkout_in_minutes'][delay_filtered['delay_at_checkout_in_minutes'] > 0].quantile(seuil_percent)
else:
    seuil_minutes = st.sidebar.slider("délai (minutes)", min_value=0, max_value=720, value=180, step=60, label_visibility = 'collapsed')
    seuil_percent = np.sum(delay_filtered['delay_at_checkout_in_minutes'][delay_filtered['delay_at_checkout_in_minutes'] > 0] <= seuil_minutes) / len(delay_filtered['delay_at_checkout_in_minutes'][delay_filtered['delay_at_checkout_in_minutes'] > 0])
delay_filtered['delay_at_checkout_in_minutes'] = delay_filtered['delay_at_checkout_in_minutes'].apply(lambda x: x - seuil_minutes)
delay_filtered['time_delta_with_previous_rental_in_minutes'] = delay_filtered['time_delta_with_previous_rental_in_minutes'].apply(lambda x: x - seuil_minutes if x is not None else x)
delay_filtered['categorized_state'] = delay_filtered.apply(categorize_state, axis=1, df=delay_filtered)

st.sidebar.write('Selectionnez le(s) type(s) de check-in :')
columns = st.sidebar.columns([1,1])
option_connect = columns[0].checkbox('Connect', value=True, key = 'connect')
option_mobile = columns[1].checkbox('Mobile', value=True, key = 'mobile')
selected_options = []
if option_connect:
    selected_options.append('connect')
if option_mobile:
    selected_options.append('mobile')
if not selected_options:
    st.sidebar.error("Veuillez sélectionner au moins un type de check-in.")
else:
    delay = delay[delay['checkin_type'].isin(selected_options)]
    delay_filtered = delay_filtered[delay_filtered['checkin_type'].isin(selected_options)]


## APPLICATION ##
st.write("Ce dashboard a pour but de visualiser les données de GetAround, d'appliquer un délai minimum entre deux locations, puis d'analyser les données pour prendre des décisions.")
st.write("⬅️ Utilisez la barre latérale pour sélectionner le délai minimum entre deux locations et/ou le type de check-in.")
st.write("Il est également possible de prédire le prix journalier moyen de location d'un véhicule en fonction de ses caractéristiques.")

st.write('---')

st.write('Affichage des données :')
selection_data = st.radio(label = "Selection data", options = ['Aucune donnée', 'Données initiales', 'Données modifiées'], horizontal=True, label_visibility = 'collapsed')
if selection_data == 'Données initiales':
    st.dataframe(delay)
elif selection_data == 'Données modifiées':
    st.dataframe(delay_filtered)

st.write("---")

st.subheader("📈 Analyse globale 📈")

columns = st.columns([1,1], gap = 'medium')
with columns[0]:
    st.write('')
    st.metric('Nombre de locations prises en compte', f'{len(delay):,}'.replace(',', ' '))
    checkin = delay['checkin_type'].value_counts(normalize=True)*100
    fig = px.bar(y = checkin.index, x = checkin.values, title = 'Répartition des types de check-in', labels={'x':'Pourcentage', 'y':'Type de check-in'}, height = 300)
    fig.update_traces(hovertemplate='%{x:.3f}%')
    st.plotly_chart(fig, use_container_width = True)
    

with columns[1]:
    categorized_state_counts = delay['categorized_state'].value_counts()
    fig = px.pie(names = categorized_state_counts.index, values = categorized_state_counts.values, width = 800, title = "Distribution des motifs de retard et d'annulation")
    st.plotly_chart(fig, use_container_width = True)

st.write("---")

columns = st.columns([1,1], gap = 'medium')
with columns[0]:
    st.subheader("📈 Analyse (situation actuelle) 📈")
    st.metric('Délai sélectionné :', 'Aucun délai')
    st.metric('Pourcentage des locations impactées :', 'Aucun impact')
    mean_price = pricing['rental_price_per_day'].mean()
    number_canceled = len(delay[delay['categorized_state'] == 'Annulation causée par retard précédente location'])
    price_loss_cancel = mean_price * len(delay[delay['categorized_state'] == 'Annulation causée par retard précédente location'])
    st.metric('Montant des pertes actuelles', f"{price_loss_cancel:,.0f} €".replace(',', ' '))
    number_late = len(delay[delay['categorized_state'] == 'Retard causé par retard précedente location'])
    st.metric('Nombre de retards causés par le retard de la précédente location', f"{number_late}")
    st.metric('Nombre d\'annulations causées par le retard de la précédente location', f"{number_canceled}")
    number_late_canceled = number_late + number_canceled
    st.metric('Nombre d\'impacts en retards et en annulations', number_late_canceled)
    
with columns[1]:
    st.subheader("📈 Analyse (après application du seuil) 📈")
    st.metric('Délai sélectionné :', f'{seuil_minutes:.0f} minutes')
    st.metric('Pourcentage des locations impactées :', f'{seuil_percent * 100:.2f} %')
    price_loss_filtered = mean_price * len(delay_filtered[(delay_filtered['time_delta_with_previous_rental_in_minutes'] < 0) & (delay_filtered['state'] == 'ended')])
    st.metric('Montant des pertes estimées', f"{price_loss_filtered:,.0f} €".replace(',', ' '))
    number_late_filtered = len(delay_filtered[delay_filtered['categorized_state'] == 'Retard causé par retard précedente location'])
    st.metric('Nombre de retards causés par le retard de la précédente location', f"{number_late_filtered}")
    number_canceled_filtered = len(delay_filtered[delay_filtered['categorized_state'] == 'Annulation causée par retard précédente location'])
    st.metric('Nombre d\'annulations causées par le retard de la précédente location', f"{number_canceled_filtered}")
    number_avoided = (number_late_canceled) - (number_late_filtered + number_canceled_filtered)
    st.metric('Nombre de retards et d\'annulations évités', f"{number_avoided}")

st.write('---')

st.subheader('💰 Prédiction du prix de location 💰')
st.write('Veuillez selectionner les filtres que vous souhaitez prendre en compte dans la prédiciton. Ensuite appuyer sur **Lancer les recommandations**')
bool_options = [True, False]

columns = st.columns([1,1,1,1,1])
model_key_filter = columns[0].selectbox('Selectionnez la marque', pricing['model_key'].sort_values().unique(), key = 'model_key')
mileage_filter = columns[1].number_input('Selectionnez le kilométrage', min_value = 0, max_value = 500000, step = 10000, key = 'mileage')
engine_power_filter = columns[2].number_input('Selectionnez la motorisation (cv)', min_value = 60, max_value = 550, step = 10, key = 'engine_power')
# engine_power_filter = columns[2].selectbox('Selectionnez la motorisation (cv)', pricing['engine_power'].sort_values().unique(), key = 'engine_power')
fuel_filter = columns[3].selectbox('Selectionnez le type de carburant', pricing['fuel'].sort_values().unique(), key = 'fuel')
paint_color_filter = columns[4].selectbox('Selectionnez la couleur', pricing['paint_color'].sort_values().unique(), key = 'paint_color')

columns = st.columns([1,1,1,1,1])
car_type_filter = columns[0].selectbox('Selectionnez le type de véhicule', pricing['car_type'].sort_values().unique(), key = 'car_type')
private_parking_available_filter = columns[1].selectbox('Parking privé disponible', bool_options, key = 'private_parking_available')
has_gps_filter = columns[2].selectbox('GPS disponible', bool_options, key = 'has_gps')
has_air_conditioning_filter = columns[3].selectbox('Air conditionnée disponible', bool_options, key = 'has_air_conditioning')
automatic_car_filter = columns[4].selectbox('Véhicule automatique', bool_options, key = 'automatic_car')

columns = st.columns([1,1,1,1,1])
has_getaround_connect_filter = columns[1].selectbox('GetAround connect disponible', bool_options, key = 'has_getaround_connect')
has_speed_regulator_filter = columns[2].selectbox('Régulateur de vitesse disponible', bool_options, key = 'has_speed_regulator')
winter_tires_filter = columns[3].selectbox('Pneus neige disponible', bool_options, key = 'winter_tires')

filters_dict = {
    'model_key': model_key_filter,
    'mileage': mileage_filter,
    'engine_power': engine_power_filter,
    'fuel': fuel_filter,
    'paint_color': paint_color_filter,
    'car_type': car_type_filter,
    'private_parking_available': int(private_parking_available_filter),
    'has_gps': int(has_gps_filter),
    'has_air_conditioning': int(has_air_conditioning_filter),
    'automatic_car': int(automatic_car_filter),
    'has_getaround_connect': int(has_getaround_connect_filter),
    'has_speed_regulator': int(has_speed_regulator_filter),
    'winter_tires': int(winter_tires_filter)
}
filters_list = list(filters_dict.values())
filters_list = [int(value) if isinstance(value, pd.Int64Dtype().type) else value for value in filters_list]
data_dict = {"filters_list": filters_list}

columns = st.columns([2,1,2])
recommandations = columns[1].button('Lancer les recommandations', type = 'primary')

if recommandations:
    success = False
    try:
        api_urls = ["http://localhost:4000/predict",
                    "https://getaround-fastapi.onrender.com/predict",
                    "https://getaround-fastapi1-f159113e9f42.herokuapp.com/predict"]
        for api_url in api_urls:
            try:
                response = requests.post(api_url, json=data_dict)
                if response.status_code == 200:
                    result = response.json()
                    st.write('Vous pouvez louer votre véhicule au prix journalier de :')
                    st.metric('Prix de location', f"{result['prediction']:.2f} €", label_visibility='collapsed')
                    success = True 
                    break
            except requests.RequestException as e:
                pass
    except Exception as e:
        pass
    if not success:
        prediction = predict_rental_price(filters_list)
        st.write('Vous pouvez louer votre véhicule au prix journalier de :')
        st.metric('Prix de location', f"{prediction:.2f} €", label_visibility='collapsed')
        

### FOOTER ###
st.write("---")
st.write("Powered by [Streamlit](https://streamlit.io/). Lien vers le [GitHub](https://github.com/Clementbroeders/getaround-dashboard).")
st.write('© 2024 Clément Broeders.')