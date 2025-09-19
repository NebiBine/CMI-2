<script setup>
import { useMessage } from "naive-ui";
import { ref } from "vue";
import '../assets/styles/AUTHStyle.css'
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';
import { error } from "naive-ui/es/_utils/naive/warn";


const router = useRouter();
const formRef = ref(null);
const message = useMessage(); 
const size = ref("medium");
const value = ref(false)
const errorMessage = ref("");

const formValue = ref({
  user: {
    username: "",
    password: ""
  },
});

const rules = {
    //required polja za vsak vnos
  user: {
    username: {
      required: true,
      message: "Please input your username",
      trigger: "blur"
    },
    password: {
      required: true,
      message: "Please input your pasword",
      trigger: "blur"
    }
  },
};
//axios post
const login = async () => {
  try {
    const response = await axios.post("http://localhost:8080/auth/login", {
      identifier: formValue.value.user.identifier,
      password: formValue.value.user.password
    },{
      withCredentials: true
    })
    console.log("✅ CMI Login success:", response.data)
    //ob successfull loginu redirect na dashboard
    if (response.data.success === true) {
      router.push("/app/Dashboard");
    } else {
      errorMessage.value = "Invalid credentials. Please try again.";
    }
  } catch (error) {
    console.error("❌ CMI Login error:", error);
    errorMessage.value = "Login failed. Please check your connection or credentials.";
  }
 
};
</script>
<template>
  <div class="auth-page">
    <div class="auth-left">
      <div class="login-container">
        <h1>Welcome Back to CMI!</h1>
        <p class="subtitle">Log in to manage your city services and stay updated.</p>

        <n-form
          ref="formRef"
          :label-width="0"
          :model="formValue"
          :rules="rules"
          :size="size"
        >
          <n-form-item path="user.identifier">
            <n-input v-model:value="formValue.user.identifier" placeholder="Username" />
          </n-form-item>

          <n-form-item path="user.password">
            <n-input type="password" v-model:value="formValue.user.password" placeholder="Password" />
          </n-form-item>
          <n-space item-style="display: flex;" align="center">
            <n-checkbox
              checked-value="Oznaceno"
              unchecked-value="Neoznaceno"
              @update:checked="handleRememberMe">
              Remember me
            </n-checkbox>
          </n-space>

          <n-button type="primary" @click = "login">Log In</n-button>
        </n-form>

        <div class="login-footer">
          <p>
            Don’t have an account?
            <RouterLink to="/auth/register">Register here</RouterLink>
          </p>
          <p><RouterLink to="/auth/ForgotPassword">Forgot your password?</RouterLink></p>
        </div>
      </div>
    </div>
    <n-alert title="Error Text" type="error" closable v-if="errorMessage">
      I{{errorMessage}}
    </n-alert>

    <div class="auth-right">
      <img src="../assets/images/login_photo.jpg" alt="City Infrastructure Map" />
    </div>
  </div>
</template>