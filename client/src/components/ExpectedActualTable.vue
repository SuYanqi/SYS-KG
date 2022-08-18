<template>    
   <!-- <div>
       <table>
           <tr>
               <td rowspan="2">bugid</td>
               <td> Expected Result </td>
           </tr>
           <tr>
               <td> Actual Result </td>
           </tr>

       </table>
   </div> -->
    <el-table :data="tableData" style="width: 100%" >
        <el-table-column prop="BugId" :min-width="20" label="Bug ID" />
        <!-- <el-table-column prop="ExpectedResults" label="Expected Results"  :min-width="40" /> -->
        <el-table-column label="Expected Results" :min-width="40">
            <template v-slot="props">          
                <p class="card-pre-text" v-if="!props.row.ExpectedResults">{{props.row.ExpectedResults}}</p>
                <p class="card-pre-text" v-else > 
                    <Highlighter class="my-highlight" 
                    highlightClassName="highlight"
                    :searchWords="props.row.ExpectedResultsElements"
                    :autoEscape="true"
                    :textToHighlight="props.row.ExpectedResults" 
                    :highlightStyle="{ background: 'rgba(236, 250, 222, 0.493)' }" />
                </p>
            </template>	
        </el-table-column>
        <!-- <el-table-column prop="ActualResults" label="Actual Results"  :min-width="40"/> -->
        <el-table-column label="Actual Results" :min-width="40">
            <template v-slot="props">          
                <p class="card-pre-text" v-if="!props.row.ActualResults">{{props.row.ActualResults}}</p>
                <p class="card-pre-text" v-else>
                    <Highlighter class="my-highlight" 
                        highlightClassName="highlight"
                        :searchWords="props.row.ActualResultsElements"
                        :autoEscape="true"
                        :textToHighlight="props.row.ActualResults" 
                        :highlightStyle="{ background: 'rgba(236, 250, 222, 0.493)' }"/>
                </p>
            </template>	
        </el-table-column>
  </el-table>
</template>
<script >
import Highlighter from 'vue-highlight-words';

export default {
    name:'ExpectedActualTable',
    props:["tableData"],
    components:{
        Highlighter,
    },
    data() {
    
    return {

    }
  },
}

</script>

<style lang="scss">
.el-table{
    word-break: normal;
}
</style>
