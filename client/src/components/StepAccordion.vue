<template>    
    <div class="steps-accordin">
    <el-collapse id="step-items" v-model="activeNames" @change="handleChange" accordion>
        <el-collapse-item v-for="(item ,index) in steps" :key="index" :title="item.StepText" >
        <!-- :name="item"> -->
            <div>
                Step Cluster: {{item.ClusterIndex}}
            </div>
            <div>
                <ExpectedActualTable :tableData="item.ExpectedActualResultsDictList"/>
            </div>
        </el-collapse-item>
    </el-collapse>
    </div>
</template>
<script>
import ExpectedActualTable from "./ExpectedActualTable.vue";

export default {
    name:'StepAccordion',
    props:['steps'],
    components:{
        ExpectedActualTable
    }
}
// console.log(this.todos)
</script>
<style lang="scss">

</style>
