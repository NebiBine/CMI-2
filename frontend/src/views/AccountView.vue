<script setup>
    import '../assets/styles/mainStyle.css';
    import axios from 'axios';
    import { ref,onMounted, computed } from 'vue';
    import checkMark from '../assets/icons/checkMark.png';
    import crossMark from '../assets/icons/crossMark.png';
    import { useMessage } from 'naive-ui';

    const editModeStandard = ref(false);
    const editModeSecurity = ref(false);
    const userProfile = ref({});
    const userProfilePicture = ref("");
    const userEmail = ref("");
    const userUsername = ref("");
    const newPassword = ref("");
    const confirmNewPassword = ref("");
    const passwordChangeState = ref(false);
    const message = useMessage();
    const oldPassword = ref("");

    function toggleEditModeStandard() {
        editModeStandard.value = !editModeStandard.value;
    }

    function toggleEditModeSecurity() {
        editModeSecurity.value = !editModeSecurity.value;
        if(editModeSecurity.value == false) {
            userProfile.value.password = "********";
            newPassword.value = "";
            confirmNewPassword.value = "";
        }
    }
    function changePasswordActiveState() {
        passwordChangeState.value = !passwordChangeState.value;
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
            userProfilePicture.value = response.data.pfp;
            userEmail.value = response.data.email;
            userUsername.value = response.data.username;
            console.log("Profile data retrieved successfully", userProfile.value);
            console.log("Profile picture URL:", userProfilePicture.value);
        }
        catch(error){
            console.log(error);
        }
    }
    //PRAVILA ZA MENJAVO PASSWORDA
    const isLengthValid = computed(() => newPassword.value.length >= 8 && confirmNewPassword.value.length >= 8);
    const passwordMatch = computed(() => newPassword.value === confirmNewPassword.value && newPassword.value.length > 0 && confirmNewPassword.value.length > 0);
    const hasUpperCase = computed(() => /[A-Z]/.test(newPassword.value));
    const hasNumber = computed(() => /[0-9]/.test(newPassword.value));
    const hasSpecialChar = computed(() => /[!@#$%^&*(),.?":{}|<>]/.test(newPassword.value));


    async function changePassword() {
        if (!isLengthValid.value || !passwordMatch.value || !hasUpperCase.value || !hasNumber.value || !hasSpecialChar.value) {
            message.warning("Please make sure your new password meets all the requirements before saving changes.");
            return;
        }
        try {
            const response = await axios.post('http://localhost:8000/auth/newPassword', 
            { 
                oldPassword: oldPassword.value,
                newPassword: newPassword.value
            },
            { withCredentials: true });
            message.success("Password changed successfully!");
            changePasswordActiveState(); //izklopim edit mode za password
            if(response.data.statusCode != 200){
                message.error(response.data.message);
            }
        } catch (error) {
            console.log(error);
            message.error("An error occurred while changing the password. Please try again.");
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
            <!--TODO: V dokumentacijo napisi da so bili razlicne opcije za servanje slike.-->
            <div class="profile-pic" style="align-items: center; justify-content: center; display: flex;">
                <img :src="userProfilePicture" alt="Profile Picture" class="profile-pic">
            </div>
            <p id="username"><strong>Username:</strong> {{ userUsername }}</p>
            <p id="email"><strong>Email:</strong> {{ userEmail }}</p>
        </div>
    <n-tabs type="line" animated>
        <n-tab-pane name="basicInfo" tab="Basic Information">
            <div class="edit_profile">
                <h2>Your information</h2>
                <n-button class="edit_profile_btn" @click="toggleEditModeStandard">Edit Profile <img src="../assets/icons/edit_profile.svg" alt="Edit Profile Icon" width="20px" height="20px" style="margin-left: 7px;"></n-button>
            </div>
        <div class="profile_info">
                <div class="firstLastName">
                    <p><strong>First Name:</strong> <n-input v-model:value="userProfile.first_name" :disabled="!editModeStandard"></n-input></p>
                    <p><strong>Last Name:</strong> <n-input v-model:value="userProfile.last_name" :disabled="!editModeStandard"></n-input></p>
                </div>
                <div class="dobMob">
                    <p><strong>Date of Birth:</strong> <n-input v-model:value="userProfile.birthdate" :disabled="!editModeStandard"></n-input></p>
                    <p><strong>Mobile Number:</strong> <n-input v-model:value="userProfile.phone" :disabled="!editModeStandard"></n-input></p>
                </div>
                <div class="location">
                    <p><strong>Country:</strong> <n-input v-model:value="userProfile.country" :disabled="!editModeStandard"></n-input></p>
                    <p><strong>City:</strong> <n-input v-model:value="userProfile.city" :disabled="!editModeStandard"></n-input></p>
                    <p><strong>Address:</strong> <n-input v-model:value="userProfile.address" :disabled="!editModeStandard"></n-input></p>
                </div>
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
            <div class="password-change-user">
                <p>Password: <n-input type="password" disabled placeholder="*********"></n-input></p>
                <n-button class="change_password_btn" @click="changePasswordActiveState">Change Password</n-button>
            </div>
            <div v-if="passwordChangeState" class="newPassword">
                <div class="new_password_fields">
                    <p>New Password:&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;<n-input type="password" v-model:value="newPassword" style="justify-content: center;"></n-input></p>
                    <p>Confirm New Password: <n-input type="password" v-model:value="confirmNewPassword" style="justify-content: center;"></n-input></p>
                </div>
                
                <div class="passRequirements">
                    <div style="display: flex; flex-direction: row; gap: 5px;">
                        <img :src="passwordMatch ? checkMark : crossMark" 
                            style="width: 20px; height: 20px;">
                        <p :style="{ color: passwordMatch ? 'green' : 'red' }">Passwords need to match</p>
                    </div>
                    <div style="display: flex; flex-direction: row; gap: 5px;">
                        <img :src="isLengthValid ? checkMark : crossMark" 
                            style="width: 20px; height: 20px;">
                        <p :style="{ color: isLengthValid ? 'green' : 'red' }">
                            Password must be at least 8 characters long
                        </p>
                    </div>
                    <div style="display: flex; flex-direction: row; gap: 5px;">
                        <img :src="hasUpperCase ? checkMark : crossMark" 
                            style="width: 20px; height: 20px;">
                        <p :style="{ color: hasUpperCase ? 'green' : 'red' }">Password must contain at least one uppercase letter</p>
                    </div>
                    <div style="display: flex; flex-direction: row; gap: 5px;">
                            <img :src="hasNumber ? checkMark : crossMark" 
                            style="width: 20px; height: 20px;">
                        <p :style="{ color: hasNumber ? 'green' : 'red' }">Password must contain at least one number</p>
                    </div>
                    <div style="display: flex; flex-direction: row; gap: 5px;">
                        <img :src="hasSpecialChar ? checkMark : crossMark" 
                            style="width: 20px; height: 20px;">
                        <p :style="{ color: hasSpecialChar ? 'green' : 'red' }">Password must contain at least one special character</p>
                    </div>
                </div>

                <div v-if="newPassword.length > 0 && confirmNewPassword.length > 0">
                    <p>Current Password: <n-input type="password" v-model:value="oldPassword" placeholder="Enter current password: "></n-input></p>
                </div>
                <div class="save_changes">
                    <n-button class="save_changes_btn" @click="changePassword">Save Changes</n-button>
                    <n-button class="cancel_changes_btn" @click="changePasswordActiveState">Cancel</n-button>
                </div>
            </div>
        </div>
        </n-tab-pane>
    </n-tabs>
</template>