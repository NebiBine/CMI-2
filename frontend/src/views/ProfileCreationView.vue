<script setup>
import { ref } from "vue";
import "../assets/styles/AUTHStyle.css";
import Stepper from "../components/Stepper/Stepper/Stepper.vue";
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';
import { message } from "ant-design-vue";
import Confetti from '@/components/ui/confetti/Confetti.vue';



const firstName = ref("");
const lastName = ref("");
const bio = ref("");
const dob = ref(null);
const phone = ref("");
const address = ref("");
const city = ref("");
const country = ref("");
const profilePicture = ref(null);
const fileList = ref([]);
const confettiRef = ref(null);


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
async function handleFinalStepCompleted() {
    try {
        const formdata = new FormData();
        formdata.append("first_name", firstName.value);
        formdata.append("last_name", lastName.value);
        formdata.append("birthdate", new Date(dob.value).toLocaleDateString("sl-SI"));
        formdata.append("phone", phone.value);
        formdata.append("address", address.value);
        formdata.append("city", city.value);
        formdata.append("country", country.value);
        formdata.append("bio", bio.value);

        if (profilePicture.value) {
            formdata.append("profilePicture", profilePicture.value);
        }
        //axios post vseh podatkov vkljucno z sliko
        const response = await axios.post(
            "http://localhost:8000/profile/createProfile",
            formdata,
            { withCredentials: true }
        );
        //success
        console.log("Profile creation success", response)
        if (response.data.statusCode === 200) {
            confettiRef.value?.fire({
                particleCount: 90,
                spread: 140,
                startVelocity: 35,
                ticks: 160,
                gravity: 0.8,
                scalar: 1.3,
                colors: ['#22d3ee', '#f59e0b', '#10b981', '#6366f1'],
                origin: { x: 0.5, y: 0.35 }
            });
            setTimeout(() => router.push('/app/Dashboard'), 1500);
            message.success(response.data.message);
        }

    }
    //error
    catch (error) {
        console.log('Full axios error:', error);
        console.log('Response:', error.response);
        console.log('Response data:', error.response?.data);

        if (error.response?.data?.detail) {
            message.error(error.response.data.detail);
        } else if (error.response?.data?.message) {
            message.error(error.response.data.message);
        } else if (error.response?.status) {
            message.error(`Error ${error.response.status}: ${error.response.statusText || 'Request failed'}`);
        } else {
            message.error('Network error. Please check your connection.');
        }
    }
};


</script>

<template>
    <div class="auth-left">
        <div class="Welcoming-Message">
            <h1>Welcome! Let’s get you set up</h1>
            <p>This will only take a couple of minutes.</p>
        </div>
        <div class="stepper-container">
            <Stepper :initial-step="1" :on-step-change="handleStepChange"
                :on-final-step-completed="handleFinalStepCompleted" back-button-text="Go Back" next-button-text="Next">
                <div class="step1">
                    <h2><b>Let’s set up your profile</b></h2>
                    <n-input type="text" v-model:value="firstName" placeholder="First Name"></n-input>
                    <n-input type="text" v-model:value="lastName" placeholder="Last Name"></n-input>
                    <n-input type="text" v-model:value="bio" placeholder="Bio"></n-input>
                </div>

                <div class="step2">
                    <h2>Tell us about yourself</h2>
                    <n-date-picker v-model:value="dob" type="date" placeholder="Date of birth" />
                    <n-input type="text" v-model:value="phone" placeholder="Phone Number"></n-input>
                </div>

                <div class="step3">
                    <h2>Where can we reach you?</h2>
                    <n-input type="text" v-model:value="address" placeholder="Street Address"></n-input>
                    <n-input type="text" v-model:value="city" placeholder="City"></n-input>
                    <n-input type="text" v-model:value="country" placeholder="Country"></n-input>
                </div>
                <div class="step4">
                    <h2>Upload your profile picture</h2>
                    <n-upload :default-file-list="fileList" list-type="image-card" :on-change="handleFileChange"
                        :max="1" accept=".jpg,.jpeg,.png,.gif,.webp,.jp2,.heif,.heic">
                        Click to Upload
                    </n-upload>
                </div>
                <div class="step5">
                    <h2>Review your details</h2>
                    <p><b>Full Name:</b> {{ firstName }}{{ lastName }}</p>
                    <p><b>Date of Birth:</b> {{ dob }}</p>
                    <p><b>Phone:</b> {{ phone }}</p>
                    <p><b>Street:</b> {{ address }}</p>
                    <p><b>City:</b> {{ city }}</p>
                    <p><b>Country:</b> {{ country }}</p>
                </div>
                <div class="step6">
                    <Confetti ref="confettiRef" class="absolute inset-0 z-0 size-full pointer-events-none" />
                    <h2>You have successfully set up your profile!</h2>
                    <p>Your profile has been set up successfully. Click 'Complete' to proceed to your dashboard.</p>
                </div>
            </Stepper>
        </div>
    </div>
</template>
