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
    <div class="app">
  <div class="text">
    <h1>Join CMI – Your City, Smarter</h1>
  </div>
  <div class = "RegisterDescription">
    <p>Sign up to access city services and personalized updates.</p>
</div>

  <div class="register-form">
    <n-form
      ref="formRef"
      :label-width="80"
      :model="formValue"
      :rules="rules"
      :size="size"
        >
      <n-form-item label="Username" path="user.username">
        <n-input v-model:value="formValue.user.username" placeholder="Username" />
      </n-form-item>
      <n-form-item label="Email" path="user.username">
        <n-input v-model:value="formValue.user.email" placeholder="Email" />
      </n-form-item>
      <n-form-item label="Password" path="user.password">
        <n-input v-model:value="formValue.user.password" placeholder="Password" />
      </n-form-item>
      <n-button @click="register">Create Account</n-button>
    </n-form>
    <p>Already registered? <router-link to="/auth/login">Log in here</router-link></p>
  </div>
</div>
</template>