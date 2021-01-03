<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Multi-Vehicle-ASC-Controller</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.machine-modal>Add Machine</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Vorname</th>
              <th scope="col">Maschine</th>
              <th scope="col">Gruppe 1 Spritzen</th>
              <th scope="col">Gruppe 2 Sähen</th>
              <th scope="col">Gruppe 3 Düngen</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(machine, index) in machines" :key="index">
              <td>{{ machine.drivername }}</td>
              <td>{{ machine.forename }}</td>
              <td>{{ machine.machineid }}</td>
              <td>
                <span v-if="machine.one">X</span>
                <span v-else></span>
              </td>
              <td>
                <span v-if="machine.two">X</span>
                <span v-else></span>
              </td>
              <td>
                <span v-if="machine.three">X</span>
                <span v-else></span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.machine-update-modal
                          @click="editBook(book)">
                      Update
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addMachineModal"
            id="machine-modal"
            title="Add a new machine"
            hide-footer>
      <b-form @submit="onSubmit" class="w-100">
      <b-form-group id="form-drivername-group"
                    label="Name:"
                    label-for="form-drivername-input">
          <b-form-input id="form-drivername-input"
                        type="text"
                        v-model="addMachineForm.drivername"
                        required
                        placeholder="Enter Name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-forename-group"
                      label="Vorname:"
                      label-for="form-forename-input">
            <b-form-input id="form-forename-input"
                          type="text"
                          v-model="addMachineForm.forename"
                          required
                          placeholder="Enter Vorname">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-machineid-group"
                      label="Maschine:"
                      label-for="form-machineid-input">
            <b-form-input id="form-machineid-input"
                          type="text"
                          v-model="addMachineForm.machineid"
                          required
                          placeholder="Enter Maschine">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-group">
          <b-form-checkbox-group v-model="addMachineForm.one" id="form-checks-one">
            <b-form-checkbox value="true">Gruppe1</b-form-checkbox>
          </b-form-checkbox-group>
          <b-form-checkbox-group v-model="addMachineForm.two" id="form-checks-two">
            <b-form-checkbox value="true">Gruppe 2</b-form-checkbox>
          </b-form-checkbox-group>
          <b-form-checkbox-group v-model="addMachineForm.three" id="form-checks-three">
            <b-form-checkbox value="true">Gruppe 3</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      polling: null,
      machines: [],
      addMachineForm: {
        drivername: '',
        forename: '',
        one: [],
        two: [],
        three: [],
      },
      message: '',
      showMessage: false,
      editForm: {
        id: '',
        drivername: '',
        forename: '',
        read: [],
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    pollData() {
      // this.polling = setInterval(function(){ alert("Hello world"); }, 3000);
    },
    getMachines() {
      const path = 'http://localhost:5000/mv';
      axios.get(path)
        .then((res) => {
          this.machines = res.data.machines;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addMachine(payload) {
      const path = 'http://localhost:5000/mv';
      axios.post(path, payload)
        .then(() => {
          this.getMachines();
          this.message = 'Machine added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getMachines();
        });
    },
    initForm() {
      this.addMachineForm.drivername = '';
      this.addMachineForm.forename = '';
      this.addMachineForm.machineid = '';
      this.addMachineForm.one = [];
      this.addMachineForm.two = [];
      this.addMachineForm.three = [];
      this.editForm.id = '';
      this.editForm.drivername = '';
      this.editForm.forename = '';
      this.editForm.read = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addMachineModal.hide();
      let one = false;
      if (this.addMachineForm.one[0]) one = true;
      let two = false;
      if (this.addMachineForm.two[0]) two = true;
      let three = false;
      if (this.addMachineForm.three[0]) three = true;
      const payload = {
        drivername: this.addMachineForm.drivername,
        forename: this.addMachineForm.forename,
        one, // property shorthand
        two,
        three,
      };
      this.addMachine(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addMachineModal.hide();
      this.initForm();
    },
    editBook(book) {
      this.editForm = book;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editMachineModal.hide();
      let read = false;
      if (this.editForm.read[0]) read = true;
      const payload = {
        drivername: this.editForm.drivername,
        forename: this.editForm.forename,
        read,
      };
      this.updateBook(payload, this.editForm.id);
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios.put(path, payload)
        .then(() => {
          this.getMachines();
          this.message = 'Book updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getMachines();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editMachineModal.hide();
      this.initForm();
      this.getMachines(); // why?
    },
  },
  created() {
    this.getMachines();
    // this.pollData();
  },
  beforeDestroy() {
    // clearInterval(this.polling);
  },

};
</script>
