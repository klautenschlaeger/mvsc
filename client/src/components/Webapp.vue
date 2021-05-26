<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Multi-Vehicle-ASC-Controller</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <b-button id="show-btn" @click="$bvModal.show('bv-modal')">Open all Machines</b-button>


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
import { LMap, LTileLayer, LPolygon, LControlAttribution, } from 'vue2-leaflet';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      zoom: 15,
      center: [51.7283462477326, 12.116302453006],
      polygon1: {
        latlngs: [],
        color: 'yellow',
        group: 1,
      },
      polygon2: {
        latlngs: [],
        color: 'red',
        group: 2,
      },
      polygon3: {
        latlngs: [],
        color: 'blue',
        group: 3,
      },
      polling_polys: null,
      polling_machines: null,
      machines: [],
      counter: [0, 0, 0],
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
      const path = 'http://localhost:5001/mv/poly';
      const payload = {
        counters: this.counter,
      };
      axios.post(path, payload)
        .then((res) => {
          this.polygon1.latlngs = this.polygon1.latlngs.concat(res.data.polys1);
          this.polygon2.latlngs = this.polygon2.latlngs.concat(res.data.polys2);
          this.polygon3.latlngs = this.polygon3.latlngs.concat(res.data.polys3);
          this.counter = res.data.counters;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    poll_data() {
      this.polling_polys = setInterval(() => { this.pollpolys(); }, 15000);
      this.polling_machines = setInterval(() => { this.getMachines(); }, 30000);
    },
    getMachines() {
      const path = 'http://localhost:5001/mv';
      axios.get(path)
        .then((res) => {
          this.machines = res.data.machines;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      if (this.machines.length !== 10) {
        clearInterval(this.polling_machines);
      }
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
    this.getMachines();
    this.poll_data();
  },
  beforeDestroy() {
    clearInterval(this.polling_polys);
    if (this.polling_machines !== null) {
      clearInterval(this.polling_machines);
    }
  },

};
</script>
