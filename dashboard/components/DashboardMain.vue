<template>
    <div class="h-screen w-full text-white bg-main">
      <div class="flex ml-16">
        <img class="rounded-full" width="95" src="https://www.freepnglogos.com/uploads/discord-logo-png/discord-logo-logodownload-download-logotipos-1.png" id="servericon" alt="Server Icon">
        <select @change="OnServerSelect()" name="servers" id="server-select" class="text-white bg-transparent ml-3 h-10">
          <option class="bg-transparent text-black" value="select">Select a server:</option>
          <option class="bg-transparent text-black" value="in" v-for="server in guilds" :key="server.name">
            {{ server.name }}
          </option>
          <option class="bg-transparent text-gray-500" value="notin" v-for="servernot in guildsNotIn" :key="servernot.name">
            {{ servernot.name }}
          </option>
        </select>
      </div>
      <!-- Bot Config Div -->
      <div id="botConfigDivs" class="hidden">
        <div class="flex ml-16">
        <div class=" w-6/12 bg-blue-accent rounded-lg">
          <h1 class="font-bold text-xl ml-7 mt-5">Bot Configuration</h1>
          <form class="ml-7 mt-3" action="">
            <div class="items-center inline-flex mb-1">
              <p class="text-gray-500 ml-2 font-semibold">Prefix</p>
              <img src="~/static/imgs/gethelp.svg" class="w-5 ml-2" alt="Question Mark Help">
              <p class="ml-4 text-green-500 hidden" id="successText">Update Successful!</p>
              <p class="ml-4 text-red-500 hidden">Uh oh, Something went wrong! Try again</p>
            </div>
            <div class="flex mb-3">
              <input type="text" name="prefix" id="prefixConfig" class="w-9/12 p-2 bg-main rounded-lg" value="prefix">
              <button class="bg-primary-blue ml-6 px-6 rounded-lg font-bold" @click.prevent="confirmConfig()">Confirm</button>
            </div>

            <div class="items-center inline-flex mb-1">
              <p class="text-gray-500 ml-2 font-semibold">Moderator Roles</p>
              <img src="~/static/imgs/gethelp.svg" class="w-5 ml-2" alt="Question Mark Help">
            </div>
            <div class="flex mb-3">
              <input type="text" name="modRoles" id="modRoles" class="w-9/12 p-2 bg-main rounded-lg"  value="moderator roles">
              <img src="~/static/imgs/add.svg" class="relative right-10" alt="Add Roles">
              <button class="bg-primary-blue px-6 rounded-lg font-bold">Confirm</button>
            </div>

            <div class="items-center inline-flex mb-1">
              <p class="text-gray-500 ml-2 font-semibold">Blacklisted Channels</p>
              <img src="~/static/imgs/gethelp.svg" class="w-5 ml-2" alt="Question Mark Help">
            </div>
            <div class="flex mb-3">
              <input type="text" name="modRoles" id="modRoles" class="w-9/12 p-2 bg-main rounded-lg" value="blacklisted channels">
              <img src="~/static/imgs/add.svg" class="relative right-10" alt="Add Channels">
              <button class="bg-primary-blue px-6 rounded-lg font-bold">Confirm</button>
            </div>

            <div class="items-center inline-flex mb-1">
              <p class="text-gray-500 ml-2 font-semibold">Blacklisted Roles</p>
              <img src="~/static/imgs/gethelp.svg" class="w-5 ml-2" alt="Question Mark Help">
            </div>
            <div class="flex">
              <input type="text" name="modRoles" id="modRoles" value="blacklisted roles" class="w-9/12 p-2 bg-main rounded-lg">
              <img src="~/static/imgs/add.svg" class="relative right-10" alt="Add Roles">
              <button class="bg-primary-blue px-6 rounded-lg font-bold">Confirm</button>
            </div>
          </form>
        </div>
        <div class="flex flex-col ml-8 w-2/12">
          <div class="h-64 bg-blue-accent rounded-xl">
            <h1 class="font-bold text-xl ml-7 mt-5">Server Information</h1>
            <div class="grid grid-cols-2 ml-7 mt-5">
              <p class="mb-3 text-gray-500">Members:</p>
              <p id="memberCount" class="ml-5"></p>
              <p class="mb-3 text-gray-500">Roles</p>
              <p id="roleCount" class="ml-5"></p>
              <p class="mb-3 text-gray-500">Text Channels</p>
              <p id="textCount" class="ml-5"></p>
              <p class="mb-3 text-gray-500">Voice Channels</p>
              <p id="voiceCount" class="ml-5"></p>
            </div>
            <div class="items-center inline-flex ml-7">
              <img src="~/static/imgs/copy.svg" alt="">
              <p @click="copyId()" value="" id="copyGuildId" class="primary-blue text-sm cursor-pointer" href="#">COPY ID</p>
            </div>
          </div>
          <div class="bg-blue-accent mt-4 h-32 rounded-xl">
            <h1 class="font-bold text-xl ml-7 mt-5">Recent Changelogs</h1>
            <p class="ml-7 mt-2 text-gray-500">1st Jan, 22 <a href="#" class="text-blue-500">Bot Hotfixes #3</a></p>
          </div>
        </div>
      </div>
        </div>
      <div class="w-96 h-24 bg-blue-accent hidden ml-16 rounded-lg" id="addToServer">
        <div class="flex flex-col justify-center text-center">
          <p class="mt-2">Whoh! Im not in that server. Add me now!!!</p> 
          <button value="" @click="addBotToGuild()" class="text-white bg-primary-blue mx-3 py-1 mt-3" id="addToServerBtn">Add me to Server</button>
        </div>
      </div>
    </div>
</template>
<script>
export default {
  name: 'ExultDashMain',
  data() {
    return {
      guilds: [],
      guildsNotIn: [],
    }
  },

  methods: {
    async confirmConfig() {
      var prefixValue = document.getElementById("prefixConfig").value
      var guildId = document.getElementById("copyGuildId").value
      var successText = document.getElementById("successText")
      const data = await this.$http.$patch(`http://localhost:3000/api/v1/guilds/${guildId}/config?prefix=${prefixValue}`)
      if (data.success == true) {
        successText.classList.remove("hidden")
        setTimeout(() => { successText.classList.add("hidden") }, 5000);
      }
    },
    addBotToGuild() {
      if (process.browser) {
        var addToGuildBtnValue = document.getElementById("addToServerBtn").value

        location.href = `https://discord.com/oauth2/authorize?client_id=889185777555210281&permissions=3757567166&scope=bot%20applications.commands&guild_id=${addToGuildBtnValue}`
      }
    },
    async copyId() {
      if (process.browser) {
        var copyIdObject = document.getElementById("copyGuildId").value

        navigator.clipboard.writeText(copyIdObject).then(function() {
        }, function(err) {
          console.error(err);
        });
      }
    },
    async OnServerSelect() {
      // Requires .env file for secrets
      require('dotenv').config()

      if (process.browser) {

        // Get server-select Object AND get the text (server name) from the option they chose
        var selectedObject = document.getElementById("server-select")
        var servernameselect = selectedObject.options[selectedObject.selectedIndex].text

        // Grab the current array holding all the guild names.
        // arrayguilds: there is a mutual relation between user and bot
        var arrayguilds = this.guilds
        // arrayguildsNotIn: there is NOT a mutual relation at all
        var arrayguildsNotIn = this.guildsNotIn

        // If the selected option is has a mutual relation in servers with user and bot
        if (selectedObject.value == 'in') {
          var botConfigDivs = document.getElementById("botConfigDivs");
          var addToServer = document.getElementById("addToServer");
          botConfigDivs.classList.remove("hidden");
          addToServer.classList.add("hidden");

          for(let i = 0; i < arrayguilds.length; i++) {
          if (servernameselect == arrayguilds[i].name) {

            let guildId = arrayguilds[i].id
            let iconHash = arrayguilds[i].icon
            let img = document.getElementById("servericon")

            var copyIdObject = document.getElementById("copyGuildId")
            copyIdObject.value = guildId

            const guildinfo = await this.$http.$get(`http://localhost:3000/api/v1/guilds/${guildId}`, {
              debug: true,
              retry: 1.1,
            })

            var config = guildinfo.config

            var botConfigPrefix = document.getElementById("prefixConfig")
            botConfigPrefix.value = config.prefix


            var memberCount = document.getElementById("memberCount")
            var roleCount = document.getElementById("roleCount")
            var textCount = document.getElementById("textCount")
            var voiceCount = document.getElementById("voiceCount")

            memberCount.innerHTML = guildinfo.guild_members
            roleCount.innerHTML = Object.keys(guildinfo.guild_roles).length
            textCount.innerHTML = Object.keys(guildinfo.guild_text).length
            voiceCount.innerHTML = Object.keys(guildinfo.guild_voice).length

            if (iconHash == null) {
              img.src = `https://www.freepnglogos.com/uploads/discord-logo-png/discord-logo-logodownload-download-logotipos-1.png`
            }
            else {
              img.src = `https://cdn.discordapp.com/icons/${guildId}/${iconHash}.webp?size=96`
              onerror="this.onerror=null;this.src='https://www.freepnglogos.com/uploads/discord-logo-png/discord-logo-logodownload-download-logotipos-1.png';"
            }
          }
        }
        } else if(selectedObject.value == 'select') { 
          var botConfigDivs = document.getElementById("botConfigDivs");
          var addToServer = document.getElementById("addToServer");
          botConfigDivs.classList.add("hidden");
          addToServer.classList.add("hidden");

          let img = document.getElementById("servericon")
          img.src = `https://www.freepnglogos.com/uploads/discord-logo-png/discord-logo-logodownload-download-logotipos-1.png`
        } else {
          var botConfigDivs = document.getElementById("botConfigDivs");
          var addToServer = document.getElementById("addToServer");
          botConfigDivs.classList.add("hidden");
          addToServer.classList.remove("hidden");

          for(let i = 0; i < arrayguildsNotIn.length; i++) {
            if (servernameselect == arrayguildsNotIn[i].name) {

              let guildId = arrayguildsNotIn[i].id
              let iconHash = arrayguildsNotIn[i].icon
              let img = document.getElementById("servericon")

              var addToGuildBtn = document.getElementById("addToServerBtn")
              addToGuildBtn.value = guildId

              if (iconHash == null) {
                img.src = `https://www.freepnglogos.com/uploads/discord-logo-png/discord-logo-logodownload-download-logotipos-1.png`
              }
              else {
                img.src = `https://cdn.discordapp.com/icons/${guildId}/${iconHash}.webp?size=96`
                onerror="this.onerror=null;this.src='https://www.freepnglogos.com/uploads/discord-logo-png/discord-logo-logodownload-download-logotipos-1.png';"
              }
            }
          }
        }
      }
    }
  },
  async fetch() {
    // Requires .env file for secrets
    require('dotenv').config()

    // Setting Headers for HTTP GET request for all the users guilds
    var code = await this.$auth.strategy.token.get()
    await this.$http.setHeader('authorization', `${code}`)

    const userGuilds = await this.$http.$get('https://discord.com/api/users/@me/guilds', {
      debug: true,
      retry: 1.1,
    })

    // Convert to Binary Function
    function convertToBinary1 (number) {
      let num = number;
      let binary = (num % 2).toString();
      for (; num > 1; ) {
          num = parseInt(num / 2);
          binary =  (num % 2) + (binary);
      }
      return binary
    }

    // Getting list of all Guilds bot is in
    const guildStats = await this.$http.$get(`http://localhost:3000/api/v1/guilds`, {
      debug: true,
    })

    // Setting up Select Menu
    for(let i = 0; i < userGuilds.length; i++) {
      if(convertToBinary1(userGuilds[i].permissions | 8) == convertToBinary1(userGuilds[i].permissions) || convertToBinary1(userGuilds[i].permissions | 32) == convertToBinary1(userGuilds[i].permissions)) {
        const result = guildStats.filter(word => word.guild_id == userGuilds[i].id);
        if(result[0] != undefined) {
          // If there is a mutual between user and bot guild we push to guilds
          this.guilds.push(userGuilds[i])
        } else {
          // If there isnt a mutual relation we push guildsNotIn
          this.guildsNotIn.push(userGuilds[i])
        }
      }
    }
  }
}

</script>