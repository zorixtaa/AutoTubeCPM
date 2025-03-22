import unittest
import os
import sys
import json
from datetime import datetime

# Ajouter le répertoire parent au chemin pour importer les modules du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importer les modules du projet
from scripts.niche_discovery import NicheDiscovery
from scripts.content_generation import ContentGenerator
from scripts.tts import TTSEngine
from scripts.video_production import VideoProducer
from scripts.youtube_publishing import YouTubeAuth, YouTubePublisher
from scripts.analytics import PerformanceAnalyzer

class TestNicheDiscovery(unittest.TestCase):
    """Tests pour le module de découverte de niches"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.niche_discovery = NicheDiscovery()
    
    def test_high_cpm_categories(self):
        """Teste si les catégories à fort CPM sont correctement définies"""
        self.assertIn('finance', self.niche_discovery.high_cpm_categories)
        self.assertIn('technology', self.niche_discovery.high_cpm_categories)
        self.assertIn('business', self.niche_discovery.high_cpm_categories)
    
    def test_get_top_niches(self):
        """Teste la récupération des meilleures niches"""
        top_niches = self.niche_discovery.get_top_niches(count=3)
        self.assertIsInstance(top_niches, list)
        self.assertLessEqual(len(top_niches), 3)
    
    def test_generate_topic_ideas(self):
        """Teste la génération d'idées de sujets"""
        ideas = self.niche_discovery.generate_topic_ideas('finance', 'investing', count=3)
        self.assertIsInstance(ideas, list)
        self.assertEqual(len(ideas), 3)

class TestContentGenerator(unittest.TestCase):
    """Tests pour le module de génération de contenu"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.content_generator = ContentGenerator()
    
    def test_script_templates(self):
        """Teste si les templates de script sont correctement chargés"""
        self.assertIn('finance', self.content_generator.script_templates)
        self.assertIn('technology', self.content_generator.script_templates)
        self.assertIn('default', self.content_generator.script_templates)
    
    def test_generate_script(self):
        """Teste la génération d'un script"""
        script_data = self.content_generator.generate_script_with_manus(
            topic="Test Investment Strategies",
            category="finance",
            subcategory="investing",
            target_audience="beginners"
        )
        self.assertIsInstance(script_data, dict)
        self.assertIn('script', script_data)
        self.assertIn('metadata', script_data)
    
    def test_format_script_for_tts(self):
        """Teste le formatage d'un script pour la synthèse vocale"""
        script_data = {
            'title': 'Test Script',
            'hook': 'This is a hook',
            'topic_intro': 'This is an intro',
            'learning_points': 'These are learning points',
            'section1_title': 'Section 1',
            'section1_point1': 'Point 1.1',
            'section1_point2': 'Point 1.2',
            'section1_example': 'Example 1',
            'section2_title': 'Section 2',
            'section2_point1': 'Point 2.1',
            'section2_point2': 'Point 2.2',
            'section2_example': 'Example 2',
            'section3_title': 'Section 3',
            'section3_point1': 'Point 3.1',
            'section3_point2': 'Point 3.2',
            'section3_example': 'Example 3',
            'recap': 'This is a recap',
            'call_to_action': 'This is a call to action',
            'engagement_question': 'This is a question'
        }
        tts_text = self.content_generator.format_script_for_tts(script_data)
        self.assertIsInstance(tts_text, str)
        self.assertIn('This is a hook', tts_text)
        self.assertIn('This is an intro', tts_text)

class TestTTSEngine(unittest.TestCase):
    """Tests pour le module de synthèse vocale"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.tts_engine = TTSEngine()
    
    def test_available_voices(self):
        """Teste si les voix disponibles sont correctement définies"""
        self.assertIn('male_professional', self.tts_engine.available_voices)
        self.assertIn('female_professional', self.tts_engine.available_voices)
    
    def test_generate_speech(self):
        """Teste la génération d'un fichier audio"""
        audio_path = self.tts_engine.generate_speech(
            text="This is a test speech synthesis.",
            voice_id="male_professional"
        )
        self.assertTrue(os.path.exists(audio_path))
    
    def test_get_voice_recommendations(self):
        """Teste les recommandations de voix"""
        recommendations = self.tts_engine.get_voice_recommendations('finance', 'investing')
        self.assertIsInstance(recommendations, list)
        self.assertIn('male_professional', recommendations)

class TestVideoProducer(unittest.TestCase):
    """Tests pour le module d'assemblage vidéo"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.video_producer = VideoProducer()
        
        # Créer un fichier audio de test
        self.tts_engine = TTSEngine()
        self.audio_path = self.tts_engine.generate_speech(
            text="This is a test speech for video production.",
            voice_id="male_professional"
        )
        
        # Données de script de test
        self.script_data = {
            'title': 'Test Video',
            'hook': 'This is a hook',
            'topic_intro': 'This is an intro',
            'learning_points': 'These are learning points',
            'section1_title': 'Section 1',
            'section1_point1': 'Point 1.1',
            'section1_point2': 'Point 1.2',
            'section1_example': 'Example 1',
            'section2_title': 'Section 2',
            'section2_point1': 'Point 2.1',
            'section2_point2': 'Point 2.2',
            'section2_example': 'Example 2',
            'section3_title': 'Section 3',
            'section3_point1': 'Point 3.1',
            'section3_point2': 'Point 3.2',
            'section3_example': 'Example 3',
            'recap': 'This is a recap',
            'call_to_action': 'This is a call to action',
            'engagement_question': 'This is a question'
        }
        
        # Métadonnées de test
        self.metadata = {
            'youtube_title': 'Test Video',
            'youtube_description': 'This is a test video description',
            'youtube_tags': ['test', 'video', 'autotubecpm'],
            'youtube_category_id': 22,
            'is_made_for_kids': False,
            'visibility': 'private',
            'notify_subscribers': False
        }
    
    def test_create_video(self):
        """Teste la création d'une vidéo"""
        video_path = self.video_producer.create_video(
            audio_path=self.audio_path,
            script_data=self.script_data,
            metadata=self.metadata,
            visual_style="dynamic",
            resolution=(640, 360),  # Résolution réduite pour les tests
            fps=24,
            use_intro_outro=True
        )
        self.assertTrue(os.path.exists(video_path))

class TestYouTubePublisher(unittest.TestCase):
    """Tests pour le module de publication YouTube"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        # Nous ne pouvons pas tester l'authentification réelle sans identifiants
        # Nous utilisons donc une instance simulée
        self.youtube_publisher = YouTubePublisher(auth=None)
    
    def test_prepare_metadata(self):
        """Teste la préparation des métadonnées"""
        metadata = {
            'youtube_title': 'Test Video',
            'youtube_description': 'This is a test video description',
            'youtube_tags': ['test', 'video', 'autotubecpm'],
            'youtube_category_id': 22,
            'is_made_for_kids': False,
            'visibility': 'private',
            'notify_subscribers': False
        }
        
        prepared_metadata = self.youtube_publisher._prepare_metadata(metadata)
        self.assertEqual(prepared_metadata['snippet']['title'], 'Test Video')
        self.assertEqual(prepared_metadata['snippet']['description'], 'This is a test video description')
        self.assertEqual(prepared_metadata['snippet']['tags'], ['test', 'video', 'autotubecpm'])
        self.assertEqual(prepared_metadata['snippet']['categoryId'], 22)
        self.assertEqual(prepared_metadata['status']['privacyStatus'], 'private')
    
    def test_simulate_upload(self):
        """Teste la simulation d'un téléchargement"""
        video_path = "/path/to/test/video.mp4"  # Chemin fictif
        metadata = {
            'youtube_title': 'Test Video',
            'youtube_description': 'This is a test video description',
            'youtube_tags': ['test', 'video', 'autotubecpm'],
            'youtube_category_id': 22,
            'is_made_for_kids': False,
            'visibility': 'private',
            'notify_subscribers': False
        }
        
        # Utiliser la méthode de simulation
        result = self.youtube_publisher.simulate_upload(video_path, metadata)
        self.assertIsInstance(result, dict)
        self.assertIn('id', result)
        self.assertIn('snippet', result)

class TestPerformanceAnalyzer(unittest.TestCase):
    """Tests pour le module d'analyse de performance"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.performance_analyzer = PerformanceAnalyzer()
    
    def test_available_metrics(self):
        """Teste si les métriques disponibles sont correctement définies"""
        self.assertIn('views', self.performance_analyzer.available_metrics)
        self.assertIn('estimatedRevenue', self.performance_analyzer.available_metrics)
        self.assertIn('cpm', self.performance_analyzer.available_metrics)
    
    def test_simulate_channel_performance(self):
        """Teste la simulation des performances de la chaîne"""
        start_date = (datetime.now().replace(day=1)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        metrics = ['views', 'estimatedRevenue', 'cpm']
        
        performance = self.performance_analyzer._simulate_channel_performance(start_date, end_date, metrics)
        self.assertIsInstance(performance, dict)
        self.assertIn('data', performance)
        self.assertIn('metrics', performance)
        self.assertIn('views', performance['data'])
        self.assertIn('estimatedRevenue', performance['data'])
        self.assertIn('cpm', performance['data'])
    
    def test_analyze_cpm_by_category(self):
        """Teste l'analyse du CPM par catégorie"""
        analysis = self.performance_analyzer.analyze_cpm_by_category()
        self.assertIsInstance(analysis, dict)
        self.assertIn('categories', analysis)
        self.assertIn('cpm_values', analysis)
        self.assertEqual(len(analysis['categories']), len(analysis['cpm_values']))

class TestIntegration(unittest.TestCase):
    """Tests d'intégration pour vérifier l'interaction entre les modules"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.niche_discovery = NicheDiscovery()
        self.content_generator = ContentGenerator()
        self.tts_engine = TTSEngine()
        self.video_producer = VideoProducer()
        self.performance_analyzer = PerformanceAnalyzer()
    
    def test_end_to_end_workflow(self):
        """Teste le flux de travail complet de bout en bout"""
        # 1. Découvrir une niche
        top_niches = self.niche_discovery.get_top_niches(count=1)
        self.assertIsInstance(top_niches, list)
        self.assertGreater(len(top_niches), 0)
        
        niche = top_niches[0]
        category = niche['category']
        subcategory = niche['subcategory']
        
        # 2. Générer des idées de sujets
        ideas = self.niche_discovery.generate_topic_ideas(category, subcategory, count=1)
        self.assertIsInstance(ideas, list)
        self.assertGreater(len(ideas), 0)
        
        topic = ideas[0]
        
        # 3. Générer un script
        script_data = self.content_generator.generate_script_with_manus(
            topic=topic,
            category=category,
            subcategory=subcategory
        )
        self.assertIsInstance(script_data, dict)
        self.assertIn('script', script_data)
        self.assertIn('metadata', script_data)
        
        # 4. Formater le script pour la synthèse vocale
        tts_text = self.content_generator.format_script_for_tts(script_data['script'])
        self.assertIsInstance(tts_text, str)
        
        # 5. Générer l'audio
        audio_path = self.tts_engine.generate_speech(
            text=tts_text[:100],  # Utiliser seulement les 100 premiers caractères pour le test
            voice_id="male_professional"
        )
        self.assertTrue(os.path.exists(audio_path))
        
        # 6. Créer une vidéo
        video_path = self.video_producer.create_video(
            audio_path=audio_path,
            script_data=script_data['script'],
            metadata=script_data['metadata'],
            visual_style="dynamic",
            resolution=(640, 360),  # Résolution réduite pour les tests
            fps=24,
            use_intro_outro=True
        )
        self.assertTrue(os.path.exists(video_path))
        
        # 7. Analyser les performances (simulation)
        analysis = self.performance_analyzer.analyze_cpm_by_category()
        self.assertIsInstance(analysis, dict)
        self.assertIn('categories', analysis)
        self.assertIn('cpm_values', analysis)

if __name__ == '__main__':
    unittest.main()
