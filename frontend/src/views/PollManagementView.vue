<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faPlus, faSquarePollVertical, faXmark } from '@fortawesome/free-solid-svg-icons';
import { ref,onMounted } from "vue";
import '../assets/styles/mainStyle.css';
import axios from 'axios';

const username = ref("");
const modal_state1 = ref(false);
const modal_state2 = ref(false);
const possible_points_value = ref(0);
const questions = ref([]);

const open_modal1 = () => {
    modal_state1.value = true;
}
const open_modal2 = () => {
  modal_state2.value = true;
};


const polltypeOptions = [
  { label: "Yes/No question", value: "yesno" },
  { label: "Input type question", value: "input" },
  { label: "Pick one question (radio buttons)", value: "radioButtons" },
  { label: "Pick multiple questions (checkbox)", value: "checkbox" },
];

const closeModal = () => {
  modal_state2.value = false;
};

const addQuestion = () => {
  questions.value.push({ text: "", type: "", options: [] });
};

const removeQuestion = (index) => {
  questions.value.splice(index, 1);
};

const addOption = (question) => {
  question.options.push("");
};

const setDefaultOptions = (question) => {
console.log("setDefaultOptions called for question:", question);
  if (question.type === "yesno") {
    question.options = ["Yes", "No"];
  } else if (question.type === "input") {
    question.options = [];
  } else if (question.type === "radioButtons" || question.type === "checkbox") {
    question.options = ["", "", "", ""];
  }
};
const submitQuestions = () => {
  console.log("submitQuestions called");
  console.log("Questions before submission:", questions.value);
  console.log("Submitted Questions:", questions.value);
  closeModal();
};

async function profilData() {
  try {
    const response = await axios.get(
      'http://localhost:8080/data/getProfile', {
      withCredentials: true
    })
    //vzamem username 
    username.value = response.data.username

  }
  catch (error) {
    console.log('Napaka pri pridobivanju podatkov profila');
    console.log(error);
  }
};
//ONLOAD
onMounted(() => {
  profilData()
});
</script>
<template>
    <h1>Poll Management</h1>
    <br></br>
    <p>Welcome admin {{ username }}. Here you can manage polls for your citizens!</p>

    <button class="add_btn" @click="open_modal1()">
        <FontAwesomeIcon :icon="faPlus" /> Add Poll
    </button>

    <br></br>
    <h3>Currently active polls</h3>
    <br></br>
    <h3>Past Due Polls Statistics</h3>


  <n-modal
    v-model:show="modal_state1"
    preset="dialog"
    title="Add Poll"
    positive-text="Submit"
    negative-text="Cancel"
    @positive-click="submitCallback"
    @negative-click="cancelCallback">
    <!-- poll title -->
    <label for="poll_name">Poll Name:
        <n-input type = "text" id = "poll_name" placeholder ="Enter Poll Title (eg. New city project)"></n-input>
    </label>
    <!-- poll duration -->
    <label for="poll_duration">Poll Duration:
        <n-slider v-model:value="pollDuration" :step="1" :max="60" />
    </label>
    <label for id="expires"> Expires at:
        <n-date-picker v-model:value="timestamp" type="date" />
    </label>
    <label for="possible_points">Possible points
        <n-input-number  id= "possible_points" v-model:value="possible_points_value" clearable/>
    </label>
    <n-button class = "btn_add_questions" @click="open_modal2()">Add questions</n-button>
  </n-modal>


  <!------------------- MODAL ZA DODAJANJE VPRAŠANJ ------------------->
  <n-modal
    v-model:show="modal_state2"
    preset="dialog"
    title="Create Poll Questions"
    positive-text="Submit"
    negative-text="Cancel"
    @positive-click="submitQuestions"
    @negative-click="closeModal"
  >
    <!-- Render questions -->
    <div v-for="(question, index) in questions" :key="index" class="question-item">
        <p>Debug: Options = {{ question.options }}</p>
        <label>
        Question:
        <n-input
          v-model="question.text"
          placeholder="Enter your question"
          style="width: 100%; margin-bottom: 10px;"
        />
      </label>
      <label>
        Type:
        <n-select
          v-model="question.type"
          :options="polltypeOptions"
          placeholder="Select question type"
          style="width: 100%; margin-bottom: 10px;"
          @change="setDefaultOptions(question)"
        />
      </label>
      
      <!-- Show predefined options -->
      <div v-if="question.type === 'yesno'">
        <p>Options: Yes, No</p>
      </div>
      <div v-else-if="question.type === 'input'">
        <p>Input field will be provided for the user.</p>
      </div>
      <div v-else-if="question.type === 'radioButtons' || question.type === 'checkbox'">
        <div v-for="(option, optIndex) in question.options" :key="optIndex">
          <n-input
            v-model="question.options[optIndex]"
            :placeholder="`Enter option ${optIndex + 1}`"
            style="width: 100%; margin-bottom: 5px;"
          />
        </div>
        <n-button size="small" @click="addOption(question)" style="margin-top: 5px;">
          Add Option
        </n-button>
      </div>

      <n-button
        type="error"
        size="small"
        @click="removeQuestion(index)"
        style="margin-top: 10px;"
      >
        Remove Question
      </n-button>
    </div>

    <!-- Add new question button -->
    <n-button @click="addQuestion" type="primary" style="margin-top: 10px;">
      Add Question
    </n-button>
  </n-modal>
</template>

