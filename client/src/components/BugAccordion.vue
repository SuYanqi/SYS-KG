<template>    
    <div class="bugs-accordin">
    <el-collapse id="bug-items" v-model="activeNames" @change="handleChange" accordion>
        <el-collapse-item v-for="(bugReport ,index) in relevantBugReports" :key="index" :title="bugReport.id" @click="getClickedBugId(bugReport.id)">
        <!-- :name="item"> -->
            <!-- <div>
                Step Cluster: {{item.Summary}}
            </div> -->
            <BugReportCard :bugReport=bugReport />
            <!-- <div>
                 
            </div> -->
        </el-collapse-item>
    </el-collapse>
    </div>
</template>
<script>
// import ExpectedActualTable from "./ExpectedActualTable.vue";
import BugReportCard from "./BugReportCard.vue";

export default {
    name:'BugAccordion',
    props:['relevantBugReports'],
    components:{
        BugReportCard,
    },
    methods: {
        getClickedBugId(bugId){
            this.$emit('returnBugId', bugId)
            // console.log(bugId)
            // alert(bugId)
        },

    },

}
</script>
<style lang="scss">

</style>
