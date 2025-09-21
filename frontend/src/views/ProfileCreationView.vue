<script setup>
import { ref } from "vue";
import '../assets/styles/AUTHStyle.css'
import { useRouter } from "vue-router";
import { RouterLink } from "vue-router";
import axios from 'axios';
import Stepper from "../components/Stepper/Stepper/Stepper.vue"

//konstante




</script>
<template>
    <div class="ProfileCreateWrapper">
      <Stepper
    :initial-step="1"
    :on-step-change="handleStepChange"
    :on-final-step-completed="handleFinalStepCompleted"
    back-button-text="Previous"
    next-button-text="Next"
  >
    <div class = "step1">
      <h2>Welcome to the Vue Bits stepper!</h2>
      <p>Check out the next step!</p>
    </div>

    <div class = "step2">
      <h2>Step 2</h2>
      <img
        style="height: 100px; width: 100%; object-fit: cover; border-radius: 15px; margin-top: 1em;"
        src="https://example.com/image.jpg"
        alt="Example"
      />
      <p>Custom step content!</p>
    </div>

    <div class = "step3">
      <h2>How about an input?</h2>
      <input
        v-model="name"
        class="mt-2 px-3 py-2 border border-gray-300 rounded-md w-full"
        placeholder="Your name?"
      />
    </div>

    <div class = "step4">
      <h2>Final Step</h2>
      <p>You made it!</p>
    </div>
  </Stepper>
</div>
</template>