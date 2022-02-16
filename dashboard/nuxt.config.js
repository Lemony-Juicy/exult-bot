require('dotenv').config()

export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'Exult Bot · Home',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' },
      { content: "Exult Bot - Home", property: "og:title" },
      { content: "1 Bot, heaps of top tier quality features! It can do it all. With easy yet precise configuration and all the essential features to maintain and protect your server starting from effective moderation to role menus and suggestions! Why have 10 different bots for each feature when you can have 1 that can do everything you need!", property: "og:description" },
      { content: "https://bot.exult.games/", property: "og:url" },
      { content: "https://bot.exult.games/imgs/logo.png", property:"og:image" },
      { name: "theme-color", content: "#FF0000" },
      // { name: "twitter:card", content: "summary_large_image" } this is to make img bigger
    ],
    link: [
    ],
    script: [
      // Global JS Scripts
      {src: '/js/main.js', defer:true},
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '~/static/css/main.css',
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/tailwindcss
    '@nuxtjs/tailwindcss',
    '@nuxt/postcss8',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    '@nuxt/http'
  ],

  http: {
    
  },

  auth: {
    strategies: {
      discord: {
        clientId: process.env.CLIENTID,
        clientSecret: process.env.CLIENTSECRET,
        responseType: 'code',
        scope: ['guilds','identify']
      },
    },
    redirect: {
      login: '/',
      callback: '/login',
      home: '/',
      logout: '/'
    }
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    postcss: {
      plugins: {
        tailwindcss: {},
        autoprefixer: {},
      },
    },
  }
}
