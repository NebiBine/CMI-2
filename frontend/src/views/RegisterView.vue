<script setup>
import { useMessage } from "naive-ui";
import { ref } from "vue";
import '../assets/styles/AUTHStyle.css'
import axios from 'axios';

const formRef = ref(null);
const message = useMessage(); 
const size = ref("medium");

const formValue = ref({
  user: {
    username: "",
    password: ""
  },
  phone: ""
});

const rules = {
    //required polja za vsak vnos
  user: {
    username: {
      required: true,
      message: "Please input your name",
      trigger: "blur"
    }
  },
};

//axios
//try catch ce je error samo catcham z console logom da ne crasha vse skupaj
const register = async () => {
  try {
    const response = await axios.post("http://localhost:8080/auth/register", {
      username: formValue.value.user.username,
      email : formValue.value.user.email,
      password: formValue.value.user.password

    })
    console.log("✅ CMI Register success:", response.data)
    //message.success("Registration successful!") notify userju ce je registracija uspesna
  } catch (error) {
    console.error("❌ CMI Register error:", error)
    //message.error("Registration failed") notify userju da registracija ni uspesna
  }
}

</script>

<template>
  <div class="auth-page">
    <!-- Left Side -->
    <div class="auth-left">
      <div class="login-container">
        <h1>Join CMI – Your City, Smarter</h1>
        <p class="subtitle">Sign up to access city services and personalized updates.</p>

        <n-form
          ref="formRef"
          :label-width="0"
          :model="formValue"
          :rules="rules"
          :size="size"
        >
          <n-form-item path="user.username">
            <n-input v-model:value="formValue.user.username" placeholder="Username" />
          </n-form-item>

          <n-form-item path="user.email">
            <n-input v-model:value="formValue.user.email" placeholder="Email" />
          </n-form-item>

          <n-form-item path="user.password">
            <n-input type="password" v-model:value="formValue.user.password" placeholder="Password" />
          </n-form-item>

          <n-button type="primary" @click="register">Create Account</n-button>
        </n-form>

        <div class="login-footer">
          <p>Already registered? <RouterLink to="/auth/login">Log in here</RouterLink></p>
        </div>
      </div>
    </div>

    <!-- Right Side -->
    <div class="auth-right">
      <img src="../assets/images/login_photo.jpg" alt="City Services Illustration" />
    </div>
  </div>
</template>