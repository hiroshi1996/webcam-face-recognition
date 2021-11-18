from flask import Flask, jsonify, request
from flask_cors import CORS
from detector import facedetector


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


@app.route('/boundaryBox', methods=['POST'])
def boundary_box():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    photos = post_data.get('photos')
    edited_photos = facedetector.detect_faces(photos)
    response_object['editedPhotos'] = edited_photos

    return jsonify(response_object)


if __name__ == '__main__':
    app.run()






