# HAI3（ハイサン）

沖繩，只選 3 個。No Top 10. Just 3.

2026-09-21 開。潮一點的沖繩精選平台：每個主題只給 3 個選擇，少看、快選、直接出發。
姊妹品牌 **OkiDayz**（`../okidayz/`）負責「今天在沖繩做什麼」的工具和資訊；HAI3 負責「去哪間最值得」的策展。

- 品牌定案：`docs/BRAND.md`
- 雙品牌分工、共同管理、收入：`../SonaSNS-Platform/brands/OKIDAYZ_HAI3.md`

現階段：網站 v1 先發布 8 則已查證的「這週末 3 選」，再把網站內容轉成 IG／Threads。4 則常青地點要等 `visited` 有真實日期後才上，不使用佔位店名。

## 本機開發

```sh
npm install
npm run dev
```

網站以 Vite + TypeScript 製作，GitHub Actions 在 `main` 更新後部署到 GitHub Pages。
