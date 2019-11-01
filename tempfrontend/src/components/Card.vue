<template>
    <div class = "Card">
         <textarea type="text" name="msg" v-model="msg"></textarea>
    </div> 
</template>

<script>
export default {
    name:"Card",
    props:['msg']
}
</script>