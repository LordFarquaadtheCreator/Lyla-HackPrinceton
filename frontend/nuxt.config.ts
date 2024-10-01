// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },

  // SSR must be turned off
  ssr: false,

  modules: ["@pinia/nuxt", "@nuxtjs/tailwindcss"],
  css: ['@/assets/css/main.css'],
});
