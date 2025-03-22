"""
Module d'analyse de performance pour AutoTubeCPM
Ce module analyse les performances des vidéos YouTube et fournit des insights
"""

import os
import json
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from googleapiclient.errors import HttpError

class PerformanceAnalyzer:
    """Classe pour analyser les performances des vidéos YouTube"""
    
    def __init__(self, youtube_auth=None, data_dir=None):
        """
        Initialise l'analyseur de performance
        
        Args:
            youtube_auth (YouTubeAuth, optional): Instance d'authentification YouTube
            data_dir (str, optional): Répertoire pour stocker les données d'analyse
        """
        self.youtube_auth = youtube_auth
        self.data_dir = data_dir or os.path.join(os.path.dirname(__file__), '../../data/analytics')
        
        # Créer le répertoire s'il n'existe pas
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Service YouTube Analytics
        self.youtube_analytics = None
        
        # Métriques disponibles
        self.available_metrics = {
            'views': 'Nombre de vues',
            'estimatedMinutesWatched': 'Minutes visionnées estimées',
            'averageViewDuration': 'Durée moyenne de visionnage',
            'averageViewPercentage': 'Pourcentage moyen visionné',
            'subscribersGained': 'Abonnés gagnés',
            'subscribersLost': 'Abonnés perdus',
            'likes': 'J\'aime',
            'dislikes': 'Je n\'aime pas',
            'shares': 'Partages',
            'comments': 'Commentaires',
            'annotationClickThroughRate': 'Taux de clics sur annotations',
            'annotationCloseRate': 'Taux de fermeture d\'annotations',
            'cardClickRate': 'Taux de clics sur cartes',
            'cardTeaserClickRate': 'Taux de clics sur aperçus de cartes',
            'estimatedRevenue': 'Revenus estimés',
            'estimatedAdRevenue': 'Revenus publicitaires estimés',
            'grossRevenue': 'Revenus bruts',
            'cpm': 'CPM (coût pour mille impressions)',
            'playbackBasedCpm': 'CPM basé sur le visionnage',
            'adImpressions': 'Impressions publicitaires',
            'monetizedPlaybacks': 'Lectures monétisées'
        }
    
    def _get_analytics_service(self):
        """
        Obtient le service YouTube Analytics
        
        Returns:
            object: Service YouTube Analytics
        """
        if not self.youtube_analytics and self.youtube_auth:
            credentials = self.youtube_auth.get_credentials()
            from googleapiclient.discovery import build
            self.youtube_analytics = build('youtubeAnalytics', 'v2', credentials=credentials)
        
        return self.youtube_analytics
    
    def get_channel_performance(self, start_date=None, end_date=None, metrics=None):
        """
        Récupère les performances globales de la chaîne
        
        Args:
            start_date (str, optional): Date de début au format YYYY-MM-DD
            end_date (str, optional): Date de fin au format YYYY-MM-DD
            metrics (list, optional): Liste des métriques à récupérer
            
        Returns:
            dict: Données de performance de la chaîne
        """
        # Définir les dates par défaut si non spécifiées
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        if not start_date:
            # Par défaut, 30 jours avant la date de fin
            start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # Définir les métriques par défaut si non spécifiées
        if not metrics:
            metrics = [
                'views', 'estimatedMinutesWatched', 'averageViewDuration',
                'subscribersGained', 'subscribersLost', 'likes', 'dislikes',
                'shares', 'comments', 'estimatedRevenue'
            ]
        
        # Vérifier que les métriques sont valides
        metrics = [m for m in metrics if m in self.available_metrics]
        
        try:
            analytics = self._get_analytics_service()
            
            if not analytics:
                return self._simulate_channel_performance(start_date, end_date, metrics)
            
            # Exécuter la requête
            response = analytics.reports().query(
                ids='channel==MINE',
                startDate=start_date,
                endDate=end_date,
                metrics=','.join(metrics),
                dimensions='day',
                sort='day'
            ).execute()
            
            # Traiter les résultats
            return self._process_analytics_response(response, metrics)
            
        except HttpError as e:
            print(f"Erreur lors de la récupération des performances de la chaîne: {e}")
            # En cas d'erreur, simuler les données
            return self._simulate_channel_performance(start_date, end_date, metrics)
    
    def _simulate_channel_performance(self, start_date, end_date, metrics):
        """
        Simule les données de performance de la chaîne pour la démonstration
        
        Args:
            start_date (str): Date de début au format YYYY-MM-DD
            end_date (str): Date de fin au format YYYY-MM-DD
            metrics (list): Liste des métriques à simuler
            
        Returns:
            dict: Données de performance simulées
        """
        print(f"Simulation des données de performance de la chaîne du {start_date} au {end_date}")
        
        # Générer les dates
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        date_range = [(start + timedelta(days=i)).strftime('%Y-%m-%d') 
                     for i in range((end - start).days + 1)]
        
        # Générer des données simulées
        data = {'dates': date_range}
        
        # Valeurs de base pour chaque métrique
        base_values = {
            'views': 1000,
            'estimatedMinutesWatched': 5000,
            'averageViewDuration': 180,
            'averageViewPercentage': 40,
            'subscribersGained': 50,
            'subscribersLost': 10,
            'likes': 100,
            'dislikes': 5,
            'shares': 20,
            'comments': 30,
            'annotationClickThroughRate': 0.15,
            'annotationCloseRate': 0.05,
            'cardClickRate': 0.1,
            'cardTeaserClickRate': 0.2,
            'estimatedRevenue': 50,
            'estimatedAdRevenue': 45,
            'grossRevenue': 55,
            'cpm': 8,
            'playbackBasedCpm': 7.5,
            'adImpressions': 800,
            'monetizedPlaybacks': 750
        }
        
        # Générer des données pour chaque métrique
        for metric in metrics:
            base = base_values.get(metric, 100)
            # Ajouter une tendance croissante et une variation aléatoire
            values = [max(0, base * (1 + i * 0.02 + np.random.normal(0, 0.1))) 
                     for i in range(len(date_range))]
            data[metric] = values
        
        return {
            'data': data,
            'metrics': metrics,
            'start_date': start_date,
            'end_date': end_date
        }
    
    def _process_analytics_response(self, response, metrics):
        """
        Traite la réponse de l'API YouTube Analytics
        
        Args:
            response (dict): Réponse de l'API
            metrics (list): Liste des métriques demandées
            
        Returns:
            dict: Données de performance traitées
        """
        # Extraire les colonnes
        columns = [h['name'] for h in response.get('columnHeaders', [])]
        
        # Extraire les données
        rows = response.get('rows', [])
        
        # Convertir en dictionnaire
        data = {'dates': [row[0] for row in rows]}
        
        for i, metric in enumerate(metrics):
            col_index = columns.index(metric) if metric in columns else -1
            if col_index >= 0:
                data[metric] = [row[col_index] for row in rows]
        
        return {
            'data': data,
            'metrics': metrics,
            'start_date': response.get('startDate'),
            'end_date': response.get('endDate')
        }
    
    def get_video_performance(self, video_id, start_date=None, end_date=None, metrics=None):
        """
        Récupère les performances d'une vidéo spécifique
        
        Args:
            video_id (str): ID de la vidéo YouTube
            start_date (str, optional): Date de début au format YYYY-MM-DD
            end_date (str, optional): Date de fin au format YYYY-MM-DD
            metrics (list, optional): Liste des métriques à récupérer
            
        Returns:
            dict: Données de performance de la vidéo
        """
        # Définir les dates par défaut si non spécifiées
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        if not start_date:
            # Par défaut, 30 jours avant la date de fin ou depuis la publication
            start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # Définir les métriques par défaut si non spécifiées
        if not metrics:
            metrics = [
                'views', 'estimatedMinutesWatched', 'averageViewDuration',
                'subscribersGained', 'likes', 'dislikes', 'shares', 'comments',
                'estimatedRevenue', 'cpm'
            ]
        
        # Vérifier que les métriques sont valides
        metrics = [m for m in metrics if m in self.available_metrics]
        
        try:
            analytics = self._get_analytics_service()
            
            if not analytics:
                return self._simulate_video_performance(video_id, start_date, end_date, metrics)
            
            # Exécuter la requête
            response = analytics.reports().query(
                ids='channel==MINE',
                startDate=start_date,
                endDate=end_date,
                metrics=','.join(metrics),
                dimensions='day',
                filters=f'video=={video_id}',
                sort='day'
            ).execute()
            
            # Traiter les résultats
            return self._process_analytics_response(response, metrics)
            
        except HttpError as e:
            print(f"Erreur lors de la récupération des performances de la vidéo: {e}")
            # En cas d'erreur, simuler les données
            return self._simulate_video_performance(video_id, start_date, end_date, metrics)
    
    def _simulate_video_performance(self, video_id, start_date, end_date, metrics):
        """
        Simule les données de performance d'une vidéo pour la démonstration
        
        Args:
            video_id (str): ID de la vidéo
            start_date (str): Date de début au format YYYY-MM-DD
            end_date (str): Date de fin au format YYYY-MM-DD
            metrics (list): Liste des métriques à simuler
            
        Returns:
            dict: Données de performance simulées
        """
        print(f"Simulation des données de performance pour la vidéo {video_id} du {start_date} au {end_date}")
        
        # Générer les dates
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        date_range = [(start + timedelta(days=i)).strftime('%Y-%m-%d') 
                     for i in range((end - start).days + 1)]
        
        # Générer des données simulées
        data = {'dates': date_range}
        
        # Valeurs de base pour chaque métrique, plus faibles que pour la chaîne
        base_values = {
            'views': 200,
            'estimatedMinutesWatched': 1000,
            'averageViewDuration': 180,
            'averageViewPercentage': 40,
            'subscribersGained': 10,
            'subscribersLost': 2,
            'likes': 20,
            'dislikes': 1,
            'shares': 5,
            'comments': 8,
            'annotationClickThroughRate': 0.15,
            'annotationCloseRate': 0.05,
            'cardClickRate': 0.1,
            'cardTeaserClickRate': 0.2,
            'estimatedRevenue': 10,
            'estimatedAdRevenue': 9,
            'grossRevenue': 11,
            'cpm': 8,
            'playbackBasedCpm': 7.5,
            'adImpressions': 160,
            'monetizedPlaybacks': 150
        }
        
        # Générer des données pour chaque métrique
        for metric in metrics:
            base = base_values.get(metric, 20)
            # Courbe typique d'une vidéo: pic au début puis déclin
            values = []
            for i in range(len(date_range)):
                # Facteur de déclin exponentiel
                decay = np.exp(-i / 10)
                # Valeur avec variation aléatoire
                value = max(0, base * decay * (1 + np.random.normal(0, 0.2)))
                values.append(value)
            
            data[metric] = values
        
        return {
            'data': data,
            'metrics': metrics,
            'start_date': start_date,
            'end_date': end_date,
            'video_id': video_id
        }
    
    def analyze_cpm_by_category(self, start_date=None, end_date=None):
        """
        Analyse le CPM par catégorie de contenu
        
        Args:
            start_date (str, optional): Date de début au format YYYY-MM-DD
            end_date (str, optional): Date de fin au format YYYY-MM-DD
            
        Returns:
            dict: Analyse du CPM par catégorie
        """
        # Pour une implémentation réelle, cette méthode analyserait les données
        # de plusieurs vidéos regroupées par catégorie.
        # Pour cette démonstration, nous simulons les données.
        
        # Définir les dates par défaut si non spécifiées
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        if not start_date:
            # Par défaut, 90 jours avant la date de fin
            start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y-%m-%d')
        
        print(f"Analyse du CPM par catégorie du {start_date} au {end_date}")
        
        # Catégories et leurs CPM moyens (basés sur la recherche)
        categories = {
            'finance': {'cpm': 15.0, 'videos': 5, 'views': 5000},
            'technology': {'cpm': 12.0, 'videos': 8, 'views': 8000},
            'health': {'cpm': 11.0, 'videos': 6, 'views': 6000},
            'business': {'cpm': 14.0, 'videos': 4, 'views': 4000},
            'education': {'cpm': 10.0, 'videos': 7, 'views': 7000}
        }
        
        # Ajouter une variation aléatoire
        for category, data in categories.items():
            data['cpm'] = data['cpm'] * (1 + np.random.normal(0, 0.1))
            data['revenue'] = data['cpm'] * data['views'] / 1000
        
        # Trier par CPM
        sorted_categories = sorted(categories.items(), key=lambda x: x[1]['cpm'], reverse=True)
        
        return {
            'categories': [item[0] for item in sorted_categories],
            'cpm_values': [item[1]['cpm'] for item in sorted_categories],
            'video_counts': [item[1]['videos'] for item in sorted_categories],
            'view_counts': [item[1]['views'] for item in sorted_categories],
            'revenue': [item[1]['revenue'] for item in sorted_categories],
            'start_date': start_date,
            'end_date': end_date
        }
    
    def analyze_performance_trends(self, metrics=None, period='month'):
        """
        Analyse les tendances de performance sur une période
        
        Args:
            metrics (list, optional): Liste des métriques à analyser
            period (str, optional): Période d'analyse ('week', 'month', 'quarter', 'year')
            
        Returns:
            dict: Analyse des tendances de performance
        """
        # Définir les métriques par défaut si non spécifiées
        if not metrics:
            metrics = ['views', 'estimatedRevenue', 'cpm', 'subscribersGained']
        
        # Déterminer les dates en fonction de la période
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        if period == 'week':
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            comparison_end = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            comparison_start = (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d')
        elif period == 'month':
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            comparison_end = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            comparison_start = (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d')
        elif period == 'quarter':
            start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            comparison_end = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            comparison_start = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
        else:  # year
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            comparison_end = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            comparison_start = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
        
        # Obtenir les données de performance pour la période actuelle
        current_data = self.get_channel_performance(start_date, end_date, metrics)
        
        # Obtenir les données de performance pour la période précédente
        previous_data = self.get_channel_performance(comparison_start, comparison_end, metrics)
        
        # Calculer les totaux pour chaque période
        current_totals = {metric: sum(current_data['data'].get(metric, [0])) for metric in metrics}
        previous_totals = {metric: sum(previous_data['data'].get(metric, [0])) for metric in metrics}
        
        # Calculer les variations en pourcentage
        changes = {}
        for metric in metrics:
            if previous_totals[metric] > 0:
                change_pct = ((current_totals[metric] - previous_totals[metric]) / previous_totals[metric]) * 100
            else:
                change_pct = 100  # Si la valeur précédente est 0, considérer comme 100% d'augmentation
            
            changes[metric] = {
                'current': current_totals[metric],
                'previous': previous_totals[metric],
                'change_pct': change_pct,
                'trend': 'up' if change_pct > 0 else 'down' if change_pct < 0 else 'stable'
            }
        
        return {
            'period': period,
            'start_date': start_date,
            'end_date': end_date,
            'comparison_start': comparison_start,
            'comparison_end': comparison_end,
            'metrics': metrics,
            'changes': changes
        }
    
    def generate_performance_report(self, report_type='weekly', output_format='json'):
        """
        Génère un rapport de performance complet
        
        Args:
            report_type (str, optional): Type de rapport ('daily', 'weekly', 'monthly')
            output_format (str, optional): Format de sortie ('json', 'csv', 'html')
            
        Returns:
            str: Chemin vers le rapport généré
        """
        # Déterminer les dates en fonction du type de rapport
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        if report_type == 'daily':
            start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            period = 'day'
        elif report_type == 'weekly':
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            period = 'week'
        else:  # monthly
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            period = 'month'
        
        # Métriques à inclure dans le rapport
        metrics = [
            'views', 'estimatedMinutesWatched', 'averageViewDuration',
            'subscribersGained', 'subscribersLost', 'likes', 'dislikes',
            'shares', 'comments', 'estimatedRevenue', 'cpm'
        ]
        
        # Récupérer les données de performance
        channel_data = self.get_channel_performance(start_date, end_date, metrics)
        
        # Analyser les tendances
        trends = self.analyze_performance_trends(metrics, period)
        
        # Analyser le CPM par catégorie
        cpm_analysis = self.analyze_cpm_by_category(start_date, end_date)
        
        # Assembler le rapport
        report = {
            'report_type': report_type,
            'generated_at': datetime.now().isoformat(),
            'period': {
                'start_date': start_date,
                'end_date': end_date
            },
            'channel_performance': channel_data,
            'performance_trends': trends,
            'cpm_analysis': cpm_analysis
        }
        
        # Générer le fichier de rapport
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"performance_report_{report_type}_{timestamp}"
        
        if output_format == 'json':
            output_path = os.path.join(self.data_dir, f"{filename}.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2)
        
        elif output_format == 'csv':
            output_path = os.path.join(self.data_dir, f"{filename}.csv")
            
            # Convertir les données en DataFrame
            df = pd.DataFrame(channel_data['data'])
            df.to_csv(output_path, index=False)
        
        elif output_format == 'html':
            output_path = os.path.join(self.data_dir, f"{filename}.html")
            
            # Créer un rapport HTML simple
            html_content = f"""
            <html>
            <head>
                <title>Rapport de performance {report_type}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1, h2 {{ color: #333; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                    tr:nth-child(even) {{ background-color: #f9f9f9; }}
                </style>
            </head>
            <body>
                <h1>Rapport de performance {report_type}</h1>
                <p>Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Période: {start_date} à {end_date}</p>
                
                <h2>Résumé des performances</h2>
                <table>
                    <tr>
                        <th>Métrique</th>
                        <th>Valeur actuelle</th>
                        <th>Valeur précédente</th>
                        <th>Variation</th>
                    </tr>
            """
            
            # Ajouter les métriques de tendance
            for metric in metrics:
                if metric in trends['changes']:
                    change = trends['changes'][metric]
                    html_content += f"""
                    <tr>
                        <td>{self.available_metrics.get(metric, metric)}</td>
                        <td>{change['current']:.2f}</td>
                        <td>{change['previous']:.2f}</td>
                        <td>{change['change_pct']:.2f}% ({change['trend']})</td>
                    </tr>
                    """
            
            html_content += """
                </table>
                
                <h2>Analyse du CPM par catégorie</h2>
                <table>
                    <tr>
                        <th>Catégorie</th>
                        <th>CPM moyen</th>
                        <th>Nombre de vidéos</th>
                        <th>Vues totales</th>
                        <th>Revenus estimés</th>
                    </tr>
            """
            
            # Ajouter les données de CPM par catégorie
            for i, category in enumerate(cpm_analysis['categories']):
                html_content += f"""
                <tr>
                    <td>{category}</td>
                    <td>${cpm_analysis['cpm_values'][i]:.2f}</td>
                    <td>{cpm_analysis['video_counts'][i]}</td>
                    <td>{cpm_analysis['view_counts'][i]}</td>
                    <td>${cpm_analysis['revenue'][i]:.2f}</td>
                </tr>
                """
            
            html_content += """
                </table>
            </body>
            </html>
            """
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        print(f"Rapport de performance généré: {output_path}")
        return output_path
    
    def generate_performance_charts(self, metrics=None, start_date=None, end_date=None, output_dir=None):
        """
        Génère des graphiques de performance
        
        Args:
            metrics (list, optional): Liste des métriques à visualiser
            start_date (str, optional): Date de début au format YYYY-MM-DD
            end_date (str, optional): Date de fin au format YYYY-MM-DD
            output_dir (str, optional): Répertoire de sortie pour les graphiques
            
        Returns:
            list: Liste des chemins vers les graphiques générés
        """
        # Définir les métriques par défaut si non spécifiées
        if not metrics:
            metrics = ['views', 'estimatedRevenue', 'cpm', 'subscribersGained']
        
        # Définir les dates par défaut si non spécifiées
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        if not start_date:
            # Par défaut, 30 jours avant la date de fin
            start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d')
        
        # Définir le répertoire de sortie
        output_dir = output_dir or os.path.join(self.data_dir, 'charts')
        os.makedirs(output_dir, exist_ok=True)
        
        # Récupérer les données de performance
        performance_data = self.get_channel_performance(start_date, end_date, metrics)
        
        # Générer un graphique pour chaque métrique
        chart_paths = []
        
        for metric in metrics:
            if metric in performance_data['data']:
                # Créer le graphique
                plt.figure(figsize=(10, 6))
                plt.plot(performance_data['data']['dates'], performance_data['data'][metric])
                plt.title(f"{self.available_metrics.get(metric, metric)} ({start_date} à {end_date})")
                plt.xlabel('Date')
                plt.ylabel(self.available_metrics.get(metric, metric))
                plt.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                # Sauvegarder le graphique
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                chart_path = os.path.join(output_dir, f"{metric}_chart_{timestamp}.png")
                plt.savefig(chart_path)
                plt.close()
                
                chart_paths.append(chart_path)
        
        # Générer un graphique de comparaison des CPM par catégorie
        cpm_analysis = self.analyze_cpm_by_category(start_date, end_date)
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(cpm_analysis['categories'], cpm_analysis['cpm_values'])
        
        # Ajouter les valeurs au-dessus des barres
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'${height:.2f}', ha='center', va='bottom')
        
        plt.title(f"CPM par catégorie ({start_date} à {end_date})")
        plt.xlabel('Catégorie')
        plt.ylabel('CPM ($)')
        plt.grid(True, axis='y')
        plt.tight_layout()
        
        # Sauvegarder le graphique
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        cpm_chart_path = os.path.join(output_dir, f"cpm_by_category_{timestamp}.png")
        plt.savefig(cpm_chart_path)
        plt.close()
        
        chart_paths.append(cpm_chart_path)
        
        print(f"Graphiques de performance générés: {len(chart_paths)}")
        return chart_paths
