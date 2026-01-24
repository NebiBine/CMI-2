<script setup>
import { ref, onMounted } from "vue";
import '../assets/styles/mainStyle.css'
import axios from 'axios'
import { NModal, NButton } from "naive-ui";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faCircleQuestion } from '@fortawesome/free-regular-svg-icons'

const uporabniki = ref([]);
const profil = ref([]);
const showModal = ref(false);
const selectedUser = ref(null);
const admin_state = ref(false);
const searchText = ref("");


function closeModal() {
    showModal.value = false;
}

async function update() {
    const updatedProfile = {
        id: profil.value.id ?? selectedUser.value.id,
        first_name: profil.value.first_name,
        last_name: profil.value.last_name,
        birthdate: profil.value.birthdate,
        phone: profil.value.phone,
        address: profil.value.address,
        city: profil.value.city,
        country: profil.value.country,
        isAdmin: admin_state.value
    };
    try {
        const response = await axios.post("http://localhost:8000/profile/updateProfile",
            //postam celoten form (ref gleda in belezi vsako spremembo in tako posljem zadnjo verzijo profil.value)
            updatedProfile,
            { withCredentials: true });
        console.log("Successfuly updated user", response.data);
        showModal.value = false; //zaprem modal
        await getAllUsers(); //poklicem funkcijo da dobim nove osvežene podatke
    }
    catch (error) {
        console.log(error);
    }
}
/*
1.---------------------------------------------------------------------

GET ALL USERS TI POSLE ZDEJ TO:
[
   {
      "userId":"3cb33496-96dc-493d-8842-78ff8ff0b96c",
      "username":"bine",
      "hashPass":"scrypt:32768:8:1$D7x098jYSoywOz7I$efc7849879a54a02fc619e0fb2ee5226b8d0080bcaf725d7148806314aa164f7208692db79102672b9bd1e6be14f286896c83042c742d490f7669e6c2be59265",
      "email":"bine.tavcar@gmail.com"
   },
   {
      "userId":"89f644c0-336f-4cc5-92d7-02dc83df3f2a",
      "username":"nace",
      "hashPass":"scrypt:32768:8:1$nnuzbDrZGZi6Guaq$268306560e7d925e15bead2710f00b13358607264555c458cf350b2e4f0c571c27ba982e3a772a9ae39e4d7497aadb72e072438e3aa9134059d644874d6460da",
      "email":"nacerozman3@gmail.com"
   }...
]
BREZ ADMINA,!!!!


2.--------------------------------------------------
ADMIN BO ZDEJ V TVOJI FUNKCIJI userIdSend V /DATA/GETPROFILE IN SICER: pocakat rabm tebe za test dase lahko prkaze da vids kasn json drgac vrjetn bo tko

{
   "userId":"3cb33496-96dc-493d-8842-78ff8ff0b96c",
   "username":"bine",
   "hashPass":"scrypt:32768:8:1$D7x098jYSoywOz7I$efc7849879a54a02fc619e0fb2ee5226b8d0080bcaf725d7148806314aa164f7208692db79102672b9bd1e6be14f286896c83042c742d490f7669e6c2be59265",
   "email":"bine.tavcar@gmail.com",
   "isAdmin":true/false --> za checkbox k bos odpru view more
}

3.--------------------------------------------------
ideja: 
    pr actions lahko dava se delete user, da ga zbriseva, ni velka zadeva sam da vec funkcionalnosti

4.---------------------------------------------------
K BOS UPDEJTU USER NA /data/updateUser PRCAKUJE TA DATA, LAHKO DAVA KEJ STRAN TO NI PROBLEM, DODT PA TESKO, PLUS ADMIN
updateUser prcakuje:
    data = {
    "userId":123,
    "Fullname":fullName,
    "username":username,
    "birth":birth,
    "phone":phone,
    "street":street,
    "city":city,
    "country":country,
    "zip":zip,
    "isAdmin":isAdmin --> true/false, ali je checked al ni tojto
    }

VRNE TI PA ISTI JSON KSI MI GA POSLOU, IDENTITIČEN, POD POGOJEM DA NI BLO ERRORJA, SEPRAV PO ŽE NARJENE UPDEJTU V DB

*/
async function getAllUsers() {
    try {
        const response = await axios.get(
            'http://localhost:8000/auth/getAllUsers', {
            withCredentials: true
        })
        //console.log(response.data)
        uporabniki.value = response.data
        //debug print
        console.log("ALL USERS: ", uporabniki.value)
    }
    catch (error) {
        console.log(error)
    }
}
//posljem userId ko admin klikne na more info da iz backenda prejmem podatke za dolocen userId (profil data: tel stevilko, fullname itd.)
async function userIdSend() {
    try {
        const response = await axios.post("http://localhost:8000/profile/getProfile", //||BACK POSLE ISTO ZADEVO K U DASHBOARD VIEW + ISADMIN, SAM PRKAZ PODATKE, poglej gor||    
            { userId: selectedUser.value.id },
            { withCredentials: true });
        profil.value = response.data.profile;
        admin_state.value = response.data.admin; //dobim vse admine da lahko potem primerjam ce je user admin al ne
        console.log("PROFILE DATA FOR SELECTED USER:", profil.value);
        console.log("ADMINS DATA:", admin_state.value);
    }
    catch (error) {
        console.log(error)
    }
}
const openUserModal = (uporabnik) => {
    selectedUser.value = uporabnik;
    console.log("CLICKED USER (USER ID)", selectedUser.value.id)
    //razlaga za spodnjo vrstico
    //selectedUser.value.isAdmin = admins.value.some(admin => admin.userId === uporabnik.userId)
    //klicem funkcijo ki bo dala profildata IN POSLALA USERID
    userIdSend();
    showModal.value = true;
};
onMounted(() => {
    getAllUsers();
});
</script>
<template>
    <h1>User Management</h1>
    <!--SEARCH BAR-->
    <label for="searhEngine">Search users:</label>
    <!--TOOLTIP ZA POMOC UPORABNIKOM UPORABI TA TEMPLATE VECKRAT-->
    <n-tooltip trigger="hover">
        <template #trigger>
            <FontAwesomeIcon :icon="faCircleQuestion" />
        </template>
        Search users by their username. Enter the username in the input field down below.
    </n-tooltip>
    <!--------------------------------------------------------------------------------------->
    <div class="searchBarAdminUsers">
        <n-input type="text" id="searhEngine" placeholder="Currently disabled! :(" clearable disabled=false v-model:value="searchText"></n-input>
    </div>
    
    <!--LISTAM USE USERJE-->
    <div class="users_list">
        <n-table :bordered="true" :single-line="false">
            <thead class="table_header_admin">
                <tr>
                    <th>Username</th>
                    <th>Email</th>
                    <th>UserId</th>
                    <th>Update or View User</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="uporabnik in uporabniki" :key="uporabnik.id">
                    <td>{{ uporabnik.username }}</td>
                    <td>{{ uporabnik.email }}</td>
                    <td>{{ uporabnik.id }}</td>
                    <td>
                        <n-button text @click="openUserModal(uporabnik)" class="moreinfoBTN">More
                            Info</n-button>

                    </td>
                </tr>
            </tbody>
        </n-table>
    </div>
    <n-modal v-model:show="showModal" preset="dialog" title="Edit or View User">
        <template #default>
            <label for id="firstName"> First Name:
                <n-input id="fullName" placeholder="" v-model:value="profil.first_name"></n-input>
            </label>
            <label for id="LastName"> Last Name:
                <n-input id="username" placeholder="" v-model:value="profil.last_name"></n-input>
            </label>
            <label for id="birth"> Date of Birth:
                <n-input id="birth" placeholder="" v-model:value="profil.birthdate"></n-input>
            </label>
            <label for id="phone"> Mobile Number:
                <n-input id="phone" placeholder="" v-model:value="profil.phone"></n-input>
            </label>
            <label for id="street"> Address:
                <n-input id="street" placeholder="" v-model:value="profil.address"></n-input>
            </label>
            <label for id="city"> City:
                <n-input id="city" placeholder="" v-model:value="profil.city"></n-input>
            </label>
            <label for id="country"> Country:
                <n-input id="country" placeholder="" v-model:value="profil.country"></n-input>
            </label>
            <!-- NAREDI DA LAHKO SAMO ADMIN LEVEL 2 SPREMINJA ADMIN LEVEL - KO BODO DOKONCANI LEVELI -->
            <!-- <label for id="adminLevel"> Admin Level:
                <n-input id="adminLevel" placeholder="" v-model:value="profil.adminLevel"></n-input>
            </label> -->
            <label for id="admin_state"> Add/Remove Admin?
                <n-checkbox id="admin_state" v-model:checked="admin_state"></n-checkbox>
            </label>


            <n-button @click="update">Update</n-button>
            <n-button @click="closeModal()">Close</n-button>
        </template>
    </n-modal>

</template>