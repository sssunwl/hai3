#!/usr/bin/env python3
"""HAI3 品牌素材生成器：HAI3 CODE 條碼、五個簡稱圖形、貼紙、膠帶、盲盒框、票根。

規格見 docs/BRAND.md。輸出到 assets/brand/，改這支再重跑，不要手改 SVG。
HAI3 是 streetwear／潮玩感：幾何、硬邊、黑白＋一個橘紅，不做手繪抖動（那是 OkiDayz 的）。
英文字用 Archivo Black／Space Mono，字型檔在 tools/fonts/（OFL），只嵌進有用到的 SVG，
所以 SVG 當 <img> 用、在 Sona 或 Canva 打開都長一樣。中文字不放進 SVG，交給頁面排。

    python3 tools/brand_assets.py
"""
import base64
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "brand"
FONTS = Path(__file__).resolve().parent / "fonts"

BLACK = "#0a0a0a"
PAPER = "#f5f3ee"
SIGNAL = "#ff4d1f"   # 唯一強調色
SURFACE = "#141414"
MUTED = "#a3a09a"

DISPLAY = "HAI3 Display"  # Archivo Black
MONO = "HAI3 Mono"        # Space Mono Bold
FONT_FILES = {DISPLAY: "ArchivoBlack-latin.woff2", MONO: "SpaceMono-Bold-latin.woff2"}

# 五個簡稱：key、中文、英文、問的是、貼文 emoji。順序就是條碼柱的順序。
AXES = [
    ("wow", "驚", "WOW", "有沒有讓人「哇」的東西", "🤯"),
    ("vibe", "氛", "VIBE", "氣氛、音樂、人", "🪩"),
    ("easy", "順", "EASY", "好不好去、停車、排隊", "🛼"),
    ("value", "值", "VALUE", "花的錢和時間值不值", "🪙"),
    ("pick", "推", "PICK", "SS 個人推不推", "📌"),
]
BLOCKS = "▏▎▌▊█"  # 文字版條碼：分數 1–5，越粗越強
WIDTH = (0.06, 0.14, 0.26, 0.46, 0.82)  # 條碼線寬＝欄寬 × 這個比例（1–5 分）
LABEL_FONT = "PingFang TC, Noto Sans TC, sans-serif"  # SVG 不嵌中文字型，用系統字


# ── 共用 ────────────────────────────────────────────────

def f(n):
    return f"{n:.1f}".rstrip("0").rstrip(".")


def font_css(*families):
    rules = []
    for fam in families:
        data = base64.b64encode((FONTS / FONT_FILES[fam]).read_bytes()).decode()
        rules.append(f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return "<style>" + "".join(rules) + "</style>"


def svg(w, h, body, fonts=()):
    defs = f"<defs>{font_css(*fonts)}</defs>" if fonts else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(w)} {f(h)}" '
            f'width="{f(w)}" height="{f(h)}">{defs}{body}</svg>\n')


def text(x, y, s, size, fam, fill, anchor="start", spacing=0, extra=""):
    ls = f' letter-spacing="{f(spacing)}"' if spacing else ""
    return (f'<text x="{f(x)}" y="{f(y)}" font-family="\'{fam}\'" font-size="{f(size)}" '
            f'fill="{fill}" text-anchor="{anchor}"{ls}{extra}>{s}</text>')


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{fill}"{extra}/>'


def text_code(scores):
    """貼文用的純文字條碼，例：▊█▌▊█  驚4 氛5 順3 值4 推5"""
    return "".join(BLOCKS[s - 1] for s in scores) + "  " + " ".join(f"{a[1]}{s}" for a, s in zip(AXES, scores))


def emoji_line(scores):
    return "  ".join(f"{a[4]}{s}" for a, s in zip(AXES, scores))


# ── HAI3 CODE 條碼 ──────────────────────────────────────
# 一個簡稱＝一條直線，全部一樣高，越粗越強（1 分像髮絲，5 分像磚）。5 條排起來就是條碼。
# 每條線下面寫簡稱＋分數，像真條碼底下的數字，不用猜。「推」是橘紅，整條唯一的顏色。

def code_bars(x, y, scores, fg, slot=44, h=120, label=True, label_size=17, label_fg=None):
    out = ""
    for i, s in enumerate(scores):
        w = slot * WIDTH[s - 1]
        out += rect(x + i * slot + (slot - w) / 2, y, w, h, SIGNAL if i == 4 else fg)
        if label:
            out += text(x + i * slot + slot / 2, y + h + label_size * 1.45, f"{AXES[i][1]}{s}",
                        label_size, LABEL_FONT, label_fg or fg, "middle", extra=' font-weight="700"')
    return out


def barcode(scores, theme="light", label=True):
    fg, bg = (BLACK, PAPER) if theme == "light" else (PAPER, BLACK)
    slot, bar_h, pad = 48, 120, 20
    w = slot * 5 + pad * 2
    h = pad + (30 if label else 0) + bar_h + (44 if label else pad)
    body = rect(0, 0, w, h, bg)
    top = pad + (30 if label else 0)
    if label:
        body += text(pad, pad + 14, "HAI3 CODE", 13, MONO, fg, spacing=2.4)
        body += text(w - pad, pad + 14, "越粗越強", 13, LABEL_FONT, MUTED, "end", extra=' font-weight="700"')
    body += code_bars(pad, top, scores, fg, slot, bar_h, label, 18)
    return svg(w, h, body, (MONO,) if label else ())


def barcode_strip(scores):
    """橫幅：條碼＋HAI3 CODE 大字，放圖卡底部。"""
    h, w = 120, 640
    body = rect(0, 0, w, h, BLACK)
    body += code_bars(24, 16, scores, PAPER, 38, 64, True, 16)
    body += text(24 + 38 * 5 + 30, 62, "HAI3 CODE", 34, DISPLAY, PAPER)
    body += text(24 + 38 * 5 + 30, 92, "越粗越強 · 驚氛順值推", 15, LABEL_FONT, MUTED, extra=' font-weight="700"')
    return svg(w, h, body, (DISPLAY, MONO))


# ── 五個簡稱的自家圖形（圖卡、網站用；emoji 只在貼文文字裡） ──

def glyph_wow(fg):  # 驚：放射短線
    body = ""
    for i in range(12):
        a = 2 * math.pi * i / 12
        r0, r1 = (14, 30) if i % 2 == 0 else (18, 26)
        body += (f'<line x1="{f(32 + r0 * math.cos(a))}" y1="{f(32 + r0 * math.sin(a))}" '
                 f'x2="{f(32 + r1 * math.cos(a))}" y2="{f(32 + r1 * math.sin(a))}" '
                 f'stroke="{fg}" stroke-width="5" stroke-linecap="square"/>')
    return body + f'<circle cx="32" cy="32" r="6" fill="{fg}"/>'


def glyph_vibe(fg):  # 氛：鏡面球格點
    body = f'<clipPath id="ball"><circle cx="32" cy="32" r="24"/></clipPath><g clip-path="url(#ball)">'
    for row in range(7):
        for col in range(7):
            if (row + col) % 2 == 0:
                body += rect(8 + col * 7, 8 + row * 7, 6, 6, fg)
    return body + f'</g><circle cx="32" cy="32" r="25.5" fill="none" stroke="{fg}" stroke-width="3"/>'


def glyph_easy(fg):  # 順：一條平滑到底的箭頭
    return (f'<path d="M8 44 C22 44 26 22 46 22" fill="none" stroke="{fg}" stroke-width="6" '
            f'stroke-linecap="square"/><path d="M40 12 L56 22 L40 32 Z" fill="{fg}"/>')


def glyph_value(fg):  # 值：收據撕邊
    teeth = " ".join(f"L{f(50 - i * 6 - 3)} 59 L{f(50 - (i + 1) * 6)} 54" for i in range(6))
    lines = "".join(rect(20, y, 24 if y != 34 else 14, 4, fg) for y in (16, 25, 34))
    return (f'<path d="M14 6 H50 V54 {teeth} Z" fill="none" stroke="{fg}" stroke-width="4" '
            f'stroke-linejoin="miter"/>{lines}{rect(20, 43, 24, 4, fg)}')


def glyph_pick(_fg):  # 推：實心橘紅圓點，永遠用強調色
    return f'<circle cx="32" cy="32" r="20" fill="{SIGNAL}"/><circle cx="32" cy="32" r="7" fill="{PAPER}"/>'


GLYPHS = {"wow": glyph_wow, "vibe": glyph_vibe, "easy": glyph_easy, "value": glyph_value, "pick": glyph_pick}


# ── 貼紙 slap ───────────────────────────────────────────
# key、字、底色、字色、旋轉、副字（Space Mono 小字）

SLAPS = [
    ("no-top-10", "NO TOP 10.", BLACK, PAPER, -4, "JUST 3."),
    ("just-3", "JUST 3.", SIGNAL, BLACK, 3, "HAI3 · ハイサン"),
    ("best-wow", "BEST WOW", PAPER, BLACK, -2, "1/3"),
    ("best-vibe", "BEST VIBE", BLACK, PAPER, 2, "2/3"),
    ("best-easy", "BEST EASY", PAPER, BLACK, -3, "3/3"),
    ("partner", "PARTNER", PAPER, BLACK, 0, "PAID · 付費合作"),
    ("visited", "VISITED", BLACK, SIGNAL, -5, "SS · 2026.11.07"),
    ("sold-out", "SOLD OUT", SIGNAL, PAPER, -8, "WEEKEND BOX"),
]


def slap(word, bg, fg, rot, sub):
    size = 44
    tw = len(word) * size * 0.78
    w, h = tw + 56, 108
    cw, ch = w + 40, h + 60
    inner = (rect(0, 0, w, h, PAPER, ' rx="6"') +  # die-cut 白邊
             rect(6, 6, w - 12, h - 12, bg, ' rx="3"') +
             text(w / 2, 58, word, size, DISPLAY, fg, "middle") +
             text(w / 2, 86, sub, 13, MONO, fg, "middle", 2.2, ' opacity=".8"'))
    if word == "PARTNER":  # PARTNER 要一眼看出是付費：加粗框，跟推薦卡分開
        inner += rect(6, 6, w - 12, h - 12, "none", f' stroke="{BLACK}" stroke-width="5" stroke-dasharray="10 6"')
    body = (f'<g transform="translate({f(cw / 2)} {f(ch / 2)}) rotate({rot}) translate({f(-w / 2)} {f(-h / 2)})">'
            f'<rect x="5" y="7" width="{f(w)}" height="{f(h)}" rx="6" fill="{BLACK}" opacity=".35"/>{inner}</g>')
    return svg(cw, ch, body, (DISPLAY, MONO))


# ── 警示膠帶 ────────────────────────────────────────────

def tape(msg="TOP 3 IS NOT FOR SALE", w=1080, h=64):
    body = (f'<defs><pattern id="hz" width="36" height="36" patternUnits="userSpaceOnUse" '
            f'patternTransform="rotate(45)">{rect(0, 0, 18, 36, SIGNAL)}{rect(18, 0, 18, 36, BLACK)}</pattern></defs>')
    body += rect(0, 0, w, h, "url(#hz)")
    band_h = 34
    body += rect(0, (h - band_h) / 2, w, band_h, SIGNAL)
    unit = f"{msg}  ✕  "
    body += text(16, h / 2 + 7, (unit * 8).strip(), 19, DISPLAY, BLACK, spacing=1.5)
    return svg(w, h, body, (DISPLAY,))


# ── 盲盒：封面、公仔卡、尾頁（1080×1350，IG 4:5） ────────
# 只畫框和固定字，題目、照片、地點名由輪播工作室或 Sona 頁面疊上去。

W, H = 1080, 1350


def mini_code(x, y, scores, fg, scale=1.0):
    return code_bars(x, y, scores, fg, 40 * scale, 56 * scale, True, 18 * scale)


def box_cover(series="SERIES 01", box="WEEKEND BOX"):
    body = rect(0, 0, W, H, BLACK)
    # 盒子本體＋橘紅硬陰影，微微歪
    body += f'<g transform="rotate(-2 540 700)">'
    body += rect(150, 290, 800, 900, SIGNAL)
    body += rect(120, 260, 800, 900, PAPER, f' stroke="{BLACK}" stroke-width="8"')
    body += f'<path d="M180 260 L150 196 H890 L860 260 Z" fill="#d8d5ce" stroke="{BLACK}" stroke-width="8"/>'
    body += text(160, 320, f"HAI3 · {series}", 22, MONO, BLACK, spacing=4)
    body += text(880, 320, "OKINAWA", 22, MONO, BLACK, "end", 4)
    body += rect(160, 340, 720, 4, BLACK)
    # 題目留白區（虛線框，成品會被蓋掉）
    body += rect(160, 380, 720, 420, "none", f' stroke="{MUTED}" stroke-width="3" stroke-dasharray="14 10"')
    body += text(520, 600, "TITLE AREA", 26, MONO, MUTED, "middle", 4)
    # 3 個公仔窗
    for i in range(3):
        x = 160 + i * 248
        body += rect(x, 840, 224, 200, "none", f' stroke="{BLACK}" stroke-width="5" stroke-dasharray="16 10"')
        body += text(x + 112, 965, str(i + 1), 110, DISPLAY, BLACK, "middle")
        body += text(x + 112, 1025, ("WOW", "VIBE", "EASY")[i], 18, MONO, BLACK, "middle", 3)
    body += rect(160, 1070, 720, 4, BLACK)
    body += text(160, 1120, f"{box} · 3 FIGURES INSIDE", 22, MONO, BLACK, spacing=3)
    body += mini_code(720, 1082, [4, 5, 3, 4, 5], BLACK, 0.8)
    body += "</g>"
    body += text(540, 1290, "NO TOP 10. JUST 3.", 30, DISPLAY, PAPER, "middle", 2)
    return svg(W, H, body, (DISPLAY, MONO))


def figure_card(n):
    kind = ("BEST WOW", "BEST VIBE", "BEST EASY")[n - 1]
    body = rect(0, 0, W, H, PAPER)
    body += rect(48, 48, W - 96, H - 96, "none", f' stroke="{BLACK}" stroke-width="6"')
    body += rect(48, 48, W - 96, 96, BLACK)
    body += text(84, 112, kind, 44, DISPLAY, PAPER)
    body += text(W - 84, 112, f"{n}/3", 40, DISPLAY, SIGNAL, "end")
    # 照片區
    body += rect(84, 180, W - 168, 700, "#d8d5ce")
    body += text(540, 545, "PHOTO", 30, MONO, MUTED, "middle", 6)
    # 名稱／理由留白、條碼
    body += rect(84, 920, W - 168, 4, BLACK)
    body += text(84, 970, "NAME · AREA · DATE", 22, MONO, MUTED, spacing=3)
    body += rect(84, 1180, W - 168, 4, BLACK)
    body += text(84, 1236, "HAI3 CODE", 24, MONO, BLACK, spacing=4)
    body += text(84, 1272, "越粗越強", 20, LABEL_FONT, MUTED, extra=' font-weight="700"')
    body += mini_code(W - 84 - 240, 1192, [4, 5, 3, 4, 5], BLACK, 1.2)
    return svg(W, H, body, (DISPLAY, MONO))


def end_page(series="SERIES 01"):
    body = rect(0, 0, W, H, PAPER)
    body += text(96, 170, f"{series} · COMPLETE", 26, MONO, BLACK, spacing=4)
    body += rect(96, 196, 888, 6, BLACK)
    # 大字由頁面排中文（「3 個，就夠了。」），這裡留位置
    body += rect(96, 260, 888, 420, "none", f' stroke="{MUTED}" stroke-width="3" stroke-dasharray="14 10"')
    body += text(540, 480, "SAVE · 收藏 COPY AREA", 24, MONO, MUTED, "middle", 4)
    for i in range(3):  # 三個公仔全亮＝這一盒收集完成
        x = 96 + i * 304
        body += rect(x, 760, 280, 340, BLACK)
        body += text(x + 140, 990, str(i + 1), 200, DISPLAY, PAPER, "middle")
        body += text(x + 140, 1070, ("WOW", "VIBE", "EASY")[i], 22, MONO, SIGNAL, "middle", 4)
    body += text(96, 1200, "FOLLOW @hai3", 40, DISPLAY, BLACK)
    body += text(984, 1200, "EVERY THU", 22, MONO, BLACK, "end", 3)
    return svg(W, H, body, (DISPLAY, MONO))


# ── 票根（3 DROPS 用） ───────────────────────────────────

def ticket():
    w, h = 900, 320
    notch = "".join(f'<circle cx="640" cy="{y}" r="5" fill="{BLACK}"/>' for y in range(34, 300, 22))
    body = (f'<path d="M0 0 H{w} V{h / 2 - 26} A26 26 0 0 0 {w} {h / 2 + 26} V{h} H0 V{h / 2 + 26} '
            f'A26 26 0 0 0 0 {h / 2 - 26} Z" fill="{PAPER}"/>')
    body += notch
    body += rect(0, 0, 640, 64, BLACK)
    body += text(32, 44, "HAI3 · 3 DROPS", 26, DISPLAY, PAPER)
    body += text(608, 44, "TICKET", 18, MONO, SIGNAL, "end", 4)
    for i, lab in enumerate(("EVENT", "ON SALE", "PRICE")):
        y = 116 + i * 66
        body += text(32, y, lab, 15, MONO, MUTED, spacing=3)
        body += rect(32, y + 16, 576, 3, BLACK)
    body += text(770, 140, "DROP", 30, DISPLAY, BLACK, "middle")
    body += text(770, 200, "01", 66, DISPLAY, SIGNAL, "middle")
    body += mini_code(694, 232, [4, 5, 3, 4, 5], BLACK, 0.7)
    return svg(w, h, body, (DISPLAY, MONO))


# ── 總覽頁 ──────────────────────────────────────────────

SAMPLES = [("sample-45345", [4, 5, 3, 4, 5]), ("sample-53254", [5, 3, 2, 5, 4]), ("sample-34555", [3, 4, 5, 5, 5])]


def preview_html():
    def fig(src, cap, h=96, cls=""):
        return f'<figure class="{cls}"><img src="{src}" alt="" style="height:{h}px"><figcaption>{cap}</figcaption></figure>'

    axes = "".join(
        f'<tr><td><b>{zh}</b> {en}</td><td>{q}</td><td class="emo">{emo}</td>'
        f'<td><img src="glyphs/{k}-dark.svg" alt="" class="gl"><img src="glyphs/{k}-light.svg" alt="" class="gl lt"></td></tr>'
        for k, zh, en, q, emo in AXES)
    codes = "".join(fig(f"code/{k}-light.svg", f"{k[7:]} · light", 170) + fig(f"code/{k}-dark.svg", "dark", 170)
                    for k, _ in SAMPLES[:1])
    codes += "".join(fig(f"code/{k}-light.svg", k[7:], 170) for k, _ in SAMPLES[1:])
    slaps = "".join(fig(f"slaps/{k}.svg", k, 110) for k, *_ in SLAPS)
    txt = "\n".join(f"HAI3 CODE  {text_code(s)}\n{emoji_line(s)}\n" for _, s in SAMPLES)
    return f"""<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HAI3 素材 KIT</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Noto+Sans+TC:wght@400;700;900&family=Space+Mono:wght@700&display=swap');
:root{{--bg:{BLACK};--fg:{PAPER};--accent:{SIGNAL};--muted:{MUTED};--line:#393837}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:'Noto Sans TC',sans-serif;padding:32px 16px 60px}}
main{{max-width:1040px;margin:0 auto}}
h1{{font:400 clamp(40px,10vw,72px)/.95 'Archivo Black',sans-serif;margin:0 0 8px}}
h1 b{{color:var(--accent);font-weight:400}}
h2{{font:400 26px 'Archivo Black',sans-serif;margin:44px 0 12px}}
h2 small{{font:900 15px 'Noto Sans TC';color:var(--muted);margin-left:8px}}
p.note{{margin:0;color:var(--muted);font-size:14px}}
.grid{{display:flex;flex-wrap:wrap;gap:18px;align-items:end}}
figure{{margin:0}} figure img{{display:block;max-width:100%;width:auto}}
figcaption{{font:700 11px 'Space Mono',monospace;color:var(--muted);margin-top:6px;letter-spacing:.08em}}
.big img{{height:auto!important;width:100%}} .big{{flex:1 1 280px;max-width:340px}}
table{{border-collapse:collapse;width:100%;font-size:14px}}
td,th{{border-bottom:1px solid var(--line);padding:10px;text-align:left;vertical-align:middle}}
th{{font:700 11px 'Space Mono',monospace;color:var(--muted);letter-spacing:.12em}}
td b{{font-size:20px;margin-right:4px}} .emo{{font-size:26px}}
.gl{{height:40px;display:inline-block;margin-right:8px}} .lt{{background:var(--fg)}}
pre{{background:#141414;border:1.5px solid var(--line);padding:16px;font:15px/1.6 'Space Mono',monospace;overflow-x:auto}}
.tape img{{width:100%;height:auto}}
</style></head><body><main>
<h1>HAI3 <b>KIT</b></h1>
<p class="note">由 tools/brand_assets.py 生成，改生成器再重跑。圖卡、網站用這裡的圖形；emoji 只在貼文文字裡用。</p>
<h2>HAI3 CODE<small>條碼：一個簡稱一條線，一樣高，越粗越強；線下寫簡稱＋分數，「推」是橘紅</small></h2>
<div class="grid">{codes}</div>
<div class="grid" style="margin-top:18px">{fig("code/strip-45345.svg", "strip · 圖卡底部橫幅", 72)}</div>
<h2>5 AXES<small>簡稱 × emoji × 自家圖形</small></h2>
<table><tr><th>簡稱</th><th>問的是</th><th>貼文 emoji</th><th>圖形 dark／light</th></tr>{axes}</table>
<h2>TEXT CODE<small>貼文用的純文字條碼（code.json 有同一份對照）</small></h2>
<pre>{txt}</pre>
<h2>SLAPS<small>貼紙</small></h2>
<div class="grid">{slaps}</div>
<h2>TAPE<small>警示膠帶</small></h2>
<div class="tape"><img src="tape/not-for-sale.svg" alt=""></div>
<h2>BOX<small>盲盒輪播框：封面／公仔卡 1–3／尾頁（虛線區由工作室疊字和照片）</small></h2>
<div class="grid">{fig("box/cover.svg", "cover", cls="big")}{fig("box/card-1.svg", "card 1/3", cls="big")}{fig("box/end.svg", "end", cls="big")}</div>
<h2>TICKET<small>3 DROPS 票根</small></h2>
<div class="grid">{fig("ticket/drop.svg", "drop", 160)}</div>
</main></body></html>
"""


def main():
    for sub in ("code", "glyphs", "slaps", "tape", "box", "ticket"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)
    for key, scores in SAMPLES:
        (OUT / "code" / f"{key}-light.svg").write_text(barcode(scores, "light"), encoding="utf-8")
        (OUT / "code" / f"{key}-dark.svg").write_text(barcode(scores, "dark"), encoding="utf-8")
    (OUT / "code" / "strip-45345.svg").write_text(barcode_strip([4, 5, 3, 4, 5]), encoding="utf-8")
    for key, fn in GLYPHS.items():
        for theme, fg in (("dark", PAPER), ("light", BLACK)):
            (OUT / "glyphs" / f"{key}-{theme}.svg").write_text(svg(64, 64, fn(fg)), encoding="utf-8")
    for key, word, bg, fg, rot, sub in SLAPS:
        (OUT / "slaps" / f"{key}.svg").write_text(slap(word, bg, fg, rot, sub), encoding="utf-8")
    (OUT / "tape" / "not-for-sale.svg").write_text(tape(), encoding="utf-8")
    (OUT / "box" / "cover.svg").write_text(box_cover(), encoding="utf-8")
    for n in (1, 2, 3):
        (OUT / "box" / f"card-{n}.svg").write_text(figure_card(n), encoding="utf-8")
    (OUT / "box" / "end.svg").write_text(end_page(), encoding="utf-8")
    (OUT / "ticket" / "drop.svg").write_text(ticket(), encoding="utf-8")
    # 給 Sona 發文台、起草規則讀的對照表
    code = {
        "axes": [{"key": k, "zh": zh, "en": en, "question": q, "emoji": e} for k, zh, en, q, e in AXES],
        "best": {"WOW": "🤯", "VIBE": "🪩", "EASY": "🛼"},
        "blocks": BLOCKS,
        "example": {"scores": [4, 5, 3, 4, 5], "text": text_code([4, 5, 3, 4, 5]), "emoji": emoji_line([4, 5, 3, 4, 5])},
    }
    (OUT / "code.json").write_text(json.dumps(code, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "index.html").write_text(preview_html(), encoding="utf-8")
    n = sum(1 for _ in OUT.rglob("*.svg"))
    print(f"{n} 個 SVG＋code.json → {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
