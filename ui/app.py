import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json
import sys
import time

# Ajouter le répertoire parent au chemin pour importer les modules du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importer les modules du projet
from scripts.niche_discovery import NicheDiscovery
from scripts.content_generation import ContentGenerator
from scripts.tts import TTSEngine
from scripts.video_production import VideoProducer
from scripts.youtube_publishing import YouTubeAuth, YouTubePublisher
from scripts.analytics import PerformanceAnalyzer

# Configuration de la page Streamlit
st.set_page_config(
    page_title="AutoTubeCPM - Tableau de bord",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF0000;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #333;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: white;
        margin-bottom: 1rem;
    }
    .metric-card {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: white;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #FF0000;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
    }
    .trend-up {
        color: green;
    }
    .trend-down {
        color: red;
    }
    .trend-stable {
        color: orange;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF0000;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #CC0000;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #666;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour initialiser les variables de session
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'youtube_auth' not in st.session_state:
        st.session_state.youtube_auth = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"
    if 'niches' not in st.session_state:
        st.session_state.niches = []
    if 'generated_scripts' not in st.session_state:
        st.session_state.generated_scripts = []
    if 'generated_videos' not in st.session_state:
        st.session_state.generated_videos = []
    if 'uploaded_videos' not in st.session_state:
        st.session_state.uploaded_videos = []
    if 'performance_data' not in st.session_state:
        st.session_state.performance_data = {}

# Initialiser les variables de session
init_session_state()

# Fonction pour simuler l'authentification YouTube
def authenticate_youtube():
    st.session_state.authenticated = True
    st.session_state.youtube_auth = "authenticated"
    st.success("Authentification YouTube réussie !")

# Fonction pour simuler la déconnexion
def logout():
    st.session_state.authenticated = False
    st.session_state.youtube_auth = None
    st.success("Déconnexion réussie !")

# Fonction pour charger les données simulées
def load_sample_data():
    # Simuler des données de niches
    niches = [
        {"category": "finance", "subcategory": "investing", "estimated_cpm": 18.5, "trend": "up"},
        {"category": "technology", "subcategory": "ai_machine_learning", "estimated_cpm": 15.0, "trend": "up"},
        {"category": "business", "subcategory": "entrepreneurship", "estimated_cpm": 14.5, "trend": "stable"},
        {"category": "finance", "subcategory": "cryptocurrency", "estimated_cpm": 20.0, "trend": "down"},
        {"category": "technology", "subcategory": "gadget_reviews", "estimated_cpm": 14.0, "trend": "up"}
    ]
    
    # Simuler des scripts générés
    scripts = [
        {"title": "10 Stratégies d'Investissement pour 2025", "category": "finance", "subcategory": "investing", "date": "2025-03-20", "status": "completed"},
        {"title": "Comment l'IA Transforme le Marketing Digital", "category": "technology", "subcategory": "ai_machine_learning", "date": "2025-03-18", "status": "completed"},
        {"title": "Guide Complet du Bitcoin pour Débutants", "category": "finance", "subcategory": "cryptocurrency", "date": "2025-03-15", "status": "completed"},
        {"title": "Les Meilleurs Outils SaaS pour Entrepreneurs", "category": "business", "subcategory": "entrepreneurship", "date": "2025-03-10", "status": "completed"}
    ]
    
    # Simuler des vidéos générées
    videos = [
        {"title": "10 Stratégies d'Investissement pour 2025", "duration": "12:45", "date": "2025-03-21", "status": "uploaded", "views": 1250, "revenue": 22.5},
        {"title": "Comment l'IA Transforme le Marketing Digital", "duration": "15:30", "date": "2025-03-19", "status": "uploaded", "views": 980, "revenue": 14.7},
        {"title": "Guide Complet du Bitcoin pour Débutants", "duration": "18:20", "date": "2025-03-16", "status": "ready", "views": 0, "revenue": 0},
        {"title": "Les Meilleurs Outils SaaS pour Entrepreneurs", "duration": "10:15", "date": "2025-03-11", "status": "processing", "views": 0, "revenue": 0}
    ]
    
    # Simuler des données de performance
    performance = {
        "views": {
            "current": 2230,
            "previous": 1850,
            "change_pct": 20.5,
            "trend": "up"
        },
        "revenue": {
            "current": 37.2,
            "previous": 28.5,
            "change_pct": 30.5,
            "trend": "up"
        },
        "subscribers": {
            "current": 125,
            "previous": 95,
            "change_pct": 31.6,
            "trend": "up"
        },
        "cpm": {
            "current": 16.8,
            "previous": 15.4,
            "change_pct": 9.1,
            "trend": "up"
        },
        "daily_views": [120, 135, 110, 145, 160, 175, 190, 210, 195, 220, 240, 250, 280],
        "daily_revenue": [1.8, 2.0, 1.7, 2.2, 2.4, 2.6, 2.9, 3.2, 3.0, 3.3, 3.6, 3.8, 4.2],
        "category_cpm": {
            "categories": ["Finance", "Technologie", "Business", "Santé", "Éducation"],
            "values": [18.5, 15.0, 14.5, 11.0, 10.0]
        }
    }
    
    return niches, scripts, videos, performance

# Charger les données simulées
niches, scripts, videos, performance = load_sample_data()
st.session_state.niches = niches
st.session_state.generated_scripts = scripts
st.session_state.generated_videos = videos
st.session_state.performance_data = performance

# Barre latérale
with st.sidebar:
    st.markdown('<div class="sidebar-header">🎬 AutoTubeCPM</div>', unsafe_allow_html=True)
    
    # Section d'authentification
    if not st.session_state.authenticated:
        st.markdown("### Connexion YouTube")
        st.button("Se connecter avec Google", on_click=authenticate_youtube)
    else:
        st.markdown("### Compte YouTube")
        st.success("Connecté")
        st.button("Se déconnecter", on_click=logout)
    
    st.markdown("---")
    
    # Navigation
    st.markdown("### Navigation")
    if st.button("📊 Tableau de bord"):
        st.session_state.current_page = "dashboard"
    if st.button("🔍 Découverte de niches"):
        st.session_state.current_page = "niches"
    if st.button("📝 Génération de contenu"):
        st.session_state.current_page = "content"
    if st.button("🎥 Production vidéo"):
        st.session_state.current_page = "production"
    if st.button("📈 Analyse de performance"):
        st.session_state.current_page = "analytics"
    if st.button("⚙️ Paramètres"):
        st.session_state.current_page = "settings"
    
    st.markdown("---")
    
    # Informations système
    st.markdown("### Informations système")
    st.info(f"Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Pied de page
    st.markdown('<div class="footer">AutoTubeCPM v1.0<br>Powered by Manus AI</div>', unsafe_allow_html=True)

# Contenu principal
if st.session_state.current_page == "dashboard":
    # En-tête
    st.markdown('<div class="main-header">📊 Tableau de bord</div>', unsafe_allow_html=True)
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{performance["views"]["current"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">Vues <span class="trend-{performance["views"]["trend"]}">({performance["views"]["change_pct"]:+.1f}%)</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">${performance["revenue"]["current"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">Revenus <span class="trend-{performance["revenue"]["trend"]}">({performance["revenue"]["change_pct"]:+.1f}%)</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{performance["subscribers"]["current"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">Abonnés <span class="trend-{performance["subscribers"]["trend"]}">({performance["subscribers"]["change_pct"]:+.1f}%)</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">${performance["cpm"]["current"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">CPM moyen <span class="trend-{performance["cpm"]["trend"]}">({performance["cpm"]["change_pct"]:+.1f}%)</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graphiques de performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Vues quotidiennes</div>', unsafe_allow_html=True)
        
        # Créer des dates pour les 14 derniers jours
        dates = [(datetime.now() - timedelta(days=i)).strftime('%d/%m') for i in range(13, 0, -1)]
        
        # Créer un DataFrame pour le graphique
        df_views = pd.DataFrame({
            'Date': dates,
            'Vues': performance['daily_views']
        })
        
        # Créer le graphique avec Plotly
        fig_views = px.line(df_views, x='Date', y='Vues', markers=True)
        fig_views.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="",
            yaxis_title="",
            hovermode="x unified"
        )
        st.plotly_chart(fig_views, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Revenus quotidiens</div>', unsafe_allow_html=True)
        
        # Créer un DataFrame pour le graphique
        df_revenue = pd.DataFrame({
            'Date': dates,
            'Revenus': performance['daily_revenue']
        })
        
        # Créer le graphique avec Plotly
        fig_revenue = px.bar(df_revenue, x='Date', y='Revenus')
        fig_revenue.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="",
            yaxis_title="",
            hovermode="x unified"
        )
        fig_revenue.update_traces(marker_color='#FF0000')
        st.plotly_chart(fig_revenue, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Vidéos récentes et niches à fort CPM
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Vidéos récentes</div>', unsafe_allow_html=True)
        
        # Créer un DataFrame pour les vidéos
        df_videos = pd.DataFrame(videos)
        
        # Filtrer les vidéos téléchargées
        df_uploaded = df_videos[df_videos['status'] == 'uploaded'].sort_values('date', ascending=False)
        
        if not df_uploaded.empty:
            # Afficher le tableau
            st.dataframe(
                df_uploaded[['title', 'date', 'views', 'revenue']],
                column_config={
                    'title': 'Titre',
                    'date': 'Date',
                    'views': 'Vues',
                    'revenue': st.column_config.NumberColumn('Revenus ($)', format="$%.2f")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("Aucune vidéo téléchargée pour le moment.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">CPM par catégorie</div>', unsafe_allow_html=True)
        
        # Créer un DataFrame pour le graphique
        df_cpm = pd.DataFrame({
            'Catégorie': performance['category_cpm']['categories'],
            'CPM': performance['category_cpm']['values']
        })
        
        # Créer le graphique avec Plotly
        fig_cpm = px.bar(df_cpm, x='Catégorie', y='CPM', text_auto='.2f')
        fig_cpm.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="",
            yaxis_title="CPM ($)",
            hovermode="x unified"
        )
        fig_cpm.update_traces(marker_color='#4CAF50', texttemplate='$%{text}', textposition='outside')
        st.plotly_chart(fig_cpm, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Actions rapides
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Actions rapides</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Découvrir des niches", key="quick_niches"):
            st.session_state.current_page = "niches"
    
    with col2:
        if st.button("📝 Générer un script", key="quick_script"):
            st.session_state.current_page = "content"
    
    with col3:
        if st.button("🎥 Produire une vidéo", key="quick_video"):
            st.session_state.current_page = "production"
    
    with col4:
        if st.button("📊 Voir les analyses", key="quick_analytics"):
            st.session_state.current_page = "analytics"
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "niches":
    # En-tête
    st.markdown('<div class="main-header">🔍 Découverte de niches</div>', unsafe_allow_html=True)
    
    # Paramètres de recherche
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Paramètres de recherche</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        region = st.selectbox("Région", ["États-Unis", "Canada", "Royaume-Uni", "Australie", "Global"], index=0)
    
    with col2:
        min_cpm = st.slider("CPM minimum ($)", 5.0, 25.0, 10.0, 0.5)
    
    with col3:
        categories = st.multiselect("Catégories", ["Finance", "Technologie", "Business", "Santé", "Éducation"], default=["Finance", "Technologie", "Business"])
    
    if st.button("Rechercher des niches à fort CPM", key="search_niches"):
        with st.spinner("Recherche des niches en cours..."):
            time.sleep(2)  # Simuler un délai de recherche
            st.success("Recherche terminée ! 5 niches à fort CPM trouvées.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Résultats de la recherche
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Niches à fort CPM</div>', unsafe_allow_html=True)
    
    # Créer un DataFrame pour les niches
    df_niches = pd.DataFrame(niches)
    
    # Afficher le tableau
    st.dataframe(
        df_niches,
        column_config={
            'category': st.column_config.TextColumn('Catégorie'),
            'subcategory': st.column_config.TextColumn('Sous-catégorie'),
            'estimated_cpm': st.column_config.NumberColumn('CPM estimé ($)', format="$%.2f"),
            'trend': st.column_config.TextColumn('Tendance')
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Graphique des CPM par catégorie
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">CPM par catégorie</div>', unsafe_allow_html=True)
    
    # Agréger les données par catégorie
    df_category_cpm = df_niches.groupby('category')['estimated_cpm'].mean().reset_index()
    
    # Créer le graphique avec Plotly
    fig_category_cpm = px.bar(df_category_cpm, x='category', y='estimated_cpm', text_auto='.2f')
    fig_category_cpm.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Catégorie",
        yaxis_title="CPM moyen ($)",
        hovermode="x unified"
    )
    fig_category_cpm.update_traces(marker_color='#4CAF50', texttemplate='$%{text}', textposition='outside')
    st.plotly_chart(fig_category_cpm, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Idées de contenu
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Idées de contenu</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_category = st.selectbox("Catégorie", ["Finance", "Technologie", "Business", "Santé", "Éducation"], key="idea_category")
    
    with col2:
        selected_subcategory = st.selectbox("Sous-catégorie", ["Investissement", "Crypto-monnaie", "IA & Machine Learning", "Gadgets", "Entrepreneuriat"], key="idea_subcategory")
    
    if st.button("Générer des idées de contenu", key="generate_ideas"):
        with st.spinner("Génération d'idées en cours..."):
            time.sleep(2)  # Simuler un délai de génération
            
            # Idées simulées par catégorie
            ideas = {
                "Finance": [
                    "10 Stratégies d'Investissement pour 2025",
                    "Comment Construire un Portefeuille d'Actions Résistant aux Crises",
                    "Guide Complet du Bitcoin pour Débutants",
                    "Les Erreurs à Éviter en Investissement Immobilier",
                    "Comment Économiser $10,000 en Un An"
                ],
                "Technologie": [
                    "Comment l'IA Transforme le Marketing Digital",
                    "Revue Complète des Derniers Smartphones Haut de Gamme",
                    "Guide du Développement Web pour Débutants",
                    "Les Technologies Émergentes qui Vont Changer Notre Futur",
                    "Comment Protéger Votre Vie Privée en Ligne"
                ],
                "Business": [
                    "Les Meilleurs Outils SaaS pour Entrepreneurs",
                    "Comment Lancer une Entreprise avec Moins de $1000",
                    "Stratégies de Marketing Digital pour PME",
                    "Comment Automatiser Votre Business en 2025",
                    "Les Secrets du E-commerce Rentable"
                ]
            }
            
            # Afficher les idées pour la catégorie sélectionnée
            if selected_category in ideas:
                for idea in ideas[selected_category]:
                    st.write(f"• {idea}")
            else:
                st.write("Aucune idée disponible pour cette catégorie.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "content":
    # En-tête
    st.markdown('<div class="main-header">📝 Génération de contenu</div>', unsafe_allow_html=True)
    
    # Paramètres de génération
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Paramètres de génération</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_input("Sujet de la vidéo", "Stratégies d'investissement pour 2025")
        category = st.selectbox("Catégorie", ["Finance", "Technologie", "Business", "Santé", "Éducation"], index=0)
    
    with col2:
        subcategory = st.selectbox("Sous-catégorie", ["Investissement", "Crypto-monnaie", "Bourse", "Épargne", "Immobilier"], index=0)
        target_audience = st.selectbox("Public cible", ["Débutants", "Intermédiaires", "Experts", "Général"], index=0)
    
    if st.button("Générer un script", key="generate_script"):
        with st.spinner("Génération du script en cours..."):
            time.sleep(3)  # Simuler un délai de génération
            st.success("Script généré avec succès !")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Scripts générés
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Scripts générés</div>', unsafe_allow_html=True)
    
    # Créer un DataFrame pour les scripts
    df_scripts = pd.DataFrame(scripts)
    
    # Afficher le tableau
    st.dataframe(
        df_scripts,
        column_config={
            'title': st.column_config.TextColumn('Titre'),
            'category': st.column_config.TextColumn('Catégorie'),
            'subcategory': st.column_config.TextColumn('Sous-catégorie'),
            'date': st.column_config.DateColumn('Date de génération'),
            'status': st.column_config.TextColumn('Statut')
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Aperçu du script
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Aperçu du script</div>', unsafe_allow_html=True)
    
    selected_script = st.selectbox("Sélectionner un script", [script['title'] for script in scripts])
    
    # Contenu simulé du script
    script_content = """
    # 10 Stratégies d'Investissement pour 2025

    ## Introduction
    - Hook: Saviez-vous que 80% des investisseurs manquent des opportunités majeures en 2025 ? Aujourd'hui, je vais vous montrer comment faire partie des 20% qui réussissent.
    - Introduction du sujet: Les stratégies d'investissement ont considérablement évolué ces dernières années. Que vous soyez débutant ou expérimenté, comprendre les nouvelles approches est crucial.
    - Ce que le spectateur va apprendre: Dans cette vidéo, vous découvrirez 10 stratégies d'investissement efficaces pour 2025, les erreurs courantes à éviter, et des conseils pratiques à appliquer immédiatement.

    ## Section 1: Les fondamentaux de l'investissement en 2025
    - Point principal 1: L'importance de la diversification dans un marché volatil
    - Point principal 2: Comment évaluer correctement le rapport risque/rendement
    - Exemple: Un portefeuille diversifié entre actions, obligations et actifs alternatifs a surperformé de 15% les portefeuilles traditionnels en 2024.

    ## Section 2: Stratégies émergentes à fort potentiel
    - Point principal 1: L'investissement thématique ciblant l'IA et les énergies renouvelables
    - Point principal 2: Les opportunités dans les marchés émergents post-pandémie
    - Exemple: Les ETF spécialisés en IA ont généré un rendement moyen de 22% l'année dernière, contre 8% pour les indices généraux.

    ## Section 3: Optimisation fiscale et planification à long terme
    - Point principal 1: Stratégies de réduction d'impôts légales pour investisseurs
    - Point principal 2: L'importance de la planification de retraite dès maintenant
    - Exemple: En utilisant correctement les comptes d'épargne-retraite, un investisseur peut économiser jusqu'à 40% en impôts sur ses gains.

    ## Conclusion
    - Récapitulation: Nous avons couvert 10 stratégies essentielles pour optimiser vos investissements en 2025, de la diversification aux approches thématiques et à la planification fiscale.
    - Appel à l'action: Si vous avez trouvé cette vidéo utile, n'hésitez pas à liker et vous abonner pour plus de contenu sur l'investissement intelligent.
    - Question pour engagement: Quelle stratégie d'investissement vous a donné les meilleurs résultats jusqu'à présent ? Partagez votre expérience dans les commentaires.
    """
    
    st.text_area("Contenu du script", script_content, height=400)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Modifier le script", key="edit_script"):
            st.info("Fonctionnalité de modification en développement.")
    
    with col2:
        if st.button("Générer l'audio", key="generate_audio"):
            with st.spinner("Génération de l'audio en cours..."):
                time.sleep(2)  # Simuler un délai de génération
                st.success("Audio généré avec succès !")
    
    with col3:
        if st.button("Créer une vidéo", key="create_video"):
            st.session_state.current_page = "production"
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "production":
    # En-tête
    st.markdown('<div class="main-header">🎥 Production vidéo</div>', unsafe_allow_html=True)
    
    # Paramètres de production
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Paramètres de production</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_script = st.selectbox("Script", [script['title'] for script in scripts])
        visual_style = st.selectbox("Style visuel", ["Dynamique", "Diaporama d'images", "Vidéo stock"], index=0)
    
    with col2:
        voice = st.selectbox("Voix", ["Homme professionnel", "Femme professionnelle", "Homme décontracté", "Femme décontractée"], index=0)
        resolution = st.selectbox("Résolution", ["1080p (Full HD)", "720p (HD)", "480p (SD)"], index=0)
    
    with col3:
        use_intro = st.checkbox("Utiliser une intro", value=True)
        use_outro = st.checkbox("Utiliser une outro", value=True)
        add_captions = st.checkbox("Ajouter des sous-titres", value=True)
    
    if st.button("Produire la vidéo", key="produce_video"):
        with st.spinner("Production de la vidéo en cours..."):
            time.sleep(4)  # Simuler un délai de production
            st.success("Vidéo produite avec succès !")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Vidéos produites
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Vidéos produites</div>', unsafe_allow_html=True)
    
    # Créer un DataFrame pour les vidéos
    df_videos = pd.DataFrame(videos)
    
    # Afficher le tableau
    st.dataframe(
        df_videos,
        column_config={
            'title': st.column_config.TextColumn('Titre'),
            'duration': st.column_config.TextColumn('Durée'),
            'date': st.column_config.DateColumn('Date de production'),
            'status': st.column_config.TextColumn('Statut'),
            'views': st.column_config.NumberColumn('Vues'),
            'revenue': st.column_config.NumberColumn('Revenus ($)', format="$%.2f")
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Aperçu et téléchargement
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Aperçu et téléchargement</div>', unsafe_allow_html=True)
    
    selected_video = st.selectbox("Sélectionner une vidéo", [video['title'] for video in videos])
    
    # Simuler un aperçu vidéo
    st.image("https://via.placeholder.com/800x450.png?text=Aperçu+Vidéo", use_column_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Télécharger sur YouTube", key="upload_youtube"):
            if st.session_state.authenticated:
                with st.spinner("Téléchargement sur YouTube en cours..."):
                    time.sleep(3)  # Simuler un délai de téléchargement
                    st.success("Vidéo téléchargée avec succès sur YouTube !")
            else:
                st.warning("Veuillez vous connecter à YouTube pour télécharger la vidéo.")
    
    with col2:
        if st.button("Télécharger la vidéo", key="download_video"):
            st.info("Téléchargement de la vidéo...")
    
    with col3:
        if st.button("Modifier les métadonnées", key="edit_metadata"):
            st.info("Fonctionnalité de modification des métadonnées en développement.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "analytics":
    # En-tête
    st.markdown('<div class="main-header">📈 Analyse de performance</div>', unsafe_allow_html=True)
    
    # Paramètres d'analyse
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Paramètres d'analyse</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        period = st.selectbox("Période", ["7 derniers jours", "30 derniers jours", "3 derniers mois", "Année en cours"], index=1)
    
    with col2:
        metrics = st.multiselect("Métriques", ["Vues", "Revenus", "CPM", "Abonnés", "Temps de visionnage", "Taux d'engagement"], 
                                default=["Vues", "Revenus", "CPM"])
    
    with col3:
        comparison = st.checkbox("Comparer avec la période précédente", value=True)
    
    if st.button("Générer le rapport", key="generate_report"):
        with st.spinner("Génération du rapport en cours..."):
            time.sleep(2)  # Simuler un délai de génération
            st.success("Rapport généré avec succès !")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Métriques de performance
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Métriques de performance</div>', unsafe_allow_html=True)
    
    # Créer des dates pour les 30 derniers jours
    dates = [(datetime.now() - timedelta(days=i)).strftime('%d/%m') for i in range(30, 0, -1)]
    
    # Simuler des données de performance
    np.random.seed(42)
    views = np.cumsum(np.random.randint(50, 200, size=30))
    revenue = np.cumsum(np.random.uniform(0.5, 3.0, size=30))
    cpm = 15 + np.random.normal(0, 1, size=30)
    
    # Créer un DataFrame pour le graphique
    df_performance = pd.DataFrame({
        'Date': dates,
        'Vues': views,
        'Revenus': revenue,
        'CPM': cpm
    })
    
    # Créer des onglets pour les différentes métriques
    tab1, tab2, tab3 = st.tabs(["Vues", "Revenus", "CPM"])
    
    with tab1:
        fig_views = px.line(df_performance, x='Date', y='Vues', markers=True)
        fig_views.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="",
            yaxis_title="Vues",
            hovermode="x unified"
        )
        st.plotly_chart(fig_views, use_container_width=True)
    
    with tab2:
        fig_revenue = px.line(df_performance, x='Date', y='Revenus', markers=True)
        fig_revenue.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="",
            yaxis_title="Revenus ($)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with tab3:
        fig_cpm = px.line(df_performance, x='Date', y='CPM', markers=True)
        fig_cpm.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="",
            yaxis_title="CPM ($)",
            hovermode="x unified"
        )
        st.plotly_chart(fig_cpm, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Performance par vidéo
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Performance par vidéo</div>', unsafe_allow_html=True)
    
    # Filtrer les vidéos téléchargées
    uploaded_videos = [v for v in videos if v['status'] == 'uploaded']
    
    if uploaded_videos:
        # Créer un DataFrame pour les vidéos
        df_uploaded = pd.DataFrame(uploaded_videos)
        
        # Créer un graphique à barres pour les vues
        fig_video_views = px.bar(df_uploaded, x='title', y='views', text_auto=True)
        fig_video_views.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="",
            yaxis_title="Vues",
            hovermode="x unified"
        )
        st.plotly_chart(fig_video_views, use_container_width=True)
        
        # Créer un graphique à barres pour les revenus
        fig_video_revenue = px.bar(df_uploaded, x='title', y='revenue', text_auto='.2f')
        fig_video_revenue.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="",
            yaxis_title="Revenus ($)",
            hovermode="x unified"
        )
        fig_video_revenue.update_traces(marker_color='#FF0000', texttemplate='$%{text}', textposition='outside')
        st.plotly_chart(fig_video_revenue, use_container_width=True)
    else:
        st.info("Aucune vidéo téléchargée pour le moment.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Analyse des tendances
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Analyse des tendances</div>', unsafe_allow_html=True)
    
    # Simuler des données de tendances
    trend_data = {
        'Catégorie': ['Finance', 'Technologie', 'Business', 'Santé', 'Éducation'],
        'CPM Actuel': [18.5, 15.0, 14.5, 11.0, 10.0],
        'CPM Précédent': [17.0, 14.2, 14.0, 10.5, 9.8],
        'Variation (%)': [8.8, 5.6, 3.6, 4.8, 2.0]
    }
    
    df_trends = pd.DataFrame(trend_data)
    
    # Créer un graphique de comparaison
    fig_trends = go.Figure()
    
    fig_trends.add_trace(go.Bar(
        x=df_trends['Catégorie'],
        y=df_trends['CPM Actuel'],
        name='CPM Actuel',
        marker_color='#4CAF50'
    ))
    
    fig_trends.add_trace(go.Bar(
        x=df_trends['Catégorie'],
        y=df_trends['CPM Précédent'],
        name='CPM Précédent',
        marker_color='#2196F3'
    ))
    
    fig_trends.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="",
        yaxis_title="CPM ($)",
        hovermode="x unified",
        barmode='group'
    )
    
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # Afficher le tableau de variation
    st.dataframe(
        df_trends,
        column_config={
            'Catégorie': st.column_config.TextColumn('Catégorie'),
            'CPM Actuel': st.column_config.NumberColumn('CPM Actuel ($)', format="$%.2f"),
            'CPM Précédent': st.column_config.NumberColumn('CPM Précédent ($)', format="$%.2f"),
            'Variation (%)': st.column_config.NumberColumn('Variation (%)', format="%.1f%%")
        },
        hide_index=True,
        use_container_width=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.current_page == "settings":
    # En-tête
    st.markdown('<div class="main-header">⚙️ Paramètres</div>', unsafe_allow_html=True)
    
    # Paramètres du compte
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Paramètres du compte</div>', unsafe_allow_html=True)
    
    if st.session_state.authenticated:
        st.success("Connecté à YouTube")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Nom de la chaîne", "Ma Chaîne AutoTubeCPM", disabled=True)
        
        with col2:
            st.text_input("ID de la chaîne", "UC1234567890abcdef", disabled=True)
        
        if st.button("Déconnecter le compte", key="disconnect_account"):
            st.session_state.authenticated = False
            st.session_state.youtube_auth = None
            st.success("Déconnexion réussie !")
            st.rerun()
    else:
        st.warning("Non connecté à YouTube")
        
        if st.button("Se connecter avec Google", key="connect_account"):
            authenticate_youtube()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Paramètres de génération de contenu
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Paramètres de génération de contenu</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox("Modèle de génération de script", ["Manus AI Standard", "Manus AI Premium", "Manus AI Pro"], index=0)
        st.selectbox("Moteur TTS", ["Kokoro TTS", "Tortoise TTS", "Coqui TTS"], index=0)
    
    with col2:
        st.selectbox("Source des visuels", ["Pexels API", "Stable Diffusion", "Mixte"], index=0)
        st.selectbox("Qualité vidéo par défaut", ["1080p (Full HD)", "720p (HD)", "480p (SD)"], index=0)
    
    st.slider("Longueur de script cible (minutes)", 5, 30, 10)
    
    if st.button("Enregistrer les paramètres", key="save_content_settings"):
        st.success("Paramètres de génération de contenu enregistrés !")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Paramètres de téléchargement
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Paramètres de téléchargement</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Téléchargement automatique", value=False)
        st.checkbox("Notification par email après téléchargement", value=True)
    
    with col2:
        st.selectbox("Visibilité par défaut", ["Public", "Non répertorié", "Privé"], index=0)
        st.checkbox("Activer les commentaires", value=True)
    
    st.text_area("Texte de description par défaut", "N'oubliez pas de liker et de vous abonner pour plus de contenu !\n\nSuivez-nous sur les réseaux sociaux :\nTwitter: @AutoTubeCPM\nInstagram: @AutoTubeCPM")
    
    if st.button("Enregistrer les paramètres", key="save_upload_settings"):
        st.success("Paramètres de téléchargement enregistrés !")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Paramètres système
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Paramètres système</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox("Thème", ["Clair", "Sombre", "Système"], index=0)
        st.selectbox("Langue", ["Français", "English", "Español", "Deutsch"], index=0)
    
    with col2:
        st.checkbox("Activer les notifications", value=True)
        st.checkbox("Mode développeur", value=False)
    
    if st.button("Réinitialiser tous les paramètres", key="reset_settings"):
        st.warning("Êtes-vous sûr de vouloir réinitialiser tous les paramètres ?")
        if st.button("Confirmer la réinitialisation", key="confirm_reset"):
            st.success("Tous les paramètres ont été réinitialisés !")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # À propos
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">À propos</div>', unsafe_allow_html=True)
    
    st.markdown("""
    **AutoTubeCPM v1.0**
    
    Un système automatisé de création de contenu YouTube optimisé pour le CPM, propulsé par Manus AI.
    
    © 2025 AutoTubeCPM - Tous droits réservés
    
    [Documentation](https://github.com/username/AutoTubeCPM) | [Signaler un bug](https://github.com/username/AutoTubeCPM/issues)
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
