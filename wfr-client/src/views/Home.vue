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
import HelloWorld from '@/components/HelloWorld.vue';

export default {
  name: 'Home',
  components: {
    HelloWorld,
  },
  data() {
    return {
      messages: [],
      addMessageForm: {
        text: '',
      },
      message: '',
    };
  },
  methods: {
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
