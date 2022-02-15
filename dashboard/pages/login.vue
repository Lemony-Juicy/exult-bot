<template>
<div class="font-main overflow-none-x ">
    Logging in...
</div>
</template>

<script>
export default {
  name: 'LoginPage',
//   mounted() {
//     if (!this.$auth.loggedIn) { 
//         this.$auth.loginWith('discord') 
//     }
//     else this.$auth.redirect("/")  
//   }
    created: function() {
        if (process.browser && this.$auth.loggedIn){
            location.href = '/dashboard';
        }
        else if (process.browser && !this.$auth.loggedIn){
            location.href = '/';
        }
    }
}
</script>
