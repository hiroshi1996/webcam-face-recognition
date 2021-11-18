<template>
  <div class="container">
    <div class="Home">
      <img alt="Vue logo" src="../assets/logo.png">
      <HelloWorld msg="Welcome to Your Vue.js App"/>
      <ul id="example">
        <li v-for="(msg, index) in messages" :key="index">
          <p>{{ msg.text }}</p>
        </li>
      </ul>
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
    <b-form v-if="this.allPhotosTaken()" @submit="onSubmit2" class="container">
      <b-button-group>
        <b-button type="submit" variant="primary">send photos</b-button>
      </b-button-group>
    </b-form>
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-text-group"
                    label="Text:"
                    label-for="form-text-input">
        <b-form-input id="form-text-input"
                      type="text"
                      v-model="addMessageForm.text"
                      required
                      placeholder="Enter text">
        </b-form-input>
      </b-form-group>
      <b-button-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
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
      messages: [],
      addMessageForm: {
        text: '',
      },
      message: '',
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
      // const uniquePictureName = this.generateCapturePhotoName();
      // const capturedPhotoFile = this.dataURLtoFile(dataURLs, `${uniquePictureName}.jpg`);
      const path = 'http://localhost:5000/boundaryBox';
      // const formData = new FormData();
      // formData.append('photos', photoItems.length);
      // Upload image api
      const data = {
        photos: photoItems,
      };
      axios.post(path, data).then((response) => {
        this.items = response.data.editedPhotos;
        console.log(response);
      });
    },

    generateCapturePhotoName() {
      return Math.random().toString(36).substring(2, 15);
    },
    dataURLtoFile(dataURL, filename) {
      const arr = dataURL.split(',');
      const mime = arr[0].match(/:(.*?);/)[1];
      const bstr = atob(arr[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);

      // eslint-disable-next-line no-plusplus
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new File([u8arr], filename, { type: mime });
    },
    onSubmit2(evt) {
      evt.preventDefault();
      this.sendPhotos(this.items);
    },
    getMessages() {
      const path = 'http://localhost:5000/messages';
      axios.get(path)
        .then((res) => {
          this.messages = res.data.messages;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addText(payload) {
      const path = 'http://localhost:5000/messages';
      axios.post(path, payload)
        .then(() => {
          this.getMessages();
          this.message = 'Text added!';
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getMessages();
        });
    },
    initForm() {
      this.addMessageForm.text = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        text: this.addMessageForm.text,
      };
      this.addText(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.initForm();
    },
  },
  created() {
    this.getMessages();
  },
};
</script>
