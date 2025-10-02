<script setup>
import { ref, onMounted } from "vue";
import '../assets/styles/mainStyle.css'
import axios from 'axios'
import { NModal, NButton } from "naive-ui";

const users = ref([])
const openUserModal = (user) => {
  selectedUser.value = user; 
  showModal.value = true;      
};
const showModal = ref(false);
const selectedUser = ref(null);


const getAllUsers = async () => {
    try {
        const response = await axios.get(
            'http://localhost:8080/data/getAllUsers', {
            withCredentials: true
        })
        console.log(response.data)
        users.value = response.data
    }
    catch (error) {
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
    <div class="users_list">
    <ul>
      <li v-for="user in users" :key="user.id">
        <b>Username:</b>
        {{ user.username }}
        <b> Email: </b>{{ user.email }}
        <a href="#" @click.prevent="openUserModal(user)">
        More Info
        </a>
      </li>
    </ul>
  </div>
  <n-modal v-model:show="showModal" preset="dialog" title="User Details">
    <template #default>
      <p><b>Username:</b> {{ selectedUser?.username }}</p>
      <p><b>Email:</b> {{ selectedUser?.email }}</p>
      <p><b>ID:</b> {{ selectedUser?.id }}</p>
      
    </template>
  </n-modal>

</template>