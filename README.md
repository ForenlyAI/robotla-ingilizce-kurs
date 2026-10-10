# Kafedeki Robotla Okul İngilizcesi — kurs dosyaları

Forenly AI Academy'deki **Kafedeki Robotla Okul İngilizcesi** kursunun lab dosyaları. Derslerde ekranda gördüğünüz her Python oturumu ve her şekil bu betiklerle üretildi.

Kursu izlemek için program yazmanız gerekmez. Bu dosyalar, robotun cümlelerini kendiniz saymak ve bitirme raporunuzu denetlemek isteyenler içindir.

## Gerekenler

- **Python 3.10 veya üstü**, `numpy` (2.0 ya da üstü) ve `matplotlib`. Hepsi ücretsizdir.
- Kurulum: `python -m pip install -r requirements.txt`
- Bilgisayarınıza kurmak istemezseniz tarayıcıda çalışan bir not defterine (ör. Google Colab) bu klasörü yükleyip aynı betikleri çalıştırabilirsiniz.

## Nasıl çalıştırılır

1. Bu depoyu indirin (Code → Download ZIP) ve klasörde bir terminal açın.
2. Haftaları sırayla çalıştırın: `python hafta1.py`, `python hafta2.py`, `python hafta3.py`, `python hafta4.py`.
3. Betikler çalışınca `ekran/<ders>/` klasöründe şekiller (`.png`) ve Python oturum kayıtları (`.txt`), kökte de ölçülen sayılar (`OLCUMLER.json`) oluşur.
4. İsteğe bağlı: `python komut_ciz.py` oturum kayıtlarını derslerdeki gibi resme çizer (Pillow gerekir).

## Kendi raporunuzu denetleyin (bitirme projesi)

```python
from arac import kalip_say
rapor = ["I am a humanoid robot.", "I work in a cafe.", "Today I carried a glass of tea."]   # kendi sekiz cümleniz
{k: v for k, v in kalip_say(rapor).items() if v}
```

Kalıp bulucu kural tabanlıdır ve yalnız bu kursun fiil listesini (`arac.FIIL`) tanır; listede olmayan fiili "diğer" sayabilir. Gerekirse fiili listeye ekleyin.

## Sonucunuzu karşılaştırın

`beklenen/OLCUMLER.json` ekibimizin 2026-10-10 koşumunda ölçtüğü sayılardır; `beklenen/ekran/` aynı koşumun şekilleri ve oturum kayıtlarıdır.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ortak.py` | Kaydı okuma (`kayit`), yumuşatma, ölçüm yazma, oturum kaydı ve şekil kaydetme |
| `arac.py` | Evrelere ayırma, rota ve dönüş yönü; kelime ayırma, kalıp bulucu (`zaman_eki`, `kalip_say`), kelime sıklığı; çizim yardımcıları |
| `konusmalar.py` | Robotun 124 cümlesi (tanıtım, sipariş, telefon, yol, kurallar, rapor, plan…); sayılar kayıttan hesaplanır |
| `kaynaklar.py` | Kursun dayandığı müfredat ve düzey kaynakları |
| `hafta1.py` | Kendini tanıtmak: geniş zaman, There is / are, can, şimdiki zaman |
| `hafta2.py` | Sipariş almak: kibar istekler, soru kelimeleri, sıralı anlatım, telefon |
| `hafta3.py` | Yol ve talimat: yön tarifi, yer sözcükleri, must / have to, güvenlik kartı |
| `hafta4.py` | Geçmiş ve gelecek: geçmiş zaman, karşılaştırma, will / going to, günlük rapor denetleyicisi |
| `komut_ciz.py` | Oturum kayıtlarını resme çizer (isteğe bağlı) |
| `veri/cay_servisi_kaydi.csv` | Çay servisi benzetim kaydı: zaman, kol eklem açıları, bardağın konumu × 5666 örnek (saniyede 50) |
| `veri/sag_kol_parametre.csv` | Sağ kolun eklem tablosu (sınırlar, hız ve tork değerleri) |

## Veri ve müfredat hakkında

Robot verisi **benzetim kaydıdır**, gerçek robot ölçümü değildir; Forenly AI'nin [kafe projesinde](https://forenly.ai/work/cafe) bir insansı robotun çay servisini benzetimde yaptığı bir bölümden alınmıştır. Robotun cümlelerini kurs ekibi yazdı; içlerindeki süre, hız, yol ve açı sayıları kayıttan hesaplanır. Masa numarası, içecekler, müşteri replikleri ve kafe yerleşimi **ÖRNEKTİR**.

Konular MEB [İngilizce Dersi Öğretim Programı (2–8. sınıflar)](https://mufredat.meb.gov.tr/ProgramDetay.aspx?PID=327) 8. sınıf ünitelerine ve [Maarif Modeli İngilizce 9. sınıf](https://tymm.meb.gov.tr/ogretim-programlari/ingilizce-dersi-9-12/11) temalarına bağlanmıştır; ayrıntı `kaynaklar.py`.
