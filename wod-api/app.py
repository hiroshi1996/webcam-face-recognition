from flask import Flask, jsonify, request
from flask_cors import CORS
from detector import yolov3detector


# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/boundaryBox', methods=['POST'])
def boundary_box():
    response_object = {'status': 'success'}
    post_data = request.get_json()
    photos = post_data.get('photos')
    edited_photos = yolov3detector.detect_objects(photos)
    response_object['editedPhotos'] = edited_photos

    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
