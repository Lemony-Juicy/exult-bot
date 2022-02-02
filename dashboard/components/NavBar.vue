<template>
  <div class="bg-blue-accent">
    <div class="mx-50">
      <div class="flex justify-between">
        <div class="flex">
          <div>
            <img src="~/static/imgs/logo.png" class="w-24" alt="EXULT Logo">
          </div>
          <div class="uppercase text-white mt-2">
            <p class="text-3xl tracking-extra font-bold">EXULT</p>
            <p class="font-bold text-sm">Discord Bot</p>
          </div>
        </div>
        <div class="mt-3 flex mr-10">
          <div class="dropdown inline-block relative">
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
          <p class="text-white font-semibold mt-3 ml-3">Join Our Discord</p>
          <svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="img" width="20" height="20" class=" translate-y-3-5 translate-x-11-5" preserveAspectRatio="xMidYMid meet" viewBox="0 0 24 24"><path d="M13 18v-8l3.5 3.5l1.42-1.42L12 6.16l-5.92 5.92L7.5 13.5L11 10v8h2M12 2a10 10 0 0 1 10 10a10 10 0 0 1-10 10A10 10 0 0 1 2 12A10 10 0 0 1 12 2z" fill="#c6af37"/></svg>
          <button class="ml-5 mt-2 gold-accent border border-gold-accent h-8 w-28 rounded-lg"><p class="ml-4">Premium</p></button>
          <button class="bg-primary-blue text-white w-24 ml-8 mt-2 rounded-lg h-8 font-semibold">Login</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ExultNavBar'
}
</script>
