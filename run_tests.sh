#!/bin/bash

# Script d'exécution des tests pour AutoTubeCPM
# Ce script exécute tous les tests unitaires et d'intégration

echo "=== AutoTubeCPM - Exécution des tests ==="
echo "Date: $(date)"
echo "----------------------------------------"

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "Erreur: Python 3 n'est pas installé."
    exit 1
fi

# Vérifier si les dépendances sont installées
echo "Vérification des dépendances..."
pip3 install -r requirements.txt

# Créer les répertoires nécessaires s'ils n'existent pas
echo "Préparation de l'environnement de test..."
mkdir -p data/audio
mkdir -p data/videos
mkdir -p data/generated_content
mkdir -p data/analytics
mkdir -p assets/templates
mkdir -p assets/visual
mkdir -p assets/intros_outros
mkdir -p models/tts_models

# Exécuter les tests unitaires
echo "----------------------------------------"
echo "Exécution des tests unitaires..."
python3 -m unittest tests/test_modules.py

# Vérifier le résultat des tests
if [ $? -eq 0 ]; then
    echo "----------------------------------------"
    echo "✅ Tous les tests ont réussi!"
else
    echo "----------------------------------------"
    echo "❌ Certains tests ont échoué. Veuillez vérifier les erreurs ci-dessus."
fi

echo "----------------------------------------"
echo "Tests terminés à $(date)"
