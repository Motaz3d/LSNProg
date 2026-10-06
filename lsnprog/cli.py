"""واجهة سطر الأوامر للغة لسن (lsn)."""
import sys

from . import engine
from . import neural

المساعدة = """لسن (lsn) — لغة برمجة عربية رمزية-عصبية قائمة على منطق القرآن

الاستخدام:
  lsn                       واجهة تفاعلية (اسأل بالعربية)
  lsn مثال                  الأمثلة التأسيسية كاملة
  lsn استعلام <نص>           استعلام الشبكة (مثال: lsn استعلام "من يقطع فرعون")
  lsn تعلم                   عروض التعلّم (من القرآن وأمثلة متقاربة)
  lsn حركات                  الحركات وتمييز معاني الجذر الواحد (علم)
  lsn صورة                   الصورة الرمزية لـ«روح» (الحركة والذهاب)
  lsn --version              الإصدار
"""


def تفاعلي():
    """واجهة تفاعلية بسيطة."""
    ش = neural.بناء_الشبكة()
    print("لغة لسن (lsn) — اكتب سؤالاً بالعربية، أو «مثال»، أو «خروج».")
    while True:
        try:
            سطر = input("lsn> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not سطر:
            continue
        if سطر in ("خروج", "exit", "quit"):
            break
        if سطر == "مثال":
            print(engine.عرض_المثال())
            continue
        if سطر == "حركات":
            print(neural.عرض_حركات_علم())
            continue
        نتائج = ش.استعلام(سطر)
        if not نتائج:
            print("  (لا نتيجة — جرّب «مثال» لرؤية ما يعرفه النموذج)")
        else:
            for اسم, قيمة, معنى in نتائج:
                print(f"  {اسم} ({قيمة}) ← {معنى}")
    return 0


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if not args:
        return تفاعلي()

    الأمر = args[0]
    الباقي = " ".join(args[1:])

    if الأمر in ("مثال", "demo"):
        print(engine.عرض_المثال())
    elif الأمر in ("استعلام", "ask", "سؤال"):
        if not الباقي:
            print("استخدام: lsn استعلام <نص>")
            return 1
        ش = neural.بناء_الشبكة()
        نتائج = ش.استعلام(الباقي)
        if not نتائج:
            print("(لا نتيجة — النموذج لا يعرفه بعد)")
        else:
            for اسم, قيمة, معنى in نتائج:
                print(f"  {اسم} ({قيمة}) ← {معنى}")
    elif الأمر in ("تعلم", "learn"):
        print(neural.عرض_تعلم_من_القرآن_2())
    elif الأمر in ("حركات", "harakat"):
        print(neural.عرض_حركات_علم())
    elif الأمر in ("صورة", "image"):
        print(neural.عرض_صورة_روح())
    elif الأمر in ("-v", "--version", "version"):
        print("لسن 0.1.0")
    else:
        print(المساعدة)
    return 0


if __name__ == "__main__":
    sys.exit(main())
