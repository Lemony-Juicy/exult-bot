<template>
  <div class="bg-blue-accent">
    <div class="max-w-8xl ml-2 lg:ml-52">
      <div class="flex justify-between flex-col md:flex-row">
        <div class="flex justify-between">
          <div class="flex">
            <div>
              <img src="~/static/imgs/logo.png" width="6rem" height="6rem" class="w-24 min-w-6" alt="EXULT Logo">
            </div>
            <div class="uppercase text-white mt-2">
              <p class="text-3xl tracking-extra font-bold">EXULT</p>
              <p class="font-bold text-sm">Discord Bot</p>
            </div>
          </div>
          <a id="hamburger-toggle-nav" class="mt-4">
              <img src="~/static/imgs/hambuger.svg" class="w-10 block md:hidden mr-10" alt="Hamburger Menu">
          </a>
        </div>
        
        <div id="navbar-links" class="mt-3 md:flex mr-10 flex-col md:flex-row hidden">
          <div class="dropdown md:inline-block flex relative">
            <div class="text-white font-semibold mt-1 py-2 px-4 rounded inline-flex items-center">
              <span class="mr-1">Exult</span>
              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/> </svg>
            </div>
            <ul class="dropdown-menu absolute hidden text-gray-700 pt-1">
              <li><a class="rounded-t bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap" href="#">Bruh</a></li>
              <li><a class="bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap" href="#">Funny</a></li>
              <li><a class="rounded-b bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap" href="#">eeee</a></li>
            </ul>
          </div>
          <div class="dropdown inline-block relative">
            <div class="text-white font-semibold mt-1 py-2 px-4 rounded inline-flex items-center">
              <span class="mr-1">Help</span>
              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/> </svg>
            </div>
            <ul class="dropdown-menu absolute hidden text-gray-700 pt-1">
              <li><a class="rounded-t bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap" href="#">aaasesea</a></li>
              <li><a class="bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap" href="#">Link here</a></li>
              <li><a class="rounded-b bg-gray-200 hover:bg-gray-400 py-2 px-4 block whitespace-no-wrap" href="#">CiaranGames cool</a></li>
            </ul>
          </div>
          <p class="text-white font-semibold mt-3 ml-3 mr-5">Join Our Discord</p>
          <div class="flex flex-col mt-8 md:flex-row md:mt-0 -ml-8">
            <div class="items-center inline-flex">
              <svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img" width="20" height="20" class=" -translate-y-2 translate-x-11-5" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path d="M13 18v-8l3.5 3.5l1.42-1.42L12 6.16l-5.92 5.92L7.5 13.5L11 10v8h2M12 2a10 10 0 0 1 10 10a10 10 0 0 1-10 10A10 10 0 0 1 2 12A10 10 0 0 1 12 2z" fill="#c6af37"/></svg>
              <button class="ml-5 -mt-4 gold-accent border border-gold-accent h-8 w-28 rounded-lg"><p class="ml-4">Premium</p></button>
            </div>
            <button v-if="!$auth.loggedIn" @click="login()" id="login" class="bg-primary-blue text-white mt-4 mb-4 ml-10 w-24 md:ml-8 md:mt-2 rounded-lg h-8 font-semibold">Login</button>
            <!-- " this is u: {{ $auth.user.username }} # {{ $auth.user.discriminator }} " -->
            <button v-else onclick="location.href='/dashboard'" id="login" class="bg-primary-blue text-white mt-4 mb-4 ml-10 w-28 md:ml-8 md:mt-2 rounded-lg h-8 font-semibold">Dashboard</button>
          </div>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExultNavBar',
  methods: {
    login() {
      this.$auth.loginWith('discord')
    }
  }
}
</script>
