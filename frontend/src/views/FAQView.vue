<script setup>
import '../assets/styles/mainStyle.css'
import { ref } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faCircleQuestion } from '@fortawesome/free-regular-svg-icons'
</script>
<template>
    <div class="faq-page">
        <h1>FAQ</h1>
        <p>Frequently Asked Questions.</p>

        <div class="faq">
            <n-collapse>
                <template #arrow>
                    <n-icon>
                        <FontAwesomeIcon :icon="faCircleQuestion" />
                    </n-icon>
                </template>
                <n-collapse-item title="Question 1" name="1">
                    <div>good</div>
                </n-collapse-item>
                <n-collapse-item title="Question 2" name="2">
                    <div>nice</div>
                </n-collapse-item>
                <n-collapse-item title="Question 3" name="3">
                    <div>very good</div>
                </n-collapse-item>
            </n-collapse>
        </div>
    </div>
</template>