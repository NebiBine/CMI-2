<script setup>
import { ref, onMounted } from "vue";
import '../assets/styles/mainStyle.css'
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';
import { TorusGeometry } from "three";

const greeting = ref("")
const username = ref("")

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
    try{
        const response = await axios.get(
        'http://localhost:8080/data/getProfile',{
            withCredentials: true
        })
        //vzamem username 
        username.value = response.data.username
        
    }
    catch(error){
        console.log('Napaka pri pridobivanju podatkov profila');
        console.log(error);
    }



};

// DODAJ DA SE USERNAME PRIKAZE DESNO ZGORAJ V NAVBARU IN IMA TOOLTIP KI UPORABNIKA PREUSMERJA NA SIDEBAR KJER LAHKO UREJA PROFIL

</script>
<template>
<h1>{{greeting}}, {{ username }}!</h1>


</template>