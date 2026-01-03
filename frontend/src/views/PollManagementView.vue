<script setup>
import { ref, onMounted } from "vue";
import '../assets/styles/mainStyle.css';
import axios from 'axios';
import { message } from "ant-design-vue";


const username = ref("");

//MODAL STANJA
const modal_state1 = ref(false);
const modal_state2 = ref(false);

//MODAL 1 VREDNOSTI
const possible_points_value = ref(0);
const pollTitle = ref("");
const pollDuration = ref(0);

//VPRAŠANJA ARRAY
const questions = ref([]);

const Poll = ref([]);

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
const closeModal1 = () => {
  modal_state1.value = false;
};

const addQuestion = () => {
  questions.value.push({ text: "", type: "", options: ["", "", "", ""] });
};

const removeQuestion = (index) => {
  questions.value.splice(index, 1);
};

const addOption = (question) => {
  question.options.push("");
};

const handleTypeChange = (question) => {
  if (question.type === "yesno") {
    question.options = ["Yes", "No", "", ""];
  } else if (question.type === "input") {
    question.options = ["", "", "", ""];
  } else if (question.type === "radioButtons" || question.type === "checkbox") {
    question.options = ["", "", "", ""];
  }
};
const submitQuestions = () => {
  console.log("Submitted Questions:", questions.value);
  closeModal();
};

async function pollSubmit() {
  const pollData = {
    pollTitle: pollTitle.value,
    pollDuration: pollDuration.value,
    points: possible_points_value.value,
    questions: questions.value
  };
  console.log(pollData);
  closeModal1();
  try {
    const response = await axios.post(
      "http://localhost:8000/poll-reward/addPoll",
      pollData,
      { withCredentials: true });
    if (response.data.statusCode === 200) {
      message.success(response.data.message);
    }
    else {
      message.error(response.data.message);
    }
  }

  catch (error) {
    console.log(error)
  }
  pollTitle.value = "";
  pollDuration.value = 0;
  possible_points_value.value = 0;
  questions.value = [];
}





async function profilData() {
  try {
    const response = await axios.get(
      'http://localhost:8000/auth/getProfile', {
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
  <p>Welcome admin {{ username }}. Here you can manage and view polls for your citizens!</p>

  <button class="add_btn" @click="open_modal1()">
    Add Poll
  </button>

  <br></br>
  <h3>Currently active polls</h3>
  <br></br>
  <h3>Past Due Polls Statistics</h3>

  <!------------------- MODAL ZA DODAJANJE ANKETE ------------------->
  <n-modal v-model:show="modal_state1" preset="dialog" title="Add Poll" positive-text="Submit" negative-text="Cancel"
    @positive-click="pollSubmit" @negative-click="closeModal1" :style="{ width: '600px', height: 'auto' }">
    <!-- poll title -->
    <label for="poll_name">Poll Name:
      <n-input type="text" id="poll_name" v-model:value="pollTitle"
        placeholder="Enter Poll Title (eg. New city project)"></n-input>
    </label>
    <label for="poll_description">Poll Description:
      <n-input type="text" id="poll_description" v-model:value="pollDescription"
        placeholder="Enter Poll Description"></n-input>
    </label>
    <!-- poll duration -->
    <label for="poll_duration">Poll Duration:
      <n-slider v-model:value="pollDuration" :step="1" :max="7" />
    </label>
    <!-- <label for id="expires"> Expires at:
      <n-date-picker v-model:value="timestamp" type="date" />
    </label> -->
    <label for="possible_points">Possible points
      <n-input-number id="possible_points" v-model:value="possible_points_value" clearable />
    </label>
    <n-button class="btn_add_questions" @click="open_modal2()">Add questions</n-button>
    <div>
      <label for="added_questions">Added questions:
        <n-list v-if="questions.length > 0" bordered style="margin-top: 10px;">
          <template #header>
            <h4>Questions</h4>
          </template>

          <n-list-item v-for="(question1, index1) in questions" :key="index1">
            <template #prefix>
              <strong>{{ index1 + 1 }}</strong>
            </template>
            <n-thing :title="question1.text" :description="`Type: ${question1.type}`">
              <!-- YES/NO -->
              <div v-if="question1.type === 'yesno'">
                Options: Yes, No
              </div>

              <!-- INPUT -->
              <div v-else-if="question1.type === 'input'">
                User types answer (no options)
              </div>

              <!-- RADIO / CHECKBOX -->
              <div v-else>
                <p>Options:</p>
                <ul style="margin-left: 15px;">
                  <li v-for="(options1, optIndex) in question1.options" :key="optIndex">
                    {{ options1 }}
                  </li>
                </ul>
              </div>
            </n-thing>
          </n-list-item>
        </n-list>
      </label>
    </div>

  </n-modal>


  <!------------------- MODAL ZA DODAJANJE VPRAŠANJ ------------------->
  <n-modal v-model:show="modal_state2" preset="dialog" title="Create Poll Questions" positive-text="Submit"
    negative-text="Cancel" @positive-click="submitQuestions" @negative-click="closeModal">
    <!-- Vsa vprašanja -->
    <div v-for="(question, index) in questions" :key="index" class="question-item"
      style="margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #eee;">
      <label>
        Question {{ index + 1 }}:
        <n-input v-model:value="question.text" placeholder="Enter your question"
          style="width: 100%; margin-bottom: 10px;" />
      </label>

      <label>
        Type:
        <n-select v-model:value="question.type" :options="polltypeOptions" placeholder="Select question type"
          style="width: 100%; margin-bottom: 10px;" @update:value="() => handleTypeChange(question)" />
      </label>

      <!-- YES / NO -->
      <div v-if="question.type === 'yesno'">
        <p>Options: <strong>Yes</strong> / <strong>No</strong></p>
      </div>

      <!-- INPUT -->
      <div v-else-if="question.type === 'input'">
        <p>User will answer with a text input field.</p>
      </div>

      <!-- RADIO BUTTONS or CHECKBOX: 4 option inputs -->
      <div v-else-if="question.type === 'radioButtons' || question.type === 'checkbox'">
        <p>Enter up to 4 options:</p>
        <div v-for="(option, optIndex) in question.options" :key="optIndex" style="margin-bottom: 6px;">
          <n-input v-model:value="question.options[optIndex]" :placeholder="`Option ${optIndex + 1}`"
            style="width: 100%;" />
        </div>
      </div>

      <!-- Gumb za odstranjevanje vprašanja -->
      <n-button type="error" size="small" @click="removeQuestion(index)" style="margin-top: 10px;">
        Remove Question
      </n-button>
    </div>

    <!-- Dodaj novo vprašanje -->
    <n-button type="primary" @click="addQuestion">
      Add Question
    </n-button>
  </n-modal>
</template>
