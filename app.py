
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Album Paintball", layout="wide")

st.title("📘 Album Paintball - Première Division")

# Chargement ou création de la base de données
@st.cache_data
def load_players():
    # Données fictives de base
    data = []
    for i in range(1, 173):
        data.append({
            "Numéro": f"{i:03}",
            "Nom": f"Joueur {i}",
            "Équipe": f"Équipe {((i - 1) % 10) + 1}"
        })
    return pd.DataFrame(data)

df = load_players()

# Sélection de l'utilisateur
st.sidebar.header("👤 Ton profil")
username = st.sidebar.text_input("Entre ton pseudo", "Moi")

# Session utilisateur
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

if username not in st.session_state.user_data:
    st.session_state.user_data[username] = set()

# Affichage de la collection
st.subheader("🖼️ Ta collection")
cols = st.columns([1, 3, 3, 2])
cols[0].markdown("**#**")
cols[1].markdown("**Nom**")
cols[2].markdown("**Équipe**")
cols[3].markdown("**Possédé ?**")

new_user_cards = set()

for index, row in df.iterrows():
    cols = st.columns([1, 3, 3, 2])
    cols[0].write(row["Numéro"])
    cols[1].write(row["Nom"])
    cols[2].write(row["Équipe"])
    owned = row["Numéro"] in st.session_state.user_data[username]
    if cols[3].checkbox("", value=owned, key=f"{username}_{row['Numéro']}"):
        new_user_cards.add(row["Numéro"])

st.session_state.user_data[username] = new_user_cards

# Comparaison avec les autres
st.subheader("🔄 Échanges possibles")

for other_user, their_cards in st.session_state.user_data.items():
    if other_user == username:
        continue
    my_cards = st.session_state.user_data[username]
    they_need = my_cards - their_cards
    they_have = their_cards - my_cards
    possible_trades = they_need & they_have
    if possible_trades:
        st.markdown(f"**Avec {other_user} :**")
        for card in possible_trades:
            info = df[df['Numéro'] == card].iloc[0]
            st.write(f"- {card} : {info['Nom']} ({info['Équipe']})")
