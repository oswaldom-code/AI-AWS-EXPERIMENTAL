import os
import gensim.downloader as api
import difflib
import nltk
import json
import requests as http
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import OrderedDict
from flask import current_app

nltk.download('stopwords')
nltk.download('punkt')

# Global variable to store a JSON object with the routes available in the API.
# It is not a data that needs to be consulted frequently, so this variable is
# used to keep the information in cache
ROUTE_DEFINITIONS_CACHE = None

# load the model of keywords previously trained (Google News)
def load_model():
    if not hasattr(current_app, 'word2vec_model'):
        print("Loading model...")
        current_app.word2vec_model = api.load('word2vec-google-news-300')
        print("Model loaded successfully")




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
def get_tables_related_to_the_question(question, temperature=None):
    # Process the question to remove stopwords and punctuation marks.
    tokenized_question = tokenize_text(question)
    # Get the list of table names
    tables_names, error = get_list_of_table_names()
    if error is not None:
        print("Oops, something went wrong :(")
        return [], error
    
    # Get the similarity between the question and the table name
    tables_related = OrderedDict() # List of tables related to the question
    for table_name in tables_names:
        # get the similarity between the question and the table name
        # proximity_rank is a float number between 0 and 1
        proximity_value = current_app.word2vec_model.n_similarity(tokenized_question, table_name)
        if proximity_value >= temperature:
            tables_related[table_name] = proximity_value
            tables_related.append(table_name)

    # Sort the tables related to the question by proximity value
    tables_related_sorted = OrderedDict(sorted(tables_related.items(), key=lambda x: x[1], reverse=True))
    
    # if there are tables related to the question, return them
    if len(tables_related_sorted) > 0:
        return tables_related_sorted, None
    
    # if there are no tables related to the question
    return [], None


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

# get_route_definitions_from_api: Call the API and return the definitions of the route available
def get_route_definitions_from_api():
    global ROUTE_DEFINITIONS_CACHE
    # Check cache for definitions of routes
    if  ROUTE_DEFINITIONS_CACHE is not None:
        return ROUTE_DEFINITIONS_CACHE, None
    
    # If the cache is empty, call the API
    try:
        # Get list of router
        url = f"{os.getenv('URL_API')}/routes"
        response = http.get(url, timeout=5)
        
        # Check if the response is correct
        if response.status_code != 200:
            return None, response.json()
        
        # Save the response in cache
        ROUTE_DEFINITIONS_CACHE = response.json()
        # success
        return ROUTE_DEFINITIONS_CACHE, None

    except http.exceptions.RequestException as e:
        return None, e

# get_routes_related_to_the_question : Get the routes related to the question using difflib
def get_routes_related_to_the_question(question, temperature=None):
    # get all the routes
    routes_list, error = get_route_definitions_from_api()
    if error is not None:
        return [], error
    
    # Process the question to remove stopwords and punctuation marks.
    tokenized_question = tokenize_text(question)
    
    # Get the similarity between the question and the route name and description
    routes_related = OrderedDict() # List of routes related to the question
    for route in routes_list:
        # get the similarity between the question and the table name
        # proximity_rank is a float number between 0 and 1
        proximity_value = current_app.word2vec_model.n_similarity(tokenized_question, route['description'])
        if proximity_value >= temperature:
            routes_related[route['name']] = proximity_value
    
    # Sort the routes related to the question by proximity value
    routes_related_sorted = OrderedDict(sorted(routes_related.items(), key=lambda x: x[1], reverse=True))
    
    # no routes related to the question
    return None, None


def get_route_definitions(route_name):
    # get all the routes
    routes_list, error = get_route_definitions_from_api()
    if error is not None:
        return None, error
    
    # Get the route definition by name
    for route_object in routes_list:
        if route_object['name'] == route_name:
            return route_object, None
    return None, None

# get_data_related_to_the_question: Get the tables and routes related to the question
def get_data_related_to_the_question(question, temperature=None):
    # Set default value for temperature
    if temperature is None:
        temperature = 0.9 # Default value
        
    # Get tables related to the question
    tables_related, error = get_tables_related_to_the_question(question, temperature)
    # Check if there is an error
    if error is not None:
        return None, error
    
    definitions_of_tables = ""
    for table_name in tables_related:
        definition_table, error = get_simple_definitions(table_name)
        if error is not None:
            print("[Error] Error get_simple_definitions for table_name: #{table_name}")

        definitions_of_tables += definition_table + "\n"
    
    # Get Routes related to the question
    routes_related, error = get_routes_related_to_the_question(question, temperature)
    # Check if there is an error
    if error is not None:
        return None, error
    
    definitions_of_routes = []
    for route_name in routes_related:
        definition_route, error = get_route_definitions(route_name)
        if error is not None:
            print("[Error] Error get_simple_definitions for table_name: #{table_name}")

        definitions_of_routes.append(definition_route)
    
    # success
    return {
        "tables": definitions_of_tables,
        "routes": definitions_of_routes
    }, None
    
