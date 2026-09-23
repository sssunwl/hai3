import './style.css';

import { getPost, weekendPosts, type Hai3Code, type Pick, type WeekendPost } from './data';

const app = document.querySelector<HTMLDivElement>('#app');

if (!app) {
  throw new Error('Missing #app');
}

const base = import.meta.env.BASE_URL;
const iconPaths: Record<keyof Hai3Code, string> = {
  wow: '<path d="m10 1 1.7 6.3L18 5.5l-4.6 4.6 4.6 4.6-6.3-1.8L10 19l-1.7-6.1L2 14.7l4.6-4.6L2 5.5l6.3 1.8L10 1Z"/>',
  vibe: '<path d="M2 10h2m2-5v10m4-13v16m4-12v8m4-4h2"/>',
  easy: '<path d="m2 10 5 5L18 4"/><path d="m8 10 3 3 7-7" opacity=".45"/>',
  value: '<path d="m10 2 7 6-7 10L3 8l7-6Z"/><path d="M3 8h14M7 8l3 10 3-10-3-6-3 6Z"/>',
  pick: '<path d="M4 19V2m1 1h11l-3 4 3 4H5"/>',
};
const codeNames: Record<keyof Hai3Code, string> = {
  wow: '驚', vibe: '氛', easy: '順', value: '值', pick: '推',
};

const barcode = (compact = false): string => {
  const widths = compact ? [1, 2, 1, 3, 1, 1, 2, 3, 1, 2, 1, 1] : [2, 1, 3, 1, 2, 4, 1, 3, 2, 1, 4, 1, 2, 3, 1, 1, 3];
  return `<span class="barcode" aria-hidden="true">${widths.map((width) => `<i style="--bar:${width}"></i>`).join('')}</span>`;
};

const logo = (): string => `<a class="logo" href="${base}" aria-label="HAI3 首頁"><strong>HAI3</strong><span>ハイサン</span></a>`;

const themeButton = (): string => `
  <button class="theme-toggle" type="button" aria-label="切換日夜模式" aria-pressed="false">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/><circle cx="12" cy="12" r="4"/></svg>
    <span>NIGHT</span>
  </button>`;

const ticker = (variant = ''): string => {
  const line = `${barcode(true)}<span>JUST 3</span><b>不接受業配排名</b>${barcode(true)}<span>這週末 3 選</span><b>HAI3 CODE</b>`;
  return `<div class="ticker ${variant}" aria-label="JUST 3・不接受業配排名・這週末 3 選・HAI3 CODE"><div class="ticker-track">${line}${line}${line}</div></div>`;
};

const header = (): string => `
  ${ticker('ticker-top')}
  <header class="site-header">
    ${logo()}
    <nav aria-label="主要導覽">
      <a href="${base}#issues">這週末 3 選</a>
      <a href="${base}#code">HAI3 CODE</a>
    </nav>
    ${themeButton()}
  </header>`;

const codeChart = (code: Hai3Code): string => {
  const entries = Object.entries(code) as [keyof Hai3Code, number][];
  const highest = Math.max(...entries.map(([, score]) => score));
  return `<div class="code-chart" aria-label="HAI3 CODE 示範評分">
    ${entries.map(([key, score]) => `
      <div class="code-metric${score === highest ? ' is-high' : ''}" title="${codeNames[key]} ${score} 分">
        <svg viewBox="0 0 20 20" aria-hidden="true">${iconPaths[key]}</svg>
        <span class="score-bars" aria-hidden="true">${Array.from({ length: 5 }, (_, index) => `<i class="${index < score ? 'on' : ''}"></i>`).join('')}</span>
        <span class="sr-only">${codeNames[key]} ${score} 分</span>
      </div>`).join('')}
  </div>`;
};

const pickCard = (pick: Pick, postId: string, index: number): string => `
  <article class="pick-card pick-card-${index + 1}">
    <div class="card-visual" aria-hidden="true"><span>${String(index + 1).padStart(2, '0')}</span></div>
    <div class="paper-tag tag-${index + 1}">
      <small>HAI3・${postId}</small>
      <strong>${pick.category}</strong>
      ${barcode(true)}
    </div>
    <div class="card-body">
      <p class="date-label">${pick.dateLabel}</p>
      <h3>${pick.title}</h3>
      <p class="reason">${pick.reason}</p>
      ${pick.note ? `<p class="pick-note">→ ${pick.note}</p>` : ''}
      ${codeChart(pick.code)}
    </div>
  </article>`;

const issueSection = (post: WeekendPost, headingLevel = 'h2'): string => {
  const H = headingLevel;
  return `<section class="issue" id="issue-${post.id}">
    <div class="issue-heading">
      <p class="eyebrow">ISSUE ${post.id}・${post.publishDate.replaceAll('-', '.')}</p>
      <${H}>${post.headline}</${H}>
      <div class="issue-meta"><strong>${post.window}</strong><span>${post.subtitle}</span></div>
      ${post.note ? `<p class="issue-note">${post.note}</p>` : ''}
    </div>
    <div class="pick-grid">${post.picks.map((item, index) => pickCard(item, post.id, index)).join('')}</div>
    <p class="score-disclaimer">HAI3 CODE 為 Claude 依公開資訊給的初稿評分・正式發文前由 SS 確認</p>
  </section>`;
};

const footer = (): string => `
  <footer>
    <div>${logo()}<p>沖繩，只選 3 個。</p></div>
    <p class="partner-rule">Top 3 位置不能用錢買。<br />合作內容一律標 <strong>PARTNER</strong>。</p>
    <p class="footer-meta">HAI3<br />OKINAWA・2026</p>
  </footer>`;

const archiveCards = (): string => weekendPosts.map((post) => `
  <a class="archive-card" href="${base}posts/${post.id}/">
    <div><span>ISSUE ${post.id}</span><time datetime="${post.publishDate}">${post.publishDate.replaceAll('-', '.')}</time></div>
    <strong>${post.window}</strong>
    <h3>${post.headline}</h3>
    <p>${post.subtitle}</p>
    <span class="arrow" aria-hidden="true">↗</span>
  </a>`).join('');

const home = (): string => `
  ${header()}
  <main id="main">
    <section class="hero">
      <p class="vertical-copy">沖繩　只選　3　個</p>
      <div class="stamp" aria-label="JUST 3"><span>JUST</span><strong>3</strong></div>
      <div class="hero-tag">${barcode()}<span>ISSUE 001—012</span><strong>THIS WEEKEND</strong></div>
      <div class="hero-caption"><p>沖繩，只選 3 個。</p><span>JUST 3.</span></div>
    </section>
    ${ticker('ticker-divider')}
    <section class="archive" id="issues">
      <div class="section-intro"><p>每週四發・8 ISSUES</p><h1>這週末<br /><em>3</em> 選</h1><span>選擇少一點。<br />直接出發。</span></div>
      <div class="archive-grid">${archiveCards()}</div>
    </section>
    ${ticker('ticker-divider ticker-reverse')}
    <section class="code-explainer" id="code">
      <div><p class="eyebrow">OUR SYSTEM</p><h2>HAI3<br />CODE</h2></div>
      <div class="code-copy"><p>五個角度，一眼看懂。不是排名，是我們選它的理由。</p>${codeChart({ wow: 5, vibe: 4, easy: 3, value: 4, pick: 5 })}<small>示範用圖・每則實際分數見各期內文</small></div>
    </section>
  </main>
  ${footer()}`;

const postPage = (post: WeekendPost): string => {
  const currentIndex = weekendPosts.findIndex((item) => item.id === post.id);
  const previous = weekendPosts[(currentIndex - 1 + weekendPosts.length) % weekendPosts.length];
  const next = weekendPosts[(currentIndex + 1) % weekendPosts.length];
  return `
    ${header()}
    <main id="main">
      <section class="post-hero">
        <a class="back-link" href="${base}#issues">← ALL ISSUES</a>
        <p class="vertical-copy">沖繩　只選　3　個</p>
        <div class="post-number">${post.id}</div>
        <div class="stamp small" aria-label="JUST 3"><span>JUST</span><strong>3</strong></div>
        <div class="hero-tag">${barcode()}<span>ISSUE ${post.id}</span><strong>${post.window}</strong></div>
        <div class="post-hero-copy"><p>${post.window}</p><h1>${post.headline}</h1><span>${post.subtitle}</span></div>
      </section>
      ${ticker('ticker-divider')}
      ${issueSection(post, 'h2')}
      <nav class="issue-nav" aria-label="期數導覽">
        <a href="${base}posts/${previous.id}/"><span>← PREV</span><strong>ISSUE ${previous.id}</strong></a>
        <a href="${base}posts/${next.id}/"><span>NEXT →</span><strong>ISSUE ${next.id}</strong></a>
      </nav>
    </main>
    ${footer()}`;
};

const requestedPost = document.body.dataset.postId;
const post = requestedPost ? getPost(requestedPost) : undefined;
app.innerHTML = requestedPost && post ? postPage(post) : home();

const storedTheme = localStorage.getItem('hai3-theme');
if (storedTheme === 'light') {
  document.documentElement.dataset.theme = 'light';
}

const toggle = document.querySelector<HTMLButtonElement>('.theme-toggle');
const themeMeta = document.querySelector<HTMLMetaElement>('meta[name="theme-color"]');

const syncTheme = (): void => {
  const isLight = document.documentElement.dataset.theme === 'light';
  if (toggle) {
    toggle.setAttribute('aria-pressed', String(isLight));
    const label = toggle.querySelector('span');
    if (label) label.textContent = isLight ? 'DAY' : 'NIGHT';
  }
  themeMeta?.setAttribute('content', isLight ? '#f5f3ee' : '#0a0a0a');
};

toggle?.addEventListener('click', () => {
  const isLight = document.documentElement.dataset.theme === 'light';
  document.documentElement.dataset.theme = isLight ? 'dark' : 'light';
  localStorage.setItem('hai3-theme', isLight ? 'dark' : 'light');
  syncTheme();
});

syncTheme();
