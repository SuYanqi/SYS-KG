<template>
    <div class="card">
        <div class="card-body">
          <h6 class="card-title">Bug ID </h6>
          <a class="bug-link" href="">None</a>
          <h6 class="card-title">Summary</h6>
          <p class="card-summary-text"></p>
          <h6 class="card-title">Preconditions</h6>
          <p class="card-preconditions-text">None</p>
          <h6 class="card-title">Steps to Reproduce</h6>
          
          <div class="steps-accordin">
            <el-collapse id="step-items" v-model="activeNames" @change="handleChange">
                <div v-for="t in steps" :key="t.id">
                    <el-collapse-item v-bind:title="t">
                        <el-row>
                            <div>
                                <div>{{t.displayName}} editor</div>
                                <input type="text" />
                                <!-- <el-button v-on:click="collapse">
                                Close
                                </el-button> -->
                            </div>
                            This will contain some other fields for this item
                        </el-row>
                        <div>
                            {t}: Consistent within interface: all elements should be consistent, such
                            as: design style, icons and texts, position of elements, etc.
                        </div>
                    </el-collapse-item>
                </div>

                <!-- <el-collapse-item title="${}" name="1">
                    <div>
                        Consistent within interface: all elements should be consistent, such
                        as: design style, icons and texts, position of elements, etc.
                    </div>
                </el-collapse-item>
                <el-collapse-item title="Consistency" name="1">
                    <div>
                        Consistent within interface: all elements should be consistent, such
                        as: design style, icons and texts, position of elements, etc.
                    </div>
                </el-collapse-item> -->
            </el-collapse>
          </div>
            
          <h6 class="card-title">Expected Results</h6>
          <p class="card-expected-text">None</p>
          <h6 class="card-title">Actual Results</h6>
          <p class="card-actual-text">None</p>
          <h6 class="card-title">Notes</h6>
          <p class="card-notes-text">None</p>
          <h6 class="card-title">Attachment</h6>
          <p class="card-attach-text">None</p>
          <!-- <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p> -->
        </div>
      <!-- <img src="" class="card-img-bottom" alt=""> -->
    </div>
  <!-- <a class="bug-link" href="https://bugzilla.mozilla.org/show_bug.cgi?id=1678633">https://bugzilla.mozilla.org/show_bug.cgi?id=1678633</a> -->
  
  <!-- <div class="tips">
    <h6 class="title">
        Summary
    </h6>
    <div class="panel-body">
        go fighting
    </div>
  </div>

  <div class="tips">
    <h6 class="title">
        Summary
    </h6>
    <div class="panel-body">
        go fighting
    </div>
   </div> -->

</template>

<script>
export default {
    props: {
        steps: [],
    },
    data() {
    
        return {
            
            todos: [
                    { id: 'first',  displayName: 'First' }, 
                    { id: 'second', displayName: 'Second' }, 
                    { id: 'third',  displayName: 'Third'}
                ]
        }
  },

}
</script>

<style>
/* .bug-link{
    text-align: left;
    float: left
} */
.el-link {
  margin-right: 8px;
  float: left;
  /* font-size: 0.800em; */
  /* width: 100px; */
}
.el-link .el-icon--right.el-icon {
  vertical-align: text-bottom;
}
.tips{
    border-top: 1px solid red; 
    background-color: #2bf; 
    text-align: left;
    margin-top: 10px; 
    margin-bottom: 10px;
}
.card{
  text-align: left;  
}
p{
    font-size: 0.900rem;
}
h6{
    font-weight: 12px;
}


</style>