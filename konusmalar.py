"""Kafedeki Robotla Okul İngilizcesi — robotun konuşma kalıpları (kursun derlemi).
Cümleleri kurs ekibi yazdı; içlerindeki SÜRE, HIZ, YÜKSEKLİK, YOL ve EKLEM sınırı sayıları benzetim kaydından ve kol parametre
tablosundan hesaplanır (arac.evre_ozeti, arac.rota, veri/sag_kol_parametre.csv). Masa numarası, içecek adları ve müşteri repliklerinin
içeriği ÖRNEK'tir (kayıtta yok).
  derlem()  → {bolum: [cümle, ...]}   bütün bölümler
  hepsi()   → [(bolum, cümle), ...]"""
import csv, math
from ortak import LAB
from arac import evre_ozeti, rota, yon


def _parametre():
    with open(LAB / "veri/sag_kol_parametre.csv", encoding="utf-8") as f:
        return {r["ad"]: r for r in csv.DictReader(f)}


def _s(x):  # saniye → tam sayı
    return int(round(x))


def derlem():
    oz = evre_ozeti(); L, C, P = oz["lifting"], oz["carrying"], oz["putting down"]
    nok, parca = rota()
    dirsek = _parametre()["dirsek"]
    bukme = int(round(math.degrees(float(dirsek["ust_rad"]))))
    hiz = round(C["hiz_max"], 2)
    kaldir_cm = int(round((L["yukseklik_son"] - L["yukseklik_bas"]) * 100))
    toplam = _s(P["son"])
    yol_m = sum(p["boy"] for p in parca)

    d = {}
    d["tanitim"] = [
        "Hello, I am a humanoid robot.",
        "I work in a cafe.",
        "I serve tea to the customers.",
        "I carry one glass at a time.",
        "My job starts in the morning.",
        "I don't drink tea.",
        "The robot works every day.",
        "It doesn't sit down.",
        "Do you like tea?",
        "Nice to meet you.",
    ]
    d["masa"] = [
        "There is a glass on the tray.",
        "There is a counter in the cafe.",
        "There are four tables near the window.",
        "There is a sugar bowl next to the glass.",
        "There are two chairs at each table.",
        "There isn't a glass on table four.",
        "Is there any tea in the pot?",
        "The tray is on the counter.",
        "The robot is between the counter and the tables.",
        "The glass is in my hand.",
    ]
    d["yetenek"] = [
        "I can carry a glass of tea.",
        f"My elbow can bend {bukme} degrees.",
        f"I can move the glass at {hiz} metres per second.",
        "I can't climb the stairs.",
        "I can't make coffee.",
        "Can you carry two glasses?",
        "No, I can't.",
        "Can I help you?",
    ]
    d["simdi"] = [
        f"I am lifting the glass now.",
        "I am holding the glass with my right hand.",
        f"I am carrying the glass to table four.",
        "I am walking slowly.",
        "I am not running.",
        "I am putting down the glass.",
        "The customer is waiting at the table.",
        "Are you waiting for your tea?",
        "We are cleaning the tables.",
    ]
    d["siparis"] = [
        "Good morning! Welcome to our cafe.",
        "What would you like to drink?",
        "Would you like tea or coffee?",
        "I'd like a glass of tea, please.",
        "Would you like sugar?",
        "Yes, please. Two sugars.",
        "Can I have some water, too?",
        "Of course.",
        "Anything else?",
        "No, thank you.",
        "Your tea is coming.",
        "Here you are. Enjoy your tea!",
    ]
    d["sorular"] = [
        "What is your name?",
        "Where is table four?",
        "How many glasses are on the tray?",
        "How long does the job take?",
        f"It takes about {toplam} seconds.",
        "Which table is yours?",
        "When does the cafe open?",
        "Who wants tea?",
        "Why are you stopping?",
        "Because there is a person in front of me.",
    ]
    d["adimlar"] = [
        "First, pick up the glass.",
        f"Then, lift it {kaldir_cm} centimetres.",
        "Next, carry it to the table.",
        "After that, put it down slowly.",
        "Finally, say: Enjoy your tea!",
        "Don't run with the glass.",
        "Keep the glass level.",
    ]
    d["telefon"] = [
        "Hello, this is the cafe robot.",
        "Can I speak to the manager, please?",
        "Hold on, please.",
        "I'm sorry, she is busy right now.",
        "Can I take a message?",
        "Yes, please. Two teas for table four.",
        "Could you say that again, please?",
        "Thank you for calling.",
    ]
    yonler = []
    for j, p in enumerate(parca):
        y = yon(p.get("donus")) if j else "go straight"
        yonler.append(f"{y[0].upper() + y[1:]} and walk {round(p['boy'], 1)} metres.")
    yonler += ["The table is on your left.", "Stop at the table.", "Go past the counter.", "Turn around and come back."]
    d["yol"] = yonler
    d["kurallar"] = [
        "You must keep the glass level.",
        f"You mustn't bend the elbow more than {bukme} degrees.",
        f"You mustn't move faster than {hiz} metres per second.",
        "You have to stop for people.",
        "You must say hello to every customer.",
        "You don't have to clean the floor.",
        "The robot has to wait at the counter.",
        "You must not touch hot glasses.",
    ]
    d["talimat"] = [
        "SAFETY CARD",
        "Read these rules before work.",
        "Check the battery.",
        "Pick up one glass at a time.",
        "Hold the glass with your right hand.",
        "Walk slowly near people.",
        "Do not spill the tea.",
        "Put the glass on the table, not on the edge.",
        "Return to the counter.",
    ]
    d["rapor"] = [
        f"I started work at the counter.",
        f"I lifted the glass in {_s(L['sure'])} seconds.",
        f"I carried it for {_s(C['sure'])} seconds.",
        f"I walked about {round(yol_m, 1)} metres.",
        f"I put it down in {_s(P['sure'])} seconds.",
        "I didn't spill the tea.",
        "The customer said thank you.",
        f"The job took {toplam} seconds.",
        "Was the tea hot? Yes, it was.",
        "Did you stop? No, I didn't.",
    ]
    hizlar = {k: v["hiz_max"] for k, v in oz.items()}
    en_uzun = max(oz, key=lambda k: oz[k]["sure"]); en_kisa = min(oz, key=lambda k: oz[k]["sure"])
    en_hizli = max(hizlar, key=hizlar.get)
    d["karsilastirma"] = [
        f"Carrying was longer than lifting.",
        f"Putting down was shorter than lifting.",
        f"{en_uzun.capitalize()} was the longest part of the job.",
        f"{en_kisa.capitalize()} was the shortest part.",
        f"The glass was faster in carrying than in lifting.",
        f"{en_hizli.capitalize()} was the fastest part.",
        "The counter is bigger than the table.",
        "Tea is more popular than coffee in our cafe.",
    ]
    d["plan"] = [
        "Tomorrow I am going to serve the garden tables.",
        "I am going to carry two glasses.",
        f"It will take about {toplam} seconds.",
        "The cafe will be busy on Saturday.",
        "I think the customers will like the new tea.",
        "I won't run with the glass.",
        "Are you going to order tea?",
        "I'll bring your tea in a minute.",
    ]
    return d


def hepsi():
    return [(b, c) for b, l in derlem().items() for c in l]
