<script setup>
import GridDistortion from '../components/Backgrounds/GridDistortion/GridDistortion.vue';
import TextType from '../components/TextAnimations/TextType/TextType.vue';
import '../assets/styles/WelcomePageStyle.css'
import { NButton } from 'naive-ui'
</script>

<template>
    <div class="WelcomePage-Logo">
        <img src="../assets/images/WelcomePage-Logo.png"></img>
    </div>
    <div class="welcomePage-Background">
        <GridDistortion
            imageSrc="https://picsum.photos/1920/1080"
            :grid="10"
            :mouse="0.1"
            :strength="0.15"
            :relaxation="0.9"
            class="force-fs"
        />
        <div class="dark-overlay"></div>
        </div>
    
    <div class = "WelcomeText">
        <TextType 
            :text="['Welcome to CMI', 'City Management Interface']"
            :typingSpeed="50"
            :pauseDuration="1000"
            :showCursor="false"
            cursorCharacter="|"
        />
    </div>
    <div class="WelcomePageDescription">
        <p>CMI is a centralized platform designed for smart and efficient urban management. It empowers administrators, planners, and decision-makers to organize, monitor, and optimize city operations from one intuitive interface. From infrastructure and public services to planning, analytics, and real-time monitoring, CMI provides the tools to keep cities connected, responsive, and future-ready.</p>
    </div>


    <div class="EnterButton">
  <router-link to="/auth/login">
    <n-button strong secondary>
      LogIn
    </n-button>
  </router-link>

  <router-link to="/auth/register">
    <n-button strong secondary>
      Register
    </n-button>
  </router-link>
</div>
  </template>