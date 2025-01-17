import { defineConfig } from "astro/config";
import react from "@astrojs/react";

export default defineConfig({
  integrations: [react()],
  site: 'https://drunkonjava.github.io',
  base: '/HelloWorldGitHub',
  server: {
    host: "localhost",
    port: 3000
  }
});
