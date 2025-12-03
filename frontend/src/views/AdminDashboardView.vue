<script setup>
import { ref } from "vue";
import '../assets/styles/mainStyle.css';


const announcementModal = ref(false);
const announcementHeadline = ref("");
const announcementContent = ref("");

const showAnnouncementModal = () => {
    announcementModal.value = true;
}
const closeAnnouncementModal = () => {
    announcementModal.value = false;
}
function announcementData() {
    console.log("Headline:", announcementHeadline.value);
    console.log("Content:", announcementContent.value);
    announcementModal.value = false;
}

</script>
<template>
    <h1>Admin Dashboard</h1>
    <p>Welcome to the CMI Admin Panel. Use the sidebar on the left to manage users, content, and settings.</p>
    <button @click="showAnnouncementModal()">Add an announcement</button>
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
            <n-input id="headline" v-model:value="announcementHeadline" placeholder="Headline"></n-input>

            <label for="content">Add content for the announcement:</label>
            <n-input id="content" v-model:value="announcementContent" placeholder="Content"></n-input>
            <button @click="announcementData()" class="modal_btn">Submit your announcement</button>
            <button @click="closeAnnouncementModal()" class="modal_btn">Close</button>
        </template>
    </n-modal>
</template>