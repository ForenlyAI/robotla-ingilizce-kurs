"""Hafta 1 · Kendini Tanıtmak — Ders 1.1–1.4.
  python hafta1.py   → ekran/1.x/*.txt + *.png, OLCUMLER.json (d1_*)"""
import numpy as np
import matplotlib.pyplot as plt
from ortak import kayit, olc, oturum, sekil, LAB
from arac import (evre_verisi, evre_ozeti, kalip_say, zaman_eki, sik, kelimeler, cubuk, kutu, bos_eksen,
                  EVRE_EN, EVRE_RENK, MAVI, TURUNCU, YESIL, GRI, KIRMIZI)
from konusmalar import derlem

D = derlem()


def ders_1_1():
    """Geniş zaman (present simple): robot kendini tanıtıyor; özne + fiil eki."""
    ns = oturum("1.1", "tanitim-cumleleri", """
from konusmalar import derlem
from arac import zaman_eki
cumleler = derlem()["tanitim"]
for c in cumleler:
    print(f"{zaman_eki(c):16s} {c}")
len(cumleler)
""")
    ns = oturum("1.1", "fiil-eki", """
from arac import kelimeler, UCUNCU, YALIN
for c in cumleler:
    k = kelimeler(c)
    ekli = [w for w in k if w in UCUNCU and w != "is"]
    if k[0] in ("the", "it", "he", "she") or ekli:
        print(f"{c:30s} -> ekli fiil: {ekli}")
ekli_say = sum(1 for c in cumleler for w in kelimeler(c) if w in UCUNCU and w != "is")
olumsuz = [c for c in cumleler if "don't" in c or "doesn't" in c]
ekli_say, len(olumsuz)
""", ns)
    say = dict(sik(D["tanitim"], 8))
    cubuk(say, "Robotun tanıtım cümlelerinde en sık kelimeler", renk=MAVI, xetiket="kaç kez geçti")
    sekil("1.1", "kelime-sikligi")
    olc(d1_1_cumle=len(ns["cumleler"]), d1_1_genis_zaman=kalip_say(ns["cumleler"])["present simple"],
        d1_1_ekli_fiil=ns["ekli_say"], d1_1_olumsuz=len(ns["olumsuz"]), d1_1_sik=list(say.items())[:3])


def ders_1_2():
    """There is / there are + yer edatları: robot kafeyi anlatıyor."""
    ns = oturum("1.2", "there-is-are", """
from konusmalar import derlem
from arac import kelimeler
cumleler = derlem()["masa"]
tekil = [c for c in cumleler if c.lower().startswith(("there is", "there isn't", "is there"))]
cogul = [c for c in cumleler if c.lower().startswith(("there are", "there aren't", "are there"))]
for c in tekil: print("is  ", c)
for c in cogul: print("are ", c)
len(tekil), len(cogul)
""")
    ns = oturum("1.2", "yer-edatlari", """
edatlar = ["on", "in", "next to", "near", "between", "at", "under", "behind"]
metin = " ".join(kelimeler(" ".join(cumleler)))
say = {e: metin.count(" " + e + " ") for e in edatlar}
{e: n for e, n in say.items() if n}
""", ns)
    fig, ax = bos_eksen("Kafe yerleşimi · robotun cümleleriyle (yerleşim ÖRNEK)")
    kutu(ax, 0.05, 0.62, 0.30, 0.22, "counter\n(tezgâh)", GRI, boy=26)
    kutu(ax, 0.14, 0.52, 0.12, 0.06, "tray", TURUNCU, boy=18)
    ax.text(0.20, 0.47, "The tray is on the counter.", ha="center", fontsize=18, color=GRI)
    for i in range(4):
        kutu(ax, 0.50 + (i % 2) * 0.24, 0.55 - (i // 2) * 0.38, 0.16, 0.16, f"table {i + 1}", MAVI, boy=22)
    kutu(ax, 0.38, 0.40, 0.08, 0.16, "robot", YESIL, boy=18)
    ax.text(0.97, 0.03, "window →", ha="right", fontsize=22, color=GRI)
    ax.text(0.05, 0.12, "There is a counter in the cafe.\nThere are four tables near the window.\nThe robot is between the counter and the tables.",
            fontsize=22, va="bottom", family="DejaVu Sans Mono")
    sekil("1.2", "kafe-yerlesimi")
    olc(d1_2_cumle=len(ns["cumleler"]), d1_2_tekil=len(ns["tekil"]), d1_2_cogul=len(ns["cogul"]),
        d1_2_edat={e: n for e, n in ns["say"].items() if n})


def ders_1_3():
    """Can / can't: robotun yapabildikleri kol parametre tablosundan ve benzetim kaydından."""
    ns = oturum("1.3", "kol-siniri", """
import csv, math
from ortak import kayit
satir = {r["ad"]: r for r in csv.DictReader(open("veri/sag_kol_parametre.csv"))}
ust = float(satir["dirsek"]["ust_rad"])
round(math.degrees(ust))
k = kayit()
round(math.degrees(k["dirsek_rad"].max()))
from arac import evre_ozeti
round(evre_ozeti()["carrying"]["hiz_max"], 2)
""")
    ns = oturum("1.3", "can-cumleleri", """
from konusmalar import derlem
from arac import kelimeler
cumleler = derlem()["yetenek"]
for c in cumleler:
    print(c)
olumlu = [c for c in cumleler if "can" in kelimeler(c) and not c.startswith("Can")]
olumsuz = [c for c in cumleler if "can't" in kelimeler(c)]
soru = [c for c in cumleler if c.startswith("Can")]
len(olumlu), len(olumsuz), len(soru)
""", ns)
    import csv, math
    k = kayit(); t = k["zaman_s"]
    ust = math.degrees(float({r["ad"]: r for r in csv.DictReader(open(LAB / "veri/sag_kol_parametre.csv"))}["dirsek"]["ust_rad"]))
    fig, ax = plt.subplots()
    ax.plot(t, np.degrees(k["dirsek_rad"]), color=MAVI, label="dirsek açısı (benzetim kaydı)")
    ax.axhline(ust, color=KIRMIZI, ls="--", label=f"sınır: My elbow can bend {ust:.0f} degrees.")
    ax.set_xlabel("zaman (s)"); ax.set_ylabel("dirsek açısı (derece)"); ax.legend(loc="upper left"); ax.set_ylim(-70, 175)
    ax.set_title("Can ile yetenek: dirsek ne kadar bükülebilir, kayıtta ne kadar büküldü")
    sekil("1.3", "dirsek-siniri")
    olc(d1_3_dirsek_sinir_derece=round(ust), d1_3_dirsek_kayit_max_derece=round(math.degrees(k["dirsek_rad"].max())),
        d1_3_hiz_max=round(evre_ozeti()["carrying"]["hiz_max"], 2),
        d1_3_olumlu=len(ns["olumlu"]), d1_3_olumsuz=len(ns["olumsuz"]), d1_3_soru=len(ns["soru"]))


def ders_1_4():
    """Şimdiki zaman (present continuous): kaydın her anında robot ne yapıyor."""
    t, hiz, evre, p = evre_verisi()
    oz = evre_ozeti()
    fig, ax = plt.subplots()
    for i, ad in enumerate(EVRE_EN):
        m = evre == i
        ax.axvspan(t[m][0], t[m][-1], color=EVRE_RENK[i], alpha=0.13)
        ax.text((t[m][0] + t[m][-1]) / 2, hiz.max() * 1.05, f"I am {ad}\nthe glass.", ha="center", va="bottom",
                color=EVRE_RENK[i], fontsize=23, weight="bold")
    ax.plot(t, hiz, color="#111111")
    ax.set_ylim(0, hiz.max() * 1.4); ax.set_xlabel("zaman (s)"); ax.set_ylabel("bardağın hızı (m/s)")
    ax.set_title("Şu anda ne yapıyor? Evreler ve şimdiki zaman cümleleri · benzetim kaydı")
    sekil("1.4", "evre-cumleleri")
    ns = oturum("1.4", "su-anda", """
import numpy as np
from arac import evre_verisi, EVRE_EN
t, hiz, evre, p = evre_verisi()
def su_anda(saniye):
    i = int(np.argmin(abs(t - saniye)))
    return f"At {saniye} seconds: I am {EVRE_EN[evre[i]]} the glass."
for s in [10, 60, 100]:
    print(su_anda(s))
""")
    ns = oturum("1.4", "ing-yazimi", """
from arac import FIIL
kurallar = {"sadece -ing": 0, "e düşer": 0, "harf çiftlenir": 0, "diğer": 0}
for yalin, (_, _, ing) in FIIL.items():
    if ing == yalin + "ing": kurallar["sadece -ing"] += 1
    elif ing == yalin[:-1] + "ing": kurallar["e düşer"] += 1
    elif ing == yalin + yalin[-1] + "ing": kurallar["harf çiftlenir"] += 1
    else: kurallar["diğer"] += 1
kurallar
[FIIL[f][2] for f in ["carry", "take", "put", "run"]]
""")
    olc(d1_4_sure_s={k: round(v["sure"], 1) for k, v in oz.items()}, d1_4_ing=ns["kurallar"],
        d1_4_fiil=len(ns["FIIL"]))


if __name__ == "__main__":
    ders_1_1(); ders_1_2(); ders_1_3(); ders_1_4()
    print("hafta 1 tamam")
