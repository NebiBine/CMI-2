<script setup>
import { ref } from "vue";
import '../assets/styles/mainStyle.css';


const announcementModal = ref(false);
const announcementTitle = ref("");
const announcementContent = ref("");
const announcementType = ref("");

const announcementTypeOptions = [
    { label: 'Default', value: 'default' },
    { label: 'Info', value: 'info' },
    { label: 'Success', value: 'success' },
    { label: 'Warning', value: 'warning' },
    { label: 'Error', value: 'error' }
]

const showAnnouncementModal = () => {
    announcementModal.value = true;
}
const closeAnnouncementModal = () => {
    announcementModal.value = false;
}
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


    <n-modal v-model:show="announcementModal" preset="dialog" title="Add an announcement">
        <!-- <template #icon>
            <FontAwesomeIcon :icon="faSquarePollVertical" style="color: blue; font-size: 20px;" />
        </template> -->
        <template #default>
            <label for="headline">Add a headline for the announcement:</label>
            <n-input id="headline" v-model:value="announcementTitle" placeholder="Headline"></n-input>

            <label for="content">Add content for the announcement:</label>
            <n-input id="content" v-model:value="announcementContent" placeholder="Content"></n-input>
            <label for="type">Add content for the announcement:</label>
            <n-select id="type" v-model:value="announcementType" :options="announcementTypeOptions" placeholder="Content"></n-select>
            <button @click="announcementData()" class="modal_btn">Submit your announcement</button>
            <button @click="closeAnnouncementModal()" class="modal_btn">Close</button>
        </template>
    </n-modal>
</template>