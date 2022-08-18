<template>
  <div class="card" style="border: 2px black solid;"> 
    <div class="card-body">
     <table style="width:100%;">
        <tr>
          <th>
            <h6 class="card-title">Bug ID</h6>
          </th>
          <th>
            <h6 class="card-title">Product::Component</h6>
          </th>
        </tr>
        <tr>
          <td>
            <a class="bug-link" target="_blank" v-bind:href="bug_url">{{bugReport.id}}</a>
          </td>
          <td >
            <div class="card-bug-pc">{{bugReport.product}}::{{bugReport.component}}</div>
          </td>
        </tr>
      </table>
      <h6 class="card-title">Summary</h6>
      <p class="card-summary-text">{{bugReport.Summary}}</p>
      <h6 class="card-title">Preconditions</h6>
      <p class="card-pre-text" v-if="!bugReport.Preconditions">{{bugReport.Preconditions}}</p>
      <p class="card-pre-text" v-else>
        <Highlighter class="my-highlight" 
            highlightClassName="highlight"
            :searchWords="bugReport.PreconditionsElements"
            :autoEscape="true"
            :textToHighlight="bugReport.Preconditions" 
            :highlightStyle="{ background: 'rgba(236, 250, 222, 0.493)' }"
          />
      </p>
      <h6 class="card-title">Steps to Reproduce</h6>
      
      <!-- <StepAccordion :steps=bugReport.StepsToReproduce /> -->
      <StepTable :steps=bugReport.StepsToReproduce />
        
      <h6 class="card-title expected-result">Expected Results</h6>
      <p id="expected-result" v-if="!bugReport.ExpectedResults">{{bugReport.ExpectedResults}}</p>
      <p v-else>
        <Highlighter class="my-highlight" 
                    highlightClassName="highlight"
                    :searchWords="bugReport.ExpectedResultsElements"
                    :autoEscape="true"
                    :textToHighlight="bugReport.ExpectedResults" 
                    :highlightStyle="{ background: 'rgba(236, 250, 222, 0.493)' }"
                 />
      </p>
      <h6 class="card-title">Actual Results</h6>
      <!-- <p class="card-actual-text">{{bugReport.ActualResults}}</p> -->
      <p class="card-pre-text" v-if="!bugReport.ActualResults">{{bugReport.ActualResults}}</p>
      <p class="card-pre-text" v-else><Highlighter class="my-highlight" 
                    highlightClassName="highlight"
                    :searchWords="bugReport.ActualResultsElements"
                    :autoEscape="true"
                    :textToHighlight="bugReport.ActualResults" 
                    :highlightStyle="{ background: 'rgba(236, 250, 222, 0.493)' }"
                 />
      </p>
      <h6 class="card-title">Notes</h6>
      <p class="card-pre-text" v-if="!bugReport.Notes" >{{bugReport.Notes}}</p>
      <p class="card-pre-text" v-else><Highlighter class="my-highlight" 
                    highlightClassName="highlight"
                    :searchWords="bugReport.NotesElements"
                    :autoEscape="true"
                    :textToHighlight="bugReport.Notes" 
                    :highlightStyle="{ background: 'rgba(236, 250, 222, 0.493)' }"
                 />
      </p>
      <h6 class="card-title">Attachments</h6>
      <p class="card-attach-text">
        <ul id="attachments">
          <li v-for="(attachment, index) in bugReport.Attachments" :key="index" class="lightboxContainer">
            <img v-bind:src="attachment.attachment_url" width="550" v-if="attachment.type == 'image'" class="lightbox" />
            <a v-else-if="attachment.content_type == 'video/quicktime'" class="attachment-link" v-bind:href="attachment.attachment_url">{{attachment.file_name}}</a>
            <video width="550" controls v-else-if="attachment.type == 'video'">
              <source v-bind:src="attachment.attachment_url" v-bind:type="attachment.content_type" >
            </video>
          </li>
        </ul>
      </p>
    </div>
  </div>
</template>

<script>

// import StepAccordion from "./StepAccordion.vue";
import StepTable from './StepTable.vue';
import Highlighter from 'vue-highlight-words';


export default {
  name: "BugReportCard",
  props:["bugReport"],
  components: {
    // StepAccordion,
    StepTable,
    Highlighter,
  },
  data() {
    return {
      bug_url: "",
      }
  },

  // data: function () {
  //   return {
  //     count: 0
  //   }
  // },
  methods: {
    
  },
  watch: { 
    bugReport: {
      handler(){
        // console.log("watch", newVal, oldVal)
        this.bug_url  = "https://bugzilla.mozilla.org/show_bug.cgi?id=" + this.bugReport['id'];
        // this.highlight('the')
        // document.getElementsByClassName("bug-link")[0].href = bug_link
        // this.count = this.count + 1
      },
      immediate: true
    }
  },
}
</script>
<style lang="scss">
  .card {
    width: 100%;
    height: auto;
    // background-color: rgb(38, 56, 136); 
    margin: 10px 0;
    border: 2px #802121 solid;
    /* // box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2); */
  }
  #attachments video,
  #attachments img{
    width: 100%;
    height: 100%;
  } 
  .card-pre-text{
    white-space: pre-line;
    // margin: 0;
    text-align: left;
    font: inherit;
    font-size: 0.900rem;
  }
  // .lightbox{
  //   cursor: zoom-in;
  // }
 
  // .lightboxContainer:hover .lightbox{
  //   position: relative;
  //   z-index: 1;
  //   top: -500px;
  //   left: 500px;
  //   width:1500px;
  //   height: auto;
  // }
  // .lightboxContainer:hover .card{
  //   overflow: visible;
  // }
</style>