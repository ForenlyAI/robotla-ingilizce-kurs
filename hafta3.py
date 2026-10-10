"""Hafta 3 · Yol ve Talimat — Ders 3.1–3.4.
  python hafta3.py   → ekran/3.x/*.txt + *.png, OLCUMLER.json (d3_*)"""
import numpy as np
import matplotlib.pyplot as plt
from ortak import kayit, olc, oturum, sekil, yumusat
from arac import (evre_verisi, evre_ozeti, rota, yon, kutu, bos_eksen, cubuk, zaman_eki,
                  MAVI, TURUNCU, YESIL, GRI, KIRMIZI, MOR)
from konusmalar import derlem

D = derlem()


def _rota_sekli(ders, ad, baslik, edat=False):
    k = kayit()
    p = yumusat(np.column_stack([k["bardak_x_m"], k["bardak_y_m"]]), 101)
    _, _, evre, _ = evre_verisi()
    nok, parca = rota()
    fig, ax = plt.subplots()
    ax.plot(p[:, 0], p[:, 1], color=GRI, lw=2, alpha=0.6, label="bardağın yolu (benzetim kaydı)")
    ax.plot(nok[:, 0], nok[:, 1], "-o", color=TURUNCU, lw=5, ms=14, label="sadeleştirilmiş rota")
    for j, pr in enumerate(parca):
        m = (nok[j] + nok[j + 1]) / 2
        cumle = (yon(pr.get("donus")) if j else "go straight") + f", {pr['boy']:.1f} m"
        ax.annotate(f"{j + 1}. {cumle}", m, xytext=(18, 14 if j == 0 else (-8 if j != 1 else 10)), textcoords="offset points", fontsize=22,
                    weight="bold", color="#111111", ha="left")
    ax.plot(*p[0], "s", ms=24, color=MAVI); ax.plot(*p[-1], "s", ms=24, color=YESIL)
    ax.annotate("counter (start)" if not edat else "The glass was ON the counter.", p[0], xytext=(-30, -55),
                textcoords="offset points", fontsize=22, color=MAVI, ha="left")
    ax.annotate("table (finish)" if not edat else "Now it is ON the table.", p[-1], xytext=(-60, -70),
                textcoords="offset points", fontsize=22, color=YESIL, ha="left")
    ax.set_xlim(0.9, 5.4); ax.set_ylim(12.45, 15.35); ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
    ax.legend(loc="lower right"); ax.set_title(baslik)
    sekil(ders, ad)
    return nok, parca


def ders_3_1():
    """Yön tarifi: kayıttaki yoldan go straight / turn left / turn right cümleleri."""
    nok, parca = _rota_sekli("3.1", "rota", "Tezgâhtan masaya: kayıttaki yol ve yön tarifi · benzetim kaydı")
    ns = oturum("3.1", "yon-tarifi", """
from arac import rota, yon
nok, parca = rota()
len(parca)
for j, p in enumerate(parca):
    donus = p.get("donus")
    y = yon(donus) if j else "go straight"
    aci = f"{donus:+.0f} derece" if donus is not None else "-"
    print(f"{j + 1}. {y:12s} {p['boy']:.1f} m   dönüş {aci}")
round(sum(p["boy"] for p in parca), 1)
""")
    ns = oturum("3.1", "yol-cumleleri", """
from konusmalar import derlem
from arac import zaman_eki
yol = derlem()["yol"]
for c in yol:
    print(f"{zaman_eki(c):14s} {c}")
sum(zaman_eki(c) == "imperative" for c in yol), len(yol)
""", ns)
    olc(d3_1_parca=len(parca), d3_1_boy_m=[round(p["boy"], 1) for p in parca],
        d3_1_donus_derece=[round(p["donus"]) for p in parca[1:]], d3_1_toplam_m=round(sum(p["boy"] for p in parca), 1),
        d3_1_emir=sum(zaman_eki(c) == "imperative" for c in D["yol"]), d3_1_cumle=len(D["yol"]))


def ders_3_2():
    """Yer bildiren edatlar: on, in, next to, between … ; bardağın kayıttaki yüksekliği."""
    _rota_sekli("3.2", "nerede", "Bardak nerede? Başta ve sonda · benzetim kaydı", edat=True)
    ns = oturum("3.2", "edat-sayimi", """
from konusmalar import hepsi
from arac import kelimeler
edatlar = ["on", "in", "at", "to", "next to", "near", "between", "in front of", "past", "from"]
metin = " " + " ".join(kelimeler(" ".join(c for b, c in hepsi()))) + " "
say = {e: metin.count(" " + e + " ") for e in edatlar}
dict(sorted(say.items(), key=lambda x: -x[1]))
""")
    ns = oturum("3.2", "bosluk-doldurma", """
sorular = [("There is a glass ___ the tray.", "on"),
           ("The robot is ___ the counter and the tables.", "between"),
           ("There is a sugar bowl ___ ___ the glass.", "next to"),
           ("Because there is a person ___ ___ ___ me.", "in front of")]
from konusmalar import hepsi
cumleler = [c for b, c in hepsi()]
for s, y in sorular:
    tam = s.replace("___ ___ ___", y).replace("___ ___", y).replace("___", y)
    print(f"{y:12s} {tam:48s} derlemde: {tam in cumleler}")
""", ns)
    olc(d3_2_edat={k: v for k, v in ns["say"].items() if v}, d3_2_soru=len(ns["sorular"]),
        d3_2_dogrulanan=sum(1 for s, y in ns["sorular"]
                            if s.replace("___ ___ ___", y).replace("___ ___", y).replace("___", y) in ns["cumleler"]))


def ders_3_3():
    """Must / mustn't / have to / don't have to: kuralları kayıtla denetlemek."""
    ns = oturum("3.3", "kurallar", """
from konusmalar import derlem
from arac import kelimeler
kurallar = derlem()["kurallar"]
tur = {"must": 0, "mustn't / must not": 0, "have to / has to": 0, "don't have to": 0}
for c in kurallar:
    s = " ".join(kelimeler(c))
    if "don't have to" in s: tur["don't have to"] += 1
    elif "have to" in s or "has to" in s: tur["have to / has to"] += 1
    elif "mustn't" in s or "must not" in s: tur["mustn't / must not"] += 1
    else: tur["must"] += 1
tur
""")
    tur = ns["tur"]
    ns = oturum("3.3", "kural-denetimi", """
import csv, math
from ortak import kayit
from arac import evre_ozeti
k = kayit()
sinir = float({r["ad"]: r for r in csv.DictReader(open("veri/sag_kol_parametre.csv"))}["dirsek"]["ust_rad"])
dirsek_max = k["dirsek_rad"].max()
hiz_max = max(v["hiz_max"] for v in evre_ozeti().values())
print(f"You mustn't bend the elbow more than {math.degrees(sinir):.0f} degrees. -> kayıtta en çok {math.degrees(dirsek_max):.0f}")
dirsek_max <= sinir
""")
    t, hiz, evre, p = evre_verisi()
    fig, ax = plt.subplots()
    ax.plot(t, hiz, color="#111111", label="bardağın hızı (benzetim kaydı)")
    ax.axhline(hiz.max(), color=KIRMIZI, ls="--", label=f"You mustn't move faster than {hiz.max():.2f} m/s.")
    ax.set_xlabel("zaman (s)"); ax.set_ylabel("hız (m/s)"); ax.legend(loc="upper right"); ax.set_ylim(0, hiz.max() * 1.35)
    ax.set_title("Kural cümlesindeki sayı kayıttan geliyor · benzetim kaydı")
    sekil("3.3", "hiz-kurali")
    olc(d3_3_kural=len(D["kurallar"]), d3_3_tur=tur,
        d3_3_dirsek_uyuyor=bool(ns["dirsek_max"] <= ns["sinir"]), d3_3_hiz_max=round(float(hiz.max()), 2))


def ders_3_4():
    """Talimat okumak: güvenlik kartı; emir cümleleri ve okuma soruları."""
    kart = D["talimat"]
    fig, ax = bos_eksen("Robotun güvenlik kartı · okuma metni")
    kutu(ax, 0.18, 0.04, 0.64, 0.86, "", "#FFF7ED")
    ax.text(0.5, 0.82, kart[0], ha="center", fontsize=34, weight="bold", color=KIRMIZI)
    for i, c in enumerate(kart[1:]):
        ax.text(0.22, 0.72 - i * 0.085, f"{i}. {c}" if i else c, fontsize=24, family="DejaVu Sans", va="center")
    sekil("3.4", "guvenlik-karti")
    ns = oturum("3.4", "kart-cozumlemesi", """
from konusmalar import derlem
from arac import zaman_eki
kart = derlem()["talimat"]
maddeler = kart[2:]
emir = [c for c in maddeler if zaman_eki(c) == "imperative"]
olumsuz = [c for c in maddeler if c.startswith(("Do not", "Don't"))]
len(maddeler), len(emir), len(olumsuz)
fiiller = [c.split()[0] if not c.startswith("Do not") else "do not " + c.split()[2] for c in maddeler]
fiiller
""")
    ns = oturum("3.4", "okuma-sorulari", """
sorular = {"How many glasses can the robot pick up at a time?": "one",
           "Which hand holds the glass?": "right",
           "Where does the robot go at the end?": "counter",
           "What must the robot check first?": "battery"}
metin = " ".join(kart).lower()
for s, y in sorular.items():
    print(f"{s:52s} {y:8s} metinde: {y in metin}")
""", ns)
    olc(d3_4_madde=len(ns["maddeler"]), d3_4_emir=len(ns["emir"]), d3_4_olumsuz=len(ns["olumsuz"]),
        d3_4_soru=len(ns["sorular"]), d3_4_metinde=sum(y in ns["metin"] for y in ns["sorular"].values()))


if __name__ == "__main__":
    ders_3_1(); ders_3_2(); ders_3_3(); ders_3_4()
    print("hafta 3 tamam")
