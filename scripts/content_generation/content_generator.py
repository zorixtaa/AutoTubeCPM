"""
Module de génération de contenu pour AutoTubeCPM
Ce module utilise Manus AI pour générer des scripts vidéo et des métadonnées
"""

import os
import json
import time
import requests
from datetime import datetime

class ContentGenerator:
    """Classe pour générer du contenu vidéo optimisé pour YouTube"""
    
    def __init__(self, templates_dir=None, output_dir=None):
        """
        Initialise le générateur de contenu
        
        Args:
            templates_dir (str, optional): Répertoire contenant les templates de scripts
            output_dir (str, optional): Répertoire de sortie pour les scripts générés
        """
        self.templates_dir = templates_dir or os.path.join(os.path.dirname(__file__), '../../assets/templates')
        self.output_dir = output_dir or os.path.join(os.path.dirname(__file__), '../../data/generated_content')
        
        # Créer les répertoires s'ils n'existent pas
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Templates par catégorie
        self.script_templates = {
            'finance': self._load_template('finance_template.txt'),
            'technology': self._load_template('technology_template.txt'),
            'health': self._load_template('health_template.txt'),
            'business': self._load_template('business_template.txt'),
            'education': self._load_template('education_template.txt'),
            'default': self._get_default_template()
        }
    
    def _load_template(self, filename):
        """
        Charge un template depuis un fichier
        
        Args:
            filename (str): Nom du fichier template
            
        Returns:
            str: Contenu du template ou template par défaut si le fichier n'existe pas
        """
        template_path = os.path.join(self.templates_dir, filename)
        
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # Créer un template par défaut si le fichier n'existe pas
            default_template = self._get_default_template()
            
            # Sauvegarder le template par défaut
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(default_template)
            
            return default_template
    
    def _get_default_template(self):
        """
        Retourne un template de script par défaut
        
        Returns:
            str: Template de script par défaut
        """
        return """# {title}

## Introduction
- Hook: {hook}
- Introduction du sujet: {topic_intro}
- Ce que le spectateur va apprendre: {learning_points}

## Section 1: {section1_title}
- Point principal 1: {section1_point1}
- Point principal 2: {section1_point2}
- Exemple ou illustration: {section1_example}

## Section 2: {section2_title}
- Point principal 1: {section2_point1}
- Point principal 2: {section2_point2}
- Exemple ou illustration: {section2_example}

## Section 3: {section3_title}
- Point principal 1: {section3_point1}
- Point principal 2: {section3_point2}
- Exemple ou illustration: {section3_example}

## Conclusion
- Récapitulation des points clés: {recap}
- Appel à l'action: {call_to_action}
- Question pour engagement: {engagement_question}

## Métadonnées YouTube
- Titre: {youtube_title}
- Description: {youtube_description}
- Tags: {youtube_tags}
"""
    
    def _create_template_files(self):
        """Crée les fichiers de template par défaut s'ils n'existent pas"""
        for category in ['finance', 'technology', 'health', 'business', 'education']:
            self._load_template(f'{category}_template.txt')
    
    def generate_script_with_manus(self, topic, category, subcategory, target_audience='general'):
        """
        Génère un script vidéo en utilisant Manus AI
        
        Dans une implémentation réelle, cette méthode ferait appel à l'API Manus.
        Pour cette démonstration, nous simulons la génération de contenu.
        
        Args:
            topic (str): Sujet de la vidéo
            category (str): Catégorie principale
            subcategory (str): Sous-catégorie
            target_audience (str, optional): Public cible. Par défaut 'general'
            
        Returns:
            dict: Script généré et métadonnées
        """
        print(f"Génération d'un script pour le sujet: {topic}")
        print(f"Catégorie: {category}, Sous-catégorie: {subcategory}")
        
        # Simuler un délai de génération
        time.sleep(1)
        
        # Sélectionner le template approprié
        template = self.script_templates.get(category, self.script_templates['default'])
        
        # Générer un script basé sur le template
        # Dans une implémentation réelle, ceci serait remplacé par un appel à Manus AI
        script_data = self._simulate_script_generation(topic, category, subcategory, target_audience, template)
        
        # Générer les métadonnées YouTube
        metadata = self._generate_metadata(topic, category, subcategory, script_data)
        
        # Combiner script et métadonnées
        result = {
            'script': script_data,
            'metadata': metadata,
            'generation_info': {
                'timestamp': datetime.now().isoformat(),
                'topic': topic,
                'category': category,
                'subcategory': subcategory,
                'target_audience': target_audience
            }
        }
        
        # Sauvegarder le résultat
        self._save_generated_content(result)
        
        return result
    
    def _simulate_script_generation(self, topic, category, subcategory, target_audience, template):
        """
        Simule la génération d'un script basé sur un template
        
        Args:
            topic (str): Sujet de la vidéo
            category (str): Catégorie principale
            subcategory (str): Sous-catégorie
            target_audience (str): Public cible
            template (str): Template de script
            
        Returns:
            dict: Données du script généré
        """
        # Générer un titre basé sur le sujet
        if "Top" in topic or "Best" in topic:
            title = topic
        else:
            title = f"The Ultimate Guide to {topic}"
        
        # Générer un hook accrocheur
        hooks = {
            'finance': f"Did you know that 80% of people are missing out on {topic}? Today, I'll show you how to be in the top 20%.",
            'technology': f"This {topic} is changing everything - and most people have no idea what's coming.",
            'health': f"What if I told you that you've been approaching {topic} all wrong? Today I'll reveal the truth.",
            'business': f"The top 1% of entrepreneurs use this {topic} strategy that I'm about to share with you.",
            'education': f"Master {topic} in half the time with these proven techniques that experts don't want you to know."
        }
        hook = hooks.get(category, f"Today we're diving deep into {topic} - and what you'll learn might surprise you.")
        
        # Générer une introduction
        topic_intro = f"{topic} has become increasingly important in today's world. Whether you're a beginner or experienced in {subcategory}, understanding the fundamentals is crucial."
        
        # Points d'apprentissage
        learning_points = f"In this video, you'll learn the key aspects of {topic}, common mistakes to avoid, and actionable strategies you can implement today."
        
        # Générer les sections
        sections = {
            'finance': [
                {"title": f"Understanding {topic} Basics", 
                 "point1": f"The fundamental principles of {topic} that everyone should know",
                 "point2": f"How {topic} differs from traditional approaches",
                 "example": f"For example, when investing in {subcategory}, most people focus only on returns but ignore risk factors."},
                {"title": f"Common {topic} Mistakes to Avoid", 
                 "point1": f"The biggest mistakes people make with {topic}",
                 "point2": f"How these mistakes can cost you thousands",
                 "example": f"I once had a client who ignored these warnings and lost over $10,000 in just three months."},
                {"title": f"Actionable {topic} Strategies", 
                 "point1": f"Step-by-step approach to mastering {topic}",
                 "point2": f"Tools and resources to help you succeed",
                 "example": f"Using this strategy, my students have seen an average improvement of 27% in their {subcategory} results."}
            ],
            'technology': [
                {"title": f"{topic} Features You Need to Know", 
                 "point1": f"The most important features of {topic}",
                 "point2": f"How these features compare to competitors",
                 "example": f"When testing {topic}, I discovered that the processing speed is 3x faster than similar products."},
                {"title": f"Setting Up {topic} Correctly", 
                 "point1": f"Step-by-step guide to optimal setup",
                 "point2": f"Common configuration mistakes to avoid",
                 "example": f"Most users skip this critical setting, which reduces performance by up to 40%."},
                {"title": f"Advanced {topic} Tips and Tricks", 
                 "point1": f"Lesser-known features that power users love",
                 "point2": f"Shortcuts and hacks to save time",
                 "example": f"This hidden menu gives you access to features that 95% of users don't even know exist."}
            ],
            'health': [
                {"title": f"The Science Behind {topic}", 
                 "point1": f"What research reveals about {topic}",
                 "point2": f"Common myths debunked by science",
                 "example": f"A recent study in the Journal of {subcategory} showed that traditional approaches are only 30% effective."},
                {"title": f"Implementing {topic} Into Your Routine", 
                 "point1": f"How to start with {topic} even if you're busy",
                 "point2": f"Creating sustainable habits around {topic}",
                 "example": f"Even spending just 10 minutes daily on this technique can improve your results by 65%."},
                {"title": f"{topic} for Long-term Results", 
                 "point1": f"How to maintain progress with {topic}",
                 "point2": f"Adjusting your approach as you advance",
                 "example": f"After six months of consistent practice, my clients report a 78% improvement in overall {subcategory} metrics."}
            ],
            'business': [
                {"title": f"{topic} Market Analysis", 
                 "point1": f"Current trends in the {topic} market",
                 "point2": f"Opportunities most businesses are missing",
                 "example": f"While most companies focus on {subcategory} segment A, the real growth is happening in segment B."},
                {"title": f"Implementing {topic} in Your Business", 
                 "point1": f"Step-by-step implementation guide",
                 "point2": f"Resource allocation and ROI expectations",
                 "example": f"When we implemented this strategy for a client, they saw a 43% increase in conversions within 30 days."},
                {"title": f"Scaling Your {topic} Strategy", 
                 "point1": f"How to grow from small tests to full implementation",
                 "point2": f"Measuring success and iterating",
                 "example": f"This case study shows how a small business scaled their {topic} approach to compete with industry leaders."}
            ],
            'education': [
                {"title": f"Core Principles of {topic}", 
                 "point1": f"The fundamental concepts you need to master",
                 "point2": f"How these principles connect to real-world applications",
                 "example": f"Understanding this principle helps solve 80% of common problems in {subcategory}."},
                {"title": f"Practical {topic} Exercises", 
                 "point1": f"Hands-on exercises to build your skills",
                 "point2": f"Common mistakes and how to avoid them",
                 "example": f"Try this exercise: {subcategory} challenge that reinforces the core concepts."},
                {"title": f"Advanced {topic} Applications", 
                 "point1": f"Taking your skills to the next level",
                 "point2": f"Real-world projects to build your portfolio",
                 "example": f"This technique is used by professionals to solve complex {subcategory} problems in minutes instead of hours."}
            ]
        }
        
        # Sélectionner les sections pour la catégorie ou utiliser un ensemble générique
        category_sections = sections.get(category, [
            {"title": f"Understanding {topic}", 
             "point1": f"Key aspects of {topic} explained",
             "point2": f"Why {topic} matters in {subcategory}",
             "example": f"For instance, {topic} can significantly impact your results in {subcategory}."},
            {"title": f"Implementing {topic}", 
             "point1": f"Step-by-step guide to {topic}",
             "point2": f"Tools and resources for {topic}",
             "example": f"When implementing {topic}, most people overlook this critical step."},
            {"title": f"Mastering {topic}", 
             "point1": f"Advanced strategies for {topic}",
             "point2": f"Taking your {topic} skills to the next level",
             "example": f"This advanced technique can improve your {topic} results by up to 50%."}
        ])
        
        # Conclusion
        recap = f"Today we've covered the essentials of {topic}, including key principles, implementation strategies, and advanced techniques."
        call_to_action = "If you found this video helpful, please hit the like button and subscribe for more content on similar topics."
        engagement_question = f"What's your biggest challenge with {topic}? Let me know in the comments below!"
        
        # Assembler les données du script
        script_data = {
            'title': title,
            'hook': hook,
            'topic_intro': topic_intro,
            'learning_points': learning_points,
            'section1_title': category_sections[0]['title'],
            'section1_point1': category_sections[0]['point1'],
            'section1_point2': category_sections[0]['point2'],
            'section1_example': category_sections[0]['example'],
            'section2_title': category_sections[1]['title'],
            'section2_point1': category_sections[1]['point1'],
            'section2_point2': category_sections[1]['point2'],
            'section2_example': category_sections[1]['example'],
            'section3_title': category_sections[2]['title'],
            'section3_point1': category_sections[2]['point1'],
            'section3_point2': category_sections[2]['point2'],
            'section3_example': category_sections[2]['example'],
            'recap': recap,
            'call_to_action': call_to_action,
            'engagement_question': engagement_question
        }
        
        return script_data
    
    def _generate_metadata(self, topic, category, subcategory, script_data):
        """
        Génère les métadonnées YouTube optimisées pour le référencement
        
        Args:
            topic (str): Sujet de la vidéo
            category (str): Catégorie principale
            subcategory (str): Sous-catégorie
            script_data (dict): Données du script généré
            
        Returns:
            dict: Métadonnées YouTube
        """
        # Générer un titre YouTube optimisé
        youtube_title = script_data['title']
        if len(youtube_title) > 60:
            youtube_title = youtube_title[:57] + "..."
        
        # Générer une description YouTube
        description_parts = [
            f"{script_data['hook']}",
            "",
            f"{script_data['topic_intro']}",
            "",
            "In this video, you'll learn:",
            f"- {script_data['section1_title']}",
            f"- {script_data['section2_title']}",
            f"- {script_data['section3_title']}",
            "",
            f"{script_data['engagement_question']}",
            "",
            "TIMESTAMPS:",
            "00:00 Introduction",
            f"01:30 {script_data['section1_title']}",
            f"05:45 {script_data['section2_title']}",
            f"10:20 {script_data['section3_title']}",
            "14:30 Conclusion",
            "",
            "#" + category + " #" + subcategory + " #" + topic.replace(" ", "")
        ]
        youtube_description = "\n".join(description_parts)
        
        # Générer des tags YouTube
        base_tags = [topic, category, subcategory]
        category_tags = {
            'finance': ['money', 'investing', 'financial advice', 'wealth building', 'personal finance'],
            'technology': ['tech review', 'gadgets', 'tech tips', 'software', 'hardware'],
            'health': ['health tips', 'fitness', 'wellness', 'nutrition', 'workout'],
            'business': ['entrepreneur', 'business strategy', 'marketing', 'startup', 'success'],
            'education': ['learning', 'tutorial', 'how to', 'skills', 'education']
        }
        
        # Combiner les tags de base avec les tags spécifiques à la catégorie
        tags = base_tags + category_tags.get(category, ['tips', 'guide', 'tutorial'])
        
        # Ajouter des tags spécifiques au sujet
        topic_words = topic.lower().split()
        for word in topic_words:
            if len(word) > 3 and word not in tags:  # Éviter les mots courts et les doublons
                tags.append(word)
        
        # Limiter à 15 tags maximum
        tags = tags[:15]
        
        # Assembler les métadonnées
        metadata = {
            'youtube_title': youtube_title,
            'youtube_description': youtube_description,
            'youtube_tags': tags,
            'youtube_category_id': self._get_youtube_category_id(category),
            'is_made_for_kids': False,
            'visibility': 'public',
            'notify_subscribers': True
        }
        
        return metadata
    
    def _get_youtube_category_id(self, category):
        """
        Retourne l'ID de catégorie YouTube correspondant à la catégorie
        
        Args:
            category (str): Catégorie principale
            
        Returns:
            int: ID de catégorie YouTube
        """
        # Mapping des catégories vers les IDs YouTube
        category_mapping = {
            'finance': 20,  # Finance
            'technology': 28,  # Science & Technology
            'health': 26,  # Howto & Style (ou 22 pour People & Blogs)
            'business': 22,  # People & Blogs
            'education': 27  # Education
        }
        
        return category_mapping.get(category, 22)  # Par défaut: People & Blogs
    
    def _save_generated_content(self, content):
        """
        Sauvegarde le contenu généré
        
        Args:
            content (dict): Contenu généré (script et métadonnées)
        """
        # Créer un nom de fichier basé sur le titre et la date
        title_slug = content['script']['title'].lower().replace(' ', '_')[:30]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{title_slug}_{timestamp}.json"
        
        # Chemin complet du fichier
        file_path = os.path.join(self.output_dir, filename)
        
        # Sauvegarder le contenu au format JSON
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2)
        
        print(f"Contenu généré sauvegardé dans: {file_path}")
        
        # Générer également un fichier markdown pour le script
        self._save_script_markdown(content, title_slug, timestamp)
    
    def _save_script_markdown(self, content, title_slug, timestamp):
        """
        Sauvegarde le script au format Markdown
        
        Args:
            content (dict): Contenu généré
            title_slug (str): Slug du titre
            timestamp (str): Horodatage
        """
        script_data = content['script']
        
        # Construire le contenu Markdown
        md_content = f"# {script_data['title']}\n\n"
        
        md_content += "## Introduction\n"
        md_content += f"- Hook: {script_data['hook']}\n"
        md_content += f"- Introduction du sujet: {script_data['topic_intro']}\n"
        md_content += f"- Ce que le spectateur va apprendre: {script_data['learning_points']}\n\n"
        
        md_content += f"## {script_data['section1_title']}\n"
        md_content += f"- {script_data['section1_point1']}\n"
        md_content += f"- {script_data['section1_point2']}\n"
        md_content += f"- Exemple: {script_data['section1_example']}\n\n"
        
        md_content += f"## {script_data['section2_title']}\n"
        md_content += f"- {script_data['section2_point1']}\n"
        md_content += f"- {script_data['section2_point2']}\n"
        md_content += f"- Exemple: {script_data['section2_example']}\n\n"
        
        md_content += f"## {script_data['section3_title']}\n"
        md_content += f"- {script_data['section3_point1']}\n"
        md_content += f"- {script_data['section3_point2']}\n"
        md_content += f"- Exemple: {script_data['section3_example']}\n\n"
        
        md_content += "## Conclusion\n"
        md_content += f"- Récapitulation: {script_data['recap']}\n"
        md_content += f"- Appel à l'action: {script_data['call_to_action']}\n"
        md_content += f"- Question d'engagement: {script_data['engagement_question']}\n\n"
        
        md_content += "## Métadonnées YouTube\n"
        md_content += f"- Titre: {content['metadata']['youtube_title']}\n"
        md_content += f"- Tags: {', '.join(content['metadata']['youtube_tags'])}\n"
        md_content += "- Description:\n```\n"
        md_content += content['metadata']['youtube_description']
        md_content += "\n```\n"
        
        # Chemin du fichier Markdown
        md_filename = f"{title_slug}_{timestamp}.md"
        md_path = os.path.join(self.output_dir, md_filename)
        
        # Sauvegarder le fichier Markdown
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"Script Markdown sauvegardé dans: {md_path}")
    
    def format_script_for_tts(self, script_data):
        """
        Formate le script pour la synthèse vocale
        
        Args:
            script_data (dict): Données du script
            
        Returns:
            str: Texte formaté pour la synthèse vocale
        """
        # Construire le texte pour la synthèse vocale
        tts_parts = [
            # Introduction
            script_data['hook'],
            script_data['topic_intro'],
            script_data['learning_points'],
            
            # Section 1
            f"Let's start with {script_data['section1_title']}.",
            script_data['section1_point1'],
            script_data['section1_point2'],
            script_data['section1_example'],
            
            # Section 2
            f"Now, let's move on to {script_data['section2_title']}.",
            script_data['section2_point1'],
            script_data['section2_point2'],
            script_data['section2_example'],
            
            # Section 3
            f"Finally, let's talk about {script_data['section3_title']}.",
            script_data['section3_point1'],
            script_data['section3_point2'],
            script_data['section3_example'],
            
            # Conclusion
            "To summarize,",
            script_data['recap'],
            script_data['call_to_action'],
            script_data['engagement_question']
        ]
        
        # Joindre les parties avec des pauses
        tts_text = " ".join(tts_parts)
        
        return tts_text
