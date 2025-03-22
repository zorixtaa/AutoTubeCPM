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

# Configuration de la page Streamlit
st.set_page_config(
    page_title="AutoTubeCPM - Connexion",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF0000;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #333;
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: white;
    }
    .login-button {
        background-color: #FF0000;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        width: 100%;
        margin-top: 1rem;
    }
    .login-button:hover {
        background-color: #CC0000;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #666;
        font-size: 0.8rem;
    }
    .features-container {
        margin-top: 3rem;
        padding: 2rem;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: white;
        margin-bottom: 1rem;
        text-align: center;
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour initialiser les variables de session
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

# Initialiser les variables de session
init_session_state()

# Fonction pour simuler la connexion
def login():
    st.session_state.logged_in = True
    # Rediriger vers l'application principale
    st.switch_page("app.py")

# Si l'utilisateur est déjà connecté, rediriger vers l'application principale
if st.session_state.logged_in:
    st.switch_page("app.py")

# Page de connexion
st.markdown('<div class="main-header">AutoTubeCPM</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">La machine à contenu YouTube qui chasse le CPM pour vous</div>', unsafe_allow_html=True)

# Conteneur de connexion
st.markdown('<div class="login-container">', unsafe_allow_html=True)
st.markdown("### Connexion")

email = st.text_input("Email")
password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter", key="login"):
    if email and password:  # Vérification simple que les champs ne sont pas vides
        with st.spinner("Connexion en cours..."):
            time.sleep(1)  # Simuler un délai de connexion
            login()
    else:
        st.error("Veuillez remplir tous les champs")

st.markdown("ou")

if st.button("Se connecter avec Google", key="google_login"):
    with st.spinner("Connexion avec Google en cours..."):
        time.sleep(1)  # Simuler un délai de connexion
        login()

st.markdown("Pas encore de compte ? [S'inscrire](https://example.com)")
st.markdown('</div>', unsafe_allow_html=True)

# Présentation des fonctionnalités
st.markdown('<div class="features-container">', unsafe_allow_html=True)
st.markdown("## Fonctionnalités principales")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">🔍</div>', unsafe_allow_html=True)
    st.markdown("### Découverte de niches")
    st.markdown("Identifiez automatiquement les niches à fort CPM grâce à notre analyse de données en temps réel.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">📝</div>', unsafe_allow_html=True)
    st.markdown("### Génération de contenu")
    st.markdown("Créez des scripts optimisés pour YouTube avec Manus AI et convertissez-les en voix off naturelles.")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">🎥</div>', unsafe_allow_html=True)
    st.markdown("### Production vidéo")
    st.markdown("Assemblez automatiquement des vidéos professionnelles avec animations, transitions et sous-titres.")
    st.markdown('</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">📤</div>', unsafe_allow_html=True)
    st.markdown("### Publication YouTube")
    st.markdown("Téléchargez vos vidéos sur YouTube avec des métadonnées optimisées pour la monétisation.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">📊</div>', unsafe_allow_html=True)
    st.markdown("### Analyse de performance")
    st.markdown("Suivez vos performances et optimisez votre stratégie grâce à des rapports détaillés.")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.markdown('<div class="feature-icon">⚙️</div>', unsafe_allow_html=True)
    st.markdown("### Automatisation complète")
    st.markdown("Programmez la création et la publication de contenu pour une chaîne YouTube entièrement automatisée.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Pied de page
st.markdown('<div class="footer">AutoTubeCPM v1.0<br>© 2025 - Tous droits réservés<br>Propulsé par Manus AI</div>', unsafe_allow_html=True)
