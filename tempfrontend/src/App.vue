<template>
  <div id="app">
    <div id = "charts">
    <div class="chart">
        <line-chart v-if="loaded" :chartdata="tempData" :options="tempOptions" :width="500"/>
    </div>
    <div class="chart">
        <line-chart v-if="loaded" :chartdata="humidityData" :options="humidityOptions" :width="500"/>
    </div>
    <div class="chart">
        <line-chart v-if="loaded" :chartdata="lightData" :options="lightOptions" :width="500"/>
    </div>
  </div>
  <div id ="cards">
<v-card class="mx-auto" max-width="344" outlined >
    <v-list-item three-line>
      <v-list-item-content>
        <div class="overline mb-4">Min Temp since {{this.testDate}} : {{this.minTemp}}</div>
        <v-list-item-title class="headline mb-1">Max Temp since {{this.testDate}} : {{this.maxTemp}}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </v-card>
  <button v-on:click="filterGraphs">Filter</button>
</div>
</div>
</template>

<script>
import LineChart from './components/Chart'
import axios from 'axios'
export default {
  name: 'App',
  components: { LineChart },
  data(){
    return{
      loaded: false,
      maxTemp: "",
      minTemp: "",
      testDate:"",
      masterData: Object,
      tempData: Object,
      humidityData: Object,
      lightData: Object,
      tempOptions: {title:{display: true,text: 'Temperature °C'},
            scales: {xAxes: [{type: 'time',distribution: 'linear'}],
            yAxes: [{ticks: {suggestedMin: 0,suggestedMax: 30},}]}},
      humidityOptions: {title:{display: true,text: 'Humidity Percentage'},
            scales: {xAxes: [{type: 'time',distribution: 'linear'}],
            yAxes: [{ticks: {suggestedMin: 0,suggestedMax: 30},}]}},
      lightOptions: {title:{display: true,text: 'Light Level'},
            scales: {xAxes: [{type: 'time',distribution: 'linear'}],
            yAxes: [{ticks: {suggestedMin: 0,suggestedMax: 30},}]}},
    }
  },
    methods:{
      filterGraphs(){
        var deviceNames = this.masterData.map(c=>c.device);
        var uniqueDeviceNames = Array.from(new Set(deviceNames));
        var timestampLabels = this.masterData.map(c=>c.timestamp);
        var processedDatasets = [];
        var processedChartData = {};

        uniqueDeviceNames.forEach(d=>{
          var singleObj = {};
          var dataset = this.masterData.filter(c=>c.device==d).map(c=>c.temp);
          
          var backgroundColour =  this.masterData.filter(c=>c.device==d).map(c=>c.colour)[0];
          singleObj['label'] = d.split(' ')
                                .map(w => w[0].toUpperCase() + w.substr(1).toLowerCase())
                                .join(' ');
          singleObj['data'] = dataset;
          singleObj['backgroundColor'] = backgroundColour;
          singleObj['borderColor'] = backgroundColour;
          singleObj['fill'] = false;
          processedDatasets.push(singleObj);
        });

        processedChartData['labels'] = timestampLabels
        processedChartData['datasets'] = processedDatasets
        processedChartData['labels'] = processedChartData['labels'].filter(c=> c < "2019-10-31") //<SECTION HERE USED FOR FILTERING
        // var currentTime = new Date();
        // var startDate = new Date();
        // startDate.setDate(currentTime.getDate() - 5);
        // console.log(startDate)
        // console.log(currentTime)
        this.loaded =false;
        console.log(this.tempData)
        this.tempData = processedChartData;
        this.loaded =true;
        console.log(this.tempData)
        
      },
      getMax(cObj){
        var currentTime = new Date();
        var startDate = new Date();
        startDate.setDate(currentTime.getDate() - 7);
        this.testDate = startDate.toLocaleDateString("en-GB");
        var lastWeek = cObj.filter(c=> c.timestamp > startDate.toLocaleDateString());

        var temps = lastWeek.map(c=>c.temp);
        this.maxTemp = Math.max(...temps) + '°C';
        this.minTemp = Math.min(...temps) + '°C';
      },
      processData(cObj,dtype){
        var deviceNames = cObj.map(c=>c.device);
        var uniqueDeviceNames = Array.from(new Set(deviceNames));
        var timestampLabels = cObj.map(c=>c.timestamp);
        var processedDatasets = [];
        var processedChartData = {};

        uniqueDeviceNames.forEach(d=>{
          var singleObj = {};
          var dataset;
          if (dtype == 0){
              dataset = cObj.filter(c=>c.device==d).map(c=>c.temp);
          } else if (dtype==1){
              dataset = cObj.filter(c=>c.device==d).map(c=>c.humidity);
          } else {
            dataset = cObj.filter(c=>c.device==d).map(c=>c.light);
          }
          
          var backgroundColour =  cObj.filter(c=>c.device==d).map(c=>c.colour)[0];
          //var timeset = cObj.filter(c=>c.device==d).map(c=>c.timestamp);
          singleObj['label'] = d.split(' ')
                                .map(w => w[0].toUpperCase() + w.substr(1).toLowerCase())
                                .join(' ');
          singleObj['data'] = dataset;
          singleObj['backgroundColor'] = backgroundColour;
          singleObj['borderColor'] = backgroundColour;
          singleObj['fill'] = false;
          //singleObj['t'] = timeset;
          processedDatasets.push(singleObj);
        });

        processedChartData['labels'] = timestampLabels
        processedChartData['datasets'] = processedDatasets

        //var testArray = processedChartData['labels'].filter(c=> c < "2019-10-31") <SECTION HERE USED FOR FILTERING
        // var currentTime = new Date();
        // var startDate = new Date();
        // startDate.setDate(currentTime.getDate() - 5);
        // console.log(startDate)
        // console.log(currentTime)

        return processedChartData
      },
  },
  async mounted () {
    this.loaded = false
    try {
      axios.get("http://localhost:3000/api/temperature")
          .then(res => {
            this.masterData = res.data;
            this.tempData = this.processData(res.data,0);
            this.humidityData = this.processData(res.data,1);
            this.lightData = this.processData(res.data,2);
            this.getMax(res.data);
            this.loaded = true}
            )
          .catch(err => console.log(err));
     
    } catch (e) {
      console.error(e)
    }
  }
}

</script>

<style>

  #charts{
    display:flex;
    justify-content:space-around;
  }

  #cards{
    display:flex;
    justify-content:space-around;
  }


</style>