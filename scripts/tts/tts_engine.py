"""
Module de synthèse vocale pour AutoTubeCPM
Ce module utilise Kokoro TTS pour convertir les scripts en voix off naturelles
"""

import os
import json
import torch
import torchaudio
import time
from datetime import datetime

class TTSEngine:
    """Classe pour la synthèse vocale utilisant Kokoro TTS"""
    
    def __init__(self, models_dir=None, output_dir=None):
        """
        Initialise le moteur de synthèse vocale
        
        Args:
            models_dir (str, optional): Répertoire contenant les modèles TTS
            output_dir (str, optional): Répertoire de sortie pour les fichiers audio
        """
        self.models_dir = models_dir or os.path.join(os.path.dirname(__file__), '../../models/tts_models')
        self.output_dir = output_dir or os.path.join(os.path.dirname(__file__), '../../data/audio')
        
        # Créer les répertoires s'ils n'existent pas
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialiser le modèle TTS
        self.model = None
        self.available_voices = self._get_available_voices()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def _get_available_voices(self):
        """
        Récupère la liste des voix disponibles
        
        Returns:
            dict: Dictionnaire des voix disponibles
        """
        # Dans une implémentation réelle, cette méthode scannerait le répertoire des modèles
        # Pour cette démonstration, nous définissons des voix prédéfinies
        return {
            "male_professional": {
                "name": "Male Professional",
                "gender": "male",
                "style": "professional",
                "language": "en-US",
                "description": "Voix masculine professionnelle, idéale pour les sujets business et technologie"
            },
            "female_professional": {
                "name": "Female Professional",
                "gender": "female",
                "style": "professional",
                "language": "en-US",
                "description": "Voix féminine professionnelle, idéale pour les sujets business et éducation"
            },
            "male_casual": {
                "name": "Male Casual",
                "gender": "male",
                "style": "casual",
                "language": "en-US",
                "description": "Voix masculine décontractée, idéale pour les sujets lifestyle et divertissement"
            },
            "female_casual": {
                "name": "Female Casual",
                "gender": "female",
                "style": "casual",
                "language": "en-US",
                "description": "Voix féminine décontractée, idéale pour les sujets lifestyle et santé"
            }
        }
    
    def _load_model(self):
        """
        Charge le modèle Kokoro TTS
        
        Dans une implémentation réelle, cette méthode chargerait le modèle Kokoro TTS.
        Pour cette démonstration, nous simulons le chargement du modèle.
        """
        print("Chargement du modèle Kokoro TTS...")
        
        # Simuler un délai de chargement
        time.sleep(1)
        
        # Dans une implémentation réelle, nous chargerions le modèle comme ceci:
        # from kokoro import KokoroTTS
        # self.model = KokoroTTS.from_pretrained("kokoro-82m")
        # self.model = self.model.to(self.device)
        
        print(f"Modèle Kokoro TTS chargé avec succès sur {self.device}")
        
        # Pour la démonstration, nous définissons simplement un flag
        self.model = "kokoro-82m"
    
    def generate_speech(self, text, voice_id="male_professional", output_filename=None):
        """
        Génère un fichier audio à partir d'un texte
        
        Dans une implémentation réelle, cette méthode utiliserait Kokoro TTS pour générer l'audio.
        Pour cette démonstration, nous simulons la génération d'audio.
        
        Args:
            text (str): Texte à convertir en voix
            voice_id (str, optional): Identifiant de la voix à utiliser. Par défaut "male_professional"
            output_filename (str, optional): Nom du fichier de sortie. Si None, un nom est généré automatiquement
            
        Returns:
            str: Chemin vers le fichier audio généré
        """
        # Charger le modèle si nécessaire
        if self.model is None:
            self._load_model()
        
        # Vérifier si la voix existe
        if voice_id not in self.available_voices:
            print(f"Voix {voice_id} non disponible. Utilisation de la voix par défaut.")
            voice_id = "male_professional"
        
        print(f"Génération de la voix off avec la voix {voice_id}...")
        
        # Simuler un délai de génération proportionnel à la longueur du texte
        generation_time = len(text) * 0.01  # 10ms par caractère
        time.sleep(min(generation_time, 3))  # Maximum 3 secondes pour la démo
        
        # Générer un nom de fichier si non spécifié
        if output_filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"speech_{voice_id}_{timestamp}.wav"
        
        # Chemin complet du fichier
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Dans une implémentation réelle, nous générerions l'audio comme ceci:
        # audio = self.model.synthesize(text, voice=voice_id)
        # torchaudio.save(output_path, audio, 24000)
        
        # Pour la démonstration, nous créons un fichier audio vide
        self._create_dummy_audio_file(output_path, duration_seconds=len(text) * 0.05)
        
        print(f"Voix off générée et sauvegardée dans: {output_path}")
        
        # Sauvegarder les métadonnées
        self._save_speech_metadata(text, voice_id, output_path)
        
        return output_path
    
    def _create_dummy_audio_file(self, file_path, duration_seconds=10, sample_rate=24000):
        """
        Crée un fichier audio factice pour la démonstration
        
        Args:
            file_path (str): Chemin du fichier à créer
            duration_seconds (float, optional): Durée en secondes. Par défaut 10
            sample_rate (int, optional): Taux d'échantillonnage. Par défaut 24000
        """
        # Créer un signal audio silencieux
        num_samples = int(duration_seconds * sample_rate)
        dummy_audio = torch.zeros(1, num_samples)
        
        # Sauvegarder le fichier audio
        torchaudio.save(file_path, dummy_audio, sample_rate)
    
    def _save_speech_metadata(self, text, voice_id, audio_path):
        """
        Sauvegarde les métadonnées de la synthèse vocale
        
        Args:
            text (str): Texte utilisé pour la synthèse
            voice_id (str): Identifiant de la voix utilisée
            audio_path (str): Chemin vers le fichier audio généré
        """
        metadata = {
            "text": text[:100] + "..." if len(text) > 100 else text,  # Tronquer le texte pour la lisibilité
            "voice_id": voice_id,
            "voice_name": self.available_voices[voice_id]["name"],
            "audio_path": audio_path,
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": os.path.getsize(audio_path) / (24000 * 2)  # Estimation approximative
        }
        
        # Chemin du fichier de métadonnées
        metadata_path = audio_path + ".json"
        
        # Sauvegarder les métadonnées
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
    
    def get_voice_recommendations(self, category, subcategory):
        """
        Recommande des voix adaptées à une catégorie et sous-catégorie
        
        Args:
            category (str): Catégorie principale
            subcategory (str): Sous-catégorie
            
        Returns:
            list: Liste des voix recommandées
        """
        # Recommandations par catégorie
        recommendations = {
            "finance": ["male_professional", "female_professional"],
            "technology": ["male_professional", "male_casual"],
            "health": ["female_professional", "female_casual"],
            "business": ["male_professional", "female_professional"],
            "education": ["female_professional", "male_professional"]
        }
        
        # Retourner les recommandations pour la catégorie ou une liste par défaut
        return recommendations.get(category, ["male_professional", "female_casual"])
    
    def process_script_for_tts(self, script_text):
        """
        Prétraite un script pour améliorer la qualité de la synthèse vocale
        
        Args:
            script_text (str): Texte du script
            
        Returns:
            str: Texte prétraité
        """
        # Remplacer les abréviations courantes
        replacements = {
            "e.g.": "for example",
            "i.e.": "that is",
            "etc.": "etcetera",
            "vs.": "versus",
            "approx.": "approximately",
            "Dr.": "Doctor",
            "Mr.": "Mister",
            "Mrs.": "Misses",
            "Ms.": "Miss",
            "Prof.": "Professor"
        }
        
        processed_text = script_text
        
        for abbr, full in replacements.items():
            processed_text = processed_text.replace(abbr, full)
        
        # Ajouter des pauses pour améliorer le rythme
        processed_text = processed_text.replace(". ", ". <break time='0.5s'/> ")
        processed_text = processed_text.replace("! ", "! <break time='0.5s'/> ")
        processed_text = processed_text.replace("? ", "? <break time='0.5s'/> ")
        processed_text = processed_text.replace("\n\n", "\n<break time='1s'/>\n")
        
        return processed_text
    
    def batch_generate_speech(self, script_sections, voice_id="male_professional"):
        """
        Génère des fichiers audio pour chaque section d'un script
        
        Args:
            script_sections (dict): Sections du script
            voice_id (str, optional): Identifiant de la voix à utiliser. Par défaut "male_professional"
            
        Returns:
            dict: Dictionnaire des chemins audio par section
        """
        audio_paths = {}
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Générer l'audio pour chaque section
        for section_name, text in script_sections.items():
            # Prétraiter le texte
            processed_text = self.process_script_for_tts(text)
            
            # Générer un nom de fichier
            filename = f"{section_name}_{voice_id}_{timestamp}.wav"
            
            # Générer l'audio
            audio_path = self.generate_speech(processed_text, voice_id, filename)
            
            # Stocker le chemin
            audio_paths[section_name] = audio_path
        
        return audio_paths
