<template>
  <el-table class="step-table" :data="steps" style="width: 100%; color: black;" :row-class-name="getRowClass" ref="multipleTable" @row-click="rowClick" >
    
    <el-table-column class="step-column" type="expand" >
      <template #default="props" >
        <div>
            <ExpectedActualTable :tableData="props.row.ExpectedActualResultsDictList" />
            <!-- <p v-else> No Data </p> -->
        </div>
        <!-- <p>Result: {{ props.row.ExpectedActualResultsDictList }}</p> -->
        <!-- <p>City: {{ props.row.city }}</p>
        <p>Address: {{ props.row.address }}</p>
        <p>Zip: {{ props.row.zip }}</p> -->
      </template>
    </el-table-column>
    <el-table-column label="Cluster" prop="ClusterIndex" min-width="20"/>
    <!-- <el-table-column label="Step" prop="StepText" /> -->
    <el-table-column label="Step" >
      <template v-slot="props">          
        <div v-if="!props.row.StepText">{{props.row.StepText}}</div>
        <Highlighter class="my-highlight" :style="{ color: 'black' }"
          highlightClassName="highlight"
          :searchWords="props.row.StepElements"
          :autoEscape="true"
          :textToHighlight="props.row.StepText" 
          :highlightStyle="{ background: 'rgba(182, 243, 207, 0.493)' }"
          v-else />
      </template>	
    </el-table-column>
  </el-table>
</template>

<script>
import Highlighter from 'vue-highlight-words';

import ExpectedActualTable from "./ExpectedActualTable.vue";

export default {
    name:'StepTable',
    props:['steps'],
    components:{
        ExpectedActualTable,
        Highlighter,

    },
    data() {
    
    return {
      highlightWords: [],
    //   index: 0,
    }
  },
  methods: {
      // 判断表格是否有子项，无子项不显示展开按钮 https://juejin.cn/post/6939294564435886111
    getRowClass(row) {
        if (row.row.ExpectedActualResultsDictList.length === 0) {
            return 'row-expand-cover'
        }
    },
    //优化点击展开
    rowClick(row) {
        // this.$refs.multipleTable.toggleRowExpansion(row)
    },

  },
  // computed: {
  //   keywords() {
  //     if (this.steps.StepElements){
  //       for(let i=0; i < this.steps.StepElements.length; i++){
  //         this.highlightWords.push(this.steps.StepElements[i])
  //       }   
  //     }

  //     return this.highlightWords
  //   }
  // }

}
</script>

<style>
/* @import url("//unpkg.com/element-ui@2.13.2/lib/theme-chalk/index.css"); */
/* .el-table-column{ */
.step-column{
    width: auto;
}
/* .el-table { */
.step-table{
  color: black;
}
/* .el-table thead {
  color: black;
} */

/*没有子项的时候不显示展开的小箭头*/
.el-table .row-expand-cover .cell .el-table__expand-icon {
  display: none;
  
  word-break: normal;
}

</style>
