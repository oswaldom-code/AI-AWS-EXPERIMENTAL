import gensim.downloader as api
from flask import Flask, jsonify, request
from microservice_helper import get_simple_definitions, get_list_of_table_names, get_tables_related_to_the_question

app = Flask(__name__)

# singelton pattern to load the model only once when the first request is received
def load_model():
    if not hasattr(app.config, 'modelo_word2vec'):
        app.config['modelo_word2vec'] = api.load('word2vec-google-news-300')
    return app.config['modelo_word2vec']



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
            'message': 'Ups, something went wrong :(, this page does not exist'}, 404


# get question route
@app.route('/question', methods=['POST'])
def get_question():
    # get the question from the request body
    data = request.json
    question = data.get("question")
    table, error = get_tables_related_to_the_question(question)
    if error is not None:
        return {'success': False,
                'error': error,
                'message': 'Ups, something went wrong :('}, 500
    if table is None:
        return {'success': False,
                'error': 'Empty list',
                'message': 'No tables related to the question were found'}, 200
    question = {'question': question, 'table': table}
    
    return {'success': True,
            'error': None,
            'message': 'success',
            'data': question}, 200

# get definition of table route by name
@app.route('/definition/<table_name>', methods=['GET'])
def get_definition_by_name(table_name):
    definition, error = get_simple_definitions(table_name)
    if error is not None:
        return {'success': False,
                'error': error,
                'message': 'Ups, something went wrong :('}, 500
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
                'message': 'Ups, something went wrong :('}, 500
        
    return {'success': True,
            'error': None,
            'message': 'List of table names found successfully',
            'data': list_of_table_names}, 200


# entry point for the application
if __name__ == '__main__':
    # setting debug to True enables hot reload
    app.debug = True
    load_model()
    app.run()