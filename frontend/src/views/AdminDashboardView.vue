<script setup>
import { ref } from "vue";
import '../assets/styles/mainStyle.css';
import axios from 'axios';


const announcementModal = ref(false);
const announcementTitle = ref("");
const announcementContent = ref("");
const announcementType = ref("");

const announcementTypeOptions = [
    { label: '📢 Default', value: 'default' },
    { label: 'ℹ️ Info', value: 'info' },
    { label: '✅ Success', value: 'success' },
    { label: '⚠️ Warning', value: 'warning' },
    { label: '❌ Error', value: 'error' }
]

const showAnnouncementModal = () => {
    announcementModal.value = true;
}
const closeAnnouncementModal = () => {
    announcementModal.value = false;
}
//TODO: NAREDI DA SE LAHKO ANNOUNCEMENT TUDI IZBRISE IZ BAZE
async function announcementData() {
    try{
        const response = await axios.post('http://localhost:8000/dashboard/createAnnouncement',
        {
            title: announcementTitle.value,
            content: announcementContent.value,
            type: announcementType.value
        },
        {withCredentials: true});
        if (response.status === 200) {
            console.log('Announcement submitted successfully');
        }
    }
    catch (error) {
        console.log('Error while submitting announcement');
        console.log(error);
    }
    closeAnnouncementModal();
    announcementTitle.value = "";
    announcementContent.value = "";
    announcementType.value = "";
}

</script>
<template>
    <h1>Admin Dashboard</h1>
    <p>Welcome to the CMI Admin Panel. Use the sidebar on the left to manage users, content, and settings.</p>
    <button @click="showAnnouncementModal()" class="add_btn_announcement">Add an announcement</button>
    <div class="Announcements">
        <h2>A quick overview</h2>
    </div>
    <div class="Announcements">
        <h2>A quick overview</h2>
    </div>


    <n-modal v-model:show="announcementModal" preset="dialog" title="Add an announcement" class="announcementModal">
        <template #icon>
            <img src="../assets/icons/megaphone.png" />
        </template>
        <template #default>
            <label for="headline">Add a headline for the announcement:</label>
            <n-input id="headline" v-model:value="announcementTitle" placeholder="Headline"></n-input>

            <label for="content">Add content for the announcement:</label>
            <n-input id="content" v-model:value="announcementContent" placeholder="Content"></n-input>
            <label for="type">Pick the type of the announcement:</label>
            <n-select id="type" v-model:value="announcementType" :options="announcementTypeOptions" placeholder="Type"></n-select>
            <button @click="announcementData()" class="add_btn_announcement">Submit your announcement</button>
            <button @click="closeAnnouncementModal()"  style="margin-left: 5px;margin-top: 5px;" class="deleteReward">Close</button>
        </template>
    </n-modal>
</template>