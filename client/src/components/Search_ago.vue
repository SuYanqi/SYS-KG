<template>
  <h1>{{ msg }}</h1>
  <div class="search">
    
    <input type="text" v-model="input" placeholder="Please input here..."/>
    
    <button class='search-btn' @click="handleInput">Search</button>
    
  </div>
  <!-- <div class="result-container">
    <div class="left">
      <h5>Bug Report</h5>
      <BugReportTable />
      
    </div>
    <div class="main">
      <h5>Exploratory Testing</h5>
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Card title</h5>
          <p class="card-text">This is a wider card with supporting text.</p>
          <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
                    <p class="card-text">This is a wider card with supporting text.</p>
          <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
                    <p class="card-text">This is a wider card with supporting text.</p>
          <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
                    <p class="card-text">This is a wider card with supporting text.</p>
          <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Card title</h5>
          <p class="card-text">This is a wider card with supporting text.</p>
          <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p>
        </div>
      </div>
    </div>
    <div class="right">
      <h5>Relevant Bug Report</h5>
      <div class="demo-collapse">
    <el-collapse v-model="activeName" accordion>
      <el-collapse-item title="Consistency" name="1">
        <div>
          Consistent with real life: in line with the process and logic of real
          life, and comply with languages and habits that the users are used to;
        </div>
        <div>
          Consistent within interface: all elements should be consistent, such
          as: design style, icons and texts, position of elements, etc.
        </div>
      </el-collapse-item>
     
  

    </el-collapse>
  </div>
  </div> 
     </div> -->
</template>

<script>
import axios from "axios";
// import BugReportTable from "./BugReportTable.vue";
// import "bootstrap/dist/css/bootstrap.min.css";
// import "bootstrap/dist/js/bootstrap.min.js";

export default {
  name: "Search",
  components: {
    // BugReportTable
  },
  props: {
    msg: String,
    // steps: this.searchResult['Steps to Reproduce'],
  },
  data() {
    
    return {
      input: "",
      searchResult: "",
      // tableHtml: "",
      // stepHtml: "",

    }
  },
  methods: {

    async handleInput() {
      // `this` inside methods points to the current active instance
      // `event` is the native DOM event
      // if (event) {
        console.log(this.input);
        var input_val = {'input': this.input};
        await axios.post("http://localhost:5000/", input_val)
                        .then((res) => {this.searchResult = res.data})
                        console.log(this.searchResult);
        this.$emit('search-input', this.searchResult);
        // if (this.input) {
        //   document.getElementsByClassName("result-container")[0].style.display = "flex";
        //   // this.showTable()
        //   this.showBugTable()

        // } 

      // }
    },
    showTable() {
      
      let array = [[1,2], [3,4]]
      this.tableHtml = "";
    for(var i=0; i<array.length; i++) {
        this.tableHtml += "<tr>";
        for(var j=0; j<array[i].length; j++){
            this.tableHtml += "<td>"+array[i][j]+"</td>";
        }
        this.tableHtml += "</tr>";
    }
    // this.tableHtml += "</table>";
    console.log(this.tableHtml)

    },
    //  beforeUpdate() {
       
    //  },
    showBugTable(){
      var bug_link = "https://bugzilla.mozilla.org/show_bug.cgi?id=" + this.searchResult['id'];
      document.getElementsByClassName("bug-link")[0].href = bug_link
      document.getElementsByClassName("bug-link")[0].innerHTML = this.searchResult['id']
      document.getElementsByClassName("card-summary-text")[0].innerHTML = this.searchResult['Summary']
      document.getElementsByClassName("card-preconditions-text")[0].innerHTML = this.searchResult['Preconditions']
      document.getElementsByClassName("card-expected-text")[0].innerHTML = this.searchResult['Expected Results']
      document.getElementsByClassName("card-actual-text")[0].innerHTML = this.searchResult['Actual Results']
      document.getElementsByClassName("card-notes-text")[0].innerHTML = this.searchResult['Notes']

      var steps = this.searchResult['Steps to Reproduce'];

      for (var i = 0; i < steps.length; i++) {
      //   // console.log(steps[i]);
        this.stepHtml += "<el-collapse-item title='" + "Title" + "' name='"+ (i + 1) + "'>" +
                    "<div>"+ steps[i][0] + "</div> </el-collapse-item>"
      }
      // console.log(stepHtml)
      document.getElementById("step-items").innerHTML = this.stepHtml
    }
  },

};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
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
.search{
  width: 100%;
  padding: 20px;
  background-color: rgb(255, 255, 255);
}
.result-container{
  display: none;
  justify-content: center;
  border-radius: 0%;
  height: 100%;
  width: 100%;
  // box-sizing: border-box;
  text-align: center;
  padding: 1px;
  height: 100vh;
  background-color: rgb(255, 255, 255);
}
.left{
  // background-color: rgb(243, 155, 155);
  border-style: solid;
  border-width: 2px;
  border-color: rgba(182, 243, 207, 0.493);
  flex: 1;
}
input{
  width: 570px;
  height: 40px;
  border: 3px solid #42b983;
}
.search-btn{
  height: 40px;
  border: 3px solid #42b983;
  background-color: #42b983;
  padding: 0 7px;
}
.main{
  // border-style: solid;
  // border-width: 2px;
  // border-color: #020202;
  background-color: rgba(182, 243, 207, 0.493);
  flex: 1;
  overflow: auto;
}
.card{
  width: 100%;
  height: auto;
  // background-color: rgb(201, 208, 241);
  margin:10px 0;
  border-style: solid;
  border-width: 2px;
  border-color: #020202;
  // box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}
.right{
  // background-color: rgb(214, 241, 203);
  border-style: solid;
  border-width: 2px;
  border-color: rgba(182, 243, 207, 0.493);
  flex: 1;
  overflow: auto;
}
.item{
  width: 100%;
  height: 100px;
  background-color: rgb(201, 208, 241);
  margin:10px 0;
}

::-webkit-scrollbar
{
  width: 6px;
  height:6px;
  background-color: #fff;
}

::-webkit-scrollbar-thumb
{
  border-radius: 10px;
  /* -webkit-box-shadow:inset 0 0 6px rgba(184, 156, 156, 0.3);*/
  // background-color: rgba(27, 107, 34, 0.5); 
  background-color: #42b983
}

</style>
