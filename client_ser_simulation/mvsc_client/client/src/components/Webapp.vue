<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Multi-Vehicle-ASC-Machine-2</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <b-button v-if="disable" v-b-modal.machine-modal>Add Machine</b-button>
        <b-button v-if="!disable" id="show-btn" @click="$bvModal.show('bv-modal')">Open all Machines</b-button>


        <br><br>
      </div>
    </div>
    <div class="map" id="map" ref="mapElement">
      <l-map style="height: 350px" :zoom="zoom" :center="center">
        <l-tile-layer :url="url"></l-tile-layer>
        <l-control-attribution position="bottomright" prefix='Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>"'></l-control-attribution>
        <l-polygon :lat-lngs="polygon1.latlngs" :color="polygon1.color"></l-polygon>
        <l-polygon :lat-lngs="polygon2.latlngs" :color="polygon2.color"></l-polygon>
        <l-polygon :lat-lngs="polygon3.latlngs" :color="polygon3.color"></l-polygon>
        <l-polygon :lat-lngs="polygon_own.latlngs" :color="polygon_own.color"></l-polygon>
      </l-map>
    </div>
    <b-modal @show="getMachines" id="bv-modal" size="xl" hide-footer>
      <template #modal-title>
        All Machines
      </template>
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
          </tr>
        </tbody>
      </table>
      <b-button class="mt-3" block @click="$bvModal.hide('bv-modal')">Close Me</b-button>
    </b-modal>
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
<style>
.map {
  height: 100%;
  width: 100%;
}
</style>
<script>
import axios from 'axios';
import { LMap, LTileLayer, LPolygon, LControlAttribution } from 'vue2-leaflet';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      disable: true,
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      zoom: 15,
      center: [51.7283462477326, 12.116302453006],
      polygon1: {
        latlngs: [],
        color: 'blue',
        group: 1,
      },
      polygon2: {
        latlngs: [],
        color: 'blue',
        group: 2,
      },
      polygon3: {
        latlngs: [],
        color: 'blue',
        group: 3,
      },
      polygon_own: {
        latlngs: [],
        color: 'black',
        group: 0,
      },
      polling_polys: null,
      machines: [],
      addMachineForm: {
        drivername: '',
        forename: '',
        machineid: '',
        one: [],
        two: [],
        three: [],
      },
      counter: [0, 0, 0, 0],
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
    LMap,
    LTileLayer,
    LPolygon,
    LControlAttribution,
  },
  methods: {
    pollpolys() {
      const path = 'http://localhost:5005/mv/poly';
      const payload = {
        counters: this.counter,
      };
      axios.post(path, payload)
        .then((res) => {
          this.polygon1.latlngs = this.polygon1.latlngs.concat(res.data.polys1);
          this.polygon2.latlngs = this.polygon2.latlngs.concat(res.data.polys2);
          this.polygon3.latlngs = this.polygon3.latlngs.concat(res.data.polys3);
          this.polygon_own.latlngs = this.polygon_own.latlngs.concat(res.data.polys_own);
          this.counter = res.data.counters;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    poll_data() {
      this.polling_polys = setInterval(() => { this.pollpolys(); }, 15005);
    },
    getMachines() {
      const path = 'http://localhost:5005/mv';
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
      const path = 'http://localhost:5005/mv';
      axios.post(path, payload)
        .then(() => {
          this.getMachines();
          this.message = 'Machine added!';
          this.showMessage = true;
          this.disable = false;
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
        machineid: this.addMachineForm.machineid,
        one, // property shorthand
        two,
        three,
      };
      this.addMachine(payload);
      this.initForm();
    },
  },
  created() {
    this.poll_data();
    this.polling_polys = setInterval(() => { this.pollpolys(); }, 15005);
  },
  beforeDestroy() {
    clearInterval(this.polling_polys);
  },
};
</script>
