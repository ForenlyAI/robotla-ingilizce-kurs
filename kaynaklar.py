"""Kafedeki Robotla Okul İngilizcesi — kursun dayandığı gerçek kaynaklar (müfredat ve düzey).
Hepsi 2026-10-10'da web'de açılarak doğrulandı (dogrulama alanı). Kayıt dışı bilimsel sayı kullanılmadı; derslerdeki bütün sayılar
benzetim kaydından (veri/cay_servisi_kaydi.csv), kol parametre tablosundan (veri/sag_kol_parametre.csv) ya da robotun cümle derleminin
sayımından (konusmalar.py) gelir. Masa numarası, içecekler, müşteri replikleri ve kafe yerleşimi ÖRNEK'tir."""

KAYNAKLAR = [
    dict(anahtar="meb2018", yazar="T.C. Millî Eğitim Bakanlığı, Talim ve Terbiye Kurulu Başkanlığı", yil=2018,
         baslik="İngilizce Dersi Öğretim Programı (İlkokul ve Ortaokul 2, 3, 4, 5, 6, 7 ve 8. Sınıflar)",
         yayin="Ankara: MEB · https://mufredat.meb.gov.tr/ProgramDetay.aspx?PID=327",
         kullanim="8. sınıf üniteleri: Friendship, Teen Life, In the Kitchen, On the Phone, The Internet, Adventures, Tourism, Chores, Science, Natural Forces",
         dogrulama="Program sayfası açıldı: İngilizce, 2–8. sınıflar; ünite adları okul konu listeleri ve il milli eğitim konu-soru dağılım belgeleriyle karşılaştırıldı"),
    dict(anahtar="tymm2024", yazar="T.C. Millî Eğitim Bakanlığı", yil=2024,
         baslik="Türkiye Yüzyılı Maarif Modeli — İngilizce Dersi (9–12. Sınıflar) Öğretim Programı, 9. sınıf",
         yayin="https://tymm.meb.gov.tr/ogretim-programlari/ingilizce-dersi-9-12/11",
         kullanim="9. sınıf temaları: School Life, Classroom Life, Personal Life, Family Life, Life in the House & Neighbourhood, "
                  "Life in the City & Country, Life in the World & Nature, Life in the Universe & Future (sayfada düzey B1.1)",
         dogrulama="Sayfa açıldı, sekiz tema adı ve düzey okundu (2026-10-10)"),
    dict(anahtar="coe2020", yazar="Council of Europe", yil=2020,
         baslik="Common European Framework of Reference for Languages: Learning, teaching, assessment — Companion volume",
         yayin="Strasbourg: Council of Europe Publishing · ISBN 978-92-871-8621-8 · https://rm.coe.int/16809ea0d4",
         kullanim="A1–A2 düzey adlandırması (kursun düzeyi)",
         dogrulama="Yayıncı sayfası ve künye web aramasıyla doğrulandı (2026-10-10)"),
]
