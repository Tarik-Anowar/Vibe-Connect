from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

class TopicExtractor:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.kw_model = KeyBERT(model=self.model)

    def extract_topics(self, text, top_n=5):
        keywords = self.kw_model.extract_keywords(
            text, keyphrase_ngram_range=(1, 2), stop_words="english", top_n=top_n
        )
        return [phrase for phrase, _ in keywords]

def extract_topics_from_text(text, top_n=5):
    extractor = TopicExtractor()
    return extractor.extract_topics(text, top_n)

