<template>
    <div class="h-screen w-full text-white bg-main">
        <p>Welcome {{ $auth.user.username }}#{{ $auth.user.discriminator }} in {{  }}  </p>
         <ul>
          <li v-for="server in servers" :key="server.id">
            {{ server.id }}
          </li>
        </ul>
    </div>
</template>
<script>
export default {
  name: 'ExultDashMain',
  data() {
    return {
      servers: []
    }
  },

  async fetch() {
    var axios = require('axios');
    var code = this.$auth.strategy.token.get()
    var config = {
      method: 'get',
      url: 'https://discord.com/api/users/@me/guilds',
      headers: { 
        'authorization': `${code}`, 
      },
    };

    await this.$axios(config)
    .then(function (response) {
      var output = response.data
      // console.log(response.data);
      // console.log(JSON.stringify(response.data[1]));
      var actual = JSON.stringify(response.data[1])
    })
    .catch(function (error) {
      console.log(error);
    });

    this.servers = [
      {"id":"197038439483310086","name":"Discord Testers","icon":"54e272f2ea4e797e2514eb8d5cbe9c31","owner":false,"permissions":328704,"features":["DISCOVERABLE","NEW_THREAD_PERMISSIONS","THREADS_ENABLED","PRIVATE_THREADS","SEVEN_DAY_THREAD_ARCHIVE","VERIFIED","INVITE_SPLASH","MEMBER_VERIFICATION_GATE_ENABLED","WELCOME_SCREEN_ENABLED","BANNER","MEMBER_PROFILES","COMMUNITY","THREE_DAY_THREAD_ARCHIVE","ENABLED_DISCOVERABLE_BEFORE","VANITY_URL","ROLE_ICONS","ANIMATED_ICON","ANIMATED_BANNER","MORE_EMOJI","NEWS","PREVIEW_ENABLED"],"permissions_new":"693637547008"},
      {"id":"12345","name":"Discord Testers","icon":"54e272f2ea4e797e2514eb8d5cbe9c31","owner":true,"permissions":328704,"features":["DISCOVERABLE","NEW_THREAD_PERMISSIONS","THREADS_ENABLED","PRIVATE_THREADS","SEVEN_DAY_THREAD_ARCHIVE","VERIFIED","INVITE_SPLASH","MEMBER_VERIFICATION_GATE_ENABLED","WELCOME_SCREEN_ENABLED","BANNER","MEMBER_PROFILES","COMMUNITY","THREE_DAY_THREAD_ARCHIVE","ENABLED_DISCOVERABLE_BEFORE","VANITY_URL","ROLE_ICONS","ANIMATED_ICON","ANIMATED_BANNER","MORE_EMOJI","NEWS","PREVIEW_ENABLED"],"permissions_new":"693637547008"}
    ]
  },

}

</script>