<template>
<div class="font-main overflow-none-x ">
  <NavBar/>
  <Landing/>
</div>
</template>

<script>
export default {
  name: 'IndexPage',
   mounted: function() {
    if (process.browser) {
      const faders = document.querySelectorAll('.fade-in');
      const sliders = document.querySelectorAll('.slide-in');

      const appearOptions = {
          threshhold: 0.5,
          rootMargin: "0px 0px -200px 0px"
      };

      const appearOnScroll = new IntersectionObserver(function(entries, appearOnScroll) {
          entries.forEach(entry => {
              if (!entry.isIntersecting) {
                  return;
              } else {
                  entry.target.classList.add('appear');
                  appearOnScroll.unobserve(entry.target);
              }
          })
      }, appearOptions);

      faders.forEach(fader => {
          appearOnScroll.observe(fader)
      })

      sliders.forEach(slider => {
          appearOnScroll.observe(slider)
      })

      // navbar responsiveness

      const hamburgermenu = document.getElementById("hamburger-toggle-nav")
      const navBar = document.getElementById("navbar-links")

      hamburgermenu.addEventListener('click', () => {
          navBar.classList.toggle('hidden')
          console.log()
      })
    }
  }
}
</script>
