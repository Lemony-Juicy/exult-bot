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
            <ul class="w-80-cent mt-2 -ml-7">
                <div class="items-center inline-flex mt-2">
                    <img src="~/static/imgs/dashboard.svg" class="relative left-8 active-svg" alt="dashboard icon">
                    <NuxtLink to="/dashboard/dashboard" class="cursor-pointer">
                    <li class="active border-0 w-52 rounded-lg p-px2 text-gray-400"><p class="ml-12">Dashboard</p></li>
                    </NuxtLink>
                </div>
                <div class="items-center inline-flex mt-2">
                    <img src="~/static/imgs/modules.svg" class="relative left-8" alt="modules icon">
                    <NuxtLink to="/dashboard/modules" class="cursor-pointer">
                        <li class=" border-0 w-52 rounded-lg p-px2 text-gray-400"><p class="ml-12">Modules</p></li>
                    </NuxtLink>
                </div>
                <div class="items-center inline-flex mt-2">
                    <img src="~/static/imgs/settings.svg" class="relative left-8" alt="settings icon">
                    <NuxtLink to="/dashboard/settings" class="cursor-pointer">
                        <li class=" border-0 w-52 rounded-lg p-px2 text-gray-400"><p class="ml-12">Settings</p></li>
                    </NuxtLink>
                </div>
                <div class="items-center inline-flex mt-2">
                    <img src="~/static/imgs/premuim.svg" class="relative left-8" alt="settings icon">
                    <li class=" border-0 w-52 rounded-lg p-px2 gold-accent"><p class="ml-12">Get Premuim</p></li>
                </div>
                <div class="items-center inline-flex mt-2">
                    <img src="~/static/imgs/gethelp.svg" class="relative left-8" alt="settings icon">
                    <a href="https://discord.gg/3J7nW3MDz7">
                        <li class=" border-0 w-52 rounded-lg p-px2 primary-blue"><p class="ml-12">Get Help</p></li>
                    </a>
                </div>
                <div class="items-center inline-flex mt-2">
                    <img src="~/static/imgs/signout.svg" class="relative left-8" alt="settings icon">
                    <a class=" cursor-pointer" @click="logout()"><li class="border-0 rounded-lg p-px2 red-accent" ><p class="ml-12">Logout</p></li></a>
                </div>
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