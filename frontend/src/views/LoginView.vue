<script setup>
import { useMessage } from "naive-ui";
import { ref } from "vue";
import '../assets/styles/AUTHStyle.css'
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';

const router = useRouter();
const formRef = ref(null);
const message = useMessage(); 
const size = ref("medium");
const errorMessage = ref("");

// ✅ keep consistent: using username everywhere
const formValue = ref({
  user: {
    username: "",
    password: ""
  },
});

const rules = {
  user: {
    username: {
      required: true,
      message: "Please input your username",
      trigger: "blur"
    },
    password: {
      required: true,
      message: "Please input your password",
      trigger: "blur"
    }
  },
};

// axios login
const login = async () => {
  try {
    const response = await axios.post("http://localhost:8080/auth/login", {
      identifier: formValue.value.user.username, // ✅ now matches
      password: formValue.value.user.password
    },{
      withCredentials: true
    })
    console.log("✅ CMI Login success:", response.data)

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

        <!-- ✅ Error alert now above the form -->
        <n-alert v-if="errorMessage" type="error" title="Login Error" closable style="margin-bottom: 1rem">
          {{ errorMessage }}
        </n-alert>

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

          <n-form-item path="user.password">
            <n-input type="password" v-model:value="formValue.user.password" placeholder="Password" />
          </n-form-item>

          <n-space item-style="display: flex;" align="center">
            <n-checkbox>Remember me</n-checkbox>
          </n-space>

          <n-button type="primary" @click="login">Log In</n-button>
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

  </div>
</template>
