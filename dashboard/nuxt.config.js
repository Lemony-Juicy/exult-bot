require('dotenv').config()

export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'Exult Bot · Home',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      // Standard Stuff
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' },
      // Import Meta Data
      { name: "description", content: "1 Bot, heaps of top tier quality features! It can do it all. With easy yet precise configuration and all the essential features to maintain and protect your server starting from effective moderation to role menus and suggestions! Why have 10 different bots for each feature when you can have 1 that can do everything you need!"},
      { name: "keywords", content: "discord,bot,exult,top.gg,discord.py,moderation bot,role menus,utility bot, suggestions bot, fun bot" },
      { name: "author", content: "Exult Games"},
      { name: "robots", content: "follow, index"},
      // Graph Meta Tags
      { content: "Exult Bot - Home", property: "og:title" },
      { content: "Exult is a bot with an easy yet precise configuration and all the essential features to maintain and protect your server starting from effective moderation to role menus and suggestions!", property: "og:description" },
      { content: "https://bot.exult.games/", property: "og:url" },
      { content: "website", property: "og:type"},
      { content: "https://bot.exult.games/imgs/logo.png", property:"og:image" },
      { content: "Exult Games logo", property: "og:image:alt"},
      { name: "theme-color", content: "#1F2424" },
      // Twitter Meta Tags
      { name: "twitter:title", content: "Exult Bot - Home"},
      { name: "twitter:description", content: "Exult is a bot with an easy yet precise configuration and all the essential features to maintain and protect your server starting from effective moderation to role menus and suggestions!"},
      { name: "twitter:image", content: "https://bot.exult.games/imgs/logo.png"},
      { name: "twitter:image:alt", content: "Exult Games logo"},
      { name: "twitter:site", content: "@Andehlive"},
      { name: "twitter:creator", content: "@Andehlive" },
      // { name: "twitter:card", content: "summary_large_image" } this is to make img bigger (longer)
    ],
    link: [
      { rel:"shortcut icon", href: "https://bot.exult.games/imgs/favicon.ico" },
      { rel: "apple-touch-icon", href: "https://bot.exult.games/imgs/logo.png" }
    ],
    script: [
      // Global JS Scripts
    ]
  },

  serverMiddleware: {
    '/api': '~/api'
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '@/static/css/main.css',
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
    '@nuxt/http',
    '@nuxtjs/dotenv',
  ],

  dotenv: {
    /* module options */
  },

  http: {
    
  },

  auth: {
    strategies: {
      discord: {
        clientId: process.env.CLIENTID,
        clientSecret: process.env.CLIENTSECRET,
        responseType: 'code',
        scope: ['guilds','identify', 'guilds.members.read']
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
    extend (config, ctx) {
      config.node = {
          fs: "empty"
      };
  }
  }
}
