from flask import Flask, request, redirect, url_for
import json, os

app = Flask(__name__)

CARDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cards.json")


def load_cards():
    if not os.path.exists(CARDS_FILE):
        return []
    try:
        with open(CARDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_cards(cards):
    with open(CARDS_FILE, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ZOHAL - مدیریت کارت‌ها</title>
<style>
  @font-face {{
    font-family: 'Vazirmatn';
    src: url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/webfonts/Vazirmatn-Regular.woff2') format('woff2');
    font-weight: 400;
  }}
  @font-face {{
    font-family: 'Vazirmatn';
    src: url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/webfonts/Vazirmatn-Bold.woff2') format('woff2');
    font-weight: 700;
  }}
  :root {{
    --bg: #0d0d0d;
    --card-bg: #1a1a1a;
    --yellow: #f5c518;
    --text: #f2f2f2;
    --muted: #888;
    --danger: #e14b4b;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    min-height: 100vh;
    background: var(--bg);
    color: var(--text);
    font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  h1 {{ color: var(--yellow); margin-bottom: 5px; text-align: center; }}
  .subtitle {{ color: var(--muted); margin-bottom: 25px; font-size: 14px; }}
  .container {{ width: 100%; max-width: 600px; }}
  .add-box {{
    background: var(--card-bg);
    border: 2px solid var(--yellow);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 25px;
  }}
  .add-box h3 {{ color: var(--yellow); margin-top: 0; font-size: 15px; }}
  textarea, input[type=text] {{
    width: 100%;
    background: #111;
    border: 1px solid #333;
    color: var(--text);
    padding: 10px;
    border-radius: 8px;
    font-family: inherit;
    font-size: 14px;
    resize: vertical;
  }}
  form {{ display: flex; flex-direction: column; gap: 10px; }}
  button {{
    background: var(--yellow);
    color: #111;
    border: none;
    padding: 10px 18px;
    border-radius: 8px;
    font-weight: bold;
    font-size: 14px;
    font-family: inherit;
    cursor: pointer;
  }}
  button:hover {{ opacity: 0.9; }}
  .danger {{ background: var(--danger); color: #fff; }}
  .card-item {{
    background: var(--card-bg);
    border: 1px solid #333;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 12px;
  }}
  .card-item form {{ gap: 8px; }}
  .card-item .row {{
    display: flex;
    gap: 8px;
    justify-content: flex-end;
  }}
  .count {{
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 15px;
    text-align: center;
  }}
  .index-badge {{
    color: var(--yellow);
    font-size: 12px;
    margin-bottom: 6px;
    display: block;
  }}
</style>
</head>
<body>
<h1>مدیریت کارت‌ها — ZOHAL</h1>
<div class="subtitle">پورت ۵۰۰۱ — اضافه، ویرایش یا حذف کارت‌ها</div>

<div class="container">
  <div class="add-box">
    <h3>➕ افزودن کارت جدید</h3>
    <form method="POST" action="/add">
      <textarea name="text" rows="3" placeholder="متن کارت جدید را بنویس..." required></textarea>
      <button type="submit">افزودن کارت</button>
    </form>
  </div>

  <div class="count">تعداد کل کارت‌ها: {count}</div>

  {cards_html}
</div>
</body>
</html>
"""

CARD_ITEM_TEMPLATE = """
<div class="card-item">
  <span class="index-badge">کارت #{num}</span>
  <form method="POST" action="/edit/{idx}">
    <textarea name="text" rows="2">{text}</textarea>
    <div class="row">
      <button type="submit">ذخیره</button>
      <button type="submit" formaction="/delete/{idx}" formmethod="POST" class="danger" onclick="return confirm('حذف این کارت؟');">حذف</button>
    </div>
  </form>
</div>
"""


def escape(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


@app.route("/")
def index():
    cards = load_cards()
    cards_html = ""
    for idx, text in enumerate(cards):
        cards_html += CARD_ITEM_TEMPLATE.format(num=idx + 1, idx=idx, text=escape(text))
    return PAGE_TEMPLATE.format(count=len(cards), cards_html=cards_html)


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text", "").strip()
    if text:
        cards = load_cards()
        cards.append(text)
        save_cards(cards)
    return redirect(url_for("index"))


@app.route("/edit/<int:idx>", methods=["POST"])
def edit(idx):
    text = request.form.get("text", "").strip()
    cards = load_cards()
    if 0 <= idx < len(cards) and text:
        cards[idx] = text
        save_cards(cards)
    return redirect(url_for("index"))


@app.route("/delete/<int:idx>", methods=["POST"])
def delete(idx):
    cards = load_cards()
    if 0 <= idx < len(cards):
        cards.pop(idx)
        save_cards(cards)
    return redirect(url_for("index"))


if __name__ == "__main__":
    if not os.path.exists(CARDS_FILE):
        save_cards([])
    app.run(debug=True, port=5001, host="0.0.0.0")
