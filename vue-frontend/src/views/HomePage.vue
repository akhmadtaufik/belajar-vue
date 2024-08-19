<template>
  <Navbar />
  <main>
    <h1>Home Page</h1>
    <Form>
      <div class="flex">
        <div class="flex">
          <label for="tweet">Tweet</label>
          <textarea rows="10" cols="10"></textarea>
        </div>
        <div class="button">
          <button class="button">Submit</button>
          <button @click="showModal">Show Modal</button>
        </div>
      </div>
    </Form>

    <Card />
    <Card />
    <Card />
    <Card />
    <Card />

    <div class="modal" v-if="showModal">
      <div class="modal-container">
        <div class="flex">
          <label for="upload_foto">Upload Foto</label>
          <input type="file" id="foto" class="foto" />
        </div>
        <div class="flex">
          <label for="tweet_modal">Tweet</label>
          <textarea type="text" cols="10" id="tweet"></textarea>
        </div>
        <div class="button">
          <button>Submit</button>
          <button @click="toggleModal">Cancel</button>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import Form from '@/components/Form.vue'
import Card from '@/components/Card.vue'

import { ref } from 'vue'

const showModal = ref(false)

const toggleModal = () => {
    console.log("Click")
    showModal.value = !showModal.value
}
</script>

<style scoped>
main {
  margin-top: 10pt;
  padding-left: 20%;
  padding-right: 20%;
}

form {
  background-color: #ebebeb;
  padding: 20pt;
  border-radius: 10pt;
}

.flex {
  display: flex;
  flex-direction: column;
}

.button{
    margin-top:.5rem;
   
}

button {
  padding: 10pt;
  background-color: blue;
  color: white;
  border: none;
  border-radius: 5pt;
  margin: 10pt;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.7)
}

.input{
  border: 1px solid black;
  padding: 10pt;
}

.modal-container{
  background-color: #ebebeb;
  padding: 20pt;
  margin-top: 20pt;
  width: 60%;
  margin-left: 20%;}
</style>
