import pickle
from gensim.models import Word2Vec, TfidfModel
from gensim.models.phrases import Phraser
import spacy
import gensim
from gensim.utils import simple_preprocess

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

# Custom stop words
stop_words = set(gensim.parsing.preprocessing.STOPWORDS)

class TopicExtractor:
    def __init__(self):
        # Load models
        with open("models/dictionary.pkl", "rb") as f:
            self.dictionary = pickle.load(f)
        self.tfidf_model = TfidfModel.load("models/tfidf_model.model")
        self.w2v_model = Word2Vec.load("models/word2vec_model.model")
        self.phraser = Phraser.load("models/phraser.model")
    
    def preprocess_with_gensim(self, text):
        # Tokenize and lemmatize using spaCy
        doc = nlp(text)
        tokens = [token.lemma_ for token in doc if token.text.lower() not in stop_words and token.is_alpha]
        return tokens

    def extract_topics(self, text, top_n=5):
        # Preprocess text and apply phrase model
        processed_tokens = self.preprocess_with_gensim(text)
        phrase_tokens = self.phraser[processed_tokens]
        
        # Convert to BoW and get TF-IDF scores
        bow = self.dictionary.doc2bow(phrase_tokens)
        tfidf_scores = self.tfidf_model[bow]
        
        # Select top terms based on TF-IDF scores
        sorted_terms = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)[:top_n]
        topics = [(self.dictionary[term_id], score) for term_id, score in sorted_terms]
        
        return topics

def extract_topics_from_text(text):
    extractor = TopicExtractor()
    topics = extractor.extract_topics(text)
    topics_term = []
    for term, score in topics:
        topics_term.append(term)
    return topics_term
