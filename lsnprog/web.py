"""واجهة ويب بسيطة للغة لسن (بلا تبعيات خارجية)."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from . import neural

_الصفحة = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>لسن — اسأل بالعربية</title>
<style>
  :root { color-scheme: dark; }
  body { font-family: -apple-system, system-ui, "Segoe UI", sans-serif; background:#0f1115; color:#eaeaea; margin:0; padding:18px; }
  h1 { font-size: 1.5rem; text-align:center; margin: 8px 0 4px; }
  .sub { text-align:center; color:#889; font-size:.9rem; margin-bottom:18px; }
  .box { max-width: 640px; margin: 0 auto; }
  input { width:100%; font-size:1.1rem; padding:14px; border-radius:12px; border:1px solid #2a2f3a; background:#1a1d24; color:#fff; box-sizing:border-box; }
  button { width:100%; font-size:1.1rem; padding:14px; border-radius:12px; border:none; background:#2f6fed; color:#fff; margin-top:10px; cursor:pointer; }
  button:active { background:#2558c9; }
  .item { background:#1a1d24; border-radius:12px; padding:12px 14px; margin-top:8px; }
  .name { font-weight:700; }
  .score { color:#6b8; font-size:.85rem; }
  .ex { color:#8ab; cursor:pointer; text-decoration:underline; margin:4px; display:inline-block; font-size:.9rem; }
  .hint { color:#667; font-size:.85rem; text-align:center; margin-top:14px; }
</style>
</head>
<body>
<div class="box">
  <h1>لسن · LSN</h1>
  <div class="sub">نموذج عربي رمزي-عصبي — اسأل بالعربية</div>
  <input id="q" placeholder="اكتب سؤالك… مثال: من يقطع فرعون" autocomplete="off" />
  <button onclick="اسأل()">اسأل</button>
  <div id="res"></div>
  <div class="hint">جرّب:
    <span class="ex" onclick="ضبط('من يقطع فرعون')">من يقطع فرعون</span>
    <span class="ex" onclick="ضبط('ما معنى عيسى')">ما معنى عيسى</span>
    <span class="ex" onclick="ضبط('يد الله فوق أيديهم')">يد الله فوق أيديهم</span>
    <span class="ex" onclick="ضبط('ما هي الكاميرا')">ما هي الكاميرا</span>
    <span class="ex" onclick="ضبط('ما الفرق بين سلطان وملك')">سلطان وملك</span>
  </div>
</div>
<script>
function ضبط(t){ document.getElementById('q').value = t; اسأل(); }
async function اسأل(){
  const q = document.getElementById('q').value.trim();
  const r = document.getElementById('res');
  if(!q){ return; }
  r.innerHTML = '<div class="item">…</div>';
  try {
    const resp = await fetch('/api?q=' + encodeURIComponent(q));
    const data = await resp.json();
    if(!data.نتائج || data.نتائج.length === 0){
      r.innerHTML = '<div class="item">لا نتيجة — النموذج لا يعرفها بعد.</div>';
      return;
    }
    r.innerHTML = data.نتائج.map(x =>
      '<div class="item"><span class="name">' + x.اسم + '</span> ' +
      '<span class="score">(' + x.قيمة + ')</span><br>' + x.معنى + '</div>'
    ).join('');
  } catch(e) {
    r.innerHTML = '<div class="item">تعذّر الاتصال بالخادم.</div>';
  }
}
document.getElementById('q').addEventListener('keydown', e => { if(e.key === 'Enter') اسأل(); });
</script>
</body>
</html>
"""


class _معالج(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        مسار = urlparse(self.path)
        if مسار.path in ("/", "/index.html"):
            self._أرسل(_الصفحة, "text/html; charset=utf-8")
        elif مسار.path == "/api":
            س = parse_qs(مسار.query).get("q", [""])[0]
            ش = neural.بناء_الشبكة()
            نتائج = ش.استعلام(س)
            بيانات = {"نتائج": [{"اسم": ن, "قيمة": ق, "معنى": م} for ن, ق, م in نتائج]}
            self._أرسل(json.dumps(بيانات, ensure_ascii=False), "application/json; charset=utf-8")
        else:
            self.send_error(404)

    def _أرسل(self, نص, نوع):
        b = نص.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", نوع)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)


def شغّل(منفذ=8000):
    """يشغّل واجهة الويب على المنفذ المحدد."""
    خادم = HTTPServer(("0.0.0.0", منفذ), _معالج)
    print(f"لسن (lsn) — افتح في المتصفح: http://127.0.0.1:{منفذ}")
    print("(للموبايل: استخدم عنوان جهازك على الشبكة، مثل http://192.168.x.x:{0})".format(منفذ))
    try:
        خادم.serve_forever()
    except KeyboardInterrupt:
        print()
