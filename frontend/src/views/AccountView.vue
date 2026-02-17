<script setup>
    import '../assets/styles/mainStyle.css';
    import axios from 'axios';
    import { ref,onMounted } from 'vue';

    const editModeStandard = ref(false);
    const editModeSecurity = ref(false);
    const InEdit = ref(false);
    const userProfile = ref({});

    function toggleEditModeStandard() {
        editModeStandard.value = !editModeStandard.value;
    }

    function toggleEditModeSecurity() {
        editModeSecurity.value = !editModeSecurity.value;
        if(editModeSecurity.value == false) {
            userProfile.value.password = "********";
        }
    }
    async function updateProfile() {
        const updatedProfile = {
            id: userProfile.value.id,
            first_name: userProfile.value.first_name,
            last_name: userProfile.value.last_name,
            birthdate: userProfile.value.birthdate,
            phone: userProfile.value.phone,
            address: userProfile.value.address,
            city: userProfile.value.city,
            country: userProfile.value.country,
            //password: userProfile.value.password,
            isAdmin: false,
            type: 0
        };
        try {
            const response = await axios.post("http://localhost:8000/profile/updateProfile",
                updatedProfile,
                { withCredentials: true });
            console.log("Profile updated successfully", response.data);
            getProfileData(); //osvežim podatke da se prikaže nova verzija
            editModeStandard.value = false; //izklopim edit mode    
        }
        catch (error) {
            console.log(error);
        }
    }

    async function getProfileData(){
        try{
            const response = await axios.post('http://localhost:8000/profile/getProfile',
            { userId: 0,
                type: 0 }, //type 0 ker hocem podatke o trenutnem userju, type 1 je za admin user management view da dobim podatke o userju ki ga admin gleda
            {withCredentials: true});
            userProfile.value = response.data.profile;
            console.log("Profile data retrieved successfully", userProfile.value);
        }
        catch(error){
            console.log(error);
        }
    }
onMounted(() => {
    getProfileData();
});
</script>
<template>
        <h1>My Account</h1>
        <p>Manage your profile, security, and preferences.</p>
        <div class = "profile_card">
            <h2 style="font-weight: bolder; font-size: 25px;">Profile Information</h2>
            <div class="profile-pic" style="align-items: center;"><img :src="userProfile.profile_picture_url" alt="Profile Picture"></div>
            <p id="username"><strong>Username:</strong> {{ userProfile.username }}</p>
            <p id="email"><strong>Email:</strong> {{ userProfile.email }}</p>
        </div>
    <n-tabs type="line" animated>
        <n-tab-pane name="basicInfo" tab="Basic Information">
            <div class="edit_profile">
                <h2>Your information</h2>
                <n-button class="edit_profile_btn" @click="toggleEditModeStandard">Edit Profile <img src="../assets/icons/edit_profile.svg" alt="Edit Profile Icon" width="20px" height="20px" style="margin-left: 7px;"></n-button>
            </div>
        <div class="profile_info">
                <p><strong>First Name:</strong> <n-input v-model:value="userProfile.first_name" :disabled="!editModeStandard"></n-input></p>
                <p><strong>Last Name:</strong> <n-input v-model:value="userProfile.last_name" :disabled="!editModeStandard"></n-input></p>
                <p>Date of Birth: <n-input v-model:value="userProfile.birthdate" :disabled="!editModeStandard"></n-input></p>
                <p>Mobile Number: <n-input v-model:value="userProfile.phone" :disabled="!editModeStandard"></n-input></p>
                <p>Country: <n-input v-model:value="userProfile.country" :disabled="!editModeStandard"></n-input></p>
                <p>City: <n-input v-model:value="userProfile.city" :disabled="!editModeStandard"></n-input></p>
                <p>Address:<n-input v-model:value="userProfile.address" :disabled="!editModeStandard"></n-input></p>
                <div v-if="editModeStandard == true" class="save_changes">
                    <n-button class="save_changes_btn" @click="updateProfile" >Save Changes</n-button>
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
            <p><strong>Password:</strong> <n-input v-model:value="userProfile.password" :disabled="!editModeSecurity"></n-input></p>
            <p><strong>Last Login:</strong> 01/01/2024 12:00 PM</p>
        </div>
        </n-tab-pane>
    </n-tabs>
</template>