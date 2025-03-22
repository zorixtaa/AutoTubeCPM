# Flux de travail du système AutoTubeCPM

Ce document décrit le flux de travail détaillé du système AutoTubeCPM, de la découverte des niches à l'analyse des performances.

## 1. Découverte et sélection de niches

```mermaid
flowchart TD
    A[Début] --> B[Collecte des données de tendances]
    B --> C[Analyse des CPM par niche]
    C --> D[Classement des niches]
    D --> E{Sélection automatique?}
    E -- Oui --> F[Sélection de la niche la plus rentable]
    E -- Non --> G[Interface utilisateur pour sélection]
    F --> H[Génération de sujets dans la niche]
    G --> H
    H --> I[Sélection du sujet final]
    I --> J[Fin de la phase de découverte]
```

## 2. Génération de contenu

```mermaid
flowchart TD
    A[Début] --> B[Récupération du sujet et de la niche]
    B --> C[Préparation du prompt pour Manus AI]
    C --> D[Génération du script brut]
    D --> E[Optimisation SEO]
    E --> F[Vérification de la qualité du contenu]
    F --> G{Contenu approuvé?}
    G -- Non --> H[Ajustement des paramètres]
    H --> C
    G -- Oui --> I[Génération des métadonnées]
    I --> J[Stockage du script et métadonnées]
    J --> K[Fin de la phase de génération]
```

## 3. Synthèse vocale

```mermaid
flowchart TD
    A[Début] --> B[Récupération du script]
    B --> C[Sélection de la voix]
    C --> D[Préparation du texte pour TTS]
    D --> E[Génération audio avec Kokoro TTS]
    E --> F[Post-traitement audio]
    F --> G{Qualité acceptable?}
    G -- Non --> H[Ajustement des paramètres]
    H --> E
    G -- Oui --> I[Stockage du fichier audio]
    I --> J[Fin de la phase de synthèse vocale]
```

## 4. Production vidéo

```mermaid
flowchart TD
    A[Début] --> B[Récupération du fichier audio]
    B --> C[Analyse du script pour visuels]
    C --> D{Source des visuels?}
    D -- Pexels API --> E[Recherche de vidéos stock]
    D -- Stable Diffusion --> F[Génération d'images AI]
    E --> G[Sélection des segments vidéo]
    F --> G
    G --> H[Synchronisation audio/vidéo]
    H --> I[Ajout de sous-titres]
    I --> J[Ajout d'animations et transitions]
    J --> K[Ajout d'intro/outro]
    K --> L[Rendu final de la vidéo]
    L --> M[Fin de la phase de production]
```

## 5. Publication YouTube

```mermaid
flowchart TD
    A[Début] --> B[Récupération de la vidéo et métadonnées]
    B --> C[Génération de la miniature]
    C --> D[Authentification YouTube]
    D --> E[Préparation du téléchargement]
    E --> F[Téléchargement de la vidéo]
    F --> G{Téléchargement réussi?}
    G -- Non --> H[Gestion des erreurs]
    H --> E
    G -- Oui --> I[Configuration des paramètres de monétisation]
    I --> J{Publication immédiate?}
    J -- Oui --> K[Publication de la vidéo]
    J -- Non --> L[Planification de la publication]
    K --> M[Fin de la phase de publication]
    L --> M
```

## 6. Analyse et suivi

```mermaid
flowchart TD
    A[Début] --> B[Attente après publication]
    B --> C[Collecte des données initiales]
    C --> D[Suivi périodique des performances]
    D --> E[Analyse des métriques]
    E --> F[Génération de rapports]
    F --> G[Mise à jour de la base de données de niches]
    G --> H[Recommandations pour futures vidéos]
    H --> I[Fin de la phase d'analyse]
```

## 7. Flux de travail complet

```mermaid
flowchart TD
    A[Début du processus] --> B[Découverte de niches]
    B --> C[Génération de contenu]
    C --> D[Synthèse vocale]
    D --> E[Production vidéo]
    E --> F[Publication YouTube]
    F --> G[Analyse et suivi]
    G --> H{Continuer le cycle?}
    H -- Oui --> B
    H -- Non --> I[Fin du processus]
```

Ce flux de travail est conçu pour être automatisé tout en permettant des interventions humaines aux points de décision critiques via l'interface utilisateur Streamlit.
