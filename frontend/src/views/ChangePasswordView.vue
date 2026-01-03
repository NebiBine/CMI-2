<script setup>
import { ref } from "vue";
import '../assets/styles/AUTHStyle.css'
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';
import { useRoute } from "vue-router"

const route = useRoute()
const token = route.params.token

const router = useRouter();
const formRef = ref(null);
const size = ref("medium");

const formValue = ref({
  user: {
    newPassword: "",
    confirmNewPassword:""
  },
});

const rules = {
  user: {
    newPassword: {
      required: true,
      message: "Please input your new password",
      trigger: "blur"
    },
    confirmNewPassword: [
      {
        required: true,
        message: "Please confirm your new password",
        trigger: "blur"
      },
      {
        validator: (rule, value) => { //rule passa naiveui value je pa value vnosnega polja confirm new password
          if (value !== formValue.value.user.newPassword) { //ce je value (kar je vneseno v polju drugacno od zgornjega polja)
            return new Error("Both passwords must be the same"); //returnam ta error
          }
          return true; //v nasprotnem primeru all good
        },
        trigger: "blur"
      }
    ]
  },
};

// axios
async function passwordReset() {
  try {
    await formRef.value?.validate(); // validiraj form da je vse kot mora bit potem pojdi naprej
    const response = await axios.post(`http://localhost:8000/auth/resetPassword`, {
      newPassword: formValue.value.user.newPassword,
      token
    },{
      withCredentials: true
    })
    console.log("✅ Success:", response.data)
  } catch (error) {
    console.error("❌ Error:", error);
    console.log(token);
  }
};
</script>

<template>
  <div class="auth-page">
    <div class="auth-left">
      <div class="login-container">
        <h1>Forgot your password</h1>
        <p class="subtitle">Please enter your new password below. Make sure it’s strong and secure.</p>
        <n-form
          ref="formRef"
          :label-width="0"
          :model="formValue"
          :rules="rules"
          :size="size"
        >
          <n-form-item path="user.newPassword">
            <n-input v-model:value="formValue.user.newPassword" placeholder="New password" />
          </n-form-item>
          <n-form-item path="user.confirmNewPassword">
            <n-input v-model:value="formValue.user.confirmNewPassword" placeholder="Confirm new password" />
          </n-form-item>

          <n-button type="primary" @click="passwordReset">Reset Password</n-button>
        </n-form>

        <div class="login-footer">
          <p><RouterLink to="/auth/login">← Back to Login</RouterLink></p>
          
        </div>
      </div>
    </div>

  </div>
</template>
