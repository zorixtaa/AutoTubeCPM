# AutoTubeCPM - La machine à contenu YouTube qui chasse le CPM pour vous

![AutoTubeCPM Logo](assets/logo.png)

## 🚀 Vue d'ensemble

AutoTubeCPM est un système entièrement automatisé de création et de publication de contenu YouTube optimisé pour le CPM (coût par mille impressions). Cette solution open-source vous permet de générer des vidéos de haute qualité ciblant des niches rentables, avec un minimum d'intervention humaine.

Le système identifie automatiquement les niches à fort CPM, génère des scripts optimisés, crée des voix off naturelles, assemble des vidéos professionnelles, et les publie sur YouTube avec des métadonnées optimisées pour la monétisation.

## ✨ Fonctionnalités principales

- **🔍 Découverte de niches rentables** : Identifie automatiquement les niches à fort CPM via des API comme Google Trends et des analyses de données en temps réel.
- **📝 Génération de contenu** : Crée des scripts optimisés pour YouTube avec Manus AI, garantissant un contenu engageant et adapté aux annonceurs.
- **🗣️ Synthèse vocale naturelle** : Convertit les scripts en voix off émotionnelles et naturelles grâce à Kokoro TTS ou Tortoise TTS.
- **🎬 Production vidéo automatisée** : Assemble des vidéos professionnelles avec des visuels générés par IA, des animations dynamiques et des transitions.
- **📤 Publication YouTube** : Télécharge automatiquement les vidéos sur YouTube avec des titres, tags, descriptions et paramètres de monétisation optimisés.
- **📊 Tableau de bord analytique** : Surveille les performances, suit les métriques clés et optimise votre stratégie de contenu.
- **🔐 Authentification sécurisée** : Connectez votre chaîne YouTube de manière sécurisée via OAuth2 directement depuis l'interface.

## 🛠️ Architecture du système

AutoTubeCPM est construit avec une architecture modulaire qui permet une grande flexibilité et extensibilité :

```
AutoTubeCPM/
├── data/               # Données (mots-clés, audio, vidéo)
├── scripts/            # Code Python backend
│   ├── niche_discovery/    # Module de découverte de niches
│   ├── content_generation/ # Module de génération de contenu
│   ├── tts/               # Module de synthèse vocale
│   ├── video_production/  # Module d'assemblage vidéo
│   ├── youtube_publishing/ # Module de publication YouTube
│   └── analytics/         # Module d'analyse de performance
├── models/             # Configurations des modèles
├── ui/                 # Interface Streamlit
├── notebooks/          # Notebooks compatibles avec Google Colab
├── assets/             # Ressources (templates, intro/outro)
├── tests/              # Tests unitaires et d'intégration
└── docs/               # Documentation
```

## 📋 Prérequis

- Python 3.8+
- Compte Google avec accès à l'API YouTube
- Accès à l'API Pexels (gratuit) ou Stable Diffusion local
- Espace de stockage pour les ressources audio et vidéo

## 🚀 Installation

### Option 1 : Installation locale

```bash
# Cloner le dépôt
git clone https://github.com/username/AutoTubeCPM.git
cd AutoTubeCPM

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application Streamlit
cd ui
streamlit run login.py
```

### Option 2 : Google Colab (sans installation locale)

1. Ouvrez le notebook `notebooks/setup_colab.ipynb` dans Google Colab
2. Exécutez toutes les cellules pour configurer l'environnement
3. Suivez les instructions pour lancer l'interface Streamlit

## 🔧 Configuration

1. Créez un projet dans la [Console Google Cloud](https://console.cloud.google.com/)
2. Activez l'API YouTube Data v3
3. Créez des identifiants OAuth 2.0
4. Configurez les identifiants dans l'interface AutoTubeCPM

## 💻 Utilisation

### 1. Découverte de niches

- Lancez une recherche de niches à fort CPM
- Filtrez par région, CPM minimum et catégories
- Explorez les idées de contenu générées pour chaque niche

### 2. Génération de contenu

- Sélectionnez une niche et un sujet
- Générez un script optimisé pour YouTube
- Personnalisez le script selon vos besoins

### 3. Production vidéo

- Convertissez le script en voix off naturelle
- Sélectionnez un style visuel et des paramètres de production
- Générez une vidéo professionnelle automatiquement

### 4. Publication YouTube

- Connectez votre chaîne YouTube de manière sécurisée
- Téléchargez la vidéo avec des métadonnées optimisées
- Planifiez des publications futures

### 5. Analyse de performance

- Suivez les performances de vos vidéos
- Analysez les métriques clés (vues, revenus, CPM)
- Optimisez votre stratégie de contenu

## 🌟 Fonctionnalités avancées

- **Planification automatique** : Programmez la création et la publication de contenu à l'avance
- **Génération de vignettes** : Créez des vignettes attrayantes avec DALL·E ou SDXL
- **Intégration multi-plateforme** : Publiez automatiquement sur Instagram et TikTok
- **Mode SaaS** : Support multi-utilisateurs pour les agences et équipes

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment vous pouvez contribuer :

1. Forkez le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add some amazing feature'`)
4. Poussez vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [Manus AI](https://manus.ai/) pour la génération de contenu
- [Kokoro TTS](https://github.com/koeai/kokoro-tts) et [Tortoise TTS](https://github.com/neonbjb/tortoise-tts) pour la synthèse vocale
- [MoviePy](https://zulko.github.io/moviepy/) pour l'édition vidéo
- [Pexels](https://www.pexels.com/) pour les ressources visuelles
- [Streamlit](https://streamlit.io/) pour l'interface utilisateur

---

Créé avec ❤️ par [Votre Nom]

*AutoTubeCPM - "La machine à contenu YouTube qui chasse le CPM pour vous."*
