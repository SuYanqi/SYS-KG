<template>
  <div class="about">
    <a href="https://github.com/sysKG/BugFinding" target="_blank">Replication Package</a>

    <!-- <h1>About</h1> -->
      <!-- <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="num" label="No." width="200" />
        <el-table-column prop=“bugid” label="BugID" width=600>
            <template v-slot="props">
              <a :href="props.row.bugid" target="_blank">{{props.row.bugid}}</a>          
            </template>
        </el-table-column>
        <el-table-column prop="period" label="Period" />
      </el-table>   -->
  </div>
</template>

<script>
export default {
    name:'about',
    props:[],
    components:{
    },
    data() {
    
    return {
      // tableData: [
      //               {
      //                 num: '1',
      //                 bugid: 'https://bugzilla.mozilla.org/show_bug.cgi?id=1744772',
      //                 period: 'tool development',
      //               },
                   
      //             ]

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

</style>