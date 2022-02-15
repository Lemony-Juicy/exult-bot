<template>
<div class="bg-backing bg-main h-full ">
    <div class="bg-main w-full h-landing bg-backing">
        <div class="relative h-l-half  ml-0 lg:ml-52 flex justify-center lg:justify-between">
            <div class="fade-in text-left">
                <h1 class="font-bold text-white text-4xl">The Exult Discord Bot</h1>
                <p class="text-gray-400 font-semibold mt-5">An all-in-one bot to fit all your needs. <br> Moderation, Fun, Utility and More!</p>
                <div class="flex flex-col lg:flex-row">
                    <button class="text-white bg-primary-blue px-4 py-2 mt-5 rounded-lg font-semibold ">Add to Discord</button>
                    <button class="lg:ml-4 primary-blue border border-primary-blue px-6 py-2 mt-5 rounded-lg font-semibold">Bot Features</button>
                </div>
            </div>
            <div class=" mr-52 fade-in hidden lg:block">
                <img src="~/static/imgs/logo.png" class="w-106 relative bottom-36" alt="EXULT Logo">
                <p class="text-gray-200 text-center text-lg relative bottom-44">Bringing joy through <br> the world's digital playground</p>
            </div>
        </div>
    </div>
    <div class="w-full h-20 mb-12 bg-blue-accent flex md:justify-between text-white opacity-85 justify-center">
        <h1 class="text-xl pt-6 font-semibold md:pl-16 lg:pl-48 xl:pl-52">Currently in <a class="red-accent">81</a> servers, serving <a class="red-accent">65595</a> people</h1>
        <button class=" bg-primary-blue h-10 px-9 rounded-lg mt-4 hidden md:block md:mr-20 lg:mr-52 xl:mr-96">Learn More</button>
    </div>
    <div class="flex lg:justify-between text-center flex-col lg:flex-row pt-4">
        <div class="text-white w-full lg:flex lg:flex-col lg:justify-start mt-20 from-left slide-in">
            <div class="lg:ml-48 lg:text-left">
                <h1 class="text-3xl font-bold">It's time to revamp <br> your Discord server</h1>
                <p class="mt-3 text-gray-400">The Exult Discord Bot does it all for you. <br> Sit back, relax and enjoy!</p>
            </div>
        </div>
        <div class="w-full flex justify-center lg:justify-end">
             <div class="from-right slide-in mr-0 mt-10 lg:mt-0 lg:mr-60">
                <img class="max-w-32" src="~/static/imgs/DiscordBG.svg" alt="Discord Mockup Background">
            </div>
        </div>
    </div>
    <div class="flex lg:justify-between text-center flex-col lg:flex-row pt-4">

        <div class="w-full flex from-left slide-in ml-36 justify-center lg:block sm:hidden">
            <img class=" max-w-32" src="~/static/imgs/DashboardGFX.svg" alt="Discord Mockup Background">
        </div>
        <div class="text-white w-full lg:flex lg:flex-col lg:justify-start mt-20 from-right slide-in">
            <div class=" lg:mr-42 lg:text-center">
                <h1 class="text-3xl font-bold">You're in control...</h1>
                <p class="mt-3 text-gray-400">A fully-customisable bot, <br> with a user-friendly dashboard!</p>
            </div>
        </div>
        <!-- <div class="text-white lg:mr-96 mt-20 from-left slide-in">
            <h1 class="text-3xl font-bold">It's time to revamp <br> your Discord server</h1>
            <p class="mt-3 text-gray-400">The Exult Discord Bot does it all for you. <br> Sit back, relax and enjoy!</p>
        </div> -->
        <div class="from-right lg:hidden flex justify-center mb-20 mt-10 lg:mt-0 lg:mb-0 sm:block slide-in">
            <img class="max-w-32 lg:ml-36" src="~/static/imgs/DashboardGFX.svg" alt="Discord Mockup Background">
        </div>
    </div>
    <!-- <div class="flex md:justify-between pt-4">
        <div class="flex justify-center text-center flex-col md:flex-row">
            <div class=" ml-36 from-left slide-in">
                <img class="md:-mt-20 max-w-32 min-w-32" src="~/static/imgs/DashboardGFX.svg" alt="Dashboard Coming Soon Background">
            </div>
            <div class="text-white mr-0 md:mr-96 mt-32 from-right slide-in">
                <h1 class="text-3xl font-bold">You're in control...</h1>
                <p class="mt-3 text-gray-400">A fully-customisable bot, <br> with a user-friendly dashboard!</p>
            </div>
        </div>
    </div> -->
    <h1 class="flex justify-center text-white text-4xl font-bold">Help & Resources</h1>
    <div class="mt-10 flex justify-center">
        <div class="flex flex-col md:flex-row mt-10 fade-in">
            <div class="text-white h-96 w-80 md:ml-0 mb-14 md:mb-0 rounded-2xl flex justify-center border border-gold-accent bg-blue-accent">
                <div class="mt-7">
                    <p class="text-center text-2xl font-bold">List of features</p>
                    <p class="mt-2 p-3 text-center">The Exult Discord Bot has a wide variety of many different features.
                        Make sure to read through the whole list to get the maximum potential out of the bot!
                    </p>
                    <img class="ml-3" src="~/static/imgs/BPs.svg" alt="List Preview Mockup">
                    <button class="bg-primary-blue p-3 px-5 rounded-xl ml-24 mt-3">See full list</button>
                </div>
            </div>
            <div class="text-white h-96 w-80 md:ml-20 rounded-2xl flex justify-center border border-gold-accent bg-blue-accent">
                <div class="mt-7">
                    <p class="text-center text-2xl font-bold">Setup</p>
                    <p class="text-center mt-3">It's quick and easy...</p>
                    <h1 class="mt-5  primary-blue">1. <a href="#">Add to Discord</a></h1>
                    <h1 class=""><a class="primary-blue">2.</a> Type "e!help" for all commands </h1>
                    <h1 class=""><a class="primary-blue">3.</a> Enjoy the bot! </h1>
                    <img class="mt-5" src="~/static/imgs/Cogs.svg" alt="Cogs and Squares">
                    <button class="bg-red-accent p-3 rounded-xl ml-12 mt-3">Guides Coming Soon...</button>
                </div>
            </div>
        </div>
    </div>
    <div class="w-full mt-24 h-32 bg-blue-accent text-center text-white">
    <div class="flex justify-center pt-8">
        <a href="#"><img class="mr-2" src="~/static/imgs/twitter.svg" alt="Twitter Logo"></a>
        <a href="#"><img class="mr-2" src="~/static/imgs/instagram.svg" alt="Instagram Logo"></a>
        <a href="#"><img class="mr-2" src="~/static/imgs/github.svg" alt="Instagram Logo"></a>
        <a href="#"><img class="mr-2" src="~/static/imgs/discord.svg" alt="Instagram Logo"></a>
    </div>
        <p class="pt-1">Copyright © 2021 Exult Games</p>
        <p>All Rights Reserved</p>
    </div>
</div>
</template>

<script>
export default {
  name: 'ExultLandingTop'
}

</script>