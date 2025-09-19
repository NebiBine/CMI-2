<script setup>
import { ref } from "vue";
import '../assets/styles/AUTHStyle.css'
import { v4 as uuidv4 } from "uuid"
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';

const router = useRouter();
const formRef = ref(null);
const size = ref("medium");


// ✅ keep consistent: using username everywhere
const formValue = ref({
  user: {
    email: "",
  },
});

const rules = {
  user: {
    email: {
      required: true,
      message: "Please input your email",
      trigger: "blur"
    }
  },
};

// axios 
const forgotPassword = async () => {
  const token = uuidv4()
  const resetlink = `http://localhost:5173/auth/PasswordReset/${token}`
  try {
    const response = await axios.post("http://localhost:8080/auth/ForgotPassword", {
      email: formValue.value.user.email,
      resetlink
    },{
      withCredentials: true
    })
    console.log("✅ Success:", response.data);
    console.log(resetlink);
  } catch (error) {
    console.error("❌ Error:", error);
    console.log(resetlink);
  }
};
</script>

<template>
  <div class="auth-page">
    <div class="auth-left">
      <div class="login-container">
        <h1>Forgot your password</h1>
        <p class="subtitle">Enter your email and we’ll send you a reset link.</p>
        <n-form
          ref="formRef"
          :label-width="0"
          :model="formValue"
          :rules="rules"
          :size="size"
        >
          <n-form-item path="user.email">
            <n-input v-model:value="formValue.user.email" placeholder="Email" />
          </n-form-item>

          <n-button type="primary" @click="forgotPassword">Send reset link</n-button>
        </n-form>

        <div class="login-footer">
          <p><i>Make sure to check <b>spam inbox</b> aswell!</i></p>
          <p><RouterLink to="/auth/login">← Back to Login</RouterLink></p>
        </div>
      </div>
    </div>

  </div>
</template>
