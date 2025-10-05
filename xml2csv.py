import os
import csv
from pyroSAR.drivers import identify

def nasa_xml_to_csv(indir, outfile):
    """
    NASA'dan indirilen SAR verilerinin meta verilerini okur ve bir CSV dosyasına yazar.

    Args:
        indir (str): NASA'dan indirilen verilerin bulunduğu ana klasör.
                     Bu klasör, her bir SAR ürünü için alt klasörler içermelidir.
        outfile (str): Oluşturulacak CSV dosyasının adı ve yolu.
    """
    # Tüm meta verileri depolamak için bir liste oluştur
    all_metadata = []

    # Belirtilen klasördeki tüm dosya ve klasörleri tara
    for item in os.listdir(indir):
        item_path = os.path.join(indir, item)
        
        # Sadece klasörleri dikkate al (genellikle her SAR ürünü bir klasördedir)
        if os.path.isdir(item_path):
            try:
                # pyroSAR'ın sahneyi tanımlamasını ve meta verileri çıkarmasını sağla
                scene = identify(item_path)
                
                # Meta verileri bir sözlük olarak al
                # scene.meta, tüm meta verileri içeren bir sözlüktür
                metadata = scene.meta
                
                # Hangi dosyadan okunduğunu belirtmek için dosya yolunu da ekle
                metadata['source_file'] = item_path
                
                all_metadata.append(metadata)
                print(f"Başarıyla okundu: {item_path}")

            except Exception as e:
                print(f"Hata: {item_path} okunurken bir sorun oluştu - {e}")

    if not all_metadata:
        print("Hiçbir meta veri bulunamadı.")
        return

    # CSV başlıklarını belirlemek için ilk meta veri sözlüğünün anahtarlarını kullan
    # Tüm sözlüklerdeki tüm olası anahtarları toplamak daha sağlam bir yöntemdir
    header = set()
    for meta in all_metadata:
        header.update(meta.keys())
    header = sorted(list(header))

    # CSV dosyasını yazma modunda aç
    with open(outfile, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        
        # Başlığı yaz
        writer.writeheader()
        
        # Tüm meta verileri satır satır yaz
        writer.writerows(all_metadata)

    print(f"\nCSV dosyası başarıyla oluşturuldu: {outfile}")

# --- Betiği Çalıştırma ---
if __name__ == '__main__':
    # NASA verilerinin bulunduğu ana klasörün yolunu belirtin
    # Örnek: r"C:\Users\kullanici_adiniz\Indirilenler\NASA_SAR_Verileri"
    input_directory = "S1A_IW_GRDH_1SDV_20210723T155034_20210723T155059_038907_049743_FA4D.SAFE/annotation/"
    
    # Çıktı olarak oluşturulacak CSV dosyasının adını belirtin
    output_csv_file = "nasa_sar_metadata.csv"

    if input_directory == "BURAYA_NASA_VERILERININ_OLDUGU_KLASOR_YOLUNU_YAZIN":
        print("Lütfen 'input_directory' değişkenine NASA verilerinin bulunduğu klasörün yolunu belirtin.")
    else:
        nasa_xml_to_csv(input_directory, output_csv_file)