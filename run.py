from flask import Flask, jsonify
import random, json, os

app = Flask(__name__)

CARDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards.json")

def load_cards():
    try:
        with open(CARDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list) and data:
                return data
    except Exception:
        pass
    return DEFAULT_CARDS

DEFAULT_CARDS = [
    "بدون خندیدن بگو «من امشب فقط آب می‌خورم».",
    "به نفر بغلی با جدیت کامل بگو «تو رهبر آینده‌ای من».",
    "۱۰ ثانیه مستقیم تو چشم یه نفر نگاه کن بدون خنده.",
    "با لحن خبر ساعت ۲۱ بگو «قیمت گوجه امروز نجومی شد».",
    "وانمود کن استاد دانشگاهی و درباره پشمک سخنرانی کن.",
    "با صدای خیلی جدی بگو «این جلسه رسمی است، خنده ممنوع».",
    "مثل مجری اخبار ورزشی نتیجه بازی فوتبال محله رو گزارش بده.",
    "با لحن حکیمانه یه نصیحت درباره دستمال کاغذی بده.",
    "وانمود کن داری با رئیس‌جمهور یه کشور خیالی مصاحبه می‌کنی.",
    "با صدای آروم و رسمی بگو «متاسفانه سهام شما صفر شد».",
    "مثل معلم سختگیر به یکی بگو «برو بشین سرجات!».",
    "با لحن مستند حیات وحش درباره یکی از بازیکنا توضیح بده.",
    "وانمود کن مجری تلویزیونی برنامه فال‌بینی هستی.",
    "با جدیت کامل بگو «امروز رکورد جهانی سکوت رو می‌زنیم».",
    "مثل یه فیلسوف باستانی درباره چای توضیح بده.",
    "با صدای رباتیک بگو «سیستم در حال پردازش لبخند است... خطا».",
    "وانمود کن داری اعلام برنده جایزه نوبل رو می‌کنی، اسم یکی از بازیکنا رو بگو.",
    "با لحن دکتر به یکی بگو «نسخه‌تون یک لیوان آب‌پرتقاله».",
    "مثل کاپیتان هواپیما اعلام کن «مسافران عزیز به خنده رسیدیم».",
    "با صدای بی‌احساس بگو «هرگونه خنده باعث از دست رفتن امتیاز می‌شود».",
    "وانمود کن گزارشگر جنگی هستی و وضعیت اتاق رو گزارش بده.",
    "با لحن رسمی نامه اداری بخون: «به استحضار می‌رساند...».",
    "مثل مربی تیم ملی قبل از بازی نهایی سخنرانی انگیزشی بده.",
    "با صدای آرام مدیتیشن بگو «نفس بکش... حالا لبخند نزن».",
    "وانمود کن مجری برنامه کودک هستی ولی با صدای خیلی جدی.",
    "به نفر روبروت بگو «من به شما افتخار می‌کنم» بدون تغییر حالت صورت.",
    "با لحن دادگاه بگو «متهم به خندیدن، دفاعیات خود را ارائه دهد».",
    "وانمود کن مجری مراسم اسکار هستی و برنده رو با هیجان کنترل‌شده اعلام کن.",
    "با صدای اعلانات فرودگاه بگو «پرواز به سمت خنده لغو شد».",
    "مثل یه ربات فروشگاهی بگو «خنده شما برای ما ارزشمند است، لطفاً تکرار نکنید».",
    "وانمود کن مجری هواشناسی هستی، امروز احتمال بارش خنده ۹۹٪ است ولی جدی بمون.",
    "با لحن قاضی فوتبال کارت زرد به یکی بده و دلیل جدی بیار.",
    "مثل یه مامور گمرک از یکی بازجویی کن چرا لبخند قاچاق کرده.",
    "با صدای اعلام نتایج کنکور، اسم یکی رو با هیجان کنترل‌شده بگو.",
    "وانمود کن مربی یوگا هستی و دستور بده «حالا صورت سنگ شوید».",
]

HTML_PAGE = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ZOHAL - تو بخندی باختی</title>
<style>
  @font-face {
    font-family: 'Vazirmatn';
    src: url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/webfonts/Vazirmatn-Regular.woff2') format('woff2');
    font-weight: 400;
  }
  @font-face {
    font-family: 'Vazirmatn';
    src: url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/webfonts/Vazirmatn-Bold.woff2') format('woff2');
    font-weight: 700;
  }
  :root {
    --bg: #0d0d0d;
    --card-bg: #1a1a1a;
    --yellow: #f5c518;
    --text: #f2f2f2;
    --muted: #888;
    --danger: #e14b4b;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    min-height: 100vh;
    background: var(--bg);
    color: var(--text);
    font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
  }
  h1 {
    color: var(--yellow);
    text-align: center;
    margin: 10px 0 2px;
    letter-spacing: 0.5px;
  }
  .subtitle {
    color: var(--muted);
    margin-bottom: 20px;
    font-size: 14px;
    text-align: center;
  }
  .hidden { display: none !important; }

  /* ---------- SETUP SCREEN ---------- */
  .setup-box {
    background: var(--card-bg);
    border: 2px solid var(--yellow);
    border-radius: 16px;
    padding: 25px;
    width: 100%;
    max-width: 380px;
  }
  .setup-box h2 {
    color: var(--yellow);
    margin-top: 0;
    font-size: 18px;
  }
  .player-input-row {
    display: flex;
    gap: 8px;
    margin-bottom: 10px;
  }
  .player-input-row input {
    flex: 1;
    background: #111;
    border: 1px solid #333;
    color: var(--text);
    padding: 10px;
    border-radius: 8px;
    font-family: inherit;
    font-size: 14px;
  }
  .player-list {
    list-style: none;
    padding: 0;
    margin: 10px 0;
  }
  .player-list li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #111;
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 6px;
    font-size: 14px;
  }
  .player-list li button {
    background: transparent;
    border: none;
    color: var(--danger);
    font-size: 16px;
    cursor: pointer;
    padding: 0 6px;
  }

  /* ---------- GAME SCREEN ---------- */
  .turn-banner {
    background: var(--yellow);
    color: #111;
    font-weight: bold;
    padding: 10px 20px;
    border-radius: 30px;
    margin-bottom: 18px;
    font-size: 16px;
    text-align: center;
  }
  .scene {
    perspective: 1000px;
    width: 100%;
    max-width: 380px;
  }
  .card {
    background: var(--card-bg);
    border: 2px solid var(--yellow);
    border-radius: 16px;
    padding: 40px 25px;
    min-height: 220px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-size: 20px;
    font-weight: 700;
    line-height: 1.8;
    box-shadow: 0 0 25px rgba(245, 197, 24, 0.15);
    transition: transform 0.4s ease;
    transform-style: preserve-3d;
  }
  .card.flip { transform: rotateY(360deg); }

  .controls {
    display: flex;
    gap: 12px;
    margin-top: 25px;
    flex-wrap: wrap;
    justify-content: center;
  }
  button.main-btn {
    background: var(--yellow);
    color: #111;
    border: none;
    padding: 12px 20px;
    border-radius: 10px;
    font-weight: bold;
    font-size: 14px;
    font-family: inherit;
    cursor: pointer;
    transition: transform 0.15s ease, opacity 0.15s ease;
  }
  button.main-btn:hover { transform: translateY(-2px); opacity: 0.9; }
  button.main-btn:active { transform: translateY(0); }
  .reset-btn {
    background: transparent !important;
    color: var(--yellow) !important;
    border: 2px solid var(--yellow) !important;
  }
  .danger-btn {
    background: transparent !important;
    color: var(--danger) !important;
    border: 2px solid var(--danger) !important;
  }

  .timer-wrap {
    margin-top: 20px;
    text-align: center;
  }
  .timer-wrap .value {
    color: var(--yellow);
    font-size: 30px;
    font-weight: bold;
  }
  .timer-wrap .label {
    color: var(--muted);
    font-size: 12px;
  }

  /* ---------- SCOREBOARD ---------- */
  .scoreboard {
    width: 100%;
    max-width: 380px;
    margin-top: 25px;
    background: var(--card-bg);
    border-radius: 14px;
    padding: 12px 16px;
    border: 1px solid #333;
  }
  .scoreboard h3 {
    color: var(--yellow);
    font-size: 14px;
    margin: 0 0 10px;
  }
  .score-row {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    font-size: 14px;
    border-bottom: 1px solid #222;
  }
  .score-row:last-child { border-bottom: none; }
  .score-row .name { color: var(--text); }
  .score-row .pts { color: var(--yellow); font-weight: bold; }
  .score-row.active .name { color: var(--yellow); }

  footer {
    margin-top: 35px;
    color: var(--muted);
    font-size: 12px;
    text-align: center;
  }
  @media (max-width: 480px) {
    .card { font-size: 17px; min-height: 190px; padding: 30px 18px; }
    h1 { font-size: 21px; }
  }
</style>
</head>
<body>

<h1>ZOHAL — تو بخندی باختی 😂</h1>
<div class="subtitle">با یه گوشی، به نوبت بازی کنید</div>

<!-- SETUP SCREEN -->
<div class="setup-box" id="setupScreen">
  <h2>بازیکن‌ها رو اضافه کن</h2>
  <div class="player-input-row">
    <input type="text" id="playerNameInput" placeholder="اسم بازیکن..." maxlength="14">
    <button class="main-btn" onclick="addPlayer()">افزودن</button>
  </div>
  <ul class="player-list" id="playerList"></ul>

  <div style="margin-top:15px;">
    <label style="font-size:13px; color:var(--muted);">مدت زمان هر نوبت (ثانیه)</label>
    <div class="player-input-row" style="margin-top:6px;">
      <input type="number" id="timerInput" value="10" min="3" max="120" style="text-align:center;">
    </div>
  </div>

  <button class="main-btn" style="width:100%; margin-top:10px;" onclick="startGame()">شروع بازی 🎮</button>
</div>

<!-- GAME SCREEN -->
<div id="gameScreen" class="hidden" style="width:100%; display:flex; flex-direction:column; align-items:center;">
  <div class="turn-banner" id="turnBanner">نوبت: —</div>

  <div class="scene">
    <div class="card" id="card">در حال بارگذاری...</div>
  </div>

  <div class="timer-wrap">
    <div class="value" id="timer">۱۰</div>
    <div class="label">ثانیه باقی‌مانده</div>
  </div>

  <div class="controls">
    <button class="main-btn" onclick="laughed()">😂 خندید!</button>
    <button class="main-btn" onclick="nextTurn()">نفر بعد ➡</button>
    <button class="main-btn reset-btn" onclick="resetScores()">ریست امتیازها</button>
    <button class="main-btn danger-btn" onclick="backToSetup()">بازیکن‌ها</button>
  </div>

  <div class="scoreboard">
    <h3>جدول امتیازات</h3>
    <div id="scoreList"></div>
  </div>
</div>

<footer>ساخته شده توسط گروه توسعه نرم‌افزار ZOHAL</footer>

<script>
let players = [];       // [{name, score}]
let currentIndex = 0;
let roundSeconds = 10;
let timeLeft = 10;
let timerInterval = null;

const setupScreen = document.getElementById('setupScreen');
const gameScreen = document.getElementById('gameScreen');
const playerListEl = document.getElementById('playerList');
const playerNameInput = document.getElementById('playerNameInput');
const cardEl = document.getElementById('card');
const timerEl = document.getElementById('timer');
const turnBanner = document.getElementById('turnBanner');
const scoreListEl = document.getElementById('scoreList');

const faDigits = ['۰','۱','۲','۳','۴','۵','۶','۷','۸','۹'];
function toFa(num) {
  return String(num).split('').map(d => faDigits[d] || d).join('');
}

function addPlayer() {
  const name = playerNameInput.value.trim();
  if (!name) return;
  players.push({ name, score: 0 });
  playerNameInput.value = '';
  renderPlayerList();
}

playerNameInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') addPlayer();
});

function removePlayer(idx) {
  players.splice(idx, 1);
  renderPlayerList();
}

function renderPlayerList() {
  playerListEl.innerHTML = '';
  players.forEach((p, idx) => {
    const li = document.createElement('li');
    li.innerHTML = `<span>${p.name}</span>`;
    const btn = document.createElement('button');
    btn.textContent = '✕';
    btn.onclick = () => removePlayer(idx);
    li.appendChild(btn);
    playerListEl.appendChild(li);
  });
}

function startGame() {
  if (players.length < 2) {
    alert('حداقل ۲ بازیکن اضافه کن!');
    return;
  }
  currentIndex = 0;
  const t = parseInt(document.getElementById('timerInput').value, 10);
  roundSeconds = (!isNaN(t) && t >= 3) ? t : 10;
  setupScreen.classList.add('hidden');
  gameScreen.classList.remove('hidden');
  updateTurnBanner();
  renderScoreboard();
  nextCard();
}

function backToSetup() {
  clearInterval(timerInterval);
  gameScreen.classList.add('hidden');
  setupScreen.classList.remove('hidden');
}

function updateTurnBanner() {
  turnBanner.textContent = 'نوبت: ' + players[currentIndex].name;
}

async function fetchCard() {
  const res = await fetch('/card');
  const data = await res.json();
  return data.card;
}

function startTimer() {
  clearInterval(timerInterval);
  timeLeft = roundSeconds;
  timerEl.textContent = toFa(timeLeft);
  timerInterval = setInterval(() => {
    timeLeft--;
    timerEl.textContent = toFa(timeLeft);
    if (timeLeft <= 0) {
      clearInterval(timerInterval);
      nextTurn();
    }
  }, 1000);
}

async function nextCard() {
  const text = await fetchCard();
  cardEl.classList.add('flip');
  setTimeout(() => { cardEl.textContent = text; }, 200);
  setTimeout(() => { cardEl.classList.remove('flip'); }, 400);
  startTimer();
}

function nextTurn() {
  currentIndex = (currentIndex + 1) % players.length;
  updateTurnBanner();
  nextCard();
}

function laughed() {
  players[currentIndex].score++;
  renderScoreboard();
  nextTurn();
}

function resetScores() {
  players.forEach(p => p.score = 0);
  renderScoreboard();
}

function renderScoreboard() {
  scoreListEl.innerHTML = '';
  players.forEach((p, idx) => {
    const row = document.createElement('div');
    row.className = 'score-row' + (idx === currentIndex ? ' active' : '');
    row.innerHTML = `<span class="name">${p.name}</span><span class="pts">${toFa(p.score)}</span>`;
    scoreListEl.appendChild(row);
  });
}
</script>

</body>
</html>
"""

@app.route("/")
def index():
    return HTML_PAGE

@app.route("/card")
def card():
    cards = load_cards()
    return jsonify({"card": random.choice(cards)})

if __name__ == "__main__":
    if not os.path.exists(CARDS_FILE):
        with open(CARDS_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CARDS, f, ensure_ascii=False, indent=2)
    app.run(debug=True, port=5000, host="0.0.0.0")
