import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lsnprog.engine import اشتق, معنى, نبضات, استنتاج, قراءات


def test_اشتقاق_قرآن():
    ن = اشتق("قرآن")
    assert ن["الجذر"] == "قرن"
    assert "الجمع" in ن["معنى الجذر"]


def test_رحمن_من_رحم_مع_لاحقة_ان():
    ن = اشتق("رحمن")
    assert ن["الجذر"] == "رحم"
    assert ن["اللاحقة"] == "ان"


def test_معنى_يد_في_سياق_القوة():
    ن = معنى("يد", "يد الله فوق أيديهم")
    assert "قوة" in ن["المعنى المختار"]


def test_معنى_فوق_في_سياق_السيطرة():
    ن = معنى("فوق", "يد الله فوق أيديهم")
    assert "سيطرة" in ن["المعنى المختار"] or "تعال" in ن["المعنى المختار"]


def test_نبضات_قرآن():
    # ق ر ا ن = 111110 10101 00 1110
    assert نبضات("قرآن") == "111110 10101 00 1110"


def test_استنتاج():
    assert len(استنتاج()) == 4


def test_قراءات_يوم_الدين():
    ن = قراءات("يوم الدين")
    assert ن is not None
    assert "ملك" in ن[0]
    assert any("مالِك" in س for س in ن)


if __name__ == "__main__":
    الاختبارات = [قيمة for اسم, قيمة in sorted(globals().items()) if اسم.startswith("test_")]
    for اختبار in الاختبارات:
        اختبار()
        print("✔", اختبار.__name__)
    print("كل الاختبارات نجحت ✔")
