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

      <n-button class="welcome_btn"><RouterLink to="/auth/login">Login</RouterLink></n-button>
      <n-button class="welcome_btn"><RouterLink to="/auth/register">Register</RouterLink></n-button>
    </div>
    <div class="cmiCompany">
      <h1>CMI Company</h1>
      <!-- p - 24  -->
      <p>Enterprise solutions for business growth</p>
      
      <n-button class="welcome_btn" disabled>Login</n-button>
      <n-button class="welcome_btn" disabled>Register</n-button>
    </div>
  </div>
  <section class="belowContent">
    <div class="container">
      <h2>More About CMI</h2>
      <p>Put your next page content here.</p>
      <!-- whatever you need next -->
    </div>
  </section>



</template>