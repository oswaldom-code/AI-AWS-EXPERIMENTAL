import difflib
import nltk
import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


nltk.download('stopwords')
nltk.download('punkt')

# preprocess_text: Process the text to remove stopwords and punctuation marks.
# Input: text
# Output: text without stopwords and punctuation marks
# Example: preprocess_text("I have reports") -> "have reports"words and punctuation marks.
def preprocess_text(text): 
    tokens = word_tokenize(text.lower()) # Tokenize and lowercase

    # Delete the stopwords and punctuation marks
    stop_words = set(stopwords.words('english')) # Get the stopwords for English
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(tokens)


# get_tables_related_to_the_question: Get the tables related to the question using difflib
def get_tables_related_to_the_question(question):
    processed_question = preprocess_text(question)
    # get the tables names
    table_names_list, error = get_list_of_table_names()
    print (table_names_list)
    if error is not None:
        print("Ups, something went wrong :(")
        return None, error
    
    best_matches = difflib.get_close_matches(processed_question, table_names_list, n=2, cutoff=0)
    if len(best_matches) > 0:
        print("Best match:", best_matches) # TODO
        return get_simple_definitions(best_matches[0]), None
    print("no match found", best_matches)
    return None, None

# read_json_file: Read JSON file with questions and answers and return a list of dictionaries
def read_json_file():
    try:
        with open('db_definitions.json') as json_file:
            data = json.load(json_file)
            return data, None # Return data and None if there is no error
    except Exception as error:
        print("Error reading JSON file:", error)
        return None, error # Return None and error if there is an error


# get_list_of_table_names: Read JSON file with db_definitions and return a list of table names
def get_list_of_table_names():
    table_names = []
    # Read JSON file with db_definitions and return a list of table names
    data, error = read_json_file() # Read JSON file with db_definitions
    # check if there is an error reading the file
    if error: # TODO: check if there is an error reading the file
        return [], error # Return empty list and error if there is an error
    # Get the list of table names
    for schema in data['schemas']:
        for table in schema['tables']:
            table_names.append(table['name'])

    return table_names, None # Return list of table names and None if there is no error


# get_simple_definitions: Read JSON file with db_definitions and return a definition of the table by name
def get_simple_definitions(table_name):
    # Read JSON file with db_definitions and return a definition of the table by name
    data, error = read_json_file() # Read JSON file with db_definitions
    # check if there is an error reading the file
    if error:
        return [], error # Return empty list and error if there is an error
    # Get the list of table names
    for schema in data['schemas']:
        index = 0
        for table in schema['tables']:
            if table['name'] == table_name:
                return schema['tables'][index], None # Return list of table names and None if there is no error
            index += 1 # Increase index
    return [], None # Return empty list and None if there is no error