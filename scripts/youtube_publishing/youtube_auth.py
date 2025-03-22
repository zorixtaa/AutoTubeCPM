"""
Module d'authentification YouTube pour AutoTubeCPM
Ce module gère l'authentification OAuth2 pour l'API YouTube
"""

import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Définition des scopes d'autorisation nécessaires pour gérer une chaîne YouTube
SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtubepartner'
]

class YouTubeAuth:
    """Classe pour gérer l'authentification YouTube via OAuth2"""
    
    def __init__(self, client_secrets_file, token_pickle_path):
        """
        Initialise le gestionnaire d'authentification YouTube
        
        Args:
            client_secrets_file (str): Chemin vers le fichier client_secrets.json
            token_pickle_path (str): Chemin où stocker/charger le token d'authentification
        """
        self.client_secrets_file = client_secrets_file
        self.token_pickle_path = token_pickle_path
        self.credentials = None
        self.youtube_service = None
    
    def get_credentials(self):
        """
        Obtient ou rafraîchit les credentials OAuth2
        
        Returns:
            object: Credentials OAuth2 pour l'API YouTube
        """
        # Charger les credentials existants si disponibles
        if os.path.exists(self.token_pickle_path):
            with open(self.token_pickle_path, 'rb') as token:
                self.credentials = pickle.load(token)
        
        # Si les credentials n'existent pas ou sont expirés, en obtenir de nouveaux
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file, SCOPES)
                self.credentials = flow.run_local_server(port=8080)
            
            # Sauvegarder les credentials pour la prochaine exécution
            with open(self.token_pickle_path, 'wb') as token:
                pickle.dump(self.credentials, token)
        
        return self.credentials
    
    def get_youtube_service(self):
        """
        Construit et retourne un service YouTube API
        
        Returns:
            object: Service YouTube API
        """
        if not self.youtube_service:
            credentials = self.get_credentials()
            self.youtube_service = build('youtube', 'v3', credentials=credentials)
        
        return self.youtube_service
    
    def get_channel_info(self):
        """
        Récupère les informations de la chaîne YouTube connectée
        
        Returns:
            dict: Informations sur la chaîne YouTube
        """
        try:
            youtube = self.get_youtube_service()
            request = youtube.channels().list(
                part="snippet,contentDetails,statistics",
                mine=True
            )
            response = request.execute()
            
            if response['items']:
                return response['items'][0]
            else:
                return None
                
        except HttpError as e:
            print(f"Une erreur est survenue: {e}")
            return None
    
    def get_auth_url(self):
        """
        Génère une URL d'authentification pour l'interface web
        
        Returns:
            str: URL d'authentification
        """
        flow = InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, SCOPES)
        flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
        
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        return auth_url
    
    def exchange_code(self, code):
        """
        Échange un code d'autorisation contre des credentials
        
        Args:
            code (str): Code d'autorisation obtenu de l'interface utilisateur
            
        Returns:
            bool: True si l'échange a réussi, False sinon
        """
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.client_secrets_file, SCOPES)
            flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
            
            self.credentials = flow.fetch_token(code=code)
            
            # Sauvegarder les credentials
            with open(self.token_pickle_path, 'wb') as token:
                pickle.dump(self.credentials, token)
            
            # Initialiser le service YouTube
            self.youtube_service = build('youtube', 'v3', credentials=self.credentials)
            
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'échange du code: {e}")
            return False
