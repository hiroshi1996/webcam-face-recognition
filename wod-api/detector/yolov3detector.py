import base64
import numpy as np
import cv2
from keras.models import load_model
from pathlib import Path
from detector.bbox_utils import decode_netout, correct_yolo_boxes, do_nms, get_boxes


def detect_objects(photos):
    # Load yolov3 model pretrained on MSCOCO
    model = load_model(Path('./model/yolov3_mscoco_model.h5'))

    # Defined input shape for the model
    input_w, input_h = 416, 416

    # Execute object detection for each image in photos and put results in list
    boundary_photos = []
    for base64image in photos:
        # Prepare image for model
        origin_image, image, width, height = prepare_for_model(base64image, (input_h, input_w))
        # Predict with model
        y_hat = model.predict(image)
        # Get boundary boxes, labels and scores from prediction
        b_boxes, b_labels, b_scores = get_bbox(y_hat, (input_h, input_w), (height, width))
        # Draw boxes, labels and scores in original image
        b_image = draw_boxes(origin_image, b_boxes, b_labels, b_scores)

        # Convert result back to base64 format and append to result list
        data_url, thumbnail_url = convert_to_base64(b_image)
        boundary_photos.append({'src': data_url,
                                'thumbnail': thumbnail_url, 'alt': 'some numbers on a grey background',
                                'w': width, 'h': height})

    return boundary_photos


def prepare_for_model(image, shape):
    # Get image buffer from base64
    image_buffer = image['src'].split(',')[1]
    # Convert to cv2 image and get shape
    origin_image = convert_to_cv2(image_buffer)
    height, width, _ = origin_image.shape
    # Resize, convert BGR representation of cv2 to RGB and normalize
    cv2image = cv2.resize(origin_image, shape)
    rgb_image = cv2image[..., ::-1].astype(np.float32)
    rgb_image /= 255.0
    # Expand dimension for prediction of one sample
    res_image = np.expand_dims(rgb_image, 0)
    return origin_image, res_image, width, height


def get_bbox(prediction, input_shape, target_shape):
    # Define the anchor boxes for object detection
    anchors = [[116, 90, 156, 198, 373, 326], [30, 61, 62, 45, 59, 119], [10, 13, 16, 30, 33, 23]]
    # Define prob. threshold for detected objects
    threshold = 0.6
    # Get box for each detected object
    boxes = []
    for i in range(len(prediction)):
        # Decode the prediction and add to list
        boxes += decode_netout(prediction[i][0], anchors[i], threshold, input_shape[0], input_shape[1])
    # Adapt the sizes of boxes for the original image
    boxes = correct_yolo_boxes(boxes, target_shape[0], target_shape[1], input_shape[0], input_shape[1])
    # Get only maximal boxes around detected objects (with overlapping threshold 0.5)
    do_nms(boxes, 0.5)
    # Get properties of the detected objects
    b_boxes, b_labels, b_scores = get_boxes(boxes, mscoco_labels, threshold)
    return b_boxes, b_labels, b_scores


def draw_boxes(cv2image, b_boxes, b_labels, b_scores):
    # Define drawing properties
    color = (255, 0, 0)
    line_thickness = 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    # Get shape of image
    h, w, _ = cv2image.shape
    # Draw all boxes with its labels and scores
    for i in range(len(b_boxes)):
        box = b_boxes[i]
        # Consider reverted y coordinate of cv2
        start_point = (box.xmin, box.ymin)
        end_point = (box.xmax, box.ymax)
        cv2image = cv2.rectangle(cv2image, start_point, end_point, color, line_thickness)

        label = "%s (%.3f)" % (b_labels[i], b_scores[i])
        cv2image = cv2.putText(cv2image, label, start_point, font, font_scale, color, line_thickness, cv2.LINE_AA)
    return cv2image


def convert_to_cv2(base64image):
    img_bytes = base64.b64decode(base64image)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)
    return img


def convert_to_base64(cv2image):
    # Create data_url for image
    _, img_array = cv2.imencode('.jpg', cv2image)
    img_bytes = img_array.tobytes()
    img = base64.b64encode(img_bytes)
    data_url = 'data:image/octet-stream;base64,' + img.decode('utf-8')
    # Create data_url for thumbnail
    thumbnail_img = cv2.resize(cv2image, (100, 100))
    _, thumbnail_array = cv2.imencode('.jpg', thumbnail_img)
    thumbnail_bytes = thumbnail_array.tobytes()
    thumbnail = base64.b64encode(thumbnail_bytes)
    thumbnail_url = 'data:image/octet-stream;base64,' + thumbnail.decode('utf-8')
    return data_url, thumbnail_url


mscoco_labels = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck",
                 "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "bench",
                 "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
                 "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
                 "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
                 "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana",
                 "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
                 "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse",
                 "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
                 "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
