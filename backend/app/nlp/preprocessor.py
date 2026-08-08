"""Text preprocessing module for petition analysis"""
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

class TextPreprocessor:
    """Preprocess text for NLP analysis"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text):
        """Tokenize text into words"""
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens):
        """Remove stopwords from token list"""
        return [token for token in tokens if token not in self.stop_words]
    
    def stem_tokens(self, tokens):
        """Apply stemming to tokens"""
        return [self.stemmer.stem(token) for token in tokens]
    
    def lemmatize_tokens(self, tokens):
        """Apply lemmatization to tokens"""
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def preprocess(self, text, use_stemming=False, use_lemmatization=True):
        """
        Complete preprocessing pipeline
        
        Args:
            text: Input text to preprocess
            use_stemming: Whether to apply stemming
            use_lemmatization: Whether to apply lemmatization
            
        Returns:
            Preprocessed text as string
        """
        # Clean text
        cleaned = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(cleaned)
        
        # Remove stopwords
        tokens = self.remove_stopwords(tokens)
        
        # Apply stemming or lemmatization
        if use_stemming:
            tokens = self.stem_tokens(tokens)
        elif use_lemmatization:
            tokens = self.lemmatize_tokens(tokens)
        
        return ' '.join(tokens)
    
    def extract_keywords(self, text, top_n=10):
        """Extract top keywords from text"""
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        tokens = self.remove_stopwords(tokens)
        
        # Count frequency
        from collections import Counter
        word_freq = Counter(tokens)
        
        return [word for word, _ in word_freq.most_common(top_n)]
