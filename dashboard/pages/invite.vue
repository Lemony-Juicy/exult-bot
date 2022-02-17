<template>
    <div>
        Redirecting you...
    </div>
</template>

<script>
export default {
  name: 'InvitePages',

    mounted: function() {
        if (process.browser){
            location.href = 'https://discord.com/oauth2/authorize?client_id=889185777555210281&permissions=3757567166&scope=bot%20applications.commands';
        }
    }
}
</script>
