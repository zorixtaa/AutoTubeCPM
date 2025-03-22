# Architecture du système AutoTubeCPM

## 1. Vue d'ensemble de l'architecture

AutoTubeCPM est conçu comme un système modulaire avec une architecture en couches qui permet une séparation claire des responsabilités et facilite la maintenance et l'extension. Le système suit un flux de travail linéaire avec des points de décision et de validation.

```
┌─────────────────────────────────────────────────────────────────┐
│                     Interface Utilisateur                        │
│                     (Tableau de bord Streamlit)                  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Orchestrateur Principal                      │
└───────┬───────────────┬───────────────┬───────────────┬─────────┘
        │               │               │               │
        ▼               ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│  Module de    │ │  Module de    │ │  Module de    │ │  Module de    │
│ Découverte de │ │ Génération de │ │   Synthèse    │ │  Production   │
│    Niches     │ │   Contenu     │ │    Vocale     │ │    Vidéo      │
└───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘
                                                              │
                                                              ▼
                                                     ┌───────────────┐
                                                     │  Module de    │
                                                     │ Publication   │
                                                     │   YouTube     │
                                                     └───────────────┘
                                                              │
                                                              ▼
                                                     ┌───────────────┐
                                                     │  Module       │
                                                     │ d'Analyse et  │
                                                     │   Suivi       │
                                                     └───────────────┘
```

## 2. Description des composants

### 2.1 Interface Utilisateur (Streamlit)
- **Responsabilités**:
  - Fournir un tableau de bord pour la configuration et le suivi
  - Visualiser les données de performance et les métriques CPM
  - Permettre la révision et l'approbation des contenus générés
  - Gérer la planification des publications
- **Interactions**:
  - Communique avec l'orchestrateur principal
  - Affiche les résultats de tous les modules

### 2.2 Orchestrateur Principal
- **Responsabilités**:
  - Coordonner le flux de travail entre les modules
  - Gérer les files d'attente de tâches
  - Assurer la persistance des données entre les étapes
  - Gérer les erreurs et les retries
- **Interactions**:
  - Reçoit les commandes de l'interface utilisateur
  - Distribue les tâches aux modules spécialisés
  - Collecte et agrège les résultats

### 2.3 Module de Découverte de Niches
- **Responsabilités**:
  - Analyser les tendances via Google Trends et autres API
  - Évaluer les CPM potentiels par niche
  - Classer les niches par rentabilité
  - Suggérer des sujets spécifiques dans les niches sélectionnées
- **Composants internes**:
  - Collecteur de données de tendances
  - Analyseur de CPM
  - Générateur de sujets
  - Base de données de niches

### 2.4 Module de Génération de Contenu
- **Responsabilités**:
  - Générer des scripts vidéo via Manus AI
  - Créer des titres, descriptions et tags optimisés pour YouTube
  - Assurer la qualité et la pertinence du contenu
- **Composants internes**:
  - Intégration Manus AI
  - Optimiseur SEO
  - Vérificateur de qualité de contenu
  - Bibliothèque de templates par niche

### 2.5 Module de Synthèse Vocale
- **Responsabilités**:
  - Convertir les scripts en voix off naturelles
  - Gérer différentes voix et styles
  - Optimiser la prosodie et l'intonation
- **Composants internes**:
  - Intégration Kokoro TTS
  - Processeur audio
  - Bibliothèque de voix
  - Optimiseur de prononciation

### 2.6 Module de Production Vidéo
- **Responsabilités**:
  - Sélectionner/générer les éléments visuels
  - Synchroniser audio et vidéo
  - Ajouter animations, transitions, sous-titres
  - Compiler la vidéo finale
- **Composants internes**:
  - Intégration Pexels API
  - Intégration Stable Diffusion
  - Moteur MoviePy/FFmpeg
  - Générateur de sous-titres
  - Bibliothèque d'éléments visuels

### 2.7 Module de Publication YouTube
- **Responsabilités**:
  - Télécharger les vidéos sur YouTube
  - Configurer les métadonnées et paramètres de monétisation
  - Gérer la planification des publications
- **Composants internes**:
  - Intégration YouTube Data API
  - Gestionnaire d'authentification
  - Planificateur de publications
  - Générateur de miniatures

### 2.8 Module d'Analyse et Suivi
- **Responsabilités**:
  - Collecter les données de performance
  - Analyser les métriques (vues, engagement, CPM)
  - Générer des rapports
  - Alimenter la boucle de rétroaction
- **Composants internes**:
  - Intégration YouTube Analytics API
  - Moteur d'analyse de données
  - Générateur de rapports
  - Système de recommandations

## 3. Flux de données et processus

### 3.1 Flux de travail principal
1. **Découverte de niches**:
   - Entrée: Paramètres de recherche (catégories, régions)
   - Sortie: Liste de niches classées par CPM potentiel

2. **Sélection de niche et sujet**:
   - Entrée: Niche sélectionnée (automatiquement ou par l'utilisateur)
   - Sortie: Sujet spécifique pour la vidéo

3. **Génération de contenu**:
   - Entrée: Sujet, niche, paramètres de style
   - Sortie: Script vidéo, titre, description, tags

4. **Synthèse vocale**:
   - Entrée: Script vidéo, paramètres de voix
   - Sortie: Fichier audio de voix off

5. **Production vidéo**:
   - Entrée: Fichier audio, style visuel, paramètres
   - Sortie: Vidéo complète avec audio, visuels, animations

6. **Publication YouTube**:
   - Entrée: Vidéo, métadonnées, paramètres de publication
   - Sortie: Vidéo publiée sur YouTube (ou planifiée)

7. **Analyse et suivi**:
   - Entrée: ID de vidéo publiée, période d'analyse
   - Sortie: Métriques de performance, recommandations

### 3.2 Boucles de rétroaction
- Les performances des vidéos publiées alimentent le module de découverte de niches
- Les tendances d'engagement influencent la génération de contenu
- Les métriques de monétisation affinent les critères de sélection de niches

## 4. Stockage et gestion des données

### 4.1 Structure de données
- **Base de données de niches**:
  - Catégories, sous-catégories
  - Historique des CPM
  - Tendances temporelles

- **Bibliothèque de contenu**:
  - Scripts générés
  - Fichiers audio
  - Éléments visuels
  - Vidéos finales

- **Données de performance**:
  - Métriques par vidéo
  - Métriques agrégées par niche
  - Historique des revenus

### 4.2 Persistance
- Stockage local pour le développement
- Intégration avec Google Drive via Colab pour la production
- Système de cache pour optimiser les performances

## 5. Intégration avec Google Colab

### 5.1 Architecture d'exécution
- Notebooks modulaires correspondant aux composants principaux
- Système de checkpoints pour reprendre l'exécution
- Utilisation des GPU pour les tâches intensives (Stable Diffusion, TTS)

### 5.2 Gestion des ressources
- Optimisation pour les limites de temps d'exécution de Colab
- Stockage intermédiaire sur Google Drive
- Mécanismes de reprise après interruption

## 6. Sécurité et gestion des API

### 6.1 Gestion des clés API
- Stockage sécurisé des clés API
- Rotation des clés pour éviter les limitations
- Monitoring de l'utilisation des API

### 6.2 Authentification
- OAuth pour YouTube et Google APIs
- Stockage sécurisé des tokens
- Gestion des renouvellements

## 7. Extensibilité et personnalisation

### 7.1 Points d'extension
- Interfaces standardisées pour chaque module
- Système de plugins pour fonctionnalités additionnelles
- Configuration par fichiers YAML/JSON

### 7.2 Personnalisation
- Styles visuels configurables
- Bibliothèque de voix extensible
- Templates de contenu personnalisables par niche

## 8. Considérations techniques

### 8.1 Performance
- Parallélisation des tâches indépendantes
- Mise en cache des résultats intermédiaires
- Optimisation des opérations intensives (génération d'images, montage vidéo)

### 8.2 Robustesse
- Gestion des erreurs à chaque niveau
- Système de retry avec backoff exponentiel
- Journalisation détaillée pour le diagnostic

### 8.3 Évolutivité
- Architecture permettant le traitement par lots
- Possibilité d'ajouter des workers distribués
- Séparation claire entre logique métier et infrastructure
