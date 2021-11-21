# Webcam Object Detection Demo

Application for detecting objects from photos taken by the webcam.
The application can detect potentially 80 different objects contained in the MSCOCO dataset
(https://cocodataset.org/#home).


## Usage
1. Clone the project to your working directory:

- with SSH
```
git clone git@github.com:hiroshi1996/webcam-object-detection.git
```

- or with HTTPS
```
git clone https://github.com/hiroshi1996/webcam-object-detection.git
```
2. Navigate to the project directory

- in CMD
```
cd YOUR_WORKING_DIR\webcam-object-detection
```

- in Terminal
```
cd YOUR_WORKING_DIR/webcam-object-detection
```

3. Build the Docker image for allowing communication between client and api.
```
docker-compose up -d --build
```

4. Start the Docker container: This command will start 2 services (*wod-client* for taking photos with the webcam and
*wod-api* for marking object in the photos with boundary boxes).
```
docker-compose up
```


5. After the Docker container is started, you can now proceed to http://localhost:8080/ to interact with the app.


## Technical Backgrounds
### wod-client
#### Description
*wod-client* allows the user to take photos by the webcam.
After allowing the application to use the webcam, the user can click on "Take Photos" to take multiple photos
(5 photos are taken in interval of 2 seconds).
The taken photos are displayed in a gallery below, and they can be used for object detection in *wod-api*.
The detected objected in the photos are displayed in boundary boxes with the labels and scores.
For more detailed description you can access the "About" page of the application.

#### Implementation
- **Vue.js** (https://vuejs.org/) version 2.x was used as the frontend framework
(since this application is a single page application and **Vue** is commonly used for these purpose)
- **BootstrapVue** (https://bootstrap-vue.org/) was used as CSS library to organize the pages structured
- **vue-picture-swipe** (https://github.com/rap2hpoutre/vue-picture-swipe) was used to display the photos in a gallery

### wod-api
#### Description
*wod-api* provides an API for detecting object from the taken photos.
It gets from the *wod-client* the photos as Base64 format and convert them correctly for the object detection process.
The object detection is processed with a pretrained model. It returns as response the photos with the detected objects
(with their labels and scores) in the Base64 format.

#### Used Model: YOLOv3
- For the object detection the model **YOLOv3** pretrained on the **MSCOCO**
dataset was used.
- **MSCOCO** dataset consists of 330k images with 80 object categories
and is commonly used for object detection purposes.
- **YOLOv3** is based on **DarkNet** and splits the input into a grid of cells and each cell directly predicts a
bounding box and object classification

Below you can see some pros and cons of the **YOLOv3** model

Pros | Cons 
--- | ---
Popular for fast detection speed | Accuracy not as good as for example **RetinaNet** or **Faster R-CNN**
Often used in real-time object detection in videos | There are already newer models like **YOLOv4** and **YOLOv5**

- Since this application is for demonstration purpose, it was important to focus on the detection speed
- The pretrained model is saved in the file *wod-api/model/yolov3_mscoco_model.h5*
- How to get the pretrained **YOLOv3** model is explained in the following tutorial:
https://machinelearningmastery.com/how-to-perform-object-detection-with-yolov3-in-keras/

#### Implementation
- **Flask** (https://flask.palletsprojects.com/en/2.0.x/) was used for proving the API
- **OpenCV** (https://opencv.org/) was used for processing the images (converting, resizing etc.)
- **Keras** (https://keras.io/) was used for loading and using the pretrained model
- For getting and drawing boxes from the predictions the implementation from https://github.com/experiencor/keras-yolo3
was adapted

#### Steps of Object Detection Pipeline
- Load the pretrained **YOLOv3** model
- Convert and prepare images for the model
- Predict the objects with the model
- Get boundary boxes with corresponding labels and scores from the prediction
- Draw boxes with labels and scores adapted for the original images
- Convert the images back to Base64 format and return the images

## References
- Docker: https://www.docker.com/
- Vue.js: https://vuejs.org/
- BootstrapVue: https://bootstrap-vue.org/
- vue-picture-swipe: https://github.com/rap2hpoutre/vue-picture-swipe
- Tutorial: Developing a Single Page App with Flask and Vue.js
https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/
- Tutorial: How to implement Webcam in VueJs Applcation
https://www.360learntocode.com/2020/12/how-to-implement-webcam-in-vuejs.html
- YOLOv3: https://arxiv.org/abs/1804.02767
- MSCOCO: https://cocodataset.org/#home
- Flask: https://flask.palletsprojects.com/en/2.0.x/
- OpenCV: https://opencv.org/
- Keras: https://keras.io/
- Tutorial: How to Perform Object Detection With YOLOv3 in Keras
https://machinelearningmastery.com/how-to-perform-object-detection-with-yolov3-in-keras/
- Implementation for boundary box:  https://github.com/experiencor/keras-yolo3