<script setup>
import '../assets/styles/mainStyle.css'
import { ref, onMounted } from 'vue';
import axios from 'axios';

const userPoints = ref(0);

async function getUserPoints(){
    try{
        const response = await axios.get("http://localhost:8000/poll-reward/getUserPoints",
        { withCredentials: true });
        userPoints.value = response.data;
    }
    catch(error){
        console.log(error)
    }
}

onMounted(() => {
    getUserPoints();
});
</script>
<template>
    <h1>Rewards</h1>
    <p>Look through the available rewards here and redeem them!</p>
    <p>Your current points: {{ userPoints }}</p>
    <div v-for="reward in rewards">
        <!--TODO: PRIKAZI REWARDE TUKAJ V TEM DIVU--> 
    </div>
</template>
