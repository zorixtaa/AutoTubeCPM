"""
Module de découverte de niches pour AutoTubeCPM
Ce module analyse les tendances et identifie les niches à fort CPM
"""

import os
import json
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class NicheDiscovery:
    """Classe pour découvrir et analyser les niches à fort CPM"""
    
    def __init__(self, google_api_key=None, niche_db_path=None):
        """
        Initialise le module de découverte de niches
        
        Args:
            google_api_key (str, optional): Clé API Google pour l'accès à YouTube Data API
            niche_db_path (str, optional): Chemin vers la base de données de niches
        """
        self.google_api_key = google_api_key
        self.niche_db_path = niche_db_path or os.path.join(os.path.dirname(__file__), '../../data/niche_database.json')
        self.youtube_service = None
        self.niche_database = self._load_niche_database()
        
        # Niches à fort CPM connues (basées sur la recherche)
        self.high_cpm_categories = {
            'finance': {
                'base_cpm': 15.0,
                'subcategories': {
                    'investing': 18.0,
                    'cryptocurrency': 20.0,
                    'personal_finance': 16.0,
                    'stock_market': 17.0,
                    'real_estate': 16.5
                }
            },
            'technology': {
                'base_cpm': 12.0,
                'subcategories': {
                    'software_reviews': 13.0,
                    'gadget_reviews': 14.0,
                    'programming': 12.5,
                    'ai_machine_learning': 15.0,
                    'saas': 16.0
                }
            },
            'health': {
                'base_cpm': 11.0,
                'subcategories': {
                    'fitness': 12.0,
                    'nutrition': 13.0,
                    'mental_health': 11.5,
                    'medical_information': 14.0,
                    'supplements': 13.5
                }
            },
            'business': {
                'base_cpm': 14.0,
                'subcategories': {
                    'entrepreneurship': 15.0,
                    'marketing': 16.0,
                    'ecommerce': 14.5,
                    'b2b': 17.0,
                    'productivity': 13.0
                }
            },
            'education': {
                'base_cpm': 10.0,
                'subcategories': {
                    'online_courses': 12.0,
                    'language_learning': 11.0,
                    'academic_subjects': 10.5,
                    'professional_certifications': 13.0,
                    'career_development': 12.5
                }
            }
        }
    
    def _load_niche_database(self):
        """
        Charge la base de données de niches ou en crée une nouvelle si elle n'existe pas
        
        Returns:
            dict: Base de données de niches
        """
        if os.path.exists(self.niche_db_path):
            try:
                with open(self.niche_db_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Erreur lors du chargement de la base de données de niches. Création d'une nouvelle.")
        
        # Créer le répertoire parent si nécessaire
        os.makedirs(os.path.dirname(self.niche_db_path), exist_ok=True)
        
        # Créer une nouvelle base de données
        niche_db = {
            'last_updated': datetime.now().isoformat(),
            'niches': {},
            'historical_data': {}
        }
        
        # Sauvegarder la base de données vide
        with open(self.niche_db_path, 'w') as f:
            json.dump(niche_db, f, indent=2)
        
        return niche_db
    
    def _save_niche_database(self):
        """Sauvegarde la base de données de niches"""
        self.niche_database['last_updated'] = datetime.now().isoformat()
        
        with open(self.niche_db_path, 'w') as f:
            json.dump(self.niche_database, f, indent=2)
    
    def _get_youtube_service(self):
        """
        Initialise le service YouTube API
        
        Returns:
            object: Service YouTube API
        """
        if not self.youtube_service and self.google_api_key:
            self.youtube_service = build('youtube', 'v3', developerKey=self.google_api_key)
        return self.youtube_service
    
    def get_trending_topics(self, region_code='US', category_id=None, max_results=50):
        """
        Récupère les sujets tendance sur YouTube
        
        Args:
            region_code (str, optional): Code de région (pays). Par défaut 'US'
            category_id (str, optional): ID de catégorie YouTube
            max_results (int, optional): Nombre maximum de résultats. Par défaut 50
            
        Returns:
            list: Liste des vidéos tendance
        """
        try:
            youtube = self._get_youtube_service()
            
            if not youtube:
                print("Service YouTube non disponible. Vérifiez votre clé API.")
                return []
            
            # Paramètres de la requête
            params = {
                'part': 'snippet,contentDetails,statistics',
                'chart': 'mostPopular',
                'regionCode': region_code,
                'maxResults': max_results
            }
            
            if category_id:
                params['videoCategoryId'] = category_id
            
            # Exécuter la requête
            request = youtube.videos().list(**params)
            response = request.execute()
            
            return response.get('items', [])
            
        except HttpError as e:
            print(f"Erreur lors de la récupération des tendances: {e}")
            return []
    
    def analyze_video_for_niche(self, video_item):
        """
        Analyse une vidéo pour déterminer sa niche
        
        Args:
            video_item (dict): Élément vidéo de l'API YouTube
            
        Returns:
            dict: Informations sur la niche de la vidéo
        """
        snippet = video_item.get('snippet', {})
        statistics = video_item.get('statistics', {})
        
        # Extraire les informations pertinentes
        title = snippet.get('title', '')
        description = snippet.get('description', '')
        tags = snippet.get('tags', [])
        category_id = snippet.get('categoryId', '')
        view_count = int(statistics.get('viewCount', 0))
        like_count = int(statistics.get('likeCount', 0))
        comment_count = int(statistics.get('commentCount', 0))
        
        # Calculer l'engagement
        engagement_rate = 0
        if view_count > 0:
            engagement_rate = (like_count + comment_count) / view_count
        
        # Déterminer la niche basée sur le contenu
        niche_info = self._classify_content(title, description, tags, category_id)
        
        # Ajouter les métriques d'engagement
        niche_info['engagement'] = {
            'view_count': view_count,
            'like_count': like_count,
            'comment_count': comment_count,
            'engagement_rate': engagement_rate
        }
        
        return niche_info
    
    def _classify_content(self, title, description, tags, category_id):
        """
        Classifie le contenu dans une niche
        
        Args:
            title (str): Titre de la vidéo
            description (str): Description de la vidéo
            tags (list): Tags de la vidéo
            category_id (str): ID de catégorie YouTube
            
        Returns:
            dict: Informations sur la niche
        """
        # Convertir tout en minuscules pour la comparaison
        title_lower = title.lower()
        description_lower = description.lower()
        tags_lower = [tag.lower() for tag in tags]
        
        # Combinaison de tout le texte pour l'analyse
        all_text = ' '.join([title_lower, description_lower, ' '.join(tags_lower)])
        
        # Initialiser les scores pour chaque catégorie principale
        category_scores = {category: 0 for category in self.high_cpm_categories.keys()}
        subcategory_scores = {}
        
        # Calculer les scores pour chaque catégorie et sous-catégorie
        for category, data in self.high_cpm_categories.items():
            # Vérifier si la catégorie est mentionnée
            if category in all_text:
                category_scores[category] += 5
            
            # Vérifier les sous-catégories
            for subcategory, cpm in data['subcategories'].items():
                subcategory_name = subcategory.replace('_', ' ')
                score = 0
                
                if subcategory_name in all_text:
                    score += 5
                
                # Stocker le score de la sous-catégorie
                if score > 0:
                    subcategory_key = f"{category}_{subcategory}"
                    subcategory_scores[subcategory_key] = score
                    category_scores[category] += score
        
        # Déterminer la catégorie principale
        main_category = max(category_scores.items(), key=lambda x: x[1])
        
        # Si aucune catégorie n'a de score, utiliser une approche plus générique
        if main_category[1] == 0:
            # Mots-clés génériques pour chaque catégorie
            category_keywords = {
                'finance': ['money', 'invest', 'stock', 'crypto', 'financial', 'budget', 'wealth'],
                'technology': ['tech', 'software', 'hardware', 'gadget', 'computer', 'phone', 'digital'],
                'health': ['health', 'fitness', 'workout', 'diet', 'nutrition', 'exercise', 'wellness'],
                'business': ['business', 'entrepreneur', 'startup', 'marketing', 'company', 'industry'],
                'education': ['learn', 'course', 'education', 'tutorial', 'guide', 'how to', 'lesson']
            }
            
            # Calculer les scores basés sur les mots-clés
            for category, keywords in category_keywords.items():
                for keyword in keywords:
                    if keyword in all_text:
                        category_scores[category] += 1
            
            # Recalculer la catégorie principale
            main_category = max(category_scores.items(), key=lambda x: x[1])
        
        # Si toujours aucun score, utiliser une catégorie par défaut
        if main_category[1] == 0:
            return {
                'category': 'unknown',
                'subcategory': 'general',
                'confidence': 0.0,
                'estimated_cpm': 5.0  # CPM moyen par défaut
            }
        
        # Déterminer la sous-catégorie
        main_category_name = main_category[0]
        subcategories = self.high_cpm_categories[main_category_name]['subcategories']
        
        # Filtrer les scores de sous-catégorie pour la catégorie principale
        relevant_subcategories = {k.split('_')[1]: v for k, v in subcategory_scores.items() 
                                if k.startswith(main_category_name)}
        
        # Si aucune sous-catégorie n'a de score, utiliser la base CPM
        if not relevant_subcategories:
            return {
                'category': main_category_name,
                'subcategory': 'general',
                'confidence': min(main_category[1] / 10, 1.0),
                'estimated_cpm': self.high_cpm_categories[main_category_name]['base_cpm']
            }
        
        # Déterminer la sous-catégorie principale
        main_subcategory = max(relevant_subcategories.items(), key=lambda x: x[1])
        
        return {
            'category': main_category_name,
            'subcategory': main_subcategory[0],
            'confidence': min(main_category[1] / 10, 1.0),
            'estimated_cpm': subcategories.get(main_subcategory[0], 
                                              self.high_cpm_categories[main_category_name]['base_cpm'])
        }
    
    def analyze_trending_niches(self, region_code='US', max_results=50):
        """
        Analyse les niches tendance sur YouTube
        
        Args:
            region_code (str, optional): Code de région (pays). Par défaut 'US'
            max_results (int, optional): Nombre maximum de résultats. Par défaut 50
            
        Returns:
            dict: Analyse des niches tendance
        """
        trending_videos = self.get_trending_topics(region_code, max_results=max_results)
        
        if not trending_videos:
            return {
                'status': 'error',
                'message': 'Aucune vidéo tendance trouvée'
            }
        
        # Analyser chaque vidéo
        niche_data = []
        for video in trending_videos:
            video_id = video.get('id')
            snippet = video.get('snippet', {})
            
            niche_info = self.analyze_video_for_niche(video)
            
            niche_data.append({
                'video_id': video_id,
                'title': snippet.get('title', ''),
                'channel_title': snippet.get('channelTitle', ''),
                'published_at': snippet.get('publishedAt', ''),
                'niche': niche_info
            })
        
        # Agréger les données par niche
        niche_summary = {}
        for data in niche_data:
            category = data['niche']['category']
            subcategory = data['niche']['subcategory']
            key = f"{category}_{subcategory}"
            
            if key not in niche_summary:
                niche_summary[key] = {
                    'category': category,
                    'subcategory': subcategory,
                    'video_count': 0,
                    'total_views': 0,
                    'total_likes': 0,
                    'total_comments': 0,
                    'avg_engagement_rate': 0,
                    'estimated_cpm': data['niche']['estimated_cpm'],
                    'videos': []
                }
            
            niche_summary[key]['video_count'] += 1
            niche_summary[key]['total_views'] += data['niche']['engagement']['view_count']
            niche_summary[key]['total_likes'] += data['niche']['engagement']['like_count']
            niche_summary[key]['total_comments'] += data['niche']['engagement']['comment_count']
            niche_summary[key]['videos'].append({
                'video_id': data['video_id'],
                'title': data['title'],
                'channel_title': data['channel_title']
            })
        
        # Calculer les moyennes et finaliser le résumé
        for key, summary in niche_summary.items():
            if summary['video_count'] > 0:
                summary['avg_views'] = summary['total_views'] / summary['video_count']
                
                if summary['total_views'] > 0:
                    summary['avg_engagement_rate'] = (summary['total_likes'] + summary['total_comments']) / summary['total_views']
        
        # Trier les niches par CPM estimé
        sorted_niches = sorted(niche_summary.values(), key=lambda x: x['estimated_cpm'], reverse=True)
        
        # Mettre à jour la base de données de niches
        self._update_niche_database(sorted_niches, region_code)
        
        return {
            'status': 'success',
            'date': datetime.now().isoformat(),
            'region_code': region_code,
            'total_videos_analyzed': len(trending_videos),
            'niches': sorted_niches
        }
    
    def _update_niche_database(self, niche_data, region_code):
        """
        Met à jour la base de données de niches avec de nouvelles données
        
        Args:
            niche_data (list): Données de niches à ajouter
            region_code (str): Code de région
        """
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Mettre à jour les données historiques
        if today not in self.niche_database['historical_data']:
            self.niche_database['historical_data'][today] = {}
        
        self.niche_database['historical_data'][today][region_code] = niche_data
        
        # Mettre à jour les niches actuelles
        for niche in niche_data:
            key = f"{niche['category']}_{niche['subcategory']}"
            
            if key not in self.niche_database['niches']:
                self.niche_database['niches'][key] = {
                    'category': niche['category'],
                    'subcategory': niche['subcategory'],
                    'first_seen': today,
                    'last_seen': today,
                    'historical_cpm': {},
                    'historical_engagement': {},
                    'trend': 'stable'
                }
            
            # Mettre à jour les données de la niche
            self.niche_database['niches'][key]['last_seen'] = today
            self.niche_database['niches'][key]['historical_cpm'][today] = niche['estimated_cpm']
            self.niche_database['niches'][key]['historical_engagement'][today] = niche.get('avg_engagement_rate', 0)
            
            # Calculer la tendance
            self._calculate_niche_trend(key)
        
        # Sauvegarder la base de données
        self._save_niche_database()
    
    def _calculate_niche_trend(self, niche_key):
        """
        Calcule la tendance d'une niche basée sur les données historiques
        
        Args:
            niche_key (str): Clé de la niche
        """
        niche = self.niche_database['niches'][niche_key]
        cpm_history = niche['historical_cpm']
        
        # Besoin d'au moins 2 points de données pour calculer une tendance
        if len(cpm_history) < 2:
            niche['trend'] = 'stable'
            return
        
        # Convertir les dates en objets datetime pour le tri
        dates = sorted([datetime.strptime(date, '%Y-%m-%d') for date in cpm_history.keys()])
        
        # Prendre les 7 derniers jours au maximum
        recent_dates = dates[-7:] if len(dates) > 7 else dates
        
        # Calculer la tendance
        if len(recent_dates) >= 2:
            first_date = recent_dates[0].strftime('%Y-%m-%d')
            last_date = recent_dates[-1].strftime('%Y-%m-%d')
            
            first_cpm = cpm_history[first_date]
            last_cpm = cpm_history[last_date]
            
            # Calculer le changement en pourcentage
            percent_change = ((last_cpm - first_cpm) / first_cpm) * 100
            
            # Déterminer la tendance
            if percent_change > 5:
                niche['trend'] = 'up'
            elif percent_change < -5:
                niche['trend'] = 'down'
            else:
                niche['trend'] = 'stable'
    
    def get_top_niches(self, count=10, min_videos=3, region_code='US'):
        """
        Récupère les meilleures niches basées sur le CPM estimé
        
        Args:
            count (int, optional): Nombre de niches à retourner. Par défaut 10
            min_videos (int, optional): Nombre minimum de vidéos pour considérer une niche. Par défaut 3
            region_code (str, optional): Code de région. Par défaut 'US'
            
        Returns:
            list: Liste des meilleures niches
        """
        # Vérifier si nous avons des données récentes
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Si nous n'avons pas de données récentes, analyser les tendances
        if (today not in self.niche_database.get('historical_data', {}) and 
            yesterday not in self.niche_database.get('historical_data', {})):
            self.analyze_trending_niches(region_code=region_code)
        
        # Récupérer toutes les niches
        all_niches = []
        for key, niche in self.niche_database['niches'].items():
            # Calculer le CPM moyen des 7 derniers jours
            cpm_history = niche['historical_cpm']
            recent_cpms = [cpm for date, cpm in cpm_history.items() 
                          if datetime.strptime(date, '%Y-%m-%d') >= datetime.now() - timedelta(days=7)]
            
            avg_cpm = sum(recent_cpms) / len(recent_cpms) if recent_cpms else 0
            
            all_niches.append({
                'category': niche['category'],
                'subcategory': niche['subcategory'],
                'avg_cpm': avg_cpm,
                'trend': niche['trend'],
                'last_seen': niche['last_seen']
            })
        
        # Filtrer et trier les niches
        recent_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        filtered_niches = [niche for niche in all_niches 
                          if datetime.strptime(niche['last_seen'], '%Y-%m-%d') >= datetime.strptime(recent_date, '%Y-%m-%d')]
        
        sorted_niches = sorted(filtered_niches, key=lambda x: x['avg_cpm'], reverse=True)
        
        return sorted_niches[:count]
    
    def generate_topic_ideas(self, category, subcategory, count=5):
        """
        Génère des idées de sujets pour une niche spécifique
        
        Args:
            category (str): Catégorie principale
            subcategory (str): Sous-catégorie
            count (int, optional): Nombre d'idées à générer. Par défaut 5
            
        Returns:
            list: Liste d'idées de sujets
        """
        # Modèles de titres par catégorie
        title_templates = {
            'finance': [
                "Top {n} Ways to {action} Your {financial_item} in {year}",
                "How to {action} {financial_item} - Complete Guide for Beginners",
                "The Truth About {financial_item} That Nobody Tells You",
                "{n} {financial_item} Mistakes to Avoid in {year}",
                "Why {financial_item} Is the Best Investment for {target_audience}"
            ],
            'technology': [
                "{product} Review - Is It Worth It in {year}?",
                "Top {n} {product_type} for {use_case} in {year}",
                "How to {action} with {product} - Step by Step Tutorial",
                "{n} Hidden Features of {product} You Didn't Know About",
                "Why {product} is Better Than {competitor_product}"
            ],
            'health': [
                "Top {n} {health_item} for {health_goal}",
                "How to {action} Your {body_part} in Just {time_period}",
                "{n} {diet_type} Recipes for {health_goal}",
                "The Truth About {health_topic} - What Doctors Won't Tell You",
                "Why You Should Start {health_activity} Today"
            ],
            'business': [
                "{n} Ways to {action} Your {business_type} in {year}",
                "How to Start a {business_type} with Just ${amount}",
                "The Secret to {business_goal} That Nobody Talks About",
                "Why {business_strategy} Is Essential for {business_type} Owners",
                "{n} {business_tool} Tools Every {professional_type} Needs"
            ],
            'education': [
                "Learn {subject} in {time_period} - Complete Guide",
                "Top {n} Resources to Master {subject}",
                "Why {subject} Is Important for {career_path}",
                "How to {action} {subject} - From Beginner to Expert",
                "{n} {subject} Exercises to Improve Your Skills"
            ]
        }
        
        # Données de remplacement par catégorie
        replacement_data = {
            'finance': {
                'n': ['5', '7', '10', '12', '15'],
                'action': ['Grow', 'Invest', 'Save', 'Manage', 'Maximize', 'Protect'],
                'financial_item': ['Money', 'Investments', 'Retirement Fund', 'Stock Portfolio', 'Crypto Assets', 'Savings'],
                'year': ['2025', '2026'],
                'target_audience': ['Beginners', 'Young Adults', 'Retirees', 'Entrepreneurs', 'Everyone']
            },
            'technology': {
                'n': ['5', '7', '10', '12', '15'],
                'product': ['iPhone 16', 'Samsung Galaxy S25', 'MacBook Pro', 'Windows 11', 'iPad Pro', 'Tesla Model Y'],
                'product_type': ['Smartphones', 'Laptops', 'Tablets', 'Smart Home Devices', 'Cameras', 'Headphones'],
                'use_case': ['Productivity', 'Gaming', 'Content Creation', 'Students', 'Professionals'],
                'action': ['Edit Videos', 'Take Better Photos', 'Increase Productivity', 'Save Battery Life', 'Customize'],
                'year': ['2025', '2026'],
                'competitor_product': ['Android', 'iPhone', 'Windows PC', 'MacBook', 'Google Home', 'Alexa']
            },
            'health': {
                'n': ['5', '7', '10', '12', '15'],
                'health_item': ['Supplements', 'Exercises', 'Foods', 'Habits', 'Workouts'],
                'health_goal': ['Weight Loss', 'Muscle Gain', 'Better Sleep', 'More Energy', 'Longevity'],
                'action': ['Strengthen', 'Tone', 'Improve', 'Heal', 'Detox'],
                'body_part': ['Abs', 'Core', 'Back', 'Arms', 'Legs', 'Whole Body'],
                'time_period': ['7 Days', '2 Weeks', '30 Days', 'One Month'],
                'diet_type': ['Keto', 'Vegan', 'Paleo', 'Mediterranean', 'Low-Carb'],
                'health_topic': ['Vitamins', 'Fasting', 'Cardio', 'Strength Training', 'Supplements'],
                'health_activity': ['Yoga', 'Meditation', 'Intermittent Fasting', 'Strength Training', 'Walking']
            },
            'business': {
                'n': ['5', '7', '10', '12', '15'],
                'action': ['Grow', 'Scale', 'Market', 'Automate', 'Optimize'],
                'business_type': ['E-commerce Store', 'SaaS Business', 'Consulting Practice', 'YouTube Channel', 'Startup'],
                'year': ['2025', '2026'],
                'amount': ['100', '500', '1000', '5000'],
                'business_goal': ['Passive Income', 'Customer Acquisition', 'Brand Building', 'Sales Growth'],
                'business_strategy': ['Content Marketing', 'SEO', 'Social Media', 'Email Marketing', 'Automation'],
                'business_tool': ['Marketing', 'Productivity', 'Accounting', 'CRM', 'Analytics'],
                'professional_type': ['Entrepreneurs', 'Freelancers', 'Small Business Owners', 'Marketers', 'Creators']
            },
            'education': {
                'n': ['5', '7', '10', '12', '15'],
                'subject': ['Python Programming', 'Digital Marketing', 'Data Science', 'Graphic Design', 'Public Speaking'],
                'time_period': ['7 Days', '2 Weeks', '30 Days', 'One Month'],
                'career_path': ['Tech Careers', 'Marketing', 'Business', 'Creative Fields', 'Personal Development'],
                'action': ['Master', 'Learn', 'Understand', 'Practice', 'Teach']
            }
        }
        
        import random
        
        # Vérifier si la catégorie existe
        if category not in title_templates:
            return [f"No templates available for category: {category}"]
        
        # Sélectionner les modèles pour la catégorie
        templates = title_templates[category]
        data = replacement_data[category]
        
        # Générer les idées
        ideas = []
        for _ in range(count):
            # Sélectionner un modèle aléatoire
            template = random.choice(templates)
            
            # Remplacer les variables
            idea = template
            for key, values in data.items():
                if '{' + key + '}' in idea:
                    idea = idea.replace('{' + key + '}', random.choice(values))
            
            ideas.append(idea)
        
        return ideas
