// window.onload = function() {
//     let userid = $auth.user.id
//     let avatarhash = $auth.user.avatar
//     let img = document.getElementById("avatar")

//     img.src = "https://cdn.discordapp.com/avatars/534794607221800962/6e4532381ec8851d5ac3d50f6b4e234e.webp?size=80"
//     console.log('its set')
// }

// const faders = document.querySelectorAll('.fade-in');
// const sliders = document.querySelectorAll('.slide-in');

// const appearOptions = {
//     threshhold: 0.5,
//     rootMargin: "0px 0px -200px 0px"
// };

// const appearOnScroll = new IntersectionObserver(function(entries, appearOnScroll) {
//     entries.forEach(entry => {
//         if (!entry.isIntersecting) {
//             return;
//         } else {
//             entry.target.classList.add('appear');
//             appearOnScroll.unobserve(entry.target);
//         }
//     })
// }, appearOptions);

// faders.forEach(fader => {
//     appearOnScroll.observe(fader)
// })

// sliders.forEach(slider => {
//     appearOnScroll.observe(slider)
// })

// // navbar responsiveness

// const hamburgermenu = document.getElementById("hamburger-toggle-nav")
// const navBar = document.getElementById("navbar-links")

// hamburgermenu.addEventListener('click', () => {
//     navBar.classList.toggle('hidden')
//     console.log()
// })

// img.src = `https://cdn.discordapp.com/avatars/${userid}/${avatarhash}.webp?size=80`


