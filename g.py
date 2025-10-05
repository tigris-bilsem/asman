# 1. Adım: Akıllı yardımcımızı (pyroSAR'ı) işe çağırıyoruz.
# Sadece 'identify' fonksiyonu bize lazım.
from pyroSAR import identify

# 2. Adım: Yardımcımıza, kimliğini okuyacağı dosyanın adresini gösteriyoruz.
# BURAYI KENDİ DOSYA YOLUNLA DEĞİŞTİR!
# Bu, NASA'dan indirdiğin .zip uzantılı veya klasöre çıkarılmış SAR verisinin yolu olmalı.
dosya_yolu = "S1A_IW_GRDH_1SDV_20210723T155034_20210723T155059_038907_049743_FA4D.zip"


# 3. Adım: "Oku bakalım bu dosyanın kimliğini" diyoruz.
# identify fonksiyonu dosyayı okur ve bütün bilgileri "sahne" adında bir kutuya koyar.
try:
    sahne = identify(dosya_yolu)

    # 4. Adım: "Bana özet geç" diyoruz.
    # Yardımcımızın okuduğu bilgileri ekrana yazdırıyoruz.
    print("----- Dosya Başarıyla Okundu! -----")
    print(sahne)

    print("\n----- Bazı Önemli Bilgiler -----")
    print(f"Sensör: {sahne.sensor}")
    print(f"Çekim Modu: {sahne.acquisition_mode}")
    print(f"Yörünge: {sahne.orbit}")
    print(f"Çekim Başlangıç Zamanı: {sahne.start}")
    print(f"Polarizasyonlar: {sahne.polarizations}")

except FileNotFoundError:
    print(f"HATA: Dosya bulunamadı! Lütfen dosya yolunu kontrol et: {dosya_yolu}")
except Exception as e:
    print(f"Bir hata oluştu: {e}")