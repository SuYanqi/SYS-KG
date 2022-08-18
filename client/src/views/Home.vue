<template id='tem'>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png" /> -->
    <Search msg="Welcome to SYSKG" @search-input="handleSearchInput"/>
    
    <ResultContainer :searchResult="searchResult"/>
  </div>
</template>

<script>
// @ is an alias to /src
import Search from "@/components/Search.vue";
import ResultContainer from "@/components/ResultContainer.vue";
export default {
  name: "Home",
  components: {
    Search,
    ResultContainer,
  },
  data() {
    return {
      searchResult: "",
    }
  },
  methods: {
    handleSearchInput(searchResult){
        this.searchResult=searchResult;
        console.log(this.searchResult);
    },
  },
  
};
</script>
<style>
/* #tem{
  width: 100%;
  background-color: rgb(255, 255, 255);
}
.home{
  width: 100%;
  background-color: rgb(255, 255, 255);
  padding: 20px;
}
Search{

} */
</style>