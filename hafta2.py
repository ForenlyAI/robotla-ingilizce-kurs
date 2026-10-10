"""Hafta 2 · Sipariş Almak — Ders 2.1–2.4.
  python hafta2.py   → ekran/2.x/*.txt + *.png, OLCUMLER.json (d2_*)"""
import matplotlib.pyplot as plt
from ortak import olc, oturum, sekil
from arac import evre_ozeti, kalip_say, sik, cubuk, kutu, ok, bos_eksen, MAVI, TURUNCU, YESIL, GRI, MOR
from konusmalar import derlem

D = derlem()


def ders_2_1():
    """Kibar istekler: would like, can I have; teklifi kabul ve ret."""
    ns = oturum("2.1", "siparis-diyalogu", """
from konusmalar import derlem
from arac import zaman_eki
diyalog = derlem()["siparis"]
roller = ["robot", "robot", "robot", "müşteri", "robot", "müşteri", "müşteri", "robot", "robot", "müşteri", "robot", "robot"]
for kim, c in zip(roller, diyalog):
    print(f"{kim:8s} {c}")
len(diyalog)
""")
    ns = oturum("2.1", "kibar-kaliplar", """
from arac import kelimeler
kalip = {"would you like": 0, "i'd like": 0, "can i have": 0, "please": 0, "thank you": 0}
for c in diyalog:
    s = " ".join(kelimeler(c))
    for k in kalip:
        kalip[k] += s.count(k)
kalip
""", ns)
    fig, ax = bos_eksen("Sipariş konuşmasının akışı · robot sorar, müşteri yanıtlar")
    adim = [("Good morning!\nWelcome.", MAVI), ("What would you\nlike to drink?", MAVI), ("I'd like a glass\nof tea, please.", TURUNCU),
            ("Would you\nlike sugar?", MAVI), ("Yes, please.\nTwo sugars.", TURUNCU), ("Here you are.\nEnjoy your tea!", YESIL)]
    for i, (m, r) in enumerate(adim):
        x = 0.02 + (i % 3) * 0.33; y = 0.58 - (i // 3) * 0.42
        kutu(ax, x, y, 0.28, 0.26, m, r, boy=24)
        if i % 3 < 2:
            ok(ax, x + 0.285, y + 0.13, x + 0.325, y + 0.13)
    ok(ax, 0.83, 0.57, 0.17, 0.43)
    ax.text(0.5, 0.02, "mavi: robot · turuncu: müşteri · yeşil: servis", ha="center", fontsize=22, color=GRI)
    sekil("2.1", "diyalog-akisi")
    olc(d2_1_replik=len(ns["diyalog"]), d2_1_kalip=ns["kalip"],
        d2_1_robot=ns["roller"].count("robot"), d2_1_musteri=ns["roller"].count("müşteri"))


def ders_2_2():
    """Soru kelimeleri: what, where, how many, how long …"""
    ns = oturum("2.2", "soru-kelimeleri", """
from konusmalar import hepsi
from arac import kelimeler
sorular = [c for b, c in hepsi() if c.endswith("?")]
len(sorular)
soru_kelimesi = ["what", "where", "when", "who", "which", "why", "how many", "how long"]
say = {}
for s in soru_kelimesi:
    say[s] = sum(1 for c in sorular if (" " + " ".join(kelimeler(c)) + " ").find(" " + s + " ") >= 0)
{k: v for k, v in say.items() if v}
evet_hayir = [c for c in sorular if kelimeler(c)[0] in ("do", "does", "can", "is", "are", "would", "did", "was")]
len(evet_hayir)
""")
    ns = oturum("2.2", "soru-yanit", """
from arac import evre_ozeti
toplam = round(evre_ozeti()["putting down"]["son"])
soru = "How long does the job take?"
yanit = f"It takes about {toplam} seconds."
print(soru)
print(yanit)
""")
    from konusmalar import hepsi
    from arac import kelimeler
    sorular = [c for b, c in hepsi() if c.endswith("?")]
    sk = ["what", "where", "when", "who", "which", "why", "how many", "how long"]
    say = {s: sum(1 for c in sorular if (" " + " ".join(kelimeler(c)) + " ").find(" " + s + " ") >= 0) for s in sk}
    evet = sum(1 for c in sorular if kelimeler(c)[0] in ("do", "does", "can", "is", "are", "would", "did", "was"))
    cubuk({**{k: v for k, v in say.items() if v}, "evet / hayır sorusu": evet}, "Robotun derlemindeki sorular: hangi soru kalıbı kaç kez",
          renk=MOR, xetiket="soru sayısı")
    sekil("2.2", "soru-dagilimi")
    olc(d2_2_soru=len(sorular), d2_2_soru_kelimesi={k: v for k, v in say.items() if v}, d2_2_evet_hayir=evet,
        d2_2_is_suresi_s=ns["toplam"])


def ders_2_3():
    """Sıralı anlatım: first, then, next, after that, finally + emir cümlesi; sıra kayıttaki evrelerle aynı mı."""
    oz = evre_ozeti()
    fig, ax = bos_eksen("Servisin adımları ve kayıttaki süreler · benzetim kaydı")
    adim = [("First,\npick up the glass.", "0 s", MAVI),
            (f"Then,\nlift it.", f"kaldırma {oz['lifting']['sure']:.1f} s".replace(".", ","), MAVI),
            ("Next,\ncarry it.", f"taşıma {oz['carrying']['sure']:.1f} s".replace(".", ","), TURUNCU),
            ("After that,\nput it down.", f"bırakma {oz['putting down']['sure']:.1f} s".replace(".", ","), YESIL),
            ("Finally,\nsay: Enjoy!", f"bitiş {oz['putting down']['son']:.1f} s".replace(".", ","), GRI)]
    for i, (m, s, r) in enumerate(adim):
        x = 0.02 + i * 0.198
        kutu(ax, x, 0.42, 0.155, 0.32, m, r, boy=21)
        ax.text(x + 0.078, 0.32, s, ha="center", fontsize=20, weight="bold", color=r)
        if i < 4:
            ok(ax, x + 0.165, 0.58, x + 0.19, 0.58)
    sekil("2.3", "servis-adimlari")
    ns = oturum("2.3", "siralama", """
from konusmalar import derlem
from arac import zaman_eki
adimlar = derlem()["adimlar"]
siralayicilar = ["first", "then", "next", "after that", "finally"]
bulunan = [s for c in adimlar for s in siralayicilar if c.lower().startswith(s)]
bulunan
bulunan == siralayicilar
""")
    ns = oturum("2.3", "emir-cumleleri", """
for c in adimlar:
    print(f"{zaman_eki(c):12s} {c}")
emir = [c for c in adimlar if zaman_eki(c) == "imperative"]
olumsuz_emir = [c for c in emir if c.startswith(("Don't", "Do not"))]
len(emir), len(olumsuz_emir)
""", ns)
    olc(d2_3_siralayici=len(ns["bulunan"]), d2_3_sira_dogru=bool(ns["bulunan"] == ns["siralayicilar"]),
        d2_3_emir=len(ns["emir"]), d2_3_olumsuz_emir=len(ns["olumsuz_emir"]),
        d2_3_sure_s={k: round(v["sure"], 1) for k, v in oz.items()})


def ders_2_4():
    """Telefonda sipariş: on the phone kalıpları."""
    ns = oturum("2.4", "telefon-konusmasi", """
from konusmalar import derlem
telefon = derlem()["telefon"]
for i, c in enumerate(telefon, 1):
    print(i, c)
""")
    ns = oturum("2.4", "telefon-kaliplari", """
from arac import kelimeler
kaliplar = ["this is", "can i speak to", "hold on", "can i take a message", "could you say that again", "thank you for calling"]
bulunan = [k for k in kaliplar if any(k in " ".join(kelimeler(c)) for c in telefon)]
len(bulunan), len(kaliplar)
kibar = sum(" ".join(kelimeler(c)).count("please") for c in telefon)
kibar
""", ns)
    say = dict(sik(D["siparis"] + D["telefon"], 8))
    cubuk(say, "Sipariş ve telefon konuşmalarında en sık kelimeler", renk=TURUNCU, xetiket="kaç kez geçti")
    sekil("2.4", "kelime-sikligi")
    olc(d2_4_replik=len(ns["telefon"]), d2_4_kalip=len(ns["bulunan"]), d2_4_please=ns["kibar"], d2_4_sik=list(say.items())[:3])


if __name__ == "__main__":
    ders_2_1(); ders_2_2(); ders_2_3(); ders_2_4()
    print("hafta 2 tamam")
