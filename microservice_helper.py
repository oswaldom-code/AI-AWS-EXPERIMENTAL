import os
import gensim.downloader as api
import difflib
import nltk
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import OrderedDict
from flask import current_app

nltk.download('stopwords')
nltk.download('punkt')

def load_model():
    if not hasattr(current_app, 'word2vec_model'):
        print("Loading model...")
        current_app.word2vec_model = api.load('word2vec-google-news-300')
        print("Model loaded successfully")

# load the model of keywords previously trained (Google News)

    
# preprocess_text: Process the text to remove stopwords and punctuation marks.
# Input: text
# Output: text without stopwords and punctuation marks
# Example: preprocess_text("I have reports") -> "have reports"words and punctuation marks.
def tokenize_text(text): 
    tokens = word_tokenize(text.lower()) # Tokenize and lowercase

    # Delete the stopwords and punctuation marks
    stop_words = set(stopwords.words('english')) # Get the stopwords for English
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(tokens)


# get_tables_related_to_the_question: Get the tables related to the question using difflib
def get_tables_related_to_the_question(question, temperature=1):
    tables_related = [] # List of tables related to the question
    # Process the question to remove stopwords and punctuation marks.
    tokenized_question = tokenize_text(question)
    # Get the list of table names
    tables_names, error = get_list_of_table_names()
    if error is not None:
        print("Oops, something went wrong :(")
        return None, error
    
    # Get the similarity between the question and the table name
    table_name_and_proximity_values = OrderedDict() 
    for table_name in tables_names:
        # get the similarity between the question and the table name
        # proximity_rank is a float number between 0 and 1
        proximity_value = current_app.word2vec_model.n_similarity(tokenized_question, table_name)
        table_name_and_proximity_values[table_name] = proximity_value
        print("Table:", table_name, "Ranking:", proximity_value)
        if proximity_value > temperature:
            tables_related.append(table_name)

    # if there are tables related to the question, return them
    if len(tables_related) > 0:
        return tables_related, None
    
    # if there are no tables related to the question, return the table with the highest ranking
    tables_related.append(max(table_name_and_proximity_values, key=table_name_and_proximity_values.get))
    print("No tables related to the question, returning the table with the highest ranking"
          , table_name_and_proximity_values)
    return tables_related, None


# get_list_of_table_names: Read all files in the directory and return a list of table names
def get_list_of_table_names():
    table_names = []
    for file in os.listdir(os.environ.get('PATH_DB_DEFINITION_DIR')):
        if file.endswith(".txt"):
            table_names.append(file.split('.')[0]) # Get the table name without extension
            
    return table_names, None # Return list of table names and None if there is no error


# get_simple_definitions: Read a file with db_definitions and return a definition of the table by name
def get_simple_definitions(table_name):
    try:
        path_db_definitions = os.environ.get('PATH_DB_DEFINITION_DIR')
        path_db_definitions = path_db_definitions + '/' + table_name + '.txt'
        with open(path_db_definitions) as definitions_file:
            definitions = definitions_file.read()
            return definitions, None # Return definitions and None if there is no error
    except Exception as error:
        print("Error reading file:", error)
        return None, error # Return None and error if there is an error
