<template>
  <b-container class="container">
    <b-overlay :show="waitForResponse" rounded="sm">
      <b-row class="Home" align-h="center">
        <img alt="Vue logo" src="../assets/camera-outline.svg" height="200" width="200">
      </b-row>
      <b-row class="Title mb-2" align-h="center">
        <h1>Webcam Face Recognition Demo</h1>
      </b-row>
      <b-row class="camera-control mb-3" align-h="center">
        <b-col v-if="!isCameraOpen">
          <b-button variant="outline-success" @click="toggleCamera">
            Start Webcam Stream
          </b-button>
        </b-col>
        <b-col v-if="isCameraOpen">
          <b-button variant="outline-primary" @click="capture">
            Take Photos
          </b-button>
        </b-col>
        <b-col v-if="isCameraOpen">
          <b-button variant="outline-danger" @click="toggleCamera">
            Close Webcam Stream
          </b-button>
        </b-col>
      </b-row>
      <b-row class="camera-canvas" align-h="center" v-if="isCameraOpen">
        <video ref="camera" :width="canvasWidth" :height="canvasHeight" autoplay></video>
        <canvas v-show="false" id="photoTaken" :width="canvasWidth"
                :height="canvasHeight"></canvas>
        <canvas v-show="false" id="thumbnailTaken" :width="thumbnailWidth"
                :height="thumbnailHeight"></canvas>
      </b-row>
      <b-row class="mb-3" align-h="center">
        <vue-picture-swipe :items="items"></vue-picture-swipe>
      </b-row>
      <b-row align-h="center">
        <b-form v-if="this.isSubmittable()" @click="waitForResponse = true"
                @submit="onSubmit" class="container">
          <b-button type="submit" variant="primary">send photos</b-button>
        </b-form>
      </b-row>
    </b-overlay>
  </b-container>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import VuePictureSwipe from 'vue-picture-swipe';

export default {
  name: 'Home',
  components: {
    VuePictureSwipe,
  },
  data() {
    return {
      waitForResponse: false,
      editedPhotos: false,
      numPictures: 5,
      isCameraOpen: false,
      canvasHeight: 500,
      canvasWidth: 500,
      thumbnailHeight: 100,
      thumbnailWidth: 100,
      items: [],
    };
  },
  methods: {
    toggleCamera() {
      this.editedPhotos = false;
      if (this.isCameraOpen) {
        this.isCameraOpen = false;
        this.stopCameraStream();
      } else {
        this.isCameraOpen = true;
        this.startCameraStream();
      }
    },
    startCameraStream() {
      this.items = [];
      // eslint-disable-next-line no-multi-assign
      const constraints = (window.constraints = {
        audio: false,
        video: true,
      });
      navigator.mediaDevices
        .getUserMedia(constraints)
        .then((stream) => {
          this.$refs.camera.srcObject = stream;
        }).catch((error) => {
          alert(`Browser doesn't support or there is some errors.${error}`);
        });
    },
    isSubmittable() {
      const allPhotosTaken = this.items.length === this.numPictures;
      return allPhotosTaken && !this.editedPhotos;
    },
    stopCameraStream() {
      const tracks = this.$refs.camera.srcObject.getTracks();
      tracks.forEach((track) => {
        track.stop();
      });
    },

    capture() {
      const FLASH_TIMEOUT = 50;
      const self = this;
      setTimeout(async () => {
        // eslint-disable-next-line no-plusplus
        for (let i = 0; i < this.numPictures; i++) {
          // eslint-disable-next-line no-await-in-loop
          await new Promise((resolve) => setTimeout(resolve, 2000));
          const photoCanvas = document.getElementById('photoTaken');
          const context = photoCanvas.getContext('2d');
          context.drawImage(self.$refs.camera, 0, 0, self.canvasWidth, self.canvasHeight);
          const dataUrl = photoCanvas.toDataURL('image/jpeg')
            .replace('image/jpeg', 'image/octet-stream');
          const thumbnailCanvas = document.getElementById('thumbnailTaken');
          const thumbContext = thumbnailCanvas.getContext('2d');
          thumbContext.drawImage(self.$refs.camera, 0, 0,
            self.thumbnailWidth, self.thumbnailHeight);
          const thumbnailUrl = thumbnailCanvas.toDataURL('image/jpeg')
            .replace('image/jpeg', 'image/octet-stream');
          self.addToPhotoGallery(dataUrl, thumbnailUrl);
        }
        self.isCameraOpen = false;
        self.stopCameraStream();
      }, FLASH_TIMEOUT);
    },

    addToPhotoGallery(dataURI, thumbnailURI) {
      this.items.push(
        {
          src: dataURI,
          thumbnail: thumbnailURI,
          w: this.canvasWidth,
          h: this.canvasHeight,
          alt: 'some numbers on a grey background', // optional alt attribute for thumbnail image
        },
      );
    },
    sendPhotos(photoItems) {
      const path = 'http://localhost:5000/boundaryBox';
      const data = {
        photos: photoItems,
      };
      axios.post(path, data).then((response) => {
        this.items = response.data.editedPhotos;
        console.log(response);
        this.waitForResponse = false;
        this.editedPhotos = true;
      });
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.sendPhotos(this.items);
    },
  },
};
</script>
