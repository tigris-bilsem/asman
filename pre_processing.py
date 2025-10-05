import rasterio
import numpy as np
import matplotlib.pyplot as plt

# --- DOSYA YOLLARINI BELİRLEYİN ---
# pyroSAR'ın ürettiği, sonu _TC.tif ile biten dosyalarınızın yollarını yazın
pre_fire_path = '/home/atalayb/Documents/nasa/spaceapps/islenmis_haritalar/S1A__IW___A_20210723T155034_VH_gamma0-rtc_db.tif'
post_fire_path = '/home/atalayb/Documents/nasa/spaceapps/islenmis_haritalar/S1A__IW___A_20210816T155035_VH_gamma0-rtc_db.tif'

# Görüntüleri rasterio ile açın ve NumPy dizisi olarak okuyun
with rasterio.open(pre_fire_path) as src_pre:
    pre_fire_img = src_pre.read(1) # İlk bandı oku
    profile = src_pre.profile # Coğrafi bilgileri (projeksiyon, boyut vb.) sakla

with rasterio.open(post_fire_path) as src_post:
    post_fire_img = src_post.read(1)

# pyroSAR kalibrasyon sonrası 0 değerlerini atayabilir, bunları analiz dışı bırakmak için NaN yapalım
pre_fire_img[pre_fire_img == 0] = np.nan
post_fire_img[post_fire_img == 0] = np.nan

# --- HATA DÜZELTME KODU BURADA BAŞLIYOR ---

# 1. İki görüntünün de şekillerini (shape) al
shape_pre = pre_fire_img.shape
shape_post = post_fire_img.shape

# 2. Hedef satır ve sütun sayılarını, her iki boyuttaki en küçük değer olarak belirle
target_rows = min(shape_pre[0], shape_post[0])
target_cols = min(shape_pre[1], shape_post[1])

# 3. Her iki görüntüyü de bu yeni hedef boyutlarına göre kırp (slice)
pre_fire_clipped = pre_fire_img[:target_rows, :target_cols]
post_fire_clipped = post_fire_img[:target_rows, :target_cols]

print("Görüntüler aynı boyuta getirildi.")
print("Yeni Boyutlar:", pre_fire_clipped.shape)

# --- HATA DÜZELTME KODU BURADA BİTİYOR ---

print("Yangın öncesi ve sonrası görüntüleri başarıyla okundu.")
print("Görüntü Boyutları:", pre_fire_img.shape)

# --- LOG RATIO DEĞİŞİM HARİTASI ---
# Görüntüler lineer ölçekte olduğu için önce logaritmik (dB) ölçeğe çevirelim
# 10 * log10(DN)
#pre_fire_db = 10 * np.log10(pre_fire_img)
#post_fire_db = 10 * np.log10(post_fire_img)
post_fire_db = post_fire_img
pre_fire_db= pre_fire_img

# Log Ratio = Yangın sonrası (dB) - Yangın öncesi (dB)
log_ratio_change = post_fire_db - pre_fire_db

print("Log Ratio değişim haritası oluşturuldu.")

# --- GÖRSELLEŞTİRME ---
plt.figure(figsize=(12, 10))

# Renk paletini ve aralığını ayarla
# Kırmızı tonlar büyük negatif değişimleri (yanmış alanları) gösterecek
im = plt.imshow(log_ratio_change, cmap='RdYlGn_r', vmin=-10, vmax=5)

plt.title('SAR Log Ratio Değişim Haritası (Yangın Etkisi)', fontsize=16)
plt.xlabel('Piksel (Boylam)')
plt.ylabel('Piksel (Enlem)')

# Renk çubuğu ekle
cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
cbar.set_label('Geri Saçılım Değişimi (dB)', fontsize=12)

# Görseli kaydet
plt.savefig('yangin_etki_haritasi.png', dpi=300, bbox_inches='tight')

plt.show()

# --- HARİTAYI GEOTIFF OLARAK KAYDETME (GIS YAZILIMLARINDA KULLANMAK İÇİN) ---
# Coğrafi bilgileri (profile) güncelle
profile.update(dtype=rasterio.float32, count=1)

with rasterio.open('yangin_etki_haritasi.tif', 'w', **profile) as dst:
    dst.write(log_ratio_change.astype(rasterio.float32), 1)

print("Etki haritası 'yangin_etki_haritasi.png' ve 'yangin_etki_haritasi.tif' olarak kaydedildi.")