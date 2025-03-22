"""
Module d'assemblage vidéo pour AutoTubeCPM
Ce module gère la création de vidéos à partir d'audio et d'éléments visuels
"""

import os
import json
import time
import random
import requests
from datetime import datetime
from moviepy.editor import (
    AudioFileClip, ImageClip, VideoFileClip, TextClip, 
    CompositeVideoClip, concatenate_videoclips, vfx
)

class VideoProducer:
    """Classe pour produire des vidéos à partir d'audio et d'éléments visuels"""
    
    def __init__(self, pexels_api_key=None, assets_dir=None, output_dir=None):
        """
        Initialise le producteur vidéo
        
        Args:
            pexels_api_key (str, optional): Clé API Pexels pour les vidéos stock
            assets_dir (str, optional): Répertoire contenant les éléments visuels
            output_dir (str, optional): Répertoire de sortie pour les vidéos
        """
        self.pexels_api_key = pexels_api_key
        self.assets_dir = assets_dir or os.path.join(os.path.dirname(__file__), '../../assets')
        self.output_dir = output_dir or os.path.join(os.path.dirname(__file__), '../../data/videos')
        
        # Créer les répertoires s'ils n'existent pas
        os.makedirs(self.assets_dir, exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, 'visual'), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, 'intros_outros'), exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_video(self, audio_path, script_data, metadata, visual_style="dynamic", 
                    resolution=(1920, 1080), fps=30, use_intro_outro=True):
        """
        Crée une vidéo complète à partir d'un fichier audio et des données de script
        
        Args:
            audio_path (str): Chemin vers le fichier audio
            script_data (dict): Données du script
            metadata (dict): Métadonnées de la vidéo
            visual_style (str, optional): Style visuel. Par défaut "dynamic"
            resolution (tuple, optional): Résolution de la vidéo. Par défaut (1920, 1080)
            fps (int, optional): Images par seconde. Par défaut 30
            use_intro_outro (bool, optional): Utiliser intro/outro. Par défaut True
            
        Returns:
            str: Chemin vers la vidéo générée
        """
        print(f"Création d'une vidéo pour le script: {script_data['title']}")
        print(f"Style visuel: {visual_style}, Résolution: {resolution}, FPS: {fps}")
        
        # Charger le fichier audio
        audio_clip = AudioFileClip(audio_path)
        audio_duration = audio_clip.duration
        
        print(f"Durée audio: {audio_duration} secondes")
        
        # Obtenir des visuels pour la vidéo
        visual_clips = self._get_visual_clips(script_data, audio_duration, visual_style, resolution)
        
        # Créer les clips de texte pour les sous-titres
        text_clips = self._create_text_clips(script_data, audio_duration, resolution)
        
        # Créer l'intro et l'outro si demandé
        intro_clip = None
        outro_clip = None
        
        if use_intro_outro:
            intro_clip = self._create_intro_clip(script_data['title'], resolution, fps)
            outro_clip = self._create_outro_clip(metadata, resolution, fps)
        
        # Assembler tous les clips
        video_clips = []
        
        if intro_clip:
            video_clips.append(intro_clip)
        
        # Ajouter les clips visuels avec les sous-titres
        main_clips = []
        for i, visual_clip in enumerate(visual_clips):
            # Ajouter les sous-titres correspondants si disponibles
            if i < len(text_clips):
                composite = CompositeVideoClip([visual_clip, text_clips[i]])
                main_clips.append(composite)
            else:
                main_clips.append(visual_clip)
        
        # Concaténer les clips principaux
        if main_clips:
            main_video = concatenate_videoclips(main_clips)
            
            # Ajuster la durée pour correspondre à l'audio
            if main_video.duration > audio_duration:
                main_video = main_video.subclip(0, audio_duration)
            
            # Ajouter l'audio
            main_video = main_video.set_audio(audio_clip)
            video_clips.append(main_video)
        
        if outro_clip:
            video_clips.append(outro_clip)
        
        # Concaténer tous les clips
        final_video = concatenate_videoclips(video_clips) if len(video_clips) > 1 else video_clips[0]
        
        # Générer un nom de fichier
        title_slug = script_data['title'].lower().replace(' ', '_')[:30]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"{title_slug}_{timestamp}.mp4"
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Écrire la vidéo sur le disque
        print(f"Rendu de la vidéo finale vers: {output_path}")
        final_video.write_videofile(output_path, fps=fps, codec='libx264', audio_codec='aac')
        
        # Sauvegarder les métadonnées de la vidéo
        self._save_video_metadata(output_path, script_data, metadata, audio_path, visual_style)
        
        return output_path
    
    def _get_visual_clips(self, script_data, audio_duration, visual_style, resolution):
        """
        Obtient des clips visuels pour la vidéo
        
        Args:
            script_data (dict): Données du script
            audio_duration (float): Durée de l'audio en secondes
            visual_style (str): Style visuel
            resolution (tuple): Résolution de la vidéo
            
        Returns:
            list: Liste de clips visuels
        """
        # Déterminer le nombre de segments visuels
        num_segments = 5  # Introduction + 3 sections + conclusion
        segment_duration = audio_duration / num_segments
        
        # Obtenir des mots-clés pour chaque segment
        keywords = [
            script_data['title'],  # Introduction
            script_data['section1_title'],  # Section 1
            script_data['section2_title'],  # Section 2
            script_data['section3_title'],  # Section 3
            "conclusion " + script_data['title']  # Conclusion
        ]
        
        # Obtenir des clips visuels pour chaque segment
        visual_clips = []
        
        for i, keyword in enumerate(keywords):
            # Durée du segment
            start_time = i * segment_duration
            end_time = (i + 1) * segment_duration
            duration = end_time - start_time
            
            # Obtenir un clip visuel pour ce segment
            if visual_style == "stock_video":
                clip = self._get_stock_video_clip(keyword, duration, resolution)
            elif visual_style == "image_slideshow":
                clip = self._create_image_slideshow(keyword, duration, resolution)
            else:  # "dynamic" ou autre
                clip = self._create_dynamic_background(keyword, duration, resolution)
            
            visual_clips.append(clip)
        
        return visual_clips
    
    def _get_stock_video_clip(self, keyword, duration, resolution):
        """
        Obtient un clip vidéo stock via l'API Pexels
        
        Dans une implémentation réelle, cette méthode ferait appel à l'API Pexels.
        Pour cette démonstration, nous simulons l'obtention de vidéos stock.
        
        Args:
            keyword (str): Mot-clé pour la recherche
            duration (float): Durée souhaitée en secondes
            resolution (tuple): Résolution souhaitée
            
        Returns:
            VideoClip: Clip vidéo
        """
        print(f"Recherche de vidéo stock pour le mot-clé: {keyword}")
        
        # Simuler un délai de recherche
        time.sleep(0.5)
        
        # Dans une implémentation réelle, nous ferions appel à l'API Pexels comme ceci:
        # if self.pexels_api_key:
        #     headers = {"Authorization": self.pexels_api_key}
        #     response = requests.get(
        #         f"https://api.pexels.com/videos/search?query={keyword}&per_page=1",
        #         headers=headers
        #     )
        #     data = response.json()
        #     if "videos" in data and data["videos"]:
        #         video_url = data["videos"][0]["video_files"][0]["link"]
        #         temp_path = os.path.join(self.assets_dir, "temp_video.mp4")
        #         urllib.request.urlretrieve(video_url, temp_path)
        #         clip = VideoFileClip(temp_path)
        #         return clip.resize(resolution).subclip(0, min(duration, clip.duration))
        
        # Pour la démonstration, nous créons un clip coloré
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        clip = ColorClip(resolution, color=color, duration=duration)
        
        # Ajouter un texte indiquant qu'il s'agit d'une vidéo stock
        text = TextClip(f"Stock Video: {keyword}", fontsize=30, color='white', font='Arial')
        text = text.set_position('center').set_duration(duration)
        
        return CompositeVideoClip([clip, text])
    
    def _create_image_slideshow(self, keyword, duration, resolution):
        """
        Crée un diaporama d'images
        
        Args:
            keyword (str): Mot-clé pour la recherche
            duration (float): Durée souhaitée en secondes
            resolution (tuple): Résolution souhaitée
            
        Returns:
            VideoClip: Clip vidéo de diaporama
        """
        print(f"Création d'un diaporama pour le mot-clé: {keyword}")
        
        # Nombre d'images dans le diaporama
        num_images = max(3, int(duration / 3))  # Au moins 3 images, changement toutes les 3 secondes
        
        # Créer des clips d'image colorés pour la démonstration
        image_clips = []
        for i in range(num_images):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            img_duration = duration / num_images
            
            # Créer un clip coloré
            clip = ColorClip(resolution, color=color, duration=img_duration)
            
            # Ajouter un texte
            text = TextClip(f"Image {i+1}: {keyword}", fontsize=30, color='white', font='Arial')
            text = text.set_position('center').set_duration(img_duration)
            
            # Combiner image et texte
            composite = CompositeVideoClip([clip, text])
            
            # Ajouter des effets de transition
            if i > 0:
                composite = composite.fx(vfx.fadein, 0.5)
            if i < num_images - 1:
                composite = composite.fx(vfx.fadeout, 0.5)
            
            image_clips.append(composite)
        
        # Concaténer les clips d'image
        return concatenate_videoclips(image_clips)
    
    def _create_dynamic_background(self, keyword, duration, resolution):
        """
        Crée un arrière-plan dynamique
        
        Args:
            keyword (str): Mot-clé pour le contenu
            duration (float): Durée souhaitée en secondes
            resolution (tuple): Résolution souhaitée
            
        Returns:
            VideoClip: Clip vidéo avec arrière-plan dynamique
        """
        print(f"Création d'un arrière-plan dynamique pour: {keyword}")
        
        # Créer un clip de couleur de base
        base_color = (40, 40, 40)  # Gris foncé
        clip = ColorClip(resolution, color=base_color, duration=duration)
        
        # Créer un titre animé
        title = TextClip(keyword, fontsize=60, color='white', font='Arial', bg_color='transparent')
        title = title.set_position('center').set_duration(duration)
        title = title.crossfadein(0.5).crossfadeout(0.5)
        
        # Ajouter un effet de mouvement au titre
        title = title.set_position(lambda t: ('center', 400 + 50 * (t % 5 - 2.5)**2))
        
        # Combiner les clips
        return CompositeVideoClip([clip, title])
    
    def _create_text_clips(self, script_data, audio_duration, resolution):
        """
        Crée des clips de texte pour les sous-titres
        
        Args:
            script_data (dict): Données du script
            audio_duration (float): Durée de l'audio en secondes
            resolution (tuple): Résolution de la vidéo
            
        Returns:
            list: Liste de clips de texte
        """
        # Extraire les sections principales du script
        sections = [
            script_data['topic_intro'],
            script_data['section1_point1'] + " " + script_data['section1_point2'],
            script_data['section2_point1'] + " " + script_data['section2_point2'],
            script_data['section3_point1'] + " " + script_data['section3_point2'],
            script_data['recap']
        ]
        
        # Durée par section
        section_duration = audio_duration / len(sections)
        
        # Créer un clip de texte pour chaque section
        text_clips = []
        for i, section_text in enumerate(sections):
            # Limiter la longueur du texte
            if len(section_text) > 100:
                section_text = section_text[:97] + "..."
            
            # Créer le clip de texte
            text = TextClip(section_text, fontsize=30, color='white', font='Arial', 
                           bg_color='rgba(0,0,0,0.5)', method='caption', align='center', 
                           size=(resolution[0] - 100, None))
            
            # Positionner en bas de l'écran
            text = text.set_position(('center', resolution[1] - 150))
            
            # Définir la durée et le timing
            start_time = i * section_duration
            text = text.set_start(start_time).set_duration(section_duration)
            
            # Ajouter des effets de fondu
            text = text.crossfadein(0.5).crossfadeout(0.5)
            
            text_clips.append(text)
        
        return text_clips
    
    def _create_intro_clip(self, title, resolution, fps, duration=5):
        """
        Crée un clip d'introduction
        
        Args:
            title (str): Titre de la vidéo
            resolution (tuple): Résolution de la vidéo
            fps (int): Images par seconde
            duration (float, optional): Durée de l'intro en secondes. Par défaut 5
            
        Returns:
            VideoClip: Clip d'introduction
        """
        print(f"Création d'une intro pour: {title}")
        
        # Créer un arrière-plan
        background = ColorClip(resolution, color=(20, 20, 20), duration=duration)
        
        # Créer le texte du titre
        title_clip = TextClip(title, fontsize=70, color='white', font='Arial', 
                             bg_color=None, method='caption', align='center', 
                             size=(resolution[0] - 200, None))
        title_clip = title_clip.set_position('center').set_duration(duration)
        
        # Animer le titre
        title_clip = title_clip.set_start(1)  # Commencer après 1 seconde
        title_clip = title_clip.crossfadein(1)
        
        # Créer un sous-titre
        subtitle = TextClip("Une vidéo AutoTubeCPM", fontsize=30, color='lightgrey', 
                           font='Arial', method='caption')
        subtitle = subtitle.set_position(('center', resolution[1] // 2 + 100))
        subtitle = subtitle.set_start(2).set_duration(duration - 2)  # Commencer après 2 secondes
        subtitle = subtitle.crossfadein(0.5)
        
        # Combiner les clips
        return CompositeVideoClip([background, title_clip, subtitle])
    
    def _create_outro_clip(self, metadata, resolution, fps, duration=8):
        """
        Crée un clip de conclusion
        
        Args:
            metadata (dict): Métadonnées de la vidéo
            resolution (tuple): Résolution de la vidéo
            fps (int): Images par seconde
            duration (float, optional): Durée de l'outro en secondes. Par défaut 8
            
        Returns:
            VideoClip: Clip de conclusion
        """
        print("Création d'un outro")
        
        # Créer un arrière-plan
        background = ColorClip(resolution, color=(20, 20, 20), duration=duration)
        
        # Créer le texte de remerciement
        thanks = TextClip("Merci d'avoir regardé !", fontsize=60, color='white', 
                         font='Arial', method='caption')
        thanks = thanks.set_position(('center', resolution[1] // 2 - 100))
        thanks = thanks.set_duration(duration)
        thanks = thanks.crossfadein(0.5)
        
        # Créer un appel à l'action
        cta = TextClip("N'oubliez pas de vous abonner et de laisser un commentaire", 
                      fontsize=30, color='lightgrey', font='Arial', method='caption')
        cta = cta.set_position(('center', resolution[1] // 2))
        cta = cta.set_start(1).set_duration(duration - 1)  # Commencer après 1 seconde
        cta = cta.crossfadein(0.5)
        
        # Créer des liens sociaux
        social = TextClip("Retrouvez-nous sur les réseaux sociaux", 
                         fontsize=25, color='lightblue', font='Arial', method='caption')
        social = social.set_position(('center', resolution[1] // 2 + 100))
        social = social.set_start(2).set_duration(duration - 2)  # Commencer après 2 secondes
        social = social.crossfadein(0.5)
        
        # Combiner les clips
        return CompositeVideoClip([background, thanks, cta, social])
    
    def _save_video_metadata(self, video_path, script_data, metadata, audio_path, visual_style):
        """
        Sauvegarde les métadonnées de la vidéo
        
        Args:
            video_path (str): Chemin vers la vidéo générée
            script_data (dict): Données du script
            metadata (dict): Métadonnées YouTube
            audio_path (str): Chemin vers le fichier audio utilisé
            visual_style (str): Style visuel utilisé
        """
        video_metadata = {
            "video_path": video_path,
            "title": script_data['title'],
            "audio_path": audio_path,
            "visual_style": visual_style,
            "youtube_metadata": metadata,
            "generation_timestamp": datetime.now().isoformat(),
            "file_size_mb": os.path.getsize(video_path) / (1024 * 1024)
        }
        
        # Chemin du fichier de métadonnées
        metadata_path = video_path + ".json"
        
        # Sauvegarder les métadonnées
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(video_metadata, f, indent=2)
        
        print(f"Métadonnées vidéo sauvegardées dans: {metadata_path}")


# Classe utilitaire pour créer des clips de couleur
class ColorClip(ImageClip):
    """Classe pour créer des clips de couleur unie"""
    
    def __init__(self, size, color=None, duration=None):
        """
        Initialise un clip de couleur
        
        Args:
            size (tuple): Taille du clip (largeur, hauteur)
            color (tuple, optional): Couleur RGB. Par défaut None (noir)
            duration (float, optional): Durée du clip. Par défaut None (infini)
        """
        import numpy as np
        from PIL import Image, ImageDraw
        
        color = color or (0, 0, 0)
        w, h = size
        
        # Créer une image de couleur unie
        img = Image.new('RGB', size, color)
        
        # Convertir en tableau numpy
        img_array = np.array(img)
        
        # Initialiser le clip d'image
        super().__init__(img_array, duration=duration)
