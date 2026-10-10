"""Kafedeki Robotla Okul İngilizcesi — ortak hesaplar ve dil sayaçları.
  evre_verisi(esik, pencere) : benzetim kaydından zaman, bardak hızı, evre numarası (0 kaldırma · 1 taşıma · 2 bırakma)
  evre_ozeti()               : evre süreleri ve en büyük hızlar (robotun cümlelerindeki sayılar buradan gelir)
  rota(eps)                  : taşıma evresindeki bardak yolunu düz parçalara indirir; parça boyu ve dönüş yönü (sol / sağ)
  kelimeler(metin)           : küçük harfli kelime listesi
  zaman_eki(cumle)           : cümlenin dil bilgisi kalıbı (present simple, present continuous, past simple, will, going to, can, must, imperative …)
  kalip_say(cumleler)        : kalıp başına cümle sayısı"""
import re
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from ortak import kayit, yumusat

TURUNCU, MAVI, YESIL, MOR, GRI, KIRMIZI = "#C2410C", "#1D4ED8", "#0F766E", "#7E22CE", "#6B7280", "#B91C1C"
EVRE_AD = ["kaldırma", "taşıma", "bırakma"]
EVRE_EN = ["lifting", "carrying", "putting down"]
EVRE_RENK = [MAVI, TURUNCU, YESIL]


def evre_verisi(esik=0.05, pencere=25):
    k = kayit(); t = k["zaman_s"]
    p = yumusat(np.column_stack([k["bardak_x_m"], k["bardak_y_m"], k["bardak_z_m"]]), pencere)
    v = np.gradient(p, t, axis=0)
    hiz = np.linalg.norm(v, axis=1)
    yatay = np.linalg.norm(v[:, :2], axis=1) > esik
    ilk, son = np.argmax(yatay), len(t) - 1 - np.argmax(yatay[::-1])
    sira = np.arange(len(t))
    evre = np.where(sira < ilk, 0, np.where(sira > son, 2, 1))
    return t, hiz, evre, p


def evre_ozeti():
    t, hiz, evre, p = evre_verisi()
    oz = {}
    for i, ad in enumerate(EVRE_EN):
        m = evre == i
        oz[ad] = dict(bas=float(t[m][0]), son=float(t[m][-1]), sure=float(t[m][-1] - t[m][0]),
                      hiz_max=float(hiz[m].max()), yukseklik_bas=float(p[m][0, 2]), yukseklik_son=float(p[m][-1, 2]))
    return oz


def _rdp(n, eps):
    if len(n) < 3:
        return [0, len(n) - 1]
    a, b = n[0], n[-1]; d = b - a; L = np.hypot(*d) or 1e-9
    uz = np.abs(d[0] * (n[:, 1] - a[1]) - d[1] * (n[:, 0] - a[0])) / L
    i = int(np.argmax(uz))
    if uz[i] <= eps:
        return [0, len(n) - 1]
    sol = _rdp(n[: i + 1], eps); sag = _rdp(n[i:], eps)
    return sol[:-1] + [j + i for j in sag]


def rota(eps=0.30, pencere=101):
    """Taşıma evresinde bardağın yatay yolu → düz parçalar. Dönüş: iki parça arasındaki açı (sola +, sağa −)."""
    k = kayit(); t = k["zaman_s"]
    p = yumusat(np.column_stack([k["bardak_x_m"], k["bardak_y_m"]]), pencere)
    _, _, evre, _ = evre_verisi()
    q = p[evre == 1]
    nok = q[_rdp(q, eps)]
    parca = []
    for j in range(len(nok) - 1):
        d = nok[j + 1] - nok[j]
        parca.append(dict(boy=float(np.hypot(*d)), aci=float(np.degrees(np.arctan2(d[1], d[0])))))
    for j in range(1, len(parca)):
        don = (parca[j]["aci"] - parca[j - 1]["aci"] + 180) % 360 - 180
        parca[j]["donus"] = float(don)
    return nok, parca


def yon(donus, esik=30):
    if donus is None or abs(donus) < esik:
        return "go straight"
    return "turn left" if donus > 0 else "turn right"


# ---------- dil sayaçları ----------
FIIL = {  # yalın: (3. tekil, geçmiş, -ing)
    "be": ("is", "was", "being"), "work": ("works", "worked", "working"), "serve": ("serves", "served", "serving"),
    "carry": ("carries", "carried", "carrying"), "lift": ("lifts", "lifted", "lifting"), "put": ("puts", "put", "putting"),
    "take": ("takes", "took", "taking"), "bring": ("brings", "brought", "bringing"), "go": ("goes", "went", "going"),
    "turn": ("turns", "turned", "turning"), "walk": ("walks", "walked", "walking"), "move": ("moves", "moved", "moving"),
    "stop": ("stops", "stopped", "stopping"), "wait": ("waits", "waited", "waiting"), "hold": ("holds", "held", "holding"),
    "start": ("starts", "started", "starting"), "finish": ("finishes", "finished", "finishing"), "need": ("needs", "needed", "needing"),
    "like": ("likes", "liked", "liking"), "want": ("wants", "wanted", "wanting"), "have": ("has", "had", "having"),
    "open": ("opens", "opened", "opening"), "clean": ("cleans", "cleaned", "cleaning"), "say": ("says", "said", "saying"),
    "make": ("makes", "made", "making"), "bend": ("bends", "bent", "bending"), "pick": ("picks", "picked", "picking"),
    "check": ("checks", "checked", "checking"), "keep": ("keeps", "kept", "keeping"), "follow": ("follows", "followed", "following"),
    "read": ("reads", "read", "reading"), "touch": ("touches", "touched", "touching"), "run": ("runs", "ran", "running"),
    "spill": ("spills", "spilled", "spilling"), "sit": ("sits", "sat", "sitting"), "drink": ("drinks", "drank", "drinking"),
    "enjoy": ("enjoys", "enjoyed", "enjoying"), "help": ("helps", "helped", "helping"), "come": ("comes", "came", "coming"),
    "pour": ("pours", "poured", "pouring"), "place": ("places", "placed", "placing"), "learn": ("learns", "learned", "learning"),
    "pay": ("pays", "paid", "paying"), "return": ("returns", "returned", "returning"), "order": ("orders", "ordered", "ordering"), "welcome": ("welcomes", "welcomed", "welcoming"),
}
GECMIS = {v[1] for v in FIIL.values()} | {"was", "were"}
YALIN = set(FIIL)
UCUNCU = {v[0] for v in FIIL.values()}
KALIPLAR = ["will", "going to", "present continuous", "imperative", "past simple", "would like", "can", "must / have to",
            "there is / are", "present simple", "diğer"]


def kelimeler(metin):
    return re.findall(r"[a-z]+(?:'[a-z]+)?", metin.lower())


def zaman_eki(cumle):
    """Cümlenin ana kalıbı (öncelik sırası KALIPLAR'daki gibi). Kural tabanlı, yalnız bu kursun cümleleri için."""
    k = kelimeler(cumle); s = " ".join(k)
    if re.search(r"\b(will|won't)\b|'ll\b", s):
        return "will"
    ozne = r"(i|you|we|they|he|she|it|the robot|the customer)"
    if re.search(r"\b(am|is|are|'m|'re|'s)\s+(not\s+)?going to\s+[a-z]+", s) or re.search(r"\b(am|is|are)\s+" + ozne + r"\s+going to\s+[a-z]+", s):
        return "going to"
    if re.search(r"\b(am|is|are|i'm|you're|it's|we're|they're|he's|she's)\s+(not\s+)?[a-z]+ing\b", s) or \
            re.search(r"\b(am|is|are)\s+" + ozne + r"\s+[a-z]+ing\b", s):
        return "present continuous"
    bas = [w for w in k if w not in ("please", "first", "then", "next", "finally", "after", "that")]
    if bas and bas[0] != "be" and (bas[0] in YALIN or (bas[0] in ("don't",) and len(bas) > 1 and bas[1] in YALIN) or
                                   (bas[:2] == ["do", "not"] and len(bas) > 2 and bas[2] in YALIN)):
        return "imperative"
    if any(w in GECMIS for w in k) or re.search(r"\b(did|didn't)\b", s):
        return "past simple"
    if re.search(r"\bwould\b|\bi'd\b", s):
        return "would like"
    if re.search(r"\b(can|can't|cannot|could)\b", s):
        return "can"
    if re.search(r"\b(must|mustn't|have to|has to)\b", s):
        return "must / have to"
    if re.search(r"\bthere (is|are|isn't|aren't)\b|\bthere's\b", s):
        return "there is / are"
    if any(w in YALIN | UCUNCU | {"am", "is", "are", "i'm", "it's", "don't", "doesn't", "do", "does"} for w in k):
        return "present simple"
    return "diğer"


def kalip_say(cumleler):
    c = Counter(zaman_eki(x) for x in cumleler)
    return {k: c.get(k, 0) for k in KALIPLAR}


def sik(cumleler, n=10, durak=True):
    DUR = {"the", "a", "an", "i", "you", "it", "is", "to", "and", "of", "my", "your", "on", "in", "for", "this", "at", "am", "are"}
    c = Counter(w for x in cumleler for w in kelimeler(x) if not (durak and w in DUR))
    return c.most_common(n)


# ---------- çizim ----------
def kutu(ax, x, y, w, h, metin, renk, boy=24, yazi="#ffffff"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03", fc=renk, ec="none"))
    ax.text(x + w / 2, y + h / 2, metin, ha="center", va="center", color=yazi, fontsize=boy, linespacing=1.4)


def ok(ax, x1, y1, x2, y2, renk="#111111"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=renk, lw=3, mutation_scale=28))


def bos_eksen(baslik):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); ax.set_title(baslik)
    return fig, ax


def cubuk(sayim, baslik, renk=MAVI, xetiket="cümle sayısı"):
    ad = [k for k, v in sayim.items()]; deg = [sayim[k] for k in ad]
    fig, ax = plt.subplots()
    y = np.arange(len(ad))[::-1]
    ax.barh(y, deg, color=renk)
    for yi, d in zip(y, deg):
        ax.text(d + max(deg) * 0.01 + 0.05, yi, str(d), va="center", fontsize=22, weight="bold")
    ax.set_yticks(y); ax.set_yticklabels(ad, fontsize=22); ax.set_xlabel(xetiket); ax.set_title(baslik)
    ax.set_xlim(0, max(deg) * 1.15 + 1)
    from matplotlib.ticker import MaxNLocator
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    return fig, ax


def tr(x, basamak=1):
    return f"{x:.{basamak}f}".replace(".", ",")
