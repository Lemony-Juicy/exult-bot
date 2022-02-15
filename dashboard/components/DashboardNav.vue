<template>
    <div class="h-screen w-72 text-white border-r bg-main">
        <div class="flex mt-4">
            <div>
              <img src="~/static/imgs/logo.png" width="6rem" height="6rem" class="w-24 min-w-6" alt="EXULT Logo">
            </div>
            <div class="uppercase text-white mt-2">
              <p class="text-3xl tracking-extra font-bold">EXULT</p>
              <p class="font-bold text-sm">Discord Bot</p>
            </div>
        </div>
        <div class="flex justify-center">
            <ul class="w-80-cent mt-4">
                <li class="active border-0 rounded-lg p-px2 text-gray-400"><p class="ml-10">Dashboard</p></li>
                <li class="border-0 rounded-lg p-px2 mt-2 text-gray-400"><p class="ml-10">Modules</p></li>
                <li class="border-0 rounded-lg p-px2 mt-2 text-gray-400"><p class="ml-10">Settings</p></li>
                <li class="border-0 rounded-lg p-px2 mt-2 gold-accent"><p class="ml-10">Get Premium</p></li>
                <li class="border-0 rounded-lg p-px2 mt-2 primary-blue"><p class="ml-10">Get Help</p></li>
                <a class=" cursor-pointer" @click="logout()"><li class="border-0 rounded-lg p-px2 mt-2 text-red-400"><p class="ml-10">Logout</p></li></a>
            </ul>
        </div>
    </div>
</template>
<script>
export default {
  name: 'ExultDashNav',
  methods: {
    logout() {
      this.$auth.logout('discord')
      if (process.browser){
            location.href = '/';
      }
    }
  }
}

</script>