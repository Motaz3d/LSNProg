import sys
import os
import collections

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lsnprog.alphabet import أبجدي
from lsnprog.corpus import جذر_تقريبي, صورة_رمزية_رقمية


def test_أبجدي_ابجد():
    # ا ب ج د = 1 + 2 + 3 + 4 = 10
    assert أبجدي("ابجد") == 10


def test_جذر_تقريبي_الرحمن():
    assert جذر_تقريبي("الرحمن") == "رحم"


def test_صورة_رمزية_رقمية_تربط_المعجم_بالقرآن():
    فهرس = {"رحم": {"التردد": 100, "الكلمات": collections.Counter({"رحمة": 60, "رحيم": 40})}}
    ص = صورة_رمزية_رقمية("رحم", فهرس)
    assert ص["الرمز"] == "رحم"
    assert "الرحمة" in ص["المعنى"]          # معنى من المعجم البسيط
    assert ص["التردد"] == 100                # تردد من القرآن
    assert ص["الأبجدي"] > 0
    assert ص["النبضي"] != ""


def test_جذر_غير_معروف_يأخذ_تسمية_مستخرج():
    فهرس = {"سجد": {"التردد": 5, "الكلمات": collections.Counter({"سجود": 5})}}
    ص = صورة_رمزية_رقمية("سجد", فهرس)
    assert "مستخرج" in ص["المعنى"]


if __name__ == "__main__":
    الاختبارات = [قيمة for اسم, قيمة in sorted(globals().items()) if اسم.startswith("test_")]
    for اختبار in الاختبارات:
        اختبار()
        print("✔", اختبار.__name__)
    print("كل الاختبارات نجحت ✔")
