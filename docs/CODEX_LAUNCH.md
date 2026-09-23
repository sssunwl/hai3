# HAI3 網站 v1 上線工單(給 Codex)

> 2026-09-23 起草。目的:先把網站內容做豐富,再把網站內容轉發到 IG/Threads(跟原計畫「先社群後網站」順序相反,是 SS 2026-09-23 改的決定)。

## 範圍(重要:不是全部 12 則都上)

**只做「這週末 3 選」8 則**,來源 `HAI3/docs/PICKS_001-012.md` 的第 01、03、04、06、07、09、10、12 則——這些已經查證過真實活動(日期、地點都對得上)。

**「常青 3 選」4 則(02、05、08、11)先不做頁面。** 原因:[SonaSNS-Platform/brands/OKIDAYZ_HAI3.md](../../SonaSNS-Platform/brands/OKIDAYZ_HAI3.md) L159 紅線「HAI3 只收 SS 實際去過的地方(`visited` 欄位要有日期)」,但這 4 則目前的店名都是佔位符(○○ Cafe、□□ Coffee、△△ 食堂),SS 還沒有真的去過、選定。等 `HAI3/data/places/*.yaml` 有真實地點資料再回來補這批頁面。**不要用佔位店名上線,寧可頁面數量少。**

## Stack

- **Vite + TypeScript,無框架(不用 React)**,比照 `SplitBed/` 的極簡原則——HAI3 v1 沒有表單、沒有互動運算,不需要框架的重量。
- **零後端、零資料庫、零登入**。8 則內容用一份 TS/JSON 常數檔寫死即可,之後要接 OkiDayz 的 `events.json` 自動化再說。
- 部署:**GitHub Actions**(不是舊式「從分支部署」),workflow 直接複製 `SplitBed/.github/workflows/deploy.yml` 或 `han/.github/workflows/deploy.yml` 這兩份(內容幾乎一樣,`actions/deploy-pages` 那套),改 build 產出路徑就好。
- Repo:`sssunwl/hai3`(public),GitHub Pages 網址 `sssunwl.github.io/hai3`。

## 視覺規格

視覺方向定案在這個 Design Artifact(桌機+手機版兩個 artboard,含真的能點的日夜模式切換):
https://claude.ai/artifact/Mct8f59ihJoDZT3YVKzwUo

核心元件,照著做:
- **底色深色為主**(`#0A0A0A`),右上角一顆按鈕可切白天版(`#F5F3EE`)——不是靜態圖,是真的 toggle。
- **頂部 + 分隔處的跑馬燈**:橘色底(強調色 `#FF4D1F`)+ barcode 刻度裝飾 + 文字無限循環滾動(`JUST 3`、「不接受業配排名」等)。
- **Hero 不用置中大標題**:滿版照片(先用深色漸層佔位,之後補真照片)+ 一個旋轉的橡皮章「JUST 3」+ 一張吊牌貼紙貼紙(barcode + ISSUE 001)+ 左側直書小字。**不要**寫「NO TOP 10」「台灣＋香港讀者・20-35歲」這類文字。
- **每張卡片**:貼一張旋轉的紙質吊牌貼紙(白底黑字,不跟著深/淺色主題變)取代扁平標籤,裡面放 `HAI3・01`、`BEST WOW`、一小條 barcode。
- **HAI3 CODE 五維評分**(驚/氛/順/值/推):用**純線條單色 icon**,不要用中文字——icon 圖形參考 Artifact 裡的 SVG(spark/音波/勾勾/鑽石/旗子),顏色跟隨主題色(`{{fg}}`),分數最高那一項用強調色。

字體:Archivo Black(大字)+ Noto Sans TC(中文內文)+ Space Mono(標籤、數字),都走 Google Fonts。

## 內容資料結構(建議)

每則「這週末3選」存一筆,方便以後接 OkiDayz 活動年曆自動化:

```ts
type Pick = {
  category: "BEST WOW" | "BEST VIBE" | "BEST EASY";
  title: string;
  dateLabel: string;      // "9/26—27"
  reason: string;         // "宜野灣最大的市民祭,兩天都有。"
  code: { wow: number; vibe: number; easy: number; value: number; pick: number }; // 1-5
};

type WeekendPost = {
  id: string;             // "01"
  publishDate: string;    // "2026-09-24"
  headline: string;       // "這週末,只選 3 個。"
  window: string;         // "9/26—27"
  subtitle: string;       // "祭典、音樂、最後一週的嘉年華"
  picks: [Pick, Pick, Pick];
};
```

8 則的實際內容(標題、日期、為什麼選它)直接照抄 `HAI3/docs/PICKS_001-012.md`;HAI3 CODE 的五維分數目前沒有定案數字,先用 Artifact 設計稿裡的示範分數佔位,發文前讓 SS confirm 一次。

## 驗收

- 手機(390px)和桌機兩種寬度都要看起來對,參考 Artifact 的兩個 artboard。
- 日夜切換要能用,顏色對比在兩種模式下都要夠(尤其吊牌貼紙、跑馬燈固定用白底黑字,不要跟著主題變色)。
- Top 3 位置不能用錢買、合作要標 PARTNER 這句話要出現在 footer(承襲 BRAND.md 紅線)。
- 8 則發布後,**把每則的畫面截圖/文字轉成 IG 輪播貼文**,這是原本「先社群後網站」的順序倒過來執行——SS 要親自過一次每則貼文的用字。

## 之後(不在這次工單範圍)

- 常青 3 選 4 則,等 `HAI3/data/places/*.yaml` 有 `visited` 真實資料再開新工單。
- 接 OkiDayz `events.json` 自動抓候選活動。
- HAI3 CODE 條碼視覺定案版本(目前是設計稿佔位)。
