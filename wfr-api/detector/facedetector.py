import base64
import numpy as np
import cv2


def detect_faces(photos):
    boundary_photos = []
    for base64image in photos:
        width = base64image['w']
        height = base64image['h']
        image_buffer = base64image['src'].split(',')[1]
        cv2image = convert_to_cv2(image_buffer)
        manipulated_img = rotate(cv2image, 90)

        manipulated_img = convert_to_base64(manipulated_img)
        dataUrl = 'data:image/octet-stream;base64,' + manipulated_img.decode('utf-8')
        boundary_photos.append({'src': dataUrl,
                                'thumbnail': dataUrl, 'alt': 'some numbers on a grey background',
                                'w': width, 'h': height})

    return boundary_photos


def convert_to_cv2(base64image):
    img_bytes = base64.b64decode(base64image)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)
    return img


def convert_to_base64(cv2image):
    _, img_array = cv2.imencode('.jpg', cv2image)
    img_bytes = img_array.tobytes()
    img = base64.b64encode(img_bytes)
    return img


def rotate(image, angle, background_color=255, resize=False):
    height, width = image.shape[:2]
    image_center = (width / 2, height / 2)
    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0, 0])
    abs_sin = abs(rotation_mat[0, 1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w / 2 - image_center[0]
    rotation_mat[1, 2] += bound_h / 2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_img = cv2.warpAffine(image, rotation_mat, (bound_w, bound_h),
                                 borderValue=(background_color, background_color, background_color))
    # resize to old image size
    if resize:
        rotated_img = cv2.resize(rotated_img, (width, height))
    return rotated_img
