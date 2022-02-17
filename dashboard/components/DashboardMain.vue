<template>
    <div class="h-screen w-full text-white bg-main">
        <p>Welcome {{ $auth.user.username }}#{{ $auth.user.discriminator }}. You have perms in {{ Object.keys(servers).length }} servers.</p>
        <select @change="OnServerSelect()" name="servers" id="server-select" class="text-white bg-transparent">
          <option class="bg-transparent text-black">Select a server:</option>
          <option class="bg-transparent text-black" v-for="server in servers" :key="server.name">
            {{ server.name }}
          </option>
        </select>
        <img class="rounded-full" width="95" src="https://www.freepnglogos.com/uploads/discord-logo-png/discord-logo-logodownload-download-logotipos-1.png" id="servericon" alt="Server Icon">
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

  methods: {
    async OnServerSelect() {
      require('dotenv').config()
      if (process.browser) {

      var servernameselect = document.getElementById("server-select").value
      var arrayservers = this.servers

      for(let i = 0; i < Object.keys(arrayservers).length; i++) {
        if (servernameselect == arrayservers[i].name) {

          let serverid = arrayservers[i].id
          let iconhash = arrayservers[i].icon
          let img = document.getElementById("servericon")

          const guildinfo = await this.$http.$get(`http://localhost:3000/api/v1/guilds/19389129321`, {
            debug: true,
            retry: 1.1,
          })

          console.log(guildinfo)

          // const guildChannelinfo = await this.$http.$get(`https://discord.com/api/guilds/${serverid}/channels`, {
          //   debug: true,
          //   retry: 1.1,
          // })

          // console.log(guildChannelinfo)

          if (iconhash == null) {
            img.src = `https://www.freepnglogos.com/uploads/discord-logo-png/discord-logo-logodownload-download-logotipos-1.png`
          }
          else {
            img.src = `https://cdn.discordapp.com/icons/${serverid}/${iconhash}.webp?size=96`
            onerror="this.onerror=null;this.src='https://www.freepnglogos.com/uploads/discord-logo-png/discord-logo-logodownload-download-logotipos-1.png';"
          }
        }
      }

      }
    }
  },
  async fetch() {
    require('dotenv').config()

    var code = await this.$auth.strategy.token.get()
    await this.$http.setHeader('authorization', `${code}`)
    // const stuff = await this.$http.$get('https://discord.com/api/users/@me/guilds')

    const stuff = await this.$http.$get('https://discord.com/api/users/@me/guilds', {
      debug: true,
      retry: 1.1,
    })

    function convertToBinary1 (number) {
      let num = number;
      let binary = (num % 2).toString();
      for (; num > 1; ) {
          num = parseInt(num / 2);
          binary =  (num % 2) + (binary);
      }
      return binary
    }

    this.servers = []

    // console.log(stuff)
    for(let i = 0; i < Object.keys(stuff).length; i++) {
      if (convertToBinary1(stuff[i].permissions | 8) == convertToBinary1(stuff[i].permissions) || convertToBinary1(stuff[i].permissions | 32) == convertToBinary1(stuff[i].permissions)) {
        this.servers.push(stuff[i])

        // console.log('servername:', stuff[i].name, 'normal perms:', stuff[i].permissions, 'special:', stuff[i].permissions | 8)
      }
      
    }
  }
}

</script>