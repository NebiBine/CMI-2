<script setup>
import { ref, onMounted } from "vue";
import { NAlert, NButton } from 'naive-ui'
import '../assets/styles/mainStyle.css';
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';
import { message } from "ant-design-vue";



const greeting = ref("");
const username = ref("");
const admin_state = ref(false);
const showAlert = ref(true);
const announcements = ref([]);

function setGreeting() {
  const hour = new Date().getHours()

  if (hour < 12) {
    greeting.value = "Good Morning"
  }
  else if (hour < 18) {
    greeting.value = "Good Afternoon"
  }
  else {
    greeting.value = "Good Evening"
  }
}


async function profilData() {
  try {
    const response = await axios.get(
      'http://localhost:8000/auth/getProfile', {
      withCredentials: true
    })
    //vzamem username 
    username.value = response.data.username
    //message.success(response.data.message);
  }
  catch (error) {
    console.log('Napaka pri pridobivanju podatkov profila');
    //message.error(error.response.data.error);
    console.log(error);
  }
};
async function getAnnouncement(){
  try{
    const response = await axios.get(
      'http://localhost:8000/dashboard/getAnnouncement', 
      {withCredentials: true});
      announcements.value = response.data;
  }
  catch (error) {
    console.log('Error while fetching announcements');
    console.log(error);
  }
}

onMounted(() => {
  setGreeting(),
  profilData(),
  getAnnouncement()
});
</script>
<template>

<div v-for="announcement in announcements" :key="announcement.id">
    <n-alert type="info" closable @close="showAlert = false" :title="announcement.title">
      {{ announcement.content }}
    </n-alert>
  </div>


  <div class="welcoming-block">
    <h1>{{ greeting }}, {{ username }}!</h1>
    <p>CMI connects you with essential urban services — from traffic updates and public transit to energy info and city guides. 
      Everything you need in one place.</p>
  </div>
  <div class = "widgetsWrapper">
    <div class = "PollRewardsWidget">
      <h2>Polls & Rewards Overview</h2>
    </div>
    <div class = "TrafficUpdatesWidget">
      <h2>Traffic Overview</h2>
    </div>
    <div class = "WeatherWidget">
      <h2>Weather Overview</h2>
    </div>
    <div class = "EnergyInfoWidget">
      <h2>Energy Overview</h2>
    </div>
  </div>



  <div class = "quick-access">

  </div>


</template>