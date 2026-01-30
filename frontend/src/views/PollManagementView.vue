<script setup>
import { ref, onMounted } from "vue";
import '../assets/styles/mainStyle.css';
import axios from 'axios';
import { message } from "ant-design-vue";


const archivedPolls = ref([]);
const archivedPollData = ref([]);
const PollResults = ref([]);

//array z vsemi aktivnimi polli 
const polls = ref([]);

const username = ref("");

//MODAL STANJA
const modal_state1 = ref(false);
const modal_state2 = ref(false);
const modalStatisticsState = ref(false);
//--------------------------------------------------------

//MODAL 1 VREDNOSTI
const possible_points_value = ref(0);
const pollTitle = ref("");
const pollDuration = ref(0);
const pollDescription = ref("");

//VPRAŠANJA ARRAY
const questions = ref([]);

const Poll = ref([]);
//FUNKCIJE ZA MODAL STATE (ODPIRANJE ZAPIRANJE MODALOV)
function open_modal1() {
  modal_state1.value = true;
};
function open_modal2() {
  modal_state2.value = true;
};

function closeModal() {
  modal_state2.value = false;
};

function closeModal1() {
  modal_state1.value = false;
};

function openModalstatistics(archivedPoll){
  modalStatisticsState.value = true;
  archivedPollData.value = archivedPoll;
  PollStatistics();
};

function closeModalstatistics(){
  modalStatisticsState.value = false;
};

//--------------------------------------------------------

//IZBIRE ZA TIP VPRASANJA
const polltypeOptions = [
  { label: "Yes/No question", value: "yesno" },
  { label: "Input type question", value: "input" },
  { label: "Pick one question (radio buttons)", value: "radioButtons" },
  { label: "Pick multiple questions (checkbox)", value: "checkbox" },
];


//FUNKCIJA ZA DODAJANJE VPRASANJA V QUESTIONS ARRAY KI SE KASNEJE NAPOLNI
const addQuestion = () => {
  questions.value.push({ text: "", type: "", options: ["", "", "", ""] });
};

//FUNKCIJA Z  ODSTRANJEVANJE VPRASANJA ... UPORABLJENA FUNKCIJA SPLICE NA DOLOCENEM INDEXU IN ODSTRANI 1 ELEMENT
const removeQuestion = (index) => {
  questions.value.splice(index, 1);
};

//TESTING FUNKCIJA
// const addOption = (question) => {
//   question.options.push("");
// };


//FUNCKCIJA ZA SPREMEMBO TIPA VPRASANJA IN SPREMINJANJE OPCIJ.. DELUJE NA PRINCIP ON CHANGE V DROPDOWNU
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


//FUNKCIJA ZA SUBMIT POLLA IN AXIOS POST
async function pollSubmit() {
  const pollData = {
    pollTitle: pollTitle.value,
    pollDuration: pollDuration.value,
    pollDescription : pollDescription.value,
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
  pollDescription.value = "";
  pollDuration.value = 0;
  possible_points_value.value = 0;
  questions.value = [];

  //klic funkcije da osvezim seznam vseh pollov
  getPolls();
}




// PRIDOBIVANJE USERNAMA ZA ADMIN GREETING
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

//FUNKCIJA ZA PRIDOBIVANJE VSEH AKTIVNIH POLLOV
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
//FUNKCIJA ZA PRIDOBIVANJE ARHIVIRANIH POLLOV IN SAMIH ODGOVOROV
async function getArchivedPolls(){
  try{
    const response = await axios.get('http://localhost:8000/poll-reward/getArchivedPolls',
    { withCredentials: true });
    archivedPolls.value = response.data;
    console.log("Fetched poll statistics:", archivedPolls.value);
  }
  catch(error){
    console.log(error)
  }
}
async function PollStatistics(){
  try{
    const response = await axios.post('http://localhost:8000/poll-reward/getResults',
    {id:  archivedPollData.value.id},
    { withCredentials: true });
    PollResults.value = response.data;
  }
  catch(error){
    console.log(error)
  }
}


//ONLOAD
onMounted(() => {
  profilData(),
  getPolls(),
  getArchivedPolls()
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
  <div class = "activePolls">
    <h3>Currently active polls</h3>
    <div class = "polls-container">
      <div v-for="poll in polls" :key = "poll.id" class = "EnPoll">
          <h2 style = "font-size: 20px;">Poll title: {{ poll.pollTitle }}</h2>
          <p>Description: {{ poll.pollDescription }}</p>
          <p>Points: {{ poll.points }}</p>
          <p>Expires at: {{ new Date(poll.expirationDate).toLocaleDateString('si-SI') }}</p>
          <p>Creator ID: {{ poll.creatorId }}</p>
      </div>
    </div>
  </div>

  <br></br>
   <!--PRIKAZAN ARHIV VSEH POLLOV IN NJIHOVE STATISTIKE ODGOVOROV-->
  <h3>Past Due Polls Statistics</h3>
  <div class = "polls-container">
    <div v-for="archivedPoll in archivedPolls" :key="archivedPoll.id" class = "enPoll">
      <!--PRIKAZANI VSI ARHIVIRANI POLLI -->
      <!--GUMB ZA ODPIRANJE MODALA Z REZULTATI-->
      <n-button @click="openModalstatistics(archivedPoll)">See results (se ne deluje)</n-button>
    </div>
  </div>
  <!--MODAL ZA STATISTIKO VSAKEGA POLLA -- PRIKAZANI BODO ODGOVORI!!! -->
  <n-modal
    v-model:show="modalStatisticsState"
    preset="dialog"
    title="Poll Statistics Overview"
    content="Are you sure?"
    positive-text="Submit"
    negative-text="Cancel"
    @negative-click="closeModalstatistics">
    <div v-for="question in PollResults" :key="question.id">
      <!--PRIKAZANO VSAKO VPRASANJE IN VSI ODGOVORI KATERI OBSTAJAJO ZA TOCNO TA POLL IN TO VPRASANJE-->
      <!--WORK IN PROGRESS TO SE NE BO DELOVALO-->
      <h3>{{ question.text }}</h3>
      <div v-if="question.type == 'yesno'">
        <p>Yes: {{ question.results.yes }}</p>
        <p>No: {{ question.results.no }}</p>
      </div>
      <div v-if="question.type == 'input'">
        <p>Yes: {{ question.results.yes }}</p>
        <p>No: {{ question.results.no }}</p>
      </div>
      <div v-if="question.type == 'checkbox'">
        <div v-if="question.option">
          <div v-for="(option, index) in question.options" :key="index">
            <p>{{ option }}: {{ question.results[option]}}</p>
          </div>
        </div>
      </div>
      <div v-if="question.type == 'radioButtons'">
        <p>Yes: {{ question.results.yes }}</p>
        <p>No: {{ question.results.no }}</p>
      </div>
    </div>
  </n-modal>



  <!------------------- MODAL ZA DODAJANJE ANKETE ------------------->
  <n-modal v-model:show="modal_state1" preset="dialog" title="Add Poll" positive-text="Submit" negative-text="Cancel"
    @positive-click="pollSubmit" @negative-click="closeModal1" :style="{ width: '600px', height: 'auto' }">
    <template #icon>
      <img src="../assets/icons/add_poll.svg" alt="Add Poll Icon"/>
    </template>
    <!-- poll title -->
     <div class = "pollName">
      <label for="poll_name">Poll Name:
        <n-input type="text" id="poll_name" v-model:value="pollTitle"
          placeholder="Enter Poll Title (eg. New city project)"></n-input>
      </label>
    </div>
    <!-- poll description -->
     <div class="pollDescription">
      <label for="poll_description">Poll Description:
        <n-input type="text" id="poll_description" v-model:value="pollDescription"
          placeholder="Enter Poll Description"></n-input>
      </label>
    </div>
    <!-- poll duration -->
     <div class = "pollDuration">
      <label for="poll_duration">Poll Duration:
        <n-slider v-model:value="pollDuration" :step="1" :max="7"  style = "width: 85%;" />
      </label>
    </div>
    <!-- <label for id="expires"> Expires at:
      <n-date-picker v-model:value="timestamp" type="date" />
    </label> -->

    <!-- possible points -->
     <div class="possiblePoints">
      <label for="possible_points">Possible points
        <n-input-number id="possible_points" v-model:value="possible_points_value" clearable />
      </label>
    </div>
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
                  <li v-for="options1 in question1.options" :key="optIndex">
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
    <template #icon>
      <img src="../assets/icons/add_poll.svg" alt="Add Poll Icon"/>
    </template>
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
        <div v-for="(option, optionIndex) in question.options" :key="optionIndex" style="margin-bottom: 6px;">
          <n-input v-model:value="question.options[optionIndex]" :placeholder="`Option ${optionIndex + 1}`"
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
