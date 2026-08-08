"""Sentiment analysis and priority detection module"""
import re
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

class SentimentAnalyzer:
    """Analyze sentiment and detect priority/urgency"""
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        
        # Urgency keywords
        self.urgency_keywords = {
            'critical': ['emergency', 'urgent', 'critical', 'immediate', 'asap', 'danger', 
                        'life threatening', 'severe', 'crisis', 'fatal'],
            'high': ['important', 'serious', 'quickly', 'soon', 'priority', 'major',
                    'significant', 'pressing', 'crucial', 'vital'],
            'medium': ['needed', 'required', 'necessary', 'should', 'need', 'want',
                      'request', 'please', 'kindly'],
            'low': ['minor', 'small', 'little', 'eventually', 'sometime', 'when possible']
        }
    
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of petition text
        
        Args:
            text: Petition description
            
        Returns:
            dict with sentiment scores and polarity
        """
        if not text or not text.strip():
            return {
                "compound": 0.0,
                "positive": 0.0,
                "negative": 0.0,
                "neutral": 1.0,
                "polarity": "neutral"
            }
        
        # Get VADER scores
        scores = self.sia.polarity_scores(text)
        
        # Determine polarity
        compound = scores['compound']
        if compound >= 0.05:
            polarity = "positive"
        elif compound <= -0.05:
            polarity = "negative"
        else:
            polarity = "neutral"
        
        return {
            "compound": scores['compound'],
            "positive": scores['pos'],
            "negative": scores['neg'],
            "neutral": scores['neu'],
            "polarity": polarity
        }
    
    def detect_urgency(self, text):
        """
        Detect urgency level based on keywords
        
        Args:
            text: Petition description
            
        Returns:
            dict with urgency_level and matched_keywords
        """
        if not text:
            return {
                "urgency_level": "normal",
                "matched_keywords": [],
                "urgency_score": 0
            }
        
        text_lower = text.lower()
        matched_keywords = []
        urgency_score = 0
        
        # Check for critical keywords
        for keyword in self.urgency_keywords['critical']:
            if keyword in text_lower:
                matched_keywords.append(keyword)
                urgency_score += 3
        
        # Check for high urgency keywords
        for keyword in self.urgency_keywords['high']:
            if keyword in text_lower:
                matched_keywords.append(keyword)
                urgency_score += 2
        
        # Check for medium urgency keywords
        for keyword in self.urgency_keywords['medium']:
            if keyword in text_lower:
                matched_keywords.append(keyword)
                urgency_score += 1
        
        # Determine urgency level
        if urgency_score >= 3:
            urgency_level = "critical"
        elif urgency_score >= 2:
            urgency_level = "urgent"
        else:
            urgency_level = "normal"
        
        return {
            "urgency_level": urgency_level,
            "matched_keywords": matched_keywords,
            "urgency_score": urgency_score
        }
    
    def calculate_priority(self, text):
        """
        Calculate overall priority based on sentiment and urgency
        
        Args:
            text: Petition description
            
        Returns:
            dict with priority, sentiment, and urgency info
        """
        sentiment = self.analyze_sentiment(text)
        urgency = self.detect_urgency(text)
        
        # Calculate priority score
        priority_score = 0
        
        # Negative sentiment increases priority
        if sentiment['compound'] < -0.3:
            priority_score += 2
        elif sentiment['compound'] < 0:
            priority_score += 1
        
        # Add urgency score
        priority_score += urgency['urgency_score']
        
        # Determine final priority
        if priority_score >= 4:
            priority = "high"
        elif priority_score >= 2:
            priority = "medium"
        else:
            priority = "low"
        
        return {
            "priority": priority,
            "priority_score": priority_score,
            "sentiment": sentiment,
            "urgency": urgency
        }
    
    def extract_emotion(self, text):
        """Extract dominant emotion from text"""
        sentiment = self.analyze_sentiment(text)
        urgency = self.detect_urgency(text)
        
        # Determine emotion
        if urgency['urgency_level'] in ['critical', 'urgent']:
            emotion = "distressed"
        elif sentiment['compound'] < -0.5:
            emotion = "angry"
        elif sentiment['compound'] < -0.1:
            emotion = "dissatisfied"
        elif sentiment['compound'] > 0.5:
            emotion = "hopeful"
        else:
            emotion = "neutral"
        
        return emotion
