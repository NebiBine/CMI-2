<script setup>
import { ref } from "vue";
import "../assets/styles/AUTHStyle.css";
import Stepper from "../components/Stepper/Stepper/Stepper.vue";
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';


const fullName = ref("");
const username = ref("");
const dob = ref(null);
const phone = ref("");
const street = ref("");
const city = ref("");
const country = ref("");
const zip = ref("");
const profilePicture = ref(null);
const fileList = ref([]);


//router
const router = useRouter();


// dummy handlers
const handleStepChange = (step) => {
    console.log("Step changed:", step);
};
const handleFileChange = (options) => {
  profilePicture.value = options.file.file;
};

//na koncu zajamem vse podatke
const handleFinalStepCompleted = async () => {
    try {
        const response = await axios.post(
    "http://localhost:8080/auth/newProfile",
    {
        fullname: fullName.value,
        username: username.value,
        dateOfBirth: dob.value,
        phoneNumber: phone.value,
        address_Street: street.value,
        address_City: city.value,
        address_Country: country.value,
        address_ZIP: zip.value,
    },
    { withCredentials: true }
    );
}
catch(error){
    console.log('axios error',error)
}
};


</script>

<template>
    <div class="auth-left">
        <div class = "Welcoming-Message">
            <h1>Welcome! Let’s get you set up</h1>
            <p>This will only take a couple of minutes.</p>
        </div>
        <div class="stepper-container">
            <Stepper :initial-step="1" :on-step-change="handleStepChange"
                :on-final-step-completed="handleFinalStepCompleted" back-button-text="Go Back" next-button-text="Next">
                <div class="step1">
                    <h2><b>Let’s set up your profile</b></h2>
                    <n-input type="text" v-model:value="fullName" placeholder="Full Name"></n-input>
                    <n-input type="text" v-model:value="username" placeholder="Username / Display Name"></n-input>
                </div>

                <div class="step2">
                    <h2>Tell us about yourself</h2>
                    <n-date-picker v-model:value="dob" type="date" placeholder="Date of birth" />
                    <n-input type="text"  v-model:value="phone" placeholder="Phone Number"></n-input>
                </div>

                <div class="step3">
                    <h2>Where can we reach you?</h2>
                    <n-input type="text" v-model:value="street" placeholder="Street Address"></n-input>
                    <n-input type="text" v-model:value="city" placeholder="City"></n-input>
                    <n-input type="text" v-model:value="country" placeholder="Country"></n-input>
                    <n-input type="text" v-model:value="zip" placeholder="ZIP / Postal Code"></n-input>
                </div>
                <div class="step5">
                    <h2>Review your details</h2>
                    <p><b>Full Name:</b> {{ fullName }}</p>
                    <p><b>Username:</b> {{ username }}</p>
                    <p><b>Date of Birth:</b> {{ dob }}</p>
                    <p><b>Phone:</b> {{ phone }}</p>
                    <p><b>Street:</b> {{ street }}</p>
                    <p><b>City:</b> {{ city }}</p>
                    <p><b>Country:</b> {{ country }}</p>
                    <p><b>ZIP:</b> {{ zip }}</p>
                </div>
            </Stepper>
        </div>
    </div>
</template>
