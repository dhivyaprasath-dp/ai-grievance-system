"""Named Entity Recognition module"""
import re
from datetime import datetime
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)

try:
    nltk.data.find('chunkers/maxent_ne_chunker')
except LookupError:
    nltk.download('maxent_ne_chunker', quiet=True)

try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words', quiet=True)

class EntityExtractor:
    """Extract named entities from petition text"""
    
    def __init__(self):
        pass
    
    def extract_dates(self, text):
        """Extract dates from text"""
        date_patterns = [
            r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',  # DD-MM-YYYY or DD/MM/YYYY
            r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',    # YYYY-MM-DD
            r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b',  # DD Month YYYY
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        return list(set(dates))
    
    def extract_phone_numbers(self, text):
        """Extract phone numbers from text"""
        phone_pattern = r'\b\d{10}\b|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        phones = re.findall(phone_pattern, text)
        return list(set(phones))
    
    def extract_emails(self, text):
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return list(set(emails))
    
    def extract_locations(self, text):
        """Extract location mentions (simple pattern-based)"""
        # Common location indicators
        location_keywords = ['street', 'road', 'avenue', 'colony', 'sector', 'area', 
                            'district', 'city', 'town', 'village', 'block', 'ward']
        
        locations = []
        sentences = nltk.sent_tokenize(text)
        
        for sentence in sentences:
            for keyword in location_keywords:
                if keyword.lower() in sentence.lower():
                    # Extract the phrase containing the location keyword
                    words = sentence.split()
                    for i, word in enumerate(words):
                        if keyword.lower() in word.lower():
                            # Get surrounding words
                            start = max(0, i-3)
                            end = min(len(words), i+4)
                            location_phrase = ' '.join(words[start:end])
                            locations.append(location_phrase)
        
        return list(set(locations))[:5]  # Return top 5 unique locations
    
    def extract_names(self, text):
        """Extract person names using NLTK NER"""
        try:
            tokens = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(tokens)
            chunks = nltk.ne_chunk(pos_tags)
            
            names = []
            for chunk in chunks:
                if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                    name = ' '.join(c[0] for c in chunk)
                    names.append(name)
            
            return list(set(names))
        except:
            return []
    
    def extract_organizations(self, text):
        """Extract organization names using NLTK NER"""
        try:
            tokens = nltk.word_tokenize(text)
            pos_tags = nltk.pos_tag(tokens)
            chunks = nltk.ne_chunk(pos_tags)
            
            orgs = []
            for chunk in chunks:
                if hasattr(chunk, 'label') and chunk.label() == 'ORGANIZATION':
                    org = ' '.join(c[0] for c in chunk)
                    orgs.append(org)
            
            return list(set(orgs))
        except:
            return []
    
    def extract_all_entities(self, text):
        """
        Extract all entities from text
        
        Args:
            text: Input text
            
        Returns:
            dict with all extracted entities
        """
        if not text:
            return {
                "dates": [],
                "phone_numbers": [],
                "emails": [],
                "locations": [],
                "names": [],
                "organizations": []
            }
        
        return {
            "dates": self.extract_dates(text),
            "phone_numbers": self.extract_phone_numbers(text),
            "emails": self.extract_emails(text),
            "locations": self.extract_locations(text),
            "names": self.extract_names(text),
            "organizations": self.extract_organizations(text)
        }
    
    def generate_summary(self, entities):
        """Generate a summary of extracted entities"""
        summary_parts = []
        
        if entities.get('names'):
            summary_parts.append(f"Persons mentioned: {', '.join(entities['names'][:3])}")
        
        if entities.get('locations'):
            summary_parts.append(f"Locations: {', '.join(entities['locations'][:2])}")
        
        if entities.get('organizations'):
            summary_parts.append(f"Organizations: {', '.join(entities['organizations'][:2])}")
        
        if entities.get('dates'):
            summary_parts.append(f"Dates: {', '.join(entities['dates'][:2])}")
        
        return "; ".join(summary_parts) if summary_parts else "No specific entities extracted"
