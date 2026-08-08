"""Petition classification module using machine learning"""
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np

class PetitionClassifier:
    """Classify petitions into departments using ML"""
    
    def __init__(self):
        self.model = None
        self.categories = [
            "Education",
            "Healthcare", 
            "Infrastructure",
            "Transport",
            "Water Supply",
            "Electricity",
            "Public Safety",
            "Others"
        ]
        
        # Training data - sample petitions for each category
        self.training_data = {
            "Education": [
                "school building needs repair",
                "teacher shortage in primary school",
                "lack of books in college library",
                "playground not maintained properly",
                "computer lab equipment outdated",
                "school fees too high need scholarship",
                "no proper drinking water in school",
                "classroom overcrowded need more sections"
            ],
            "Healthcare": [
                "hospital lacks basic medicines",
                "doctor not available in clinic",
                "ambulance service very slow",
                "medical equipment not working",
                "long waiting time for treatment",
                "pharmacy closed during emergency",
                "no beds available in hospital",
                "vaccination center not functional"
            ],
            "Infrastructure": [
                "road full of potholes needs repair",
                "bridge damaged dangerous for vehicles",
                "street lights not working dark at night",
                "drainage system blocked water logging",
                "footpath broken pedestrians at risk",
                "public toilet in bad condition",
                "park needs maintenance cleaning",
                "building construction illegal blocking road"
            ],
            "Transport": [
                "bus service irregular timings",
                "auto rickshaw overcharging passengers",
                "traffic signal not working properly",
                "parking space insufficient in area",
                "bus stop shelter damaged",
                "road congestion during peak hours",
                "metro station escalator broken",
                "taxi drivers refusing short distance"
            ],
            "Water Supply": [
                "no water supply for three days",
                "water pipeline leaking wasting water",
                "dirty water coming from tap",
                "water pressure very low",
                "water tanker not coming regularly",
                "sewage overflow in residential area",
                "water bill incorrect overcharged",
                "bore well contaminated need testing"
            ],
            "Electricity": [
                "power cut daily for hours",
                "electric pole damaged dangerous",
                "street light not working",
                "electricity bill wrong meter reading",
                "transformer making loud noise",
                "voltage fluctuation damaging appliances",
                "illegal electricity connection in area",
                "power cable hanging low risk"
            ],
            "Public Safety": [
                "stray dogs attacking people",
                "theft cases increasing in locality",
                "illegal liquor shop operating",
                "fire safety equipment missing",
                "suspicious activity in neighborhood",
                "street crime at night no police",
                "building fire risk no exit",
                "drug peddling near school"
            ],
            "Others": [
                "noise pollution from construction",
                "garbage not collected regularly",
                "tree cutting without permission",
                "air pollution from factory",
                "encroachment on public land",
                "corruption in government office",
                "document verification delay",
                "pension not received on time"
            ]
        }
        
        self._train_model()
    
    def _train_model(self):
        """Train the classification model"""
        # Prepare training data
        X_train = []
        y_train = []
        
        for category, texts in self.training_data.items():
            X_train.extend(texts)
            y_train.extend([category] * len(texts))
        
        # Create pipeline with TF-IDF and Naive Bayes
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=500, ngram_range=(1, 2))),
            ('clf', MultinomialNB(alpha=0.1))
        ])
        
        # Train the model
        self.model.fit(X_train, y_train)
    
    def classify(self, text):
        """
        Classify petition text into a department
        
        Args:
            text: Petition description
            
        Returns:
            dict with 'category', 'confidence', and 'all_probabilities'
        """
        if not text or not text.strip():
            return {
                "category": "Others",
                "confidence": 0.5,
                "all_probabilities": {}
            }
        
        # Get prediction and probabilities
        prediction = self.model.predict([text])[0]
        probabilities = self.model.predict_proba([text])[0]
        
        # Get confidence score
        confidence = float(max(probabilities))
        
        # Create probability dict for all categories
        all_probs = {
            cat: float(prob) 
            for cat, prob in zip(self.model.classes_, probabilities)
        }
        
        return {
            "category": prediction,
            "confidence": confidence,
            "all_probabilities": all_probs
        }
    
    def get_top_categories(self, text, top_n=3):
        """Get top N predicted categories with probabilities"""
        if not text or not text.strip():
            return []
        
        probabilities = self.model.predict_proba([text])[0]
        categories = self.model.classes_
        
        # Sort by probability
        sorted_indices = np.argsort(probabilities)[::-1][:top_n]
        
        return [
            {
                "category": categories[idx],
                "probability": float(probabilities[idx])
            }
            for idx in sorted_indices
        ]
