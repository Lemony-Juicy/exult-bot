<template>
    <div class="h-screen w-full text-white bg-main">
        <p>Welcome {{ $auth.user.username }}#{{ $auth.user.discriminator }} in {{ guilds }} </p>
         <ul>
          <li v-for="guilds in servers" :key="guilds.message">
            {{ guilds.message }}
          </li>
        </ul>
    </div>
</template>
<script>
export default {
  name: 'ExultDashMain',
  data() {
    return {
      servers: [
        
        ]
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
        'Cookie': '__dcfduid=fd1793768e7111ec91cd42010a0a001a; __sdcfduid=fd1793768e7111ec91cd42010a0a001a0c45d7d86e974da54d3798a7e1fcdad8a07ad9e811e4ffe52c6ac22c7f35bde5'
      },
    };

    this.servers = await axios(config)
    .then(function (response) {
      var output = response.data
      // console.log(response.data);
    })
    .catch(function (error) {
      console.log(error);
    }); 
  }
}

</script>