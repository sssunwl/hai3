export type Category = 'BEST WOW' | 'BEST VIBE' | 'BEST EASY';

export type Hai3Code = {
  wow: number;
  vibe: number;
  easy: number;
  value: number;
  pick: number;
};

export type Pick = {
  category: Category;
  title: string;
  dateLabel: string;
  reason: string;
  note?: string;
  code: Hai3Code;
};

export type WeekendPost = {
  id: string;
  publishDate: string;
  headline: string;
  window: string;
  subtitle: string;
  note?: string;
  picks: [Pick, Pick, Pick];
};

// HAI3 CODE 仍是設計稿示範分數，正式發文前需由 SS 確認。
const sampleCodes: Record<Category, Hai3Code> = {
  'BEST WOW': { wow: 5, vibe: 4, easy: 3, value: 4, pick: 5 },
  'BEST VIBE': { wow: 4, vibe: 5, easy: 3, value: 4, pick: 5 },
  'BEST EASY': { wow: 3, vibe: 3, easy: 5, value: 4, pick: 4 },
};

const pick = (
  category: Category,
  title: string,
  dateLabel: string,
  reason: string,
  note?: string,
): Pick => ({ category, title, dateLabel, reason, note, code: { ...sampleCodes[category] } });

export const weekendPosts: WeekendPost[] = [
  {
    id: '01',
    publishDate: '2026-09-24',
    headline: '這週末，只選 3 個。',
    window: '9/26—27',
    subtitle: '祭典、音樂、最後一週的嘉年華',
    picks: [
      pick('BEST WOW', '第 49 屆宜野灣羽衣祭', '9/26—27', '宜野灣最大的市民祭，兩天都有。'),
      pick('BEST VIBE', 'コザ・てるりん祭', '9/27', '在 Koza 紀念照屋林助的音樂祭，Koza 本來就是沖繩音樂的街。'),
      pick('BEST EASY', 'SEAPORT CHATAN CARNIVAL', '到 9/26', '北谷海邊，最後一週，順路就能去。'),
    ],
  },
  {
    id: '03',
    publishDate: '2026-10-01',
    headline: '10 月第一個週末，花火還沒結束。',
    window: '10/3—4',
    subtitle: '花火、海、Eisa',
    picks: [
      pick('BEST WOW', '恩納村 ウンナ祭＋美ら海花火大會', '10/3—4', '海邊放花火。'),
      pick('BEST VIBE', 'OCEAN FESTA 読谷 2026', '10/3', '讀谷海邊的海洋祭。'),
      pick('BEST EASY', '宜野灣市青少年 Eisa 祭', '10/3—4', '離那霸、北谷都近，年輕人跳的 Eisa。'),
    ],
  },
  {
    id: '04',
    publishDate: '2026-10-08',
    headline: '三連休，選這 3 個就夠。',
    window: '10/10—12',
    subtitle: '三連休 3 選',
    picks: [
      pick('BEST WOW', '第 56 屆那霸大綱挽', '10/10—12', '世界最大級的拔河，可以下去一起拉。', '大綱挽當天國際通附近交通管制，不要開車進那霸市區。'),
      pick('BEST VIBE', '第 38 屆全島獅子舞祭', '10/10—11', '全沖繩的獅子舞聚在一起。'),
      pick('BEST EASY', '海洋博公園 本部美食祭', '10/10—11', '去水族館順路，吃完就走。'),
    ],
  },
  {
    id: '06',
    publishDate: '2026-10-15',
    headline: '國際通會被一萬人塞滿。',
    window: '10/17—18',
    subtitle: '一萬人的 Eisa、爵士、夏威夷',
    picks: [
      pick('BEST WOW', '一万人のエイサー踊り隊', '10/18', '國際通整條街都在跳。'),
      pick('BEST VIBE', 'Jazz in Nanjo（南城市 20 周年）', '10/17', '南城的爵士夜。'),
      pick('BEST EASY', 'ALOHAISAI 2026', '10/16—18', '三天都有，排不進其他行程也能去。'),
    ],
  },
  {
    id: '07',
    publishDate: '2026-10-22',
    headline: '10 月底，還有花火。',
    window: '10/24—25',
    subtitle: '花火、讀谷祭、點燈開始',
    picks: [
      pick('BEST WOW', '宜野座村祭＋美ら島花火大會', '10/24—25', '秋天的花火。'),
      pick('BEST VIBE', '読谷まつり', '10/23—25', '讀谷祭，同期有 Okinawan Dream 和平音樂會（10/23）。'),
      pick('BEST EASY', '沖縄南国イルミネーション', '10/23 開始', '冬季點燈第一週，晚上去不用排太久。'),
    ],
  },
  {
    id: '09',
    publishDate: '2026-10-29',
    headline: '萬聖節週末，去買一個碗。',
    window: '10/31—11/1',
    subtitle: '陶器市集 × 音樂',
    note: '「萬聖節週末」只是時間點，這 3 個不是萬聖節活動。',
    picks: [
      pick('BEST WOW', '第 21 屆讀谷やちむん＆工藝市', '10/31—11/1', '窯元直接擺攤。'),
      pick('BEST VIBE', 'Mabuioto 17', '10/31—11/1', '音樂活動。'),
      pick('BEST EASY', '壺屋やちむん通り祭', '10/31—11/1', '就在那霸市區，走路就到。'),
    ],
  },
  {
    id: '10',
    publishDate: '2026-11-05',
    headline: '這個週末，沖繩最大聲。',
    window: '11/7—8',
    subtitle: 'MONGOL800 週末',
    picks: [
      pick('BEST WOW', 'MONGOL800 ga-Fest「What a Wonderful World!! 26」', '11/7—8', '沖繩樂團自己辦的音樂祭。'),
      pick('BEST VIBE', 'Tour de Okinawa（看比賽或騎古宇利大橋 42km）', '11/7—8', '會騎車的人可以報名下場。'),
      pick('BEST EASY', '空手之日紀念演武祭', '11/8', '免門票就能看的空手道。'),
    ],
  },
  {
    id: '12',
    publishDate: '2026-11-19',
    headline: '11 月的沖繩，還是很熱鬧。',
    window: '11/21—22',
    subtitle: '森巴、陶器、爵士',
    picks: [
      pick('BEST WOW', '沖縄サンバカーニバル', '11/21—22', '沖繩的森巴嘉年華。'),
      pick('BEST VIBE', 'Na Heart Jazz 爵士月', '11/6—28', '整個月都有場次，挑 21—22 那兩天的。'),
      pick('BEST EASY', '第 47 屆壺屋陶器祭', '11/20—22', '那霸市區，順路。'),
    ],
  },
];

export const getPost = (id: string): WeekendPost | undefined =>
  weekendPosts.find((post) => post.id === id);
