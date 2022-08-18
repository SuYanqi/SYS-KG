<template>

  <div class="card" style="border: 2px black solid;" v-for="(exploratoryTestReport ,index) in exploratoryTestReports" :key="index" >
    <div class="card-body">
       <!-- <h6 class="card-title">Bug ID </h6>
      <a class="bug-link" href="">{{bugReport.id}}</a>
      <h6 class="card-title">Summary</h6>
      <p class="card-summary-text">{{bugReport.Summary}}</p> -->
      
      <h6 class="card-header text-center">
        Test Scenario {{index+1}}
      </h6>
      <h6 class="card-title">Preconditions</h6>
      <p class="card-pre-text" v-if="!exploratoryTestReport.Preconditions">{{exploratoryTestReport.Preconditions}}</p>
      <p class="card-pre-text" v-else> 
        <Highlighter class="my-highlight" 
            highlightClassName="highlight"
            :searchWords="exploratoryTestReport.PreconditionsElements"
            :autoEscape="true"
            :textToHighlight="exploratoryTestReport.Preconditions" 
            :highlightStyle="{ background: 'rgba(236, 250, 222, 0.493)' }"
          />
      </p>
      <h6 class="card-title">Steps to Reproduce</h6>
      
      <!-- <StepAccordion :steps=exploratoryTestReport.StepsToReproduce />  -->
        <StepTable :steps=exploratoryTestReport.StepsToReproduce /> 

        
      <h6 class="card-title expected-result">Expected Results</h6>
      <p class="card-pre-text" v-if="!exploratoryTestReport.ExpectedResults" >{{exploratoryTestReport["ExpectedResults"]}}</p>
      <p class="card-pre-text" v-else>
        <Highlighter class="my-highlight" 
                    highlightClassName="highlight"
                    :searchWords="exploratoryTestReport.ExpectedResultsElements"
                    :autoEscape="true"
                    :textToHighlight="exploratoryTestReport.ExpectedResults" 
                    :highlightStyle="{ background: 'rgba(236, 250, 222, 0.493)' }"
                 />
      </p>
      <h6 class="card-title">Actual Results</h6>
      <p class="card-pre-text" v-if="!exploratoryTestReport.ActualResults" >{{exploratoryTestReport["ActualResults"]}}</p>
      <p class="card-pre-text" v-else>
        <Highlighter class="my-highlight" 
                    highlightClassName="highlight"
                    :searchWords="exploratoryTestReport.ActualResultsElements"
                    :autoEscape="true"
                    :textToHighlight="exploratoryTestReport.ActualResults" 
                    :highlightStyle="{ background: 'rgba(236, 250, 222, 0.493)' }"
                 />
      </p>
      <h6 class="card-title">Notes</h6>
      <p class="card-pre-text" v-if="!exploratoryTestReport.Notes" >{{exploratoryTestReport.Notes}}</p> 
      <p class="card-pre-text" v-else>
        <Highlighter class="my-highlight" 
                    highlightClassName="highlight"
                    :searchWords="exploratoryTestReport.NotesElements"
                    :autoEscape="true"
                    :textToHighlight="exploratoryTestReport.Notes" 
                    :highlightStyle="{ background: 'rgba(236, 250, 222, 0.493)' }"
                 />
      </p>
      <!-- <h6 class="card-title">See Also</h6>
      <p class="card-notes-text"></p>  -->
      <!-- <h6 class="card-title">Attachments</h6>
      <p class="card-attach-text">None</p> -->
    </div>
  </div>
</template>

<script>
import Highlighter from 'vue-highlight-words';

// import StepAccordion from "./StepAccordion.vue";
import StepTable from "./StepTable.vue";


export default {
  name: "ExploratoryTestReportCard",
  props: ["exploratoryTestReports"],
  components: {
    // StepAccordion,
    StepTable,
    Highlighter,
  },

  // data() {
  //   return {
  //     steps: this.bugReport["Steps to Reproduce"],
  //     }
  // },
  methods: {

  },
    
}
</script>

<style lang="scss">
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
  .card-header.text-center{
    margin-bottom: 10px;

  }
  .card-body:hover{
    // box-shadow: 8px 8px 8px 8px rgba(151, 237, 243,0.5);
    box-shadow: 12px 12px 12px 12px rgba(0, 0, 0, 0.20),0px 8px 20px rgba(0, 0, 0, 0.20);
    // box-shadow-light: 0px 0px 12px rgba(0, 0, 0, 0.12);
    // box-shadow-lighter: 0px 0px 6px rgba(0, 0, 0, 0.12);
    // box-shadow-dark: 0px 16px 48px 16px rgba(0, 0, 0, 0.08),0px 12px 32px rgba(0, 0, 0, 0.12),0px 8px 16px -8px rgba(0, 0, 0, 0.16);
  }
  .expected-result{
    margin-top: 10px;
  }

</style>