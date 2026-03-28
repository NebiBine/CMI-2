<script setup>
import { useMessage } from "naive-ui";
import { computed, ref } from "vue";
import '../assets/styles/AUTHStyle.css'
import axios from 'axios';
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import { message } from 'ant-design-vue';
import checkMark from '../assets/icons/checkMark.png';
import crossMark from '../assets/icons/crossMark.png';

const router = useRouter();
const formRef = ref(null);
const size = ref("medium");
const gumb_rules = ref(false);
const showRequirementsState = ref(false);

const formValue = ref({
  user: {
    username: "",
    password: ""
  },
  phone: ""
});

const rules = {
    //required polja za vsak vnos
    //vsako polje je REQUIRED in ce ni izpolnjeno pokazem message spodaj pod vnosom
  user: {
    username: {
      required: true,
      message: "Please input your name",
      trigger: "blur"
    },
    email: {
      required: true,
      message: "Please input your email",
      trigger: "blur"
    },
    password: {
      required: true,
      message: "Please input your paswword",
      trigger: "blur"
    }
  },
};
function showRequirements() {
  showRequirementsState.value = !showRequirementsState.value;;
}
const isLengthValid = computed(() => formValue.value.user.password.length >= 8);
const hasUpperCase = computed(() => /[A-Z]/.test(formValue.value.user.password));
const hasNumber = computed(() => /[0-9]/.test(formValue.value.user.password));
const hasSpecialChar = computed(() => /[!@#$%^&*(),.?":{}|<>]/.test(formValue.value.user.password));

//axios
//try catch ce je error samo catcham z console logom da ne crasha vse skupaj
async function register() {
  if(isLengthValid.value==false || hasUpperCase.value==false || hasNumber.value==false || hasSpecialChar.value==false){
    message.warning("Password does not meet the requirements.");
    return;
  }
  try {
    const response = await axios.post("http://localhost:8000/auth/register", {
      username: formValue.value.user.username,
      email : formValue.value.user.email,
      password: formValue.value.user.password,
    },
    {withCredentials: true});
    console.log("✅ CMI Register success:", response.data)
    if(response.data.statusCode === 200){
      router.push('/auth/ProfileCreation');
      message.success(response.data.message);
    }
    else{
      message.error(response.data.message)
    }
    //message.success("Registration successful!") notify userju ce je registracija uspesna
  } catch (error) {
    console.error("❌ CMI Register error:", error)
    message.error(error.response.data.message);
  }
}

</script>

<template>
  <div class="auth-page">
    <!-- Left Side -->
    <div class="auth-left">
      <h1>Join CMI – Your City, Smarter</h1>
      <div class="login-container">
        <p class="subtitle">Sign up to access city services and personalized updates.</p>
        <n-form
          ref="formRef"
          :label-width="0"
          :model="formValue"
          :rules="rules"
          :size="size"
        >
          <n-form-item path="user.username">
            <n-input v-model:value="formValue.user.username"  placeholder="Username" />
          </n-form-item>

          <n-form-item path="user.email">
            <n-input v-model:value="formValue.user.email" placeholder="Email" />
          </n-form-item>

          <n-form-item path="user.password">
            <n-input type="password" v-model:value="formValue.user.password" placeholder="Password" @focus="showRequirements"/>
          </n-form-item>
          <div class="passRequirements" v-if="showRequirementsState">
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

          <n-button type="primary"class="log-reg_btn" @click="register">Create Account</n-button>
        </n-form>

        <div class="login-footer">
          <p>Already registered? <RouterLink to="/auth/login" class="povezave">Log in here</RouterLink></p>
        </div>
      </div>
    </div>
  </div>
</template>