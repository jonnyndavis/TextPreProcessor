import spacy
import string
from nltk.stem.snowball import SnowballStemmer
from spellchecker import SpellChecker
import pandas as pd
import regex as re
spacy.load('en_core_web_sm')

class TextPreProcessor():
    r"""
    Instantiates a TextPreProcesser object for applying standard preprocessing
    techniques to text.
    
    Attributes:
        spellcheck (:obj: bool, optional dafaults to False):
            Whether to complete a spell check on each individual word in the
            text. Note, this works more effectively if punctuation has already
            been remove, and may remove punctuation as a biproduct.
        known_words (:obj: list, optional, defaults to None):
            Known words to ignore when running spell check. Only used if 
            spellcheck is True.
        lemmatize (:obj: bool, optional, defaults to False):
            Whether to lemmatize the text. If stem is also set to True,
            lemmatize takes priority.
        stem (:obj: bool, optional, defaults to False):
            Whether to stem the words in the text. If lemmatize=True,
            lemmatisation will be carried out first.
        stopwords (:obj: bool or list, optional, defaults to False):
            Whether to remove stopwords from text. Note this is not case
            sensitive.
            bool - whether to remove standar english stopwords from nltk 
            library.
            list - custom list of stopwords to remove.
        append_stopwords (:obj: bool, optional, dafaults to True):
            Whether to add the custom list of stopwords to the standard 
            english stopwords from nltk or to replace it with the custom list.
            Only applies if stopwords is a list.
        lower (:obj: bool, optional, defaults to False):
            Whether to change all characters in text to lower case.
        punctuation (:obj: bool, str or list, optional, defaults to False):
            Whether to remove punctuation from text.
            bool - whether to remove all punctuation defined in string
            libraries string.punctuation.
            str - remove all characters in the string
            list - remove all characters in the list. Note, if an value in the
            list is longer that one character, each character will be treated
            individually.
        append_punctuation (:obj: bool, optional, defaults to True):
            Whether to add the custom punctuation list or str to the pre-
            defined punctuation in string.punctuation.
        whitespace (:obj: bool, optional, defaults to True):
            Whether to scan string for multiple whitespaces and replace with a
            single whitespace.
        numbers (:obj: bool, optional defaults to False):
            Whether to remove all numerical characters from a text.
    """
    def __init__(self,
                 spellcheck=False,
                 known_words=None,
                 lemmatize=False,
                 stem=False,
                 stopwords=False,
                 append_stopwords=True,
                 lower=False,
                 punctuation=False,
                 append_punctuation=True,
                 whitespace=True,
                 numbers=False):
        self.spellcheck = spellcheck
        self.known_words = known_words
        self.lemmatize = lemmatize
        self.stem = stem
        self.append_stopwords = append_stopwords
        self.lower = lower
        self.punctuation = punctuation
        self.append_punctuation = punctuation
        self.whitespace = whitespace
        self.numbers=numbers
        
        if stopwords is not False or self.lemmatize is True:
            self.sp = spacy.load('en_core_web_sm')
            
        if stopwords is False:
            self.stopwords = False
        elif stopwords is True:
            self.stopwords = list(spacy.lang.en.stop_words.STOP_WORDS)
        elif type(stopwords) is list:
            self.stopwords = [word.lower() for word in stopwords]
            if self.append_stopwords is True:
                self.stopwords = self.stopwords + list(spacy.lang.en.stop_words.STOP_WORDS)

        if punctuation is False:
            self.punctuation = False
        elif punctuation is True:
            self.punctuation = string.punctuation
        elif type(punctuation) is list or type(punctuation) is str:
            self.punctuation = ''.join(punctuation)
            if self.append_punctuation is True:
                self.punctuation = self.punctuation + string.punctuation
                
                
    def spellchecking(self, text):
        r"""
        Spell check the input text and correct any detected spelling errors.
        
        Args:
            text (:obj: str):
                Text to spell check.
                
        Returns:
            text_checked (:obj: str)
            Text with any detected spelling errors corrected.
        """
        spell = SpellChecker()
        if type(self.known_words) == list:
            spell.word_frequency.load_words(self.known_words)
            
        text_checked = ' '.join([spell.correction(word) for word in text.split(' ')])
        return text_checked


    def lemmatize_text(self, text):
        r"""
        Lemmatize the input text.
        
        Args:
            text (:obj: str):
                Text to lemmatize.
                
        Returns:
            text_lemma (:obj: str):
                Lemmatized text.
        """
        # TODO: choose spacy language size
        text_lemma = self.sp(text)
        text_lemma = ' '.join([token.lemma_ for token in text_lemma])
        return str(text_lemma)


    def stem_text(self, text):
        r"""
        Stem the input text.
        
        Args:
            text (:obj: str):
                Text to Stem.
                
        Returns:
            text_stemmed (:obj: str):
                Stemmed text.
        """
        stemmer = SnowballStemmer(language='english')
        text_stemmed = [stemmer.stem(word) for word in self.text.split(' ')]
        text_stemmed = ' '.join(text_stemmed)
        return text_stemmed


    def remove_stopwords(self, text):
        r"""
        Remove defined list of stopwords from text.
        
        Args:
            text (:obj: str):
                Text to remove stopwords from.
                
        Returns:
            text_reduced (:obj: str):
                Text without stopwords.
        """
        text_reduced = ' '.join([word for word in text.split(' ') if word.lower() not in self.stopwords])
        return text_reduced


    def remove_punctuation(self, text):
        r"""
        Removed defined list of punctuation from text.
        
        Args:
            text (:obj: str):
                Text to remove punctuation from.
        
        Returns:
            text_reduced (:obj: str):
                Text with punctuation removed.
        """
        text_reduced = text.translate(str.maketrans('', '', self.punctuation))
        return text_reduced
    
    
    def remove_numbers(self, text):
        r"""
        Remove all numbers from a text.
        
        Args:
            text (:obj: str):
                Text to remove number from.
                
        Returns:
            text_reduced (:obj: str):
                Text with numbers removed.
        """
        text_reduced = re.sub(r'\d+', '', text)
        return text_reduced
    
    
    def normalise_whitespace(self, text):
        r"""
        Scan the text for multiple whitespaces, and replace with a single
        whitespace.
        
        Args:
            text (:obj: str):
                Text to scan for multiple whitespaces.
            
        Returns:
            text_reduced (:onj: str):
                Text with multiple whitespaces replaced with a single
                whitespace.
        """
        text_reduced = ' '.join(text.split('  '))
        return text_reduced


    def transform(self, text):
        """
        Complete text preprocessing on the passed text.
        
        Args:
            text (:obj: str):
                Text to preprocess.
                
        Returns:
            text_processed (:obj: str):
                Preprocessed text.
        """
        text_processed = text
    
        if self.whitespace is True:
            text_processed = self.normalise_whitespace(text_processed)
            
        if self.lower is True:
            text_processed = text.lower()
            
        if self.punctuation is not False:
            text_processed = self.remove_punctuation(text_processed)
        
        if self.stopwords is not False:
            text_processed = self.remove_stopwords(text_processed)
            
        if self.numbers is True:
            text_processed = self.remove_numbers(text_processed)
            
        if self.spellcheck is True:
            text_processed = self.spellchecking(text_processed)
        
        if self.lemmatize is True:
            text_processed = self.lemmatize_text(text_processed)
        
        if self.stem is True:
            text_processed = self.stem_text(text_processed)

        return text_processed
    
    
    def transform_series(self, series):
        r"""
        Complete text preprocessing on a pandas series or list.
        
        Args:
            series (:obj: Pandas Series or list)
            
        Returns:
            series_processed (:obj: Pandas Series or list)
        """
        if type(series) == pd.Series:
            series_processed= series.apply(lambda x: self.transform(x), axis=1)
        else:
            series_processed = [self.transform(text) for text in series]
        return series_processed
