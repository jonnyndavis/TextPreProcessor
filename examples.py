from TextPreProcessor import TextPreProcessor

s = 'The 2 wuick brown foxes jumped, over the  lazy dog.'

# =============================================================================
# Simple example to remove stopwords and punctuation, lowercase and lemmatize.
# =============================================================================
# Instantiate TextPreProcessor object
prp = TextPreProcessor.TextPreProcessor(stopwords=True,
                                        lemmatize=True,
                                        lower=True,
                                        punctuation=True)

# process text
print('--')
print(s)
s_processed = prp.transform(s)
print(s_processed)

# =============================================================================
# Create custom list of stopwords to append to standard stopword list
# =============================================================================
# Instantiate TextPreProcessor object
prp = TextPreProcessor.TextPreProcessor(stopwords=['fox', 'quick'],
                                        append_stopwords=True)

# process text
print('--')
print(s)
s_processed = prp.transform(s)
print(s_processed)

# =============================================================================
# Remove custom list of characters, but not standard punctuation
# =============================================================================
# Instantiate TextPreProcessor object
prp = TextPreProcessor.TextPreProcessor(punctuation=[',f'],
                                        append_punctuation=False)

# process text
print('--')
print(s)
s_processed = prp.transform(s)
print(s_processed)

# =============================================================================
# Spell checking
# =============================================================================
# Instantiate TextPreProcessor object
prp = TextPreProcessor.TextPreProcessor(spellcheck=True)

# process text
print('--')
print(s)
s_processed = prp.transform(s)
print(s_processed)

# =============================================================================
# Remove numbers
# =============================================================================
# Instantiate TextPreProcessor object
prp = TextPreProcessor.TextPreProcessor(numbers=True)

# process text
print('--')
print(s)
s_processed = prp.transform(s)
print(s_processed)
