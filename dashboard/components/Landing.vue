<template>
<div class="bg-backing bg-main h-landingfull">
    <div class="bg-main w-full h-landing bg-backing">
        <div class="relative h-l-half ml-60 flex justify-between">
            <div>
                <h1 class="font-bold text-white text-4xl">The Exult Discord Bot</h1>
                <p class="text-gray-400 font-semibold mt-5">An all-in-one bot to fit all your needs. <br> Moderation, Fun, Utility and More!</p>
                <button class="text-white bg-primary-blue px-4 py-2 mt-5 rounded-lg font-semibold ">Add to Discord</button>
                <button class="ml-4 primary-blue border border-primary-blue px-6 py-2 mt-5 rounded-lg font-semibold">Bot Features</button>
            </div>
            <div class=" mr-72">
                <img src="~/static/imgs/logo.png" class="w-106 relative bottom-36" alt="EXULT Logo">
                <p class="text-gray-200 text-center text-lg relative bottom-44">Bringing joy through <br> the world's digital playground</p>
            </div>
        </div>
    </div>
    <div class="w-full h-20 mb-12 bg-blue-accent flex justify-between text-white opacity-85">
        <h1 class="text-xl pt-6 font-semibold pl-20">Currently in <a class="red-accent">84</a> servers, serving <a class="red-accent">10,204</a> people</h1>
        <button class=" bg-primary-blue h-10 px-9 rounded-lg mt-4 mr-52">Learn More</button>
    </div>
</div>
</template>

<script>
export default {
  name: 'ExultLandingTop'
}
</script>