# Guide d'installation et d'utilisation d'AutoTubeCPM

Ce guide vous explique en détail comment installer, configurer et utiliser AutoTubeCPM pour créer une chaîne YouTube automatisée et rentable.

## Table des matières

1. [Installation](#installation)
   - [Prérequis](#prérequis)
   - [Installation locale](#installation-locale)
   - [Installation sur Google Colab](#installation-sur-google-colab)
2. [Configuration](#configuration)
   - [Configuration des API](#configuration-des-api)
   - [Configuration de l'authentification YouTube](#configuration-de-lauthentification-youtube)
3. [Utilisation](#utilisation)
   - [Découverte de niches](#découverte-de-niches)
   - [Génération de contenu](#génération-de-contenu)
   - [Production vidéo](#production-vidéo)
   - [Publication YouTube](#publication-youtube)
   - [Analyse de performance](#analyse-de-performance)
4. [Dépannage](#dépannage)
   - [Problèmes courants](#problèmes-courants)
   - [FAQ](#faq)

## Installation

### Prérequis

Avant d'installer AutoTubeCPM, assurez-vous d'avoir :

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git
- Un compte Google avec accès à l'API YouTube
- Un compte Pexels pour l'API (gratuit)
- Espace disque suffisant pour stocker les ressources audio et vidéo

### Installation locale

1. **Cloner le dépôt GitHub**

```bash
git clone https://github.com/username/AutoTubeCPM.git
cd AutoTubeCPM
```

2. **Créer un environnement virtuel (recommandé)**

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

4. **Lancer l'application Streamlit**

```bash
cd ui
streamlit run login.py
```

L'application sera accessible à l'adresse http://localhost:8501

### Installation sur Google Colab

1. Accédez à [Google Colab](https://colab.research.google.com/)
2. Ouvrez le notebook `notebooks/setup_colab.ipynb` depuis GitHub ou téléchargez-le et importez-le dans Colab
3. Exécutez toutes les cellules du notebook pour configurer l'environnement
4. Suivez les instructions pour lancer l'interface Streamlit via un tunnel ngrok

## Configuration

### Configuration des API

#### YouTube Data API

1. Accédez à la [Console Google Cloud](https://console.cloud.google.com/)
2. Créez un nouveau projet ou sélectionnez un projet existant
3. Activez l'API YouTube Data v3
4. Créez des identifiants OAuth 2.0 pour une application de bureau
5. Téléchargez le fichier JSON des identifiants

#### Pexels API

1. Créez un compte sur [Pexels](https://www.pexels.com/)
2. Accédez à [Pexels API](https://www.pexels.com/api/) et demandez une clé API
3. Copiez votre clé API

### Configuration de l'authentification YouTube

1. Lancez l'application AutoTubeCPM
2. Accédez à la page Paramètres
3. Cliquez sur "Se connecter avec Google"
4. Suivez les instructions pour autoriser l'application à accéder à votre chaîne YouTube
5. Une fois connecté, vous pourrez gérer votre chaîne directement depuis l'interface

## Utilisation

### Découverte de niches

1. Dans le menu de navigation, cliquez sur "Découverte de niches"
2. Configurez les paramètres de recherche :
   - Région (États-Unis, Canada, Royaume-Uni, Australie, Global)
   - CPM minimum ($)
   - Catégories (Finance, Technologie, Business, Santé, Éducation)
3. Cliquez sur "Rechercher des niches à fort CPM"
4. Explorez les résultats et les idées de contenu générées pour chaque niche
5. Sélectionnez une niche pour la génération de contenu

### Génération de contenu

1. Dans le menu de navigation, cliquez sur "Génération de contenu"
2. Configurez les paramètres de génération :
   - Sujet de la vidéo
   - Catégorie et sous-catégorie
   - Public cible
3. Cliquez sur "Générer un script"
4. Examinez le script généré et modifiez-le si nécessaire
5. Cliquez sur "Générer l'audio" pour créer la voix off

### Production vidéo

1. Dans le menu de navigation, cliquez sur "Production vidéo"
2. Configurez les paramètres de production :
   - Script sélectionné
   - Style visuel (Dynamique, Diaporama d'images, Vidéo stock)
   - Voix (Homme professionnel, Femme professionnelle, etc.)
   - Résolution (1080p, 720p, 480p)
   - Options supplémentaires (intro, outro, sous-titres)
3. Cliquez sur "Produire la vidéo"
4. Prévisualisez la vidéo générée

### Publication YouTube

1. Dans le menu de navigation, cliquez sur "Production vidéo"
2. Sélectionnez une vidéo produite
3. Cliquez sur "Télécharger sur YouTube"
4. Vérifiez et ajustez les métadonnées si nécessaire :
   - Titre
   - Description
   - Tags
   - Miniature
   - Paramètres de visibilité et de monétisation
5. Confirmez le téléchargement

### Analyse de performance

1. Dans le menu de navigation, cliquez sur "Analyse de performance"
2. Configurez les paramètres d'analyse :
   - Période (7 derniers jours, 30 derniers jours, etc.)
   - Métriques (Vues, Revenus, CPM, Abonnés, etc.)
   - Options de comparaison
3. Explorez les graphiques et tableaux de performance
4. Utilisez ces données pour optimiser votre stratégie de contenu

## Dépannage

### Problèmes courants

#### Erreur d'authentification YouTube

Si vous rencontrez des problèmes lors de la connexion à YouTube :
1. Vérifiez que l'API YouTube Data v3 est bien activée dans votre projet Google Cloud
2. Assurez-vous que les identifiants OAuth sont correctement configurés
3. Essayez de vous déconnecter et de vous reconnecter

#### Erreur de génération de vidéo

Si la génération de vidéo échoue :
1. Vérifiez que toutes les dépendances sont correctement installées
2. Assurez-vous que le script et l'audio ont été générés correctement
3. Vérifiez l'espace disque disponible

#### Erreur de téléchargement YouTube

Si le téléchargement sur YouTube échoue :
1. Vérifiez votre connexion internet
2. Assurez-vous que votre compte YouTube est en règle
3. Vérifiez les quotas de l'API YouTube

### FAQ

**Q: Combien de vidéos puis-je générer par jour ?**

R: Le système peut théoriquement générer un nombre illimité de vidéos, mais vous êtes limité par les quotas de l'API YouTube (généralement 6 téléchargements par jour pour un compte standard).

**Q: Comment puis-je améliorer la qualité des voix off ?**

R: Vous pouvez ajuster les paramètres du moteur TTS dans les fichiers de configuration ou utiliser un service TTS externe de meilleure qualité.

**Q: Puis-je personnaliser les templates visuels ?**

R: Oui, vous pouvez ajouter vos propres templates dans le dossier `assets/templates` et les référencer dans l'interface.

**Q: Comment puis-je cibler des niches spécifiques ?**

R: Dans la section "Découverte de niches", vous pouvez filtrer par catégorie et définir un CPM minimum pour cibler des niches spécifiques.

**Q: Le système fonctionne-t-il avec d'autres plateformes que YouTube ?**

R: Actuellement, le système est optimisé pour YouTube, mais des modules pour d'autres plateformes comme TikTok et Instagram peuvent être ajoutés à l'avenir.
