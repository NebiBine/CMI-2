<script setup>
import GridDistortion from '../components/Backgrounds/GridDistortion/GridDistortion.vue';
import TextType from '../components/TextAnimations/TextType/TextType.vue';
import '../assets/styles/WelcomePageStyle.css'
import { NButton } from 'naive-ui'
</script>

<template>
  <div class="cmiWrapper">
    <div class="cmiCity">
      <h1>CMI City</h1>
      <!-- p - 24  -->
      <p>Explore urban solutions and city management</p>

      <button class="welcome_btn"><RouterLink to="/auth/login">Login</RouterLink></button>
      <button class="welcome_btn"><RouterLink to="/auth/register">Register</RouterLink></button>
    </div>
    <div class="cmiCompany">
      <h1>CMI Company</h1>
      <!-- p - 24  -->
      <p>Enterprise solutions for business growth</p>
      
      <button>Login</button>
      <button>Register</button>
    </div>



  </div>




</template>