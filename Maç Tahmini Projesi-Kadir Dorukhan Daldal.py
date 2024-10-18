import random

print("SPORT TOTO SÜPER LİG MAÇLARI TAHMİN PROJESİ")
print("Sadece Fenerbahçe(FB) baz alınarak yapılacaktır")

# Takım ve kategoriler
zayif_takimlar = ["Bodrumspor", "Eyüp", "Gaziantep", "Göztepe", "Hatay", "Kasımpaşa", "Kayserispor",
                  "Rizespor", "Samsunspor", "Altay"]
orta_takimlar = ["Adana Demirspor", "Alanyaspor", "Antalyaspor", "Başakşehir", "Konyaspor", "Sivasspor"]
guclu_takimlar = ["Beşiktaş", "Fenerbahçe", "Galatasaray", "Trabzonspor"]

tum_takimlar = zayif_takimlar + orta_takimlar + guclu_takimlar

# Takım puanlarını tutan sözlük
puanlar = {takim: 0 for takim in tum_takimlar}

# Takımın gücüne göre skor aralığını belirleyen fonksiyon
def skor_araligi_belirle(takim):
    if takim == "Fenerbahçe":
        return 3, 6  # Fenerbahçe için yüksek skor aralığı
    elif takim in guclu_takimlar:
        return 2, 5  # Diğer güçlü takımlar için orta-yüksek skor aralığı
    elif takim in orta_takimlar:
        return 1, 3  # Orta takımlar için orta skor aralığı
    elif takim in zayif_takimlar:
        return 0, 2  # Zayıf takımlar için düşük skor aralığı
    else:
        return 0, 1  # Varsayılan durum


def fikstur_olustur(takimlar):
    if len(takimlar) % 2 != 0:  # Takım sayısı tekse bir hayalet takım ekle
        takimlar.append("BYE")
    
    fikstur = []
    takim_sayisi = len(takimlar)
    for i in range(takim_sayisi - 1):
        hafta = []
        for j in range(takim_sayisi // 2):
            ev_sahibi = takimlar[j]
            deplasman = takimlar[takim_sayisi - 1 - j]
            if ev_sahibi != "BYE" and deplasman != "BYE":
                hafta.append((ev_sahibi, deplasman))
        takimlar.insert(1, takimlar.pop())  # Döngüyü kaydır
        fikstur.append(hafta)
    return fikstur

# Haftalık maçları simüle eden fonksiyon
def hafta_maclari(fikstur, dosya):
    for i, hafta in enumerate(fikstur):
        dosya.write(f"\n{i + 1}. Hafta Sonuçları:\n")
        print(f"{i + 1}. Hafta Sonuçları")

        for mac in hafta:
            ev_sahibi, deplasman = mac

            # Takım gücüne göre skorları belirleme
            ev_sahibi_skor = random.randint(*skor_araligi_belirle(ev_sahibi))
            deplasman_skor = random.randint(*skor_araligi_belirle(deplasman))

            # Maç sonucunu dosyaya ve ekrana yazdırma
            mac_sonucu = f"{ev_sahibi} {ev_sahibi_skor} - {deplasman_skor} {deplasman}"
            dosya.write(mac_sonucu + "\n")
            print(mac_sonucu)

            # Puanları güncelleme
            if ev_sahibi_skor > deplasman_skor:
                puanlar[ev_sahibi] += 3  
            elif ev_sahibi_skor < deplasman_skor:
                puanlar[deplasman] += 3  
            else:
                puanlar[ev_sahibi] += 1  
                puanlar[deplasman] += 1

# Fikstürü oluştur
fikstur = fikstur_olustur(tum_takimlar)

# Maç sonuçlarını bir dosyaya kaydetme
with open("mac_sonuclari.txt", "w", encoding="utf-8") as dosya:
    # Haftalık maçları simüle etme ve dosyaya yazdırma
    hafta_maclari(fikstur, dosya)

# Puan tablosunu sıralama
puan_tablosu = sorted(puanlar.items(), key=lambda x: x[1], reverse=True)

# Puan tablosunu hem dosyaya hem de ekrana yazdırma
with open("mac_sonuclari.txt", "a", encoding="utf-8") as dosya:
    dosya.write("\nSüper Lig Puan Tablosu\n")
    dosya.write("======================\n")
    for i, (takim, puan) in enumerate(puan_tablosu, start=1):
        dosya.write(f"{i}. {takim}: {puan} puan\n")
        print(f"{i}. {takim}: {puan} puan")
