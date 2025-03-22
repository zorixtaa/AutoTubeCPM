"""
Module de publication YouTube pour AutoTubeCPM
Ce module gère le téléchargement et la configuration des vidéos sur YouTube
"""

import os
import time
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from .youtube_auth import YouTubeAuth

class YouTubePublisher:
    """Classe pour gérer la publication de vidéos sur YouTube"""
    
    def __init__(self, auth_manager):
        """
        Initialise le gestionnaire de publication YouTube
        
        Args:
            auth_manager (YouTubeAuth): Instance du gestionnaire d'authentification YouTube
        """
        self.auth_manager = auth_manager
        self.youtube_service = None
    
    def _get_service(self):
        """
        Obtient le service YouTube API
        
        Returns:
            object: Service YouTube API
        """
        if not self.youtube_service:
            self.youtube_service = self.auth_manager.get_youtube_service()
        return self.youtube_service
    
    def upload_video(self, video_file, title, description, tags, category_id=22, 
                     privacy_status="private", notify_subscribers=True, 
                     thumbnail_file=None, language="en"):
        """
        Télécharge une vidéo sur YouTube
        
        Args:
            video_file (str): Chemin vers le fichier vidéo
            title (str): Titre de la vidéo
            description (str): Description de la vidéo
            tags (list): Liste de tags pour la vidéo
            category_id (int, optional): ID de catégorie YouTube. Par défaut 22 (People & Blogs)
            privacy_status (str, optional): Statut de confidentialité. Par défaut "private"
            notify_subscribers (bool, optional): Notifier les abonnés. Par défaut True
            thumbnail_file (str, optional): Chemin vers l'image de miniature
            language (str, optional): Code de langue. Par défaut "en"
            
        Returns:
            dict: Informations sur la vidéo téléchargée ou None en cas d'échec
        """
        try:
            youtube = self._get_service()
            
            # Définir les métadonnées de la vidéo
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'categoryId': category_id,
                    'defaultLanguage': language,
                    'defaultAudioLanguage': language
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': False,
                    'notifySubscribers': notify_subscribers
                }
            }
            
            # Préparer le fichier média
            media = MediaFileUpload(
                video_file,
                mimetype='video/*',
                resumable=True
            )
            
            # Créer la requête d'insertion
            insert_request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            # Télécharger la vidéo avec gestion de la progression
            video_id = None
            response = None
            
            print(f"Téléchargement de la vidéo '{title}' en cours...")
            while response is None:
                status, response = insert_request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"Téléchargement: {progress}%")
            
            video_id = response['id']
            print(f"Vidéo téléchargée avec succès! ID: {video_id}")
            
            # Télécharger la miniature si fournie
            if thumbnail_file and os.path.exists(thumbnail_file):
                self.set_thumbnail(video_id, thumbnail_file)
            
            return response
            
        except HttpError as e:
            print(f"Une erreur est survenue lors du téléchargement: {e}")
            return None
    
    def set_thumbnail(self, video_id, thumbnail_file):
        """
        Définit la miniature d'une vidéo
        
        Args:
            video_id (str): ID de la vidéo YouTube
            thumbnail_file (str): Chemin vers l'image de miniature
            
        Returns:
            bool: True si réussi, False sinon
        """
        try:
            youtube = self._get_service()
            
            # Préparer le fichier média
            media = MediaFileUpload(
                thumbnail_file,
                mimetype='image/jpeg',
                resumable=True
            )
            
            # Définir la miniature
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=media
            ).execute()
            
            print(f"Miniature définie avec succès pour la vidéo {video_id}")
            return True
            
        except HttpError as e:
            print(f"Erreur lors de la définition de la miniature: {e}")
            return False
    
    def update_video_metadata(self, video_id, title=None, description=None, 
                             tags=None, category_id=None, privacy_status=None, 
                             language=None):
        """
        Met à jour les métadonnées d'une vidéo existante
        
        Args:
            video_id (str): ID de la vidéo YouTube
            title (str, optional): Nouveau titre
            description (str, optional): Nouvelle description
            tags (list, optional): Nouveaux tags
            category_id (int, optional): Nouvelle catégorie
            privacy_status (str, optional): Nouveau statut de confidentialité
            language (str, optional): Nouveau code de langue
            
        Returns:
            dict: Informations sur la vidéo mise à jour ou None en cas d'échec
        """
        try:
            youtube = self._get_service()
            
            # Récupérer les métadonnées actuelles
            video_response = youtube.videos().list(
                part='snippet,status',
                id=video_id
            ).execute()
            
            if not video_response['items']:
                print(f"Vidéo {video_id} non trouvée")
                return None
            
            # Préparer les mises à jour
            snippet = video_response['items'][0]['snippet']
            status = video_response['items'][0]['status']
            
            if title:
                snippet['title'] = title
            if description:
                snippet['description'] = description
            if tags:
                snippet['tags'] = tags
            if category_id:
                snippet['categoryId'] = category_id
            if language:
                snippet['defaultLanguage'] = language
                snippet['defaultAudioLanguage'] = language
            if privacy_status:
                status['privacyStatus'] = privacy_status
            
            # Mettre à jour la vidéo
            update_response = youtube.videos().update(
                part='snippet,status',
                body={
                    'id': video_id,
                    'snippet': snippet,
                    'status': status
                }
            ).execute()
            
            print(f"Métadonnées mises à jour pour la vidéo {video_id}")
            return update_response
            
        except HttpError as e:
            print(f"Erreur lors de la mise à jour des métadonnées: {e}")
            return None
    
    def schedule_video_publication(self, video_id, publish_time):
        """
        Planifie la publication d'une vidéo privée
        
        Args:
            video_id (str): ID de la vidéo YouTube
            publish_time (str): Date et heure de publication au format ISO 8601
                                (ex: '2025-04-01T12:00:00Z')
            
        Returns:
            dict: Informations sur la vidéo planifiée ou None en cas d'échec
        """
        try:
            youtube = self._get_service()
            
            # Mettre à jour le statut de la vidéo
            update_response = youtube.videos().update(
                part='status',
                body={
                    'id': video_id,
                    'status': {
                        'privacyStatus': 'private',
                        'publishAt': publish_time
                    }
                }
            ).execute()
            
            print(f"Publication planifiée pour la vidéo {video_id} à {publish_time}")
            return update_response
            
        except HttpError as e:
            print(f"Erreur lors de la planification de la publication: {e}")
            return None
    
    def get_video_analytics(self, video_id, metrics=None, start_date=None, end_date=None):
        """
        Récupère les statistiques d'une vidéo
        
        Args:
            video_id (str): ID de la vidéo YouTube
            metrics (list, optional): Liste des métriques à récupérer
            start_date (str, optional): Date de début au format YYYY-MM-DD
            end_date (str, optional): Date de fin au format YYYY-MM-DD
            
        Returns:
            dict: Statistiques de la vidéo ou None en cas d'échec
        """
        try:
            youtube = self._get_service()
            
            # Définir les métriques par défaut si non spécifiées
            if not metrics:
                metrics = ['views', 'likes', 'dislikes', 'comments', 'shares', 
                          'estimatedMinutesWatched', 'averageViewDuration']
            
            # Récupérer les statistiques de base
            video_response = youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()
            
            if not video_response['items']:
                print(f"Vidéo {video_id} non trouvée")
                return None
            
            statistics = video_response['items'][0]['statistics']
            
            # Si les dates sont spécifiées, récupérer les statistiques détaillées
            if start_date and end_date:
                analytics = youtube.reports().query(
                    ids=f'channel==MINE',
                    startDate=start_date,
                    endDate=end_date,
                    metrics=','.join(metrics),
                    filters=f'video=={video_id}'
                ).execute()
                
                if 'rows' in analytics:
                    for i, metric in enumerate(metrics):
                        statistics[metric] = analytics['rows'][0][i]
            
            return statistics
            
        except HttpError as e:
            print(f"Erreur lors de la récupération des statistiques: {e}")
            return None
