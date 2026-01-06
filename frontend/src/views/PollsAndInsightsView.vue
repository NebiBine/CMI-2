<script setup>
import '../assets/styles/mainStyle.css'
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import PollParticipateIcon from "@/assets/icons/poll_participate_icon.svg";

const polls = ref([]);
const showModal = ref(false);
const selectedPoll = ref(null);
const selectedPollId = ref("");
//testna konstanta DONT USE... USE IN TESTING PURPOSES
//const time_left = new Date(polls.expirationDate).getDate() - new Date().getDate();


//TODO : Popravi posiljanje odgovorov ker verjetno niso v enakem formatu
//----------------------------------------------------------------------
function closeModal() {
    showModal.value = false;
}
function openModal(poll) {

    showModal.value = true;
    selectedPoll.value = poll;

    selectedPoll.value.questions.forEach(question => {
        if (question.type === 'checkbox' || question.type === 'radioButtons') {
            question.answer = ["", "", "", ""];
        } else {
            question.answer = '';
        }
    });
}

async function getPolls() {
    try {
        const response = await axios.get("http://localhost:8000/poll-reward/getPolls",
            { withCredentials: true });
        polls.value = response.data;
        console.log("Fetched polls:", polls.value);
    }
    catch (error) {
        console.log(error);
    }
}

async function pollParticipationSubmit(selectedPoll){
    //zdruzim vse vprasanja in odgovore in id v eno konstanto
    const CombinedQuestionAnswer = selectedPoll.questions.map((question) => {
        return {
            questionId : question.id,
            questionText: question.text,
            answer: question.answer
        };
    });

    const pollAnswers = {
        pollId : selectedPoll.id,
        pollQuestions: CombinedQuestionAnswer
    }
    try{
        const response = await axios.post("http://localhost:8000/poll-reward/completePoll", 
        pollAnswers, 
        { withCredentials: true });
    }
    catch(error){
        console.log(error)
    }


    console.log("Poll Answers to submit:", pollAnswers);

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
                <!--OSNOVNI PODATKI -->
                <h2 class="pollTitle">{{ poll.pollTitle }}</h2>
                <div class="pollDetails">

                    <div class="pollDescriptionInfo">
                        <p>{{ poll.pollDescription }}</p>
                    </div>

                    <div class="pollPointsInfo">
                        <p>Possible points: {{ poll.points }}</p>
                    </div>

                    <div class="timeLeftInfo">
                        <p>Time left(in days): {{ new Date(poll.expirationDate).getDate() - new Date().getDate() }}</p>
                    </div>
                </div>


                <n-button @click="openModal(poll)">Participate</n-button>
                <n-modal v-model:show="showModal" preset="dialog" title="Participate in the Poll"
                    @positive-click="pollParticipationSubmit(poll)" @negative-click="closeModal">
                    <!--IKONA MODALA-->
                    <template #icon>
                        <img src="../assets/icons/poll_participate_icon.svg" alt="Poll Participate Icon"
                            class="modal-icon" />
                    </template>
                    <div v-if="selectedPoll">
                        <!--LOOP ZA VPRASANJA-->

                        <div v-for="(question, questionIndex) in selectedPoll.questions" :key="questionIndex">
                            <p class="question-text">{{ questionIndex + 1 }}. {{ question.text }}</p>


                            <!--VSI CHECKI KATERI TIP JE ZA VSAKO VPRASANJE IN POTEM PRILAGODIM ODGOVORE GLEDE NA TYPE-->
                            <div v-if="question.type == 'yesno'" class="optionsWrapper">
                                <label>
                                    <input type="radio" :name="`poll-${selectedPoll.id}-q${questionIndex}`" value="Yes" v-model = "question.answer"> Yes
                                </label>
                                <label>
                                    <input type="radio" :name="`poll-${selectedPoll.id}-q${questionIndex}`" value="No" v-model = "question.answer"> No
                                </label>
                            </div>


                            <div v-else-if="question.type == 'input'" class="optionsWrapper">
                                <input type="text" :name="`poll-${selectedPoll.id}-q${questionIndex}`"
                                    placeholder="Your answer here:" v-model="question.answer"/>
                            </div>


                            <div v-else-if="question.type == 'radioButtons'" class="optionsWrapper">
                                <template v-for="(option, optionIndex) in question.options" :key="optionIndex">
                                    <label v-if="option" class="option-label">
                                        <input type="radio" :name="`poll-${selectedPoll.id}-q${questionIndex}`" :value="option" v-model="question.answer">
                                        {{ option }}
                                    </label>
                                </template>
                            </div>


                            <div v-else-if="question.type == 'checkbox'" class="optionsWrapper">
                                <template v-for="(option, optIndex) in question.options" :key="optIndex">
                                    <label v-if="option" class="option-label">
                                        <input type="checkbox" :name="`poll-${selectedPoll.id}-q${questionIndex}-${optIndex}`"
                                            :value="option" v-model="question.answer">
                                        {{ option }}
                                    </label>
                                </template>
                            </div>

                        </div>

                    </div>
                    <n-button type="primary" class="submitpollBtn" @click="pollParticipationSubmit(selectedPoll)">Submit your
                        answers</n-button>
                    <n-button class="cancelpollBtn" @click="closeModal">Cancel</n-button>
                </n-modal>
            </div>
        </div>
    </div>
</template>