<script setup>
import { ref, onMounted } from "vue";
import '../assets/styles/mainStyle.css'
import axios from 'axios'

const users = ref([])



const getAllUsers = async() => {
    try{
        const response = await axios.get(
      'http://localhost:8080/data/getAllUsers', {
      withCredentials: true
    })
    console.log(response.data)
    users.value = response.data
    }
    catch(error){
        console.log(error)
    }
}
onMounted(() => {
    getAllUsers()
});
</script>
<template>
    <h1>User Management</h1>
    
    <!--LISTAM USE USERJE-->
    <ul>
        <li v-for="user in users" :key="user.id">{{ user.username }},{{ user.email }}</li>
    </ul>


</template>