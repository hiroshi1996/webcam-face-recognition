from flask import Flask, jsonify, request
from flask_cors import CORS


messages = [{'text': "Hallo"}, {'text': "Hi"}]

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/messages', methods=['GET', 'POST'])
def all_messages():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        messages.append({
            'text': post_data.get('text')
        })
        response_object['message'] = 'Text added!'
    else:
        response_object['messages'] = messages
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()






