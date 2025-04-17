import streamlit as st
import pandas as pd

# === Configuration de la page ===
st.set_page_config(page_title="Moteur de Recommandation - Engagement", layout="centered")

# === 1. Chargement des données ===
@st.cache_data
def load_data():
    return pd.read_excel("utilisateurs_avec_score_engagement.xlsx")

df = load_data()

# === 2. Préparation initiale ===
df["score_sur_10"] = (df["score_engagement"] * 10).round(1)
clusters = df["cluster_label"].unique()

# === Ajouter les recommandations personnalisées selon les clusters ===
def assign_recommendation(cluster):
    mapping = {
        "Le fantôme": "📧 Relance email + contenu incitatif.",
        "Le curieux discret": "🔔 Notification personnalisée + article recommandé.",
        "Le power user": "🏆 Accès premium, badges, remerciements."
    }
    return mapping.get(cluster, "❓ Aucune recommandation disponible.")

df["recommandation"] = df["cluster_label"].apply(assign_recommendation)


# === 3. Titre et introduction ===
st.title("🎯 Moteur de Recommandation - Engagement Utilisateur")
st.markdown("Ce tableau de bord permet de visualiser le niveau d'engagement des utilisateurs et propose des actions adaptées aux différents profils détectés.")

# === 3.5. Filtrage des utilisateurs ===
st.subheader("🔎 Filtrer les utilisateurs")

# Colonnes à afficher dans le tableau
colonnes_a_afficher = [
    "visitor_id", "first_session_yyyymmdd",
    "nb_sessions", "nb_requests",
    "cluster_label", "score_engagement", "recommandation"
]

# Filtre : choix du cluster (multiselect)
clusters_disponibles = sorted(df["cluster_label"].unique())
cluster_filtre = st.multiselect("Filtrer par persona (cluster) :", clusters_disponibles, default=clusters_disponibles)

# Filtre : plage de score d'engagement
min_score = float(df["score_engagement"].min())
max_score = float(df["score_engagement"].max())
score_range = st.slider("Score d'engagement (entre 0 et 1) :", min_score, max_score, (min_score, max_score))

# Application des filtres
df_filtered = df[
    (df["cluster_label"].isin(cluster_filtre)) &
    (df["score_engagement"] >= score_range[0]) &
    (df["score_engagement"] <= score_range[1])
]

# Affichage du tableau filtré
st.markdown("**Utilisateurs filtrés :**")
st.dataframe(df_filtered[colonnes_a_afficher].reset_index(drop=True))


# === 4. Sélection d'utilisateur ===
selected_user = st.selectbox("👤 Choisir un utilisateur :", df["visitor_id"].unique())
user_data = df[df["visitor_id"] == selected_user].iloc[0]

# === 5. Profil utilisateur sélectionné ===
st.subheader("📊 Profil utilisateur")
st.markdown(f"- **Persona / Cluster :** `{user_data['cluster_label']}`")
st.markdown(f"- **Score d'engagement :** `{user_data['score_sur_10']} / 10`")
st.progress(user_data["score_engagement"])

st.markdown("**Statistiques personnelles :**")
col1, col2, col3 = st.columns(3)
col1.metric("📎 Sessions", int(user_data["nb_sessions"]))
col2.metric("🖱️ Clics", int(user_data["nb_clicks"]))
col3.metric("⏱️ Jours d'inactivité", int(user_data["days_since_last_activity"]))

# === 6. Recommandation spécifique ===
def get_recommendation(cluster):
    reco = {
        "Le fantôme": "📧 Relance par email avec contenu attractif.",
        "Le curieux discret": "🔔 Notification avec article personnalisé.",
        "Le power user": "🏆 Proposer des fonctionnalités premium ou des badges."
    }
    return reco.get(cluster, "❓ Aucune recommandation disponible.")

st.subheader("🧠 Recommandation personnalisée")
st.success(get_recommendation(user_data["cluster_label"]))

# === 7. Statistiques globales ===
with st.expander("📈 Voir les statistiques globales"):
    st.markdown("**Moyenne des scores par cluster :**")
    cluster_stats = df.groupby("cluster_label")["score_sur_10"].mean().round(2).reset_index()
    st.dataframe(cluster_stats.rename(columns={"score_sur_10": "Score moyen"}))
    st.bar_chart(cluster_stats.set_index("cluster_label"))

# === 8. Recommandations par cluster ===
st.subheader("📚 Recommandations par cluster")

reco_data = pd.DataFrame({
    "Cluster": [0, 1, 2],
    "Persona": ["Le fantôme", "Le curieux discret", "Le power user"],
    "Description": [
        "Très peu actif, dernière activité lointaine.",
        "Un peu actif mais peu engagé.",
        "Très actif, fort engagement (souvent staff ou bot)."
    ],
    "Recommandation": [
        "📧 Relance email + contenu incitatif.",
        "🔔 Notification personnalisée + article recommandé.",
        "🏆 Accès premium, badges, remerciements."
    ]
})

st.dataframe(reco_data)

# === 9. Footer ===
st.markdown("---")
st.caption("Projet - M2 Data Management • Streamlit Dashboard - Moteur de recommandation")
