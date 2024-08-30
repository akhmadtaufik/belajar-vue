<template>
  <Navbar />
  <RouterView />
</template>

<script setup>
import './assets/main.css'
import Navbar from './components/Navbar.vue'
import { RouterView } from 'vue-router'
</script>
