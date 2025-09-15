<script setup>
import { useMessage } from "naive-ui";
import { ref } from "vue";
import '../assets/styles/AUTHStyle.css'

const formRef = ref(null);
const message = useMessage(); 
const size = ref("medium");

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
          <n-form-item path="user.username">
            <n-input v-model:value="formValue.user.username" placeholder="Username" />
          </n-form-item>

          <n-form-item path="user.password">
            <n-input
              type="password"
              v-model:value="formValue.user.password"
              placeholder="Password"
            />
          </n-form-item>

          <n-button type="primary">Log In</n-button>
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

    <div class="auth-right">
      <img src="../assets/images/login_photo.jpg" alt="City Infrastructure Map" />
    </div>
  </div>
</template>
