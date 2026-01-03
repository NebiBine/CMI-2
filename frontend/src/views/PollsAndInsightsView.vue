<script setup>
import '../assets/styles/mainStyle.css'
import { ref, onMounted } from 'vue'; // 1. Added missing imports
import axios from 'axios'; 

const polls = ref([]);

async function getPolls() {
    try {
        const response = await axios.get("http://localhost:8000/poll-reward/getPolls",
            { withCredentials: true });
        polls.value = response.data;
    }
    catch (error) {
        console.log(error);
    }
}
onMounted(() => {
    getPolls();
});
</script>
<template>
    <div class="polls-and-insights-view">
        <h1>Polls and Insights</h1>
        <p>This is where users can view and participate in polls and insights.</p>
        <div class="polls-container">
            <div v-for="poll in polls" :key="poll.id" class="EnPoll">
                <h2>{{ poll.pollTitle }}</h2>
                <p>Possible points: {{ poll.points }}</p>

                <div v-for="(question, questionIndex) in poll.questions" :key="questionIndex">
                    <p>{{ questionIndex + 1 }}. {{ question.text }}</p>


                    <div v-if="question.type == 'yesno'" class="optionsWrapper">
                            <label>
                                <input type="radio" :name="`poll-${poll.id}-q${questionIndex}`" value="Yes"> Yes
                            </label>
                            <label>
                                <input type="radio" :name="`poll-${poll.id}-q${questionIndex}`" value="No"> No
                            </label>
                    </div>
                    <div v-else-if="question.type == 'input'" class="optionsWrapper">
                            <input type="text" :name="`poll-${poll.id}-q${questionIndex}`" placeholder="Your answer here:">
                    </div>
                    <div v-else-if="question.type == 'radioButtons'" class="optionsWrapper">
                        <template v-for="(option, optionIndex) in question.options" :key="optionIndex">
                            <label v-if="option" class="option-label">
                                <input type="radio" :name="`poll-${poll.id}-q${questionIndex}`" :value="option">
                                {{ option }}
                            </label>
                    </template>
                    </div>
                    <div v-else-if="question.type == 'checkbox'" class="optionsWrapper">
                    <template v-for="(option, optIndex) in question.options" :key="optIndex">
                        <label v-if="option" class="option-label">
                            <input type="checkbox" :name="`poll-${poll.id}-q${questionIndex}-${optIndex}`" :value="option">
                            {{ option }}
                        </label>
                    </template>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>