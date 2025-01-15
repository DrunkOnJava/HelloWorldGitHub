import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";
import react from "@astrojs/react";

// https://astro.build/config
export default defineConfig({
  integrations: [tailwind(), react()],
  site: "https://drunkonjava.github.io",
  base: "/HelloWorldGitHub",
  build: {
    assets: "_assets",
  },
  vite: {
    ssr: {
      external: ["svgo"],
    },
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("/src/pages/compounds/") || id.includes("/src/components/Compound")) {
            return "compound-modules";
          }
        },
      },
    },
  },
});
