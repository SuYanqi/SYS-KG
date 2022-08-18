<template>
<div>
  <h1>{{ msg }}</h1>
  <div class="search">
    <input type="text" v-model="input" @keyup.enter="handleInput" placeholder="Please input Bug ID..." autofocus />
    <button class="search-btn" @click="handleInput">Search
      <!-- <el-icon color="red">
        <Loading />
      </el-icon> -->
    </button>
  </div>

  <div class="result-container" v-if="searchResult">
    <div class="left">
      <h5>Bug Report</h5>
        <BugReportCard :bugReport=bugReport />
    </div>
    <!-- <Left :searchResult=searchResult /> -->
    <div class="main">
      <h5>Exploratory Testing</h5>
      <ExploratoryTestReportCard :exploratoryTestReports=exploratoryTestReports v-if="exploratoryTestReports"/>
      <p v-else><b>Note:</b> Please choose the Relevant Bug Report to get Test Scenarios</p>
    </div>
    <!-- <Right /> -->
    <div class="right">
      <h5>Relevant Bug Report</h5>
      <!-- <BugAccordion :relevantBugReports=relevantBugReports @returnBugId="getBugId($event)"/> -->
      <RelevantBugTable :relevantBugReports=relevantBugReports @returnBugId="getBugId($event)"/>
    </div>
    <!-- <ExpectedActualResultTable /> -->
  </div>
  <div v-else-if="afterSearch" > No Bug Report Found! </div>

  </div>
</template>

<script>
import axios from "axios";
// import Highlighter from 'vue-highlight-words';
// import {
//   // Search,
//   Loading
// } from '@element-plus/icons-vue'

import BugReportCard from "./BugReportCard.vue";
import ExploratoryTestReportCard from "./ExploratoryTestReportCard.vue";
// import BugAccordion from "./BugAccordion.vue";
import RelevantBugTable from "./RelevantBugTable.vue";
// import Right from "./Right.vue";
// import ExpectedActualTable from "./ExpectedActualTable.vue";

export default {
  name: "Search",
  components: {
    BugReportCard,
    ExploratoryTestReportCard,
    // BugAccordion,
    RelevantBugTable,
    // Loading,
    // Right,
    // ExpectedActualTable,
    // NoResearchResult,
    // StepTable,
    // Highlighter,
  },
  props: {
    msg: String,
  },
  data() {
    
    return {
      input: "",
      searchResult: "",
      bugReport: "",
      relevantBugReports: "",
      exploratoryTestReports: "",

      relevantBugId: "",
      // tableHtml: "",
      // stepHtml: "",
      // hasResult: false,
      afterSearch: false,
    }
  },
  // mounted() {
  //   this.hasResult=false;
  // },
  methods: {

    async handleInput(event) {
      // `this` inside methods points to the current active instance
      // `event` is the native DOM event
      if (event) {
        console.log(this.input);
        var input_val = {"input": this.input};
        await axios.post("http://47.242.133.237:5000/", input_val)
                        .then((res) => {this.searchResult = res.data})
        // await axios.post("http://localhost:5000/", input_val)
        //         .then((res) => {this.searchResult = res.data})
                        // console.log(this.searchResult);
        // console.log(this.searchResult);
        if (this.searchResult) {
          this.bugReport = this.searchResult["bugReport"];
          // console.log(this.bugReport)
          // document.getElementsByClassName("result-container")[0].style.display = "flex";
          // this.showBugTable();
          this.relevantBugReports = this.searchResult["relevantBugReports"]
          // console.log(this.relevantBugReports)
          // default No.1 relevantBugReport open
          this.exploratoryTestReports = this.searchResult["exploratoryTestResults"]
          // console.log(this.exploratoryTestReports)
        } 
        this.afterSearch=true;
      }
    },
    getBugId(bugId){
      this.relevantBugId=bugId
      console.log(bugId)
      this.getExploratoryTestResults()
    },

    async getExploratoryTestResults(){
      var input_val = {"bugId": this.input,
                       "relevantBugId": this.relevantBugId};
      await axios.post("http://47.242.133.237:5000/", input_val)
                      .then((res) => {this.exploratoryTestReports = res.data["exploratoryTestResults"]})
                        // console.log(this.searchResult);
      // if (this.exploratoryTestReports) {
      //   console.log(this.exploratoryTestReports)
      // } 

    },

    showBugTable(){
      var bug_link = "https://bugzilla.mozilla.org/show_bug.cgi?id=" + this.bugReport['id'];
      document.getElementsByClassName("bug-link")[0].href = bug_link
      // document.getElementsByClassName("bug-link")[0].innerHTML = this.bugReport['id']
      // document.getElementsByClassName("card-summary-text")[0].innerHTML = this.bugReport['Summary']
      // document.getElementsByClassName("card-preconditions-text")[0].innerHTML = this.bugReport['Preconditions']
      // document.getElementsByClassName("card-expected-text")[0].innerHTML = this.bugReport['Expected Results']
      // document.getElementsByClassName("card-actual-text")[0].innerHTML = this.bugReport['Actual Results']
      // document.getElementsByClassName("card-notes-text")[0].innerHTML = this.bugReport['Notes']
    },



  },

};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* @import '../../public/css/search.css'; */
/* @import './index.css'; */
h3 {
    margin: 5px 0 0;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
    margin: 0 10px;
  }
  a {
    color: #42b983;
  }
  .search {
    width: 100%;
    padding: 20px;
    background-color: rgb(255, 255, 255);
  }
  .result-container {
    display: flex;
    justify-content: center;
    border-radius: 0%;
    height: 100%;
    width: 100%;
    /* box-sizing: border-box; */
    text-align: center;
    padding: 1px;
    height: 100vh;
    background-color: rgb(255, 255, 255);
  }
  .left {
    /* background-color: rgb(243, 155, 155); */
    border-style: solid;
    border-width: 2px;
    border-color: rgba(182, 243, 207, 0.493);
    flex: 1;
    overflow: auto;
  }
  input {
    width: 570px;
    height: 40px;
    border: 3px solid #42b983;
  }
  .search-btn {
    height: 40px;
    border: 3px solid #42b983;
    background-color: #42b983;
    padding: 0 7px;
  }
  .main {
    /* // border-style: solid;
    // border-width: 2px;
    // border-color: #020202; */
    background-color: rgba(182, 243, 207, 0.493);
    flex: 1;
    overflow: auto;
  }
  .card {
    width: 100%;
    height: auto;
    /* // background-color: rgb(201, 208, 241); */
    margin: 10px 0;
    border-style: solid;
    border-width: 2px;
    border-color: #020202;

    /* // box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2); */
  }
  .right {
    /* // background-color: rgb(214, 241, 203); */
    border-style: solid;
    border-width: 2px;
    border-color: rgba(182, 243, 207, 0.493);
    flex: 1;
    overflow: auto;
  }
  .item {
    width: 100%;
    height: 100px;
    background-color: rgb(201, 208, 241);
    margin: 10px 0;
  }
  
  ::-webkit-scrollbar {
    width: 6px;
    height: 6px;
    background-color: #fff;
  }
  
  ::-webkit-scrollbar-thumb {
    border-radius: 10px;
    /* -webkit-box-shadow:inset 0 0 6px rgba(184, 156, 156, 0.3);*/
    /* // background-color: rgba(27, 107, 34, 0.5); */
    background-color: #42b983;
  }

</style>
