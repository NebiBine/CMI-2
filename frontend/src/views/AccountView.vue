<script setup>
    import '../assets/styles/mainStyle.css';
    import axios from 'axios';
    import { ref,onMounted } from 'vue';

    const editMode = ref(false);

    function toggleEditMode() {
        editMode.value = !editMode.value;
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
       <div class="edit_profile">
         <n-button class="edit_profile_btn" @click="toggleEditMode">Edit Profile <img src="../assets/icons/edit_profile.svg" alt="Edit Profile Icon" width="20px" height="20px" style="margin-left: 7px;"></n-button>
       </div>
       <div v-if="editMode == true" class="profile_info">
        <div class="user_info">
            <h2 style="font-weight: bolder; font-size: 25px;">Your information</h2>
            <p><strong>First Name:</strong> <n-input value="John" ></n-input></p>
            <p><strong>Last Name:</strong> <n-input value="Doe" ></n-input></p>
            <p>Date of Birth: <n-input value="01/01/1990" ></n-input></p>
            <p>Mobile Number: <n-input value="+386 123 4565" ></n-input></p>
            <p>Country: <n-input value="SLO" ></n-input></p>
            <p>City: <n-input value="Škofja Loka" ></n-input></p>
            <p>Address:<n-input value="Slovenska cesta 12"></n-input></p>
        </div>
        <div class="security_info">
            <h2 style="font-weight: bolder; font-size: 25px;">Security</h2>
            <p><strong>Password:</strong> <n-input value="*********" ></n-input></p>
            <p><strong>Last Login:</strong> 01/01/2024 12:00 PM</p>
        </div>
       </div>


       <div v-if="editMode == false" class="profile_info">
        <div class="user_info">
            <h2 style="font-weight: bolder; font-size: 25px;">Your information</h2>
            <p><strong>First Name:</strong> <n-input value="John" disabled></n-input></p>
            <p><strong>Last Name:</strong> <n-input value="Doe" disabled></n-input></p>
            <p>Date of Birth: <n-input value="01/01/1990" disabled></n-input></p>
            <p>Mobile Number: <n-input value="+386 123 4565" disabled></n-input></p>
            <p>Country: <n-input value="SLO" disabled></n-input></p>
            <p>City: <n-input value="Škofja Loka" disabled></n-input></p>
            <p>Address: <n-input value="Slovenska cesta 12" disabled></n-input></p>
        </div>
        <div class="security_info">
            <h2 style="font-weight: bolder; font-size: 25px;">Security</h2>
            <p><strong>Password:</strong> <n-input value="*********" disabled></n-input></p>
            <p><strong>Last Login:</strong> 01/01/2024 12:00 PM</p>
        </div>
       </div>
</template>