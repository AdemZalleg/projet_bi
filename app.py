import streamlit as st
import pandas as pd
import numpy as np

# === 1. Chargement des données ===
@st.cache_data
def load_data():
    return pd.read_excel("/content/sample_data/utilisateurs_avec_score_engagement.xlsx")

df = load_data()

# === 2. Préparation initiale ===
df["score_sur_10"] = (df["score_engagement"] * 10).round(1)  # Optionnel : score entre 0 et 10
clusters = df["cluster_label"].unique()

# === 3. Titre de l'application ===
st.set_page_config(page_title="Moteur de Recommandation - Engagement", layout="centered")
st.title("🎯 Moteur de Recommandation - Engagement Utilisateur")

st.markdown("Sélectionnez un utilisateur pour consulter son niveau d'engagement et les recommandations adaptées.")

# === 4. Sélection d'utilisateur ===
selected_user = st.selectbox("👤 Choisir un utilisateur :", df["visitor_id"].unique())

user_data = df[df["visitor_id"] == selected_user].iloc[0]

# === 5. Affichage des infos utilisateur ===
st.subheader("📊 Profil utilisateur")
st.markdown(f"- **Cluster / Persona :** `{user_data['cluster_label']}`")
st.markdown(f"- **Score d'engagement :** `{user_data['score_sur_10']} / 10`")
st.progress(user_data["score_engagement"])

# === 6. Recommandation basée sur le cluster ===
def get_recommendation(cluster):
    reco = {
        "Le fantôme": "📧 Relance par email avec contenu attractif.",
        "Le curieux discret": "🔔 Notifier d'un article ou contenu personnalisé.",
        "Le power user": "🏆 Proposer des fonctionnalités avancées ou badges de fidélité."
    }
    return reco.get(cluster, "❓ Aucune recommandation trouvée.")

st.subheader("🧠 Recommandation personnalisée")
st.success(get_recommendation(user_data["cluster_label"]))

# === 7. Section optionnelle : stats globales ===
with st.expander("📈 Voir les statistiques globales"):
    cluster_stats = df.groupby("cluster_label")["score_sur_10"].mean().round(2).reset_index()
    st.dataframe(cluster_stats.rename(columns={"score_sur_10": "Score moyen"}))

    st.bar_chart(cluster_stats.set_index("cluster_label"))

# === 8. Footer ===
st.markdown("---")
st.caption("Projet - M2 Data Management • Streamlit Dashboard - Moteur de recommandation")


# Cellule 3 - Téléversement des données (si nécessaire)
from google.colab import files
uploaded = files.upload()  # Sélectionnez votre fichier Excel

!streamlit run app.py & npx localtunnel --port 8501
