from transformers  import pipeline
import spacy

class NLPEngine:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.labels = [
            "find_professor_by_area",
            "find_available_professor",
            "general_question"
        ]

        self.keywords = ["AI", "machine learning", "data science", "professor", "faculty", "research", "availability", "office hours", "data science"]
        self.nlp = spacy.load("en_core_web_sm")

    def analyze_query(self, query):
        #intent detection
        intent_result = self.classifier(query, candidate_labels=self.labels)
        intent = intent_result['labels'][0]

        #keyword detection
        found_keywords = [word for word in self.keywords if word.lower() in query.lower()]

        #named entity recognition
        doc = self.nlp(query)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        return {
            "intent": intent,
            "keywords": found_keywords,
            "entities": entities
        }