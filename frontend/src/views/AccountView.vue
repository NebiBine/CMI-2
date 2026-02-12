<script setup>
    import '../assets/styles/mainStyle.css';
    import axios from 'axios';
    import { ref,onMounted } from 'vue';

    const editModeStandard = ref(false);
    const editModeSecurity = ref(false);

    function toggleEditModeStandard() {
        editModeStandard.value = !editModeStandard.value;
    }

    function toggleEditModeSecurity() {
        editModeSecurity.value = !editModeSecurity.value;
    }
</script>
<template>
        <h1>My Account</h1>
        <p>Manage your profile, security, and preferences.</p>
        <div class = "profile_card">
            <h2 style="font-weight: bolder; font-size: 25px;">Profile Information</h2>
            <div class="profile-pic"><!-- TODO: url(${profile_picture}) UPORABI TO V STYLU POTEM KO PRIDEM DO TEGA --></div>
            <p id="username"><strong>Username:</strong> John Doe</p>
            <p id="email"><strong>Email:</strong> john.doe@example.com</p>
        </div>
    <n-tabs type="line" animated>
        <n-tab-pane name="basicInfo" tab="Basic Information">
            <div class="edit_profile">
                <h2>Your information</h2>
                <n-button class="edit_profile_btn" @click="toggleEditModeStandard">Edit Profile <img src="../assets/icons/edit_profile.svg" alt="Edit Profile Icon" width="20px" height="20px" style="margin-left: 7px;"></n-button>
            </div>
        <div class="profile_info">
                <p><strong>First Name:</strong> <n-input value="John" :disabled="!editModeStandard"></n-input></p>
                <p><strong>Last Name:</strong> <n-input value="Doe" :disabled="!editModeStandard"></n-input></p>
                <p>Date of Birth: <n-input value="01/01/1990" :disabled="!editModeStandard"></n-input></p>
                <p>Mobile Number: <n-input value="+386 123 4565" :disabled="!editModeStandard"></n-input></p>
                <p>Country: <n-input value="SLO" :disabled="!editModeStandard"></n-input></p>
                <p>City: <n-input value="Škofja Loka" :disabled="!editModeStandard"></n-input></p>
                <p>Address:<n-input value="Slovenska cesta 12" :disabled="!editModeStandard"></n-input></p>
                <div v-if="editModeStandard == true" class="save_changes">
                    <n-button class="save_changes_btn">Save Changes</n-button>
                    <n-button class="cancel_changes_btn" @click="toggleEditModeStandard">Cancel</n-button>
                </div>
            </div>
        </n-tab-pane>
        <n-tab-pane name="security" tab="Security">
        <div class="edit_profile">
            <h2>Security Information</h2>
            <n-button class="edit_profile_btn" @click="toggleEditModeSecurity">Edit <img src="../assets/icons/edit_profile.svg" alt="Edit Profile Icon" width="20px" height="20px" style="margin-left: 7px;"></n-button>
        </div>
        <div class="profile_info">
            <h2 style="font-weight: bolder; font-size: 25px;">Security</h2>
            <p><strong>Password:</strong> <n-input value="*********" :disabled="!editModeSecurity"></n-input></p>
            <p><strong>Last Login:</strong> 01/01/2024 12:00 PM</p>
        </div>
        </n-tab-pane>
    </n-tabs>
</template>