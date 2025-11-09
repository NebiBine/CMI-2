<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faPlus,faSquarePollVertical } from '@fortawesome/free-solid-svg-icons';

import { ref, onMounted } from "vue";
import '../assets/styles/mainStyle.css'
import axios from 'axios'


const showModal = ref(false);
const pollName = ref("");
const pollDuration = ref(1);

const openModal = () => {
    showModal.value = true;
}
const closeModal = () => {
    showModal.value = false;
}
// const addPoll = () =>{
//     try{
//         const response = await axios.post("url",
//         {withCredentials:true})
//         closeModal();
//     }
//     catch(error){
//         console.log(error);
//     }
// }
</script>
<template>
    <h1>Poll Management</h1>
    <button class="add_btn" @click="openModal()">
        <FontAwesomeIcon :icon="faPlus" /> Add Poll
    </button>
    <div class="poll_section">
        <h3><b>Active now</b></h3>
        <p>test11</p>

        <h3><b>Past Due</b></h3>
        <p>test22</p>
    </div>



    <n-modal v-model:show="showModal" preset="dialog" title="Create a new poll">
        <template #icon>
            <FontAwesomeIcon :icon="faSquarePollVertical" style="color: blue; font-size: 20px;"/>
        </template>
        <template #default>
            <label for id="fullName"> Poll Name:
                <n-input id="fullName" placeholder="" v-model:value="pollName"></n-input>
            </label>
            <label for id="username"> Poll Duration:
                <n-slider v-model:value="pollDuration" :step="1" :max="60" />
            </label>
            <n-button @click="closeModal()">Add Poll</n-button>
            <n-button @click="closeModal()">Close</n-button>
        </template>
    </n-modal>
</template>