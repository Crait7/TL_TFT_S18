# -*- coding: utf-8 -*-
"""Rebuild S18羁绊天梯 with MiMo-like B/W chrome + author footer."""
from pathlib import Path

src = Path(r"E:\mimo\projects\.mimo-sessions\2026-09-20\帮我调研现版本云顶之奕棋子的羁绊分布情况，在最多10个棋子+1个花仙子转职的情况\云顶之弈Set18羁绊最优化工具.html")
old = src.read_text(encoding="utf-8")
js = old.split("<script>", 1)[1].rsplit("</script>", 1)[0]

chrome = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>S18羁绊天梯 · Crait7</title>
<style>
  :root{
    --bg:#000;--ink:#fff;--muted:#8a8a8a;--line:#222;--panel:#0a0a0a;--panel2:#141414;
    --ok:#fff;--gold:#fff;--accent:#fff;--dim:#555;
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{
    font-family:"Segoe UI","PingFang SC","Microsoft YaHei",system-ui,sans-serif;
    background:#000;color:#fff;line-height:1.5;overflow-x:hidden;
    -webkit-font-smoothing:antialiased;
  }
  a{color:#fff;text-decoration:none}

  /* —— 跑马灯底纹（MiMo 风） —— */
  .mq{
    position:fixed;left:0;width:200%;pointer-events:none;z-index:0;
    font-weight:800;letter-spacing:.35em;white-space:nowrap;
    color:#fff;opacity:.045;font-size:clamp(28px,6vw,64px);
    user-select:none;
  }
  .mq.a{top:8vh;animation:slide 48s linear infinite}
  .mq.b{top:38vh;animation:slide 62s linear infinite reverse}
  .mq.c{top:68vh;animation:slide 40s linear infinite}
  @keyframes slide{from{transform:translateX(0)}to{transform:translateX(-50%)}}

  .wrap{position:relative;z-index:1;max-width:1120px;margin:0 auto;padding:28px 18px 120px}

  /* —— 顶栏 —— */
  .hero{margin-bottom:28px}
  .kicker{
    font-size:11px;letter-spacing:.4em;color:var(--muted);text-transform:uppercase;
    margin-bottom:12px;
  }
  .kicker span{display:inline-block;animation:pulse 2.4s ease-in-out infinite}
  @keyframes pulse{0%,100%{opacity:.45}50%{opacity:1}}
  h1{
    margin:0;font-size:clamp(36px,8vw,64px);font-weight:900;letter-spacing:-.03em;line-height:1;
  }
  h1 .line2{display:block;color:var(--muted);font-weight:700;font-size:.42em;letter-spacing:.2em;margin-top:10px}
  .hero-sub{margin-top:14px;color:var(--muted);font-size:13px;max-width:520px}
  .hero-sub a{border-bottom:1px solid #333}
  .hero-sub a:hover{border-color:#fff}

  /* —— 面板 —— */
  .grid{display:grid;grid-template-columns:300px 1fr;gap:18px}
  @media(max-width:920px){.grid{grid-template-columns:1fr}}
  .card{
    background:rgba(255,255,255,.03);
    border:1px solid var(--line);
    border-radius:16px;padding:18px 18px 20px;
    backdrop-filter:blur(8px);
    transition:border-color .25s, transform .25s, background .25s;
  }
  .card:hover{border-color:#444}
  .card h2{
    margin:0 0 14px;font-size:12px;font-weight:700;letter-spacing:.22em;
    color:var(--muted);text-transform:uppercase;
  }
  label{display:block;font-size:12px;color:var(--muted);margin:12px 0 6px;letter-spacing:.06em}
  select,input[type=number]{
    width:100%;background:#0d0d0d;color:#fff;border:1px solid #2a2a2a;
    border-radius:10px;padding:10px 12px;font-size:14px;outline:none;
    transition:border-color .2s,box-shadow .2s;
  }
  select:focus,input[type=number]:focus{border-color:#fff;box-shadow:0 0 0 3px rgba(255,255,255,.08)}
  .hint{font-size:11px;color:var(--dim);margin-top:6px}
  .checks{display:flex;flex-direction:column;gap:8px;margin-top:10px}
  .checks label{
    display:flex;align-items:center;gap:10px;margin:0;color:#ddd;font-size:13px;cursor:pointer;
  }
  .checks input{width:auto;accent-color:#fff}
  .emblem-box{margin-top:8px;padding:10px;background:#0d0d0d;border-radius:10px;max-height:170px;overflow:auto;border:1px solid #1c1c1c}
  .emblem-box .g2{display:grid;grid-template-columns:1fr 1fr;gap:6px 10px}
  .emblem-box label{margin:0;font-size:12px;color:#ddd;display:flex;gap:6px;align-items:center;cursor:pointer}

  button.run{
    width:100%;margin-top:18px;background:#fff;color:#000;border:none;
    border-radius:999px;padding:14px;font-size:14px;font-weight:800;letter-spacing:.12em;
    cursor:pointer;position:relative;overflow:hidden;
    transition:transform .2s,letter-spacing .25s,box-shadow .25s;
  }
  button.run:hover{transform:translateY(-2px);letter-spacing:.2em;box-shadow:0 10px 40px rgba(255,255,255,.15)}
  button.run:active{transform:translateY(0)}
  button.run:disabled{opacity:.45;cursor:wait;transform:none}
  button.run::after{
    content:"";position:absolute;inset:0;background:linear-gradient(120deg,transparent,rgba(0,0,0,.08),transparent);
    transform:translateX(-100%);
  }
  button.run:hover::after{animation:shine .7s ease}
  @keyframes shine{to{transform:translateX(100%)}}
  .status{margin-top:12px;font-size:12px;color:var(--muted);min-height:18px;font-variant-numeric:tabular-nums}

  /* —— 结果 —— */
  .result-head{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;margin-bottom:16px}
  .big{
    font-size:clamp(48px,10vw,72px);font-weight:900;line-height:.9;letter-spacing:-.04em;
    background:linear-gradient(180deg,#fff 30%,#666);-webkit-background-clip:text;background-clip:text;color:transparent;
  }
  .meta{font-size:13px;color:var(--muted)}
  .meta b{color:#fff;font-weight:600}
  table{width:100%;border-collapse:collapse;font-size:13px}
  th,td{text-align:left;padding:8px 8px;border-bottom:1px solid #1a1a1a;vertical-align:middle}
  th{color:var(--dim);font-weight:500;font-size:11px;letter-spacing:.08em}
  .tag{
    display:inline-block;padding:2px 8px;border-radius:999px;font-size:11px;
    border:1px solid #333;color:#ccc;margin:2px 3px 2px 0;
    transition:border-color .2s,color .2s,background .2s;
  }
  .tag:hover{border-color:#fff;color:#fff}
  .tag.ok{border-color:#fff;color:#fff;background:rgba(255,255,255,.08)}
  .tag.em{border-color:#aaa;color:#fff;background:rgba(255,255,255,.04)}
  .tag.lux{border-color:#666;color:#fff}
  .tag.bad{border-color:#666;color:#888}
  .avatar{
    width:40px;height:40px;border-radius:10px;object-fit:cover;background:#111;
    border:1px solid #2a2a2a;display:block;transition:transform .25s,border-color .25s;
  }
  .avatar:hover{transform:scale(1.08) rotate(-2deg);border-color:#fff}
  .avatar.lux{border-color:#fff}
  .unit-cell{display:flex;gap:10px;align-items:center}
  .unit-cell .name{font-weight:600}
  .unit-cell .en{color:var(--dim);font-size:11px}
  .empty{color:var(--muted);font-size:13px;padding:28px 0;text-align:center}
  .note{font-size:12px;color:var(--dim);margin-top:14px;line-height:1.7}
  .split{display:grid;grid-template-columns:1.1fr .9fr;gap:16px}
  @media(max-width:700px){.split{grid-template-columns:1fr}}
  h3{font-size:11px;margin:0 0 8px;color:var(--muted);font-weight:600;letter-spacing:.16em;text-transform:uppercase}
  .src{font-size:11px;color:var(--dim)}
  .src a{border-bottom:1px solid #333}

  /* 结果入场 */
  .fade-in{animation:fadeUp .45s ease both}
  @keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}

  /* —— 作者页脚（新颖卡片） —— */
  .author{
    position:relative;z-index:1;margin-top:56px;
  }
  .author-band{
    position:relative;border-top:1px solid var(--line);padding-top:36px;
  }
  .author-label{
    font-size:11px;letter-spacing:.35em;color:var(--dim);margin-bottom:18px;text-align:center;
  }
  .author-card{
    max-width:420px;margin:0 auto;
    background:#050505;border:1px solid #222;border-radius:20px;
    padding:22px 22px 20px;
    display:flex;gap:16px;align-items:center;
    transition:transform .35s cubic-bezier(.2,.8,.2,1),border-color .3s,box-shadow .3s;
  }
  .author-card:hover{
    transform:translateY(-6px) scale(1.02);
    border-color:#fff;
    box-shadow:0 20px 60px rgba(255,255,255,.08);
  }
  .author-ava-wrap{position:relative;flex-shrink:0}
  .author-ava-wrap::before{
    content:"";position:absolute;inset:-6px;border-radius:50%;
    border:1px dashed rgba(255,255,255,.35);
    animation:spin 12s linear infinite;
  }
  @keyframes spin{to{transform:rotate(360deg)}}
  .author-ava{
    width:72px;height:72px;border-radius:50%;object-fit:cover;
    border:2px solid #fff;display:block;background:#111;
  }
  .author-info{min-width:0}
  .author-name{font-size:20px;font-weight:800;letter-spacing:.04em}
  .author-name .dot{
    display:inline-block;width:6px;height:6px;border-radius:50%;background:#fff;
    margin-left:8px;vertical-align:middle;animation:pulse 1.6s ease-in-out infinite;
  }
  .author-role{font-size:12px;color:var(--muted);margin-top:4px;letter-spacing:.08em}
  .author-links{margin-top:12px;display:flex;gap:10px;flex-wrap:wrap}
  .chip{
    display:inline-flex;align-items:center;gap:6px;
    padding:6px 12px;border-radius:999px;border:1px solid #333;
    font-size:12px;color:#ddd;transition:all .2s;
  }
  .chip:hover{border-color:#fff;color:#fff;background:rgba(255,255,255,.06)}
  .chip svg{width:14px;height:14px;fill:currentColor}
  .author-foot{
    margin-top:22px;text-align:center;font-size:11px;color:var(--dim);letter-spacing:.12em;
  }
  .author-foot .mq-mini{
    margin-top:10px;font-weight:800;letter-spacing:.4em;color:#222;font-size:12px;
  }
</style>
</head>
<body>
  <div class="mq a">S18 TRAIT LADDER S18 TRAIT LADDER S18 TRAIT LADDER S18 TRAIT LADDER S18 TRAIT LADDER </div>
  <div class="mq b">CRAIT7 CRAIT7 CRAIT7 CRAIT7 CRAIT7 CRAIT7 CRAIT7 CRAIT7 CRAIT7 CRAIT7 CRAIT7 CRAIT7 </div>
  <div class="mq c">羁绊天梯 羁绊天梯 羁绊天梯 羁绊天梯 羁绊天梯 羁绊天梯 羁绊天梯 羁绊天梯 羁绊天梯 羁绊天梯 </div>

<div class="wrap">
  <header class="hero">
    <div class="kicker"><span>TEAMFIGHT TACTICS</span> · SET 18 · ENCHANTED WILDS</div>
    <h1>S18羁绊天梯<span class="line2">TRAIT LADDER</span></h1>
    <p class="hero-sub">
      设定人口与转职，搜索可激活<b>非唯一羁绊</b>最多的阵容。
      译名对齐 <a href="https://lol.qq.com/tft/#/champion" target="_blank" rel="noreferrer">lol.qq.com/tft</a>
      · 头像参考 <a href="https://www.datatft.com/database" target="_blank" rel="noreferrer">datatft</a>
    </p>
  </header>

  <div class="grid">
    <div class="card">
      <h2>Parameters</h2>
      <label>最高人口（棋盘槽位）</label>
      <input type="number" id="slots" min="1" max="20" value="11" />
      <div class="hint">可填 1–20；常规约 10–11，峡谷野怪 10 可 +2</div>

      <label>转职情况</label>
      <select id="emblemMode">
        <option value="none">无转职</option>
        <option value="any2" selected>任意转职 ×2（重铸器）</option>
        <option value="any1">任意转职 ×1</option>
        <option value="fixed">指定转职（下方勾选）</option>
      </select>

      <div id="fixedBox" class="emblem-box" style="display:none">
        <div class="hint" style="margin-bottom:6px">勾选你拥有的转职羁绊</div>
        <div class="g2" id="emblemList"></div>
      </div>

      <label>拉克丝（大元素使）</label>
      <select id="luxMode">
        <option value="on" selected>所选羁绊按 2 计（原版规则）</option>
        <option value="off">不使用双计 / 不考虑拉克丝</option>
      </select>

      <div class="checks">
        <label><input type="checkbox" id="countRival" checked /> 统计「宿敌」</label>
        <label><input type="checkbox" id="countFlora" checked /> 统计「绝命花妖」</label>
        <label><input type="checkbox" id="preferLux" /> 同分时优先含有效拉克丝</label>
        <label><input type="checkbox" id="fastMode" checked /> 快速模式（推荐）</label>
      </div>

      <button class="run" id="btnRun">开始冲榜</button>
      <div class="status" id="status">就绪 · 快速模式约 0.3–1 秒</div>
    </div>

    <div class="card" id="resultCard">
      <h2>Leaderboard Board</h2>
      <div class="empty" id="resultBody">设置条件后点击「开始冲榜」</div>
    </div>
  </div>

  <div class="note">
    非唯一羁绊不含：月华神女、自然之力！大元素使、赏金猎人、宝石骑士、魔岩巨兽、远古树精、荆棘之兴、帝王斑蝶、翠神、顶级掠食者等唯一羁绊。
    远古巨龙占 2 人口，并为峡谷野怪 +2。
    拉克丝：所选源系按 2 计入；花仙子/野兽之灵/黑荆棘/地狱火/月蚀骑士（门槛2）可单独点亮；魔女/日蚀/灵魂莲华/永恒之森（门槛3）双计仅+2，单独上场无效。
  </div>
</div>

<!-- 作者页脚 -->
<footer class="author">
  <div class="wrap" style="padding-top:0;padding-bottom:40px">
    <div class="author-band">
      <div class="author-label">BUILT BY</div>
      <div class="author-card">
        <div class="author-ava-wrap">
          <img class="author-ava" src="https://avatars.githubusercontent.com/u/61241144?v=4" alt="Crait7"
               onerror="this.style.display='none'" />
        </div>
        <div class="author-info">
          <div class="author-name">Crait7<span class="dot"></span></div>
          <div class="author-role">S18羁绊天梯 · Creator</div>
          <div class="author-links">
            <a class="chip" href="https://github.com/Crait7" target="_blank" rel="noreferrer">
              <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
              github.com/Crait7
            </a>
            <a class="chip" href="https://github.com/Crait7" target="_blank" rel="noreferrer">Repositories →</a>
          </div>
        </div>
      </div>
      <div class="author-foot">
        <div>S18羁绊天梯 · TRAIT LADDER · 非官方工具</div>
        <div class="mq-mini">C R A I T 7 · S 1 8 · T R A I T</div>
      </div>
    </div>
  </div>
</footer>

<script>'''

footer = r'''
</script>
</body>
</html>
'''

out = chrome + js + footer
out_path = src.parent / "S18羁绊天梯.html"
out_path.write_text(out, encoding="utf-8")
print("wrote", out_path, "bytes", out_path.stat().st_size)
# also keep old name as copy for convenience? user asked rename - write new name only
# overwrite old file too so present path still works if they use old link
src.write_text(out, encoding="utf-8")
print("also updated old filename")
