<template>
  <div class="container">
    <div class="Home">
      <img alt="Vue logo" src="../assets/logo.png">
      <HelloWorld msg="Welcome to Your Vue.js App"/>
    </div>
    <div class="camera-box">
      <div style="display: flex; justify-content: center;">
        <img style="height: 25px;" v-if="isCameraOpen"
             src="https://img.icons8.com/material-outlined/50/000000/camera--v2.png"
             class="button-img camera-shoot" @click="capture"/>
        <div class="camera-button">
          <button type="button" class="button is-rounded cam-button"
                  style="margin-left: 40%; background-color: white; border: 0px;"
                  @click="toggleCamera">
        <span v-if="!isCameraOpen"><img style="height: 25px;" class="button-img"
                                        src="https://img.icons8.com/material-outlined/50/000000/camera--v2.png"></span>
            <span v-else><img style="height: 25px;" class="button-img"
                              src="https://img.icons8.com/material-outlined/50/000000/cancel.png"></span>
          </button>
        </div>
      </div>
      <div style="height: 200px">
        <div v-if="isCameraOpen" class="camera-canvas">
          <video ref="camera" :width="canvasWidth" :height="canvasHeight" autoplay></video>
          <canvas v-show="false" id="photoTaken" ref="canvas" :width="canvasWidth"
                  :height="canvasHeight"></canvas>
        </div>
      </div>
      <vue-picture-swipe :items="items"></vue-picture-swipe>
    </div>
    <b-form v-if="this.allPhotosTaken()" @submit="onSubmit" class="container">
      <b-button-group>
        <b-button type="submit" variant="primary">send photos</b-button>
      </b-button-group>
    </b-form>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import VuePictureSwipe from 'vue-picture-swipe';
import HelloWorld from '@/components/HelloWorld.vue';

export default {
  name: 'Home',
  components: {
    HelloWorld,
    VuePictureSwipe,
  },
  data() {
    return {
      numPictures: 5,
      isCameraOpen: false,
      canvasHeight: 200,
      canvasWidth: 190,
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
          const context = self.$refs.canvas.getContext('2d');
          context.drawImage(self.$refs.camera, 0, 0, self.canvasWidth, self.canvasHeight);
          const dataUrl = self.$refs.canvas.toDataURL('image/jpeg')
            .replace('image/jpeg', 'image/octet-stream');
          self.addToPhotoGallery(dataUrl);
        }
        self.isCameraOpen = false;
        self.stopCameraStream();
      }, FLASH_TIMEOUT);
    },

    addToPhotoGallery(dataURI) {
      this.items.push(
        {
          src: dataURI,
          thumbnail: dataURI,
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
      });
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.sendPhotos(this.items);
    },
  },
};
</script>
