"""Petition processing service - orchestrates NLP pipeline"""
from app.nlp import TextPreprocessor, PetitionClassifier, SentimentAnalyzer, EntityExtractor
from app.models import Department
from datetime import datetime

class PetitionProcessor:
    """Main service for processing petitions with AI/NLP"""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.classifier = PetitionClassifier()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.entity_extractor = EntityExtractor()
    
    def process_petition(self, title, description):
        """
        Process petition through complete NLP pipeline
        
        Args:
            title: Petition title
            description: Petition description
            
        Returns:
            dict with all AI-generated insights
        """
        # Combine title and description for analysis
        full_text = f"{title}. {description}"
        
        # 1. Preprocess text
        preprocessed = self.preprocessor.preprocess(full_text)
        keywords = self.preprocessor.extract_keywords(full_text, top_n=5)
        
        # 2. Classify into department
        classification = self.classifier.classify(full_text)
        
        # 3. Analyze sentiment and calculate priority
        priority_analysis = self.sentiment_analyzer.calculate_priority(full_text)
        
        # 4. Extract entities
        entities = self.entity_extractor.extract_all_entities(full_text)
        entity_summary = self.entity_extractor.generate_summary(entities)
        
        # 5. Generate petition summary
        summary = self._generate_summary(title, classification, priority_analysis, entities)
        
        return {
            "classification": {
                "category": classification["category"],
                "confidence": classification["confidence"]
            },
            "priority": {
                "level": priority_analysis["priority"],
                "score": priority_analysis["priority_score"]
            },
            "sentiment": {
                "compound": priority_analysis["sentiment"]["compound"],
                "polarity": priority_analysis["sentiment"]["polarity"]
            },
            "urgency": {
                "level": priority_analysis["urgency"]["urgency_level"],
                "keywords": priority_analysis["urgency"]["matched_keywords"]
            },
            "entities": entities,
            "keywords": keywords,
            "summary": summary,
            "preprocessed_text": preprocessed
        }
    
    def _generate_summary(self, title, classification, priority_analysis, entities):
        """Generate human-readable summary of petition"""
        parts = [f"Petition: {title}"]
        
        parts.append(f"Category: {classification['category']}")
        parts.append(f"Priority: {priority_analysis['priority']}")
        parts.append(f"Urgency: {priority_analysis['urgency']['urgency_level']}")
        
        if entities.get('locations'):
            parts.append(f"Location: {entities['locations'][0]}")
        
        return " | ".join(parts)
    
    def get_department_id(self, category_name, db_session):
        """Get department ID from category name"""
        department = db_session.query(Department).filter_by(name=category_name).first()
        return department.id if department else None
    
    def generate_petition_id(self):
        """Generate unique petition ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"PET-{timestamp}"
