import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from microservice_helper import load_model, get_simple_definitions, get_list_of_table_names, get_tables_related_to_the_question


app = Flask(__name__)

# ping route
@app.route('/ping')
def ping():
    # return a json
    return {'success': True,
            'error': None,
            'message': 'pong'}, 200


# 404 route
@app.errorhandler(404)
def not_found(error):
    return {'success': False,
            'error': 'page not found',
            'message': 'Oops, something went wrong :(, this page does not exist'}, 404


# get question route
@app.route('/question', methods=['POST'])
def get_question():
    # get the question from the request body
    data = request.json
    question = data.get("question")
    temperature = data.get("temperature")
    
    # check if the question is not None
    if question is None:
        return {'success': False,
                'error': 'question not found',
                'message': 'Oops, something went wrong :(, the question was not found'}, 400

    table, error = get_tables_related_to_the_question(question, temperature)
    
    # check if there is an error
    if error is not None:
        return {'success': False,
                'error': error,
                'message': 'Oops, something went wrong :('}, 500

    # check if the table is empty
    if len(table) == 0:
        return {'success': False,
                'error': 'Empty list',
                'message': 'No tables related to the question were found'}, 200
    
    definitions_of_tables = ""
    for table_name in table:
        print("ok")
        definition, error = get_simple_definitions(table_name)
        if error is not None:
            return {'success': False,
                    'error': error,
                    'message': 'Oops, something went wrong :('}, 500
        definitions_of_tables += definition + "\n"

    return {'success': True,
            'error': None,
            'message': 'success',
            'question': question,
            'definitions': definitions_of_tables}, 200

# get definition of table route by name
@app.route('/definition/<table_name>', methods=['GET'])
def get_definition_by_name(table_name):
    definition, error = get_simple_definitions(table_name)
    if error is not None:
        return {'success': False,
                'error': error,
                'message': 'Oops, something went wrong :('}, 500
    if len(definition) == 0:
        return {'success': False,
                'error': 'Empty list',
                'message': 'Table name not found'}, 200
        
    return {'success': True,
            'error': None,
            'message': 'Table name found successfully',
            'table': { 'name': table_name,'definition': definition }}, 200


@app.route('/debug', methods=['GET'])
def debug():
    list_of_table_names, error = get_list_of_table_names()
    if error is not None:
        return {'success': False,
                'error': error,
                'message': 'Oops, something went wrong :('}, 500
        
    return {'success': True,
            'error': None,
            'message': 'List of table names found successfully',
            'data': list_of_table_names}, 200
    
def check_env_variables():
    return os.getenv('HOST') is None or \
        os.getenv('PORT') is None or \
        os.getenv('DEBUG') is None or \
        os.getenv('PATH_DB_DEFINITION_DIR') is None
    
with app.app_context():
    load_model()



# entry point for the application
if __name__ == '__main__':
    # load env variables
    load_dotenv()
    # check env variables are loaded
    if check_env_variables():
        print('Env variables are loaded, check .env file and try again')
        exit(1)
    
    # setting debug to True enables hot reload
    app.debug = os.getenv('DEBUG')
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'))
