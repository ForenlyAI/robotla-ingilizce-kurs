"""Hafta 4 · Geçmiş ve Gelecek — Ders 4.1–4.4 (+ tanıtım dersi için bir şekil).
  python hafta4.py   → ekran/4.x/*.txt + *.png, ekran/0.1/*.png, OLCUMLER.json (d4_*, d0_*)"""
import numpy as np
import matplotlib.pyplot as plt
from ortak import olc, oturum, sekil
from arac import (evre_verisi, evre_ozeti, kalip_say, sik, cubuk, kutu, bos_eksen, zaman_eki, KALIPLAR,
                  EVRE_EN, EVRE_RENK, MAVI, TURUNCU, YESIL, GRI, MOR)
from konusmalar import derlem, hepsi

D = derlem()


def ders_4_1():
    """Geçmiş zaman (past simple): robotun iş raporu; sayılar kayıttan."""
    ns = oturum("4.1", "is-raporu", """
from konusmalar import derlem
from arac import zaman_eki
rapor = derlem()["rapor"]
for c in rapor:
    print(f"{zaman_eki(c):12s} {c}")
sum(zaman_eki(c) == "past simple" for c in rapor), len(rapor)
""")
    ns = oturum("4.1", "duzenli-duzensiz", """
from arac import FIIL, kelimeler
duzenli, duzensiz = set(), set()
for c in rapor:
    for w in kelimeler(c):
        for yalin, (_, gecmis, _) in FIIL.items():
            if w == gecmis and (w != yalin or yalin == "put"):
                (duzenli if gecmis.endswith("ed") else duzensiz).add(f"{yalin} -> {gecmis}")
sorted(duzenli)
sorted(duzensiz)
""", ns)
    t, hiz, evre, p = evre_verisi(); oz = evre_ozeti()
    fig, ax = plt.subplots()
    for i, ad in enumerate(EVRE_EN):
        m = evre == i
        ax.axvspan(t[m][0], t[m][-1], color=EVRE_RENK[i], alpha=0.13)
    ax.plot(t, p[:, 2], color="#111111")
    cum = [f"I lifted the glass\nin {oz['lifting']['sure']:.0f} seconds.", f"I carried it\nfor {oz['carrying']['sure']:.0f} seconds.",
           f"I put it down\nin {oz['putting down']['sure']:.0f} seconds."]
    for i, ad in enumerate(EVRE_EN):
        m = evre == i
        ax.text((t[m][0] + t[m][-1]) / 2, 1.06, cum[i], ha="center", va="bottom", fontsize=22, weight="bold", color=EVRE_RENK[i])
    ax.set_ylim(0.72, 1.2); ax.set_xlabel("zaman (s)"); ax.set_ylabel("bardağın yüksekliği (m)")
    ax.set_title("İş bitti, şimdi geçmiş zamanla anlatıyoruz · benzetim kaydı")
    sekil("4.1", "is-zaman-cizelgesi")
    olc(d4_1_cumle=len(ns["rapor"]), d4_1_gecmis=sum(zaman_eki(c) == "past simple" for c in ns["rapor"]),
        d4_1_duzenli=sorted(ns["duzenli"]), d4_1_duzensiz=sorted(ns["duzensiz"]),
        d4_1_sure_s={k: round(v["sure"]) for k, v in oz.items()}, d4_1_toplam_s=round(oz["putting down"]["son"]))


def ders_4_2():
    """Karşılaştırma: -er than, the -est; cümleler kayıttan üretilip denetlenir."""
    oz = evre_ozeti()
    fig, ax = plt.subplots()
    ad = EVRE_EN; sure = [oz[a]["sure"] for a in ad]
    ax.bar(ad, sure, color=EVRE_RENK)
    for i, s in enumerate(sure):
        ax.text(i, s + 1, f"{s:.1f} s".replace(".", ","), ha="center", fontsize=24, weight="bold")
    ax.set_ylabel("süre (s)"); ax.set_ylim(0, max(sure) * 1.2)
    ax.set_title("Hangisi daha uzun? Evre süreleri · benzetim kaydı")
    sekil("4.2", "evre-sureleri")
    ns = oturum("4.2", "karsilastirma-uret", """
from arac import evre_ozeti
oz = evre_ozeti()
sure = {k: round(v["sure"], 1) for k, v in oz.items()}
sure
def karsilastir(a, b):
    return f"{a.capitalize()} was {'longer' if sure[a] > sure[b] else 'shorter'} than {b}."
print(karsilastir("carrying", "lifting"))
print(karsilastir("putting down", "lifting"))
en_uzun = max(sure, key=sure.get)
print(f"{en_uzun.capitalize()} was the longest part of the job.")
round(sure["carrying"] / sure["lifting"], 1)
""")
    ns = oturum("4.2", "derlem-denetimi", """
from konusmalar import derlem
from arac import kelimeler
cumleler = derlem()["karsilastirma"]
er_than = [c for c in cumleler if " than " in c and "more" not in c]
more_than = [c for c in cumleler if "more" in kelimeler(c)]
the_est = [c for c in cumleler if any(w.endswith("est") for w in kelimeler(c))]
len(er_than), len(more_than), len(the_est)
""")
    olc(d4_2_sure_s={k: round(v["sure"], 1) for k, v in oz.items()},
        d4_2_oran=round(oz["carrying"]["sure"] / oz["lifting"]["sure"], 1),
        d4_2_er_than=len(ns["er_than"]), d4_2_more_than=len(ns["more_than"]), d4_2_the_est=len(ns["the_est"]))


def ders_4_3():
    """Will ve going to: plan ve tahmin."""
    ns = oturum("4.3", "plan-cumleleri", """
from konusmalar import derlem
from arac import zaman_eki
plan = derlem()["plan"]
for c in plan:
    print(f"{zaman_eki(c):10s} {c}")
from collections import Counter
Counter(zaman_eki(c) for c in plan)
""")
    ns = oturum("4.3", "tahmin", """
from arac import evre_ozeti
oz = evre_ozeti()
toplam = round(oz["putting down"]["son"])
print(f"Prediction: It will take about {toplam} seconds.")
iki_bardak = 2 * toplam
print(f"Two glasses, one at a time: It will take about {iki_bardak} seconds.")
""")
    say = kalip_say(D["plan"])
    cubuk({k: v for k, v in say.items() if v}, "Plan cümlelerinde will ve going to", renk=MOR, xetiket="cümle sayısı")
    sekil("4.3", "will-going-to")
    olc(d4_3_cumle=len(D["plan"]), d4_3_will=say["will"], d4_3_going_to=say["going to"],
        d4_3_tahmin_s=ns["toplam"], d4_3_iki_bardak_s=ns["iki_bardak"])


def ders_4_4():
    """Robotun günlük raporu: bütün derlemin kalıp dağılımı + öğrenci raporu denetleyicisi."""
    cumleler = [c for b, c in hepsi()]
    say = kalip_say(cumleler)
    cubuk(say, f"Robotun bütün cümleleri ({len(cumleler)}): hangi kalıp kaç kez", renk=YESIL, xetiket="cümle sayısı")
    sekil("4.4", "kalip-dagilimi")
    from ortak import LAB
    (LAB / "ekran/0.1").mkdir(parents=True, exist_ok=True)
    cubuk(say, f"Kursun derlemi: robotun {len(cumleler)} cümlesi, kalıp kalıp", renk=YESIL, xetiket="cümle sayısı")
    sekil("0.1", "kalip-dagilimi")
    ns = oturum("4.4", "en-sik-kelimeler", """
from konusmalar import hepsi
from arac import sik, kelimeler
cumleler = [c for b, c in hepsi()]
len(cumleler), sum(len(kelimeler(c)) for c in cumleler)
len({w for c in cumleler for w in kelimeler(c)})
sik(cumleler, 8)
""")
    ns = oturum("4.4", "rapor-denetleyici", """
from arac import kalip_say
ornek_rapor = ["I am a humanoid robot.", "I work in a cafe.", "Today I carried a glass of tea.",
               "It took 113 seconds.", "There is a new table near the window.", "I can carry one glass.",
               "You must keep the glass level.", "Tomorrow I am going to serve two tables."]
def denetle(rapor):
    s = kalip_say(rapor)
    return {k: v for k, v in s.items() if v}, len([k for k, v in s.items() if v and k != "diğer"])
denetle(ornek_rapor)
""")
    olc(d4_4_cumle=len(cumleler), d4_4_kalip=say)
    from arac import kelimeler
    olc(d4_4_kelime=sum(len(kelimeler(c)) for c in cumleler), d4_4_farkli_kelime=len({w for c in cumleler for w in kelimeler(c)}),
        d4_4_sik=sik(cumleler, 3), d4_4_ornek_kalip_turu=ns["denetle"](ns["ornek_rapor"])[1],
        d0_1_cumle=len(cumleler), d0_1_kalip_turu=len([k for k, v in say.items() if v and k != "diğer"]))


if __name__ == "__main__":
    ders_4_1(); ders_4_2(); ders_4_3(); ders_4_4()
    print("hafta 4 tamam")
