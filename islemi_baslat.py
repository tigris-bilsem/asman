# Gerekli yardımcıları ve fonksiyonları çağırıyoruz
import os
from pyroSAR import identify, Archive
from pyroSAR.snap.util import geocode

# --------------------------------------------------------------------------
# --- YAPILANDIRMA: Sadece bu 3 satırı değiştirmen yeterli! ---
# --------------------------------------------------------------------------

# 1. İşleyeceğin SAR verisinin tam yolunu buraya yaz.
# Örnek: "C:/verilerim/S1A_... .zip"
SAR_DOSYA_YOLU = "S1A_IW_GRDH_1SDV_20210816T155035_20210816T155100_039257_04A28F_E1A9.SAFE.zip"

# 2. Meta verilerin kaydedileceği veritabanı dosyasının adını belirle.
# Bu dosya yoksa, kod onu kendi oluşturacak.
VERITABANI_ADI = "sar_katalogum.db"

# 3. İşlenmiş haritanın kaydedileceği klasörün adını belirle.
# Bu klasör yoksa, kod onu da kendi oluşturacak.
CIKTI_KLASORU = "islenmis_haritalar"


# --- Kodun Geri Kalanı Otomatik Çalışacak ---

try:
    # --- BÖLÜM 1: VERİTABANINA EKLEME ---
    print("----- BÖLÜM 1: Veritabanı İşlemleri Başlıyor -----")

    # Önce dosyanın kimliğini okutuyoruz
    print(f"'{os.path.basename(SAR_DOSYA_YOLU)}' dosyası okunuyor...")
    sahne = identify(SAR_DOSYA_YOLU)
    print("Dosya kimliği başarıyla okundu.")

    # Veritabanı kataloğumuzu açıyoruz (yoksa oluşturuyor)
    # 'with' komutu, işi bitince kataloğu güvenli bir şekilde kapatır.
    with Archive(VERITABANI_ADI) as arsiv:
        print(f"'{VERITABANI_ADI}' veritabanı açıldı.")
        
        # Sahnenin bilgilerini veritabanına ekliyoruz.
        arsiv.insert(sahne)
        print("Sahne meta verileri veritabanına başarıyla eklendi!")

    print("----- BÖLÜM 1 Tamamlandı -----\n")


    # --- BÖLÜM 2: VERİYİ İŞLEME (GEOCODING) ---
    print("----- BÖLÜM 2: SAR Verisi İşleniyor -----")
    print("pyroSAR, şimdi SNAP yazılımını kullanarak jeokodlama yapacak.")
    print("Bu işlem, bilgisayarınızın hızına bağlı olarak BİRKAÇ DAKİKA sürebilir. Lütfen bekleyin...")

    # geocode fonksiyonu bütün sihirli işleri yapar:
    # Düzeltme, hizalama ve haritaya dönüştürme.
    geocode(
        infile=SAR_DOSYA_YOLU,      # Hangi dosyayı işleyecek?
        outdir=CIKTI_KLASORU,       # Nereye kaydedecek?
        t_srs=4326,                 # Hangi harita projeksiyon sistemini kullansın? (4326: Standart Enlem/Boylam)
        spacing=20                  # Çıktı haritanın piksel boyutu ne olsun? (metre cinsinden)
    )

    # İşlem bittiğinde çıktı klasörünün yolunu gösteriyoruz.
    tam_cikti_yolu = os.path.abspath(CIKTI_KLASORU)
    print("\nİşlem başarıyla tamamlandı!")
    print(f"Sonuçlar şu klasöre kaydedildi: {tam_cikti_yolu}")
    print("----- BÖLÜM 2 Tamamlandı -----")


# --- Olası Hatalar İçin Kontroller ---
except FileNotFoundError:
    print(f"\n!!! HATA: Dosya bulunamadı !!!")
    print(f"Lütfen 'SAR_DOSYA_YOLU' değişkenini doğru ayarladığından emin ol: {SAR_DOSYA_YOLU}")
except RuntimeError as e:
    print(f"\n!!! CİDDİ HATA: Bir şeyler ters gitti !!!")
    print(f"Hata mesajı: {e}")
    print("\nBu hata genellikle SNAP yazılımının kurulu olmamasından veya doğru yapılandırılmamasından kaynaklanır.")
    print("Lütfen SNAP'in bilgisayarınızda kurulu ve çalışır durumda olduğunu kontrol edin.")
except Exception as e:
    print(f"\n!!! BEKLENMEDİK BİR HATA OLUŞTU !!!")
    print(f"Hata: {e}")