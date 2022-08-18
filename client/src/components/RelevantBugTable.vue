<template>
    <el-table :data="relevantBugReports" 
        :row-key="getRowKeys"
        :expand-row-keys="expands" 
        :row-class-name="rowClassName"
        style="width: 100%; color: black;" ref="multipleTable" @row-click="rowClick" @expand-change="expandChange">
        
        <el-table-column type="expand" >
            <template #default="props" >
                <div>
                    <BugReportCard :bugReport="props.row.bugReport" />
                    <!-- <p v-else> No Data </p> -->
                </div>
            </template>
        </el-table-column>
        <!-- <el-table-column label="Bug ID" prop="id" min-width="30"/>
        <el-table-column label="ClusterScore" prop="cluster_index_count_sum" min-width="35"/> -->
        <!-- <el-table-column label="ClusterList" prop="cluster_index_list" min-width="30"/> -->
        <el-table-column label="No." prop="index" min-width="10" />
        <el-table-column label="ClusterList" min-width="20">
            <template v-slot="props">
               <div v-for="(val, index) in props.row.cluster_index_list" :key="index">
                <div>{{val[0]}}<sup>{{val[1]}}</sup></div>
               </div>
            </template>	
        </el-table-column>
        <el-table-column label="Product::Component" min-width="30">
            <template v-slot="props">          
                <div>{{props.row.bugReport.product}}::{{props.row.bugReport.component}}</div>
            </template>	
        </el-table-column>
        <el-table-column label="Summary" prop="Summary" min-width="40"/>
    </el-table>    
</template>
<script>
// import ExpectedActualTable from "./ExpectedActualTable.vue";
import BugReportCard from "./BugReportCard.vue";

export default {
    name:'RelevantBugTable',
    props:['relevantBugReports'],
    components:{
        BugReportCard,
    },
    data() {
        return {
            // 要展开的行，数值的元素是row的key值
            expands: [],
        }
    },
    // watch: { 
    //     relevantBugReports: {
    //         handler(){
    //             // To avoid coming across situations where undefined variables may be accessed accidentally, an if check should be added before dealing with such variables:
    //            if (typeof(this.relevantBugReports[0]) !== 'undefined') {
    //                // 要展开的行，数值的元素是row的key值,添加row的key
    //                this.expands.push(JSON.parse(JSON.stringify(this.relevantBugReports))[0].id);
    //            }
    //         },
    //         immediate: true
    //     }
    // },

    methods: {
        //优化点击展开 + return bugId
        rowClick(row) {
            this.$refs.multipleTable.toggleRowExpansion(row)
            this.$emit('returnBugId', row.id)
            // console.log(row.id)
        },
        // expand column -> return bugId
        expandChange(row){
            this.$emit('returnBugId', row.id)
        },
        // 获取row的key值
        getRowKeys(row) {
            // console.log(row.id)
            return row.id;
        },
        rowClassName({row, rowIndex}) {
            //把每一行的索引放进row.index
            row.index = rowIndex+1;
        },
    },

}
</script>
<style lang="scss">

</style>
