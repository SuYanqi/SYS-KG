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
          <td >
            <a class="bug-link" v-bind:href="bug_url">{{bugReport.id}}</a>
          </td>
          <td >
            <div class="card-bug-pc">{{bugReport.product}}::{{bugReport.component}}</div>
          </td>
        </tr>
      </table>
      <h6 class="card-title">Summary</h6>
      <p class="card-summary-text">{{bugReport.Summary}}</p>
      <h6 class="card-title">Description</h6>
      <pre class="card-description-text">{{bugReport.Description}}</pre>

      <h6 class="card-title">Attachments</h6>
      <p class="card-attach-text">
        <ul id="attachments">
          <li v-for="(attachment, index) in bugReport.Attachments" :key="index">
            <img v-bind:src="attachment.attachment_url" width="550" v-if="attachment.type == 'image'"/>
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


export default {
  name: "BugReportCard",
  props:["bugReport"],
  components: {
    // StepAccordion,
    // StepTable,
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
    text-align: left;
    /* // box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2); */
  }
  #attachments video,
  #attachments img{
    width: 100%;
    height: 100%;
  } 

</style>