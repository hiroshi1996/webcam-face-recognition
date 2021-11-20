<template>
  <div class="container">
    <b-overlay :show="waitForResponse" rounded="sm" >
    <div class="Home">
      <img alt="Vue logo" src="../assets/camera-outline.svg" height="200" width="200">
      <h1>Webcam Face Recognition Demo</h1>
    </div>
    <div class="camera-box">
      <div style="display: flex; justify-content: center;">
        <img style="height: 25px;" v-if="isCameraOpen"
             src="../assets/camera-outline.svg"
             class="button-img camera-shoot" @click="capture"/>
        <div class="camera-button">
          <button type="button" class="button is-rounded cam-button"
                  style="margin-left: 40%; background-color: white; border: 0px;"
                  @click="toggleCamera">
        <span v-if="!isCameraOpen"><img style="height: 25px;" class="button-img"
                                        src="../assets/camera-outline.svg"></span>
            <span v-else><img style="height: 25px;" class="button-img"
                              src="../assets/close-circle-outline.svg"></span>
          </button>
        </div>
      </div>
      <div style="height: 200px">
        <div v-if="isCameraOpen" class="camera-canvas">
          <video ref="camera" :width="canvasWidth" :height="canvasHeight" autoplay></video>
          <canvas v-show="false" id="photoTaken" :width="canvasWidth"
                  :height="canvasHeight"></canvas>
          <canvas v-show="false" id="thumbnailTaken" :width="thumbnailWidth"
                  :height="thumbnailHeight"></canvas>
        </div>
      </div>
      <vue-picture-swipe :items="items"></vue-picture-swipe>
    </div>
    <b-form v-if="this.allPhotosTaken()" @click="waitForResponse = true"
            @submit="onSubmit" class="container">
      <b-button-group>
        <b-button type="submit" variant="primary">send photos</b-button>
      </b-button-group>
    </b-form>
    </b-overlay>
  </div>
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
    allPhotosTaken() {
      return this.items.length === this.numPictures;
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
      });
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.sendPhotos(this.items);
    },
    resizeThumbnail(base64Str) {
      return new Promise((resolve) => {
        const img = new Image();
        img.src = base64Str;
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, this.thumbnailWidth, this.thumbnailHeight);
        resolve(canvas.toDataURL());
      });
    },
  },
};
</script>
