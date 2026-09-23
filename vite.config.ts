import { resolve } from 'node:path';

import { defineConfig } from 'vite';

const postIds = ['01', '03', '04', '06', '07', '09', '10', '12'];

export default defineConfig({
  base: '/hai3/',
  build: {
    rollupOptions: {
      input: {
        main: resolve(import.meta.dirname, 'index.html'),
        ...Object.fromEntries(
          postIds.map((id) => [
            `post-${id}`,
            resolve(import.meta.dirname, `posts/${id}/index.html`),
          ]),
        ),
      },
    },
  },
});
