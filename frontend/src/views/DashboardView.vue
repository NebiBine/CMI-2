<script setup>
import { ref, onMounted } from "vue";
import '../assets/styles/mainStyle.css'
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';


const greeting = ref("");
const username = ref("");
const admin_state = ref(false);

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
onMounted(() => {
  setGreeting()
  profilData()
});

async function profilData() {
  try {
    const response = await axios.get(
      'http://localhost:8080/data/getProfile', {
      withCredentials: true
    })
    //vzamem username 
    username.value = response.data.username

  }
  catch (error) {
    console.log('Napaka pri pridobivanju podatkov profila');
    console.log(error);
  }
};
//dokoncaj admin check za dolocene gumbe
const adminCheck = async() => {
  try{
    const response = await axios.get(
      "http://localhost:8080/auth/checkAdmin",
      {withCredentials:true}
    )
    admin_state = response.data.admin;
    console.log("PREVERJANJE ADMIN DASHBOARD: ",admin_state );
  }
  catch(error){
    console.log(error);
  }
};

onMounted(() => {
  adminCheck();
});
</script>
<template>
  <div class="welcoming-block">
    <h1>{{ greeting }}, {{ username }}!</h1>
    <p>CMI connects you with essential urban services — from traffic updates and public transit to energy info and city guides. 
      Everything you need in one place.</p>
  </div>

  <div class = "Announcements">
    <h2>Announcements</h2>
  </div>
  <div class = "Announcements">
    <h2>Announcements</h2>
  </div>


  <div class = "quick-access">

  </div>


</template>