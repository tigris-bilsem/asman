import rasterio
import numpy as np
import matplotlib.pyplot as plt

pre_fire_path = '/home/atalayb/Documents/nasa/spaceapps/islenmis_haritalar/S1A__IW___A_20210723T155034_VH_gamma0-rtc_db.tif'
post_fire_path = '/home/atalayb/Documents/nasa/spaceapps/islenmis_haritalar/S1A__IW___A_20210816T155035_VH_gamma0-rtc_db.tif'


with rasterio.open(pre_fire_path) as src_pre:
    pre_fire_img = src_pre.read(1)
    profile = src_pre.profile

with rasterio.open(post_fire_path) as src_post:
    post_fire_img = src_post.read(1)


target_rows = min(pre_fire_img.shape[0], post_fire_img.shape[0])
target_cols = min(pre_fire_img.shape[1], post_fire_img.shape[1])

pre_fire_clipped = pre_fire_img[:target_rows, :target_cols]
post_fire_clipped = post_fire_img[:target_rows, :target_cols]

print("Görüntüler aynı boyuta getirildi. Yeni Boyutlar:", pre_fire_clipped.shape)


log_ratio_change = post_fire_clipped - pre_fire_clipped

print("Değişim haritası (dB farkı) oluşturuldu.")

plt.figure(figsize=(12, 10))
im = plt.imshow(log_ratio_change, cmap='RdYlGn_r', vmin=-10, vmax=5)
plt.title('SAR Geri Saçılım Değişim Haritası (Yangın Etkisi)', fontsize=16)
plt.xlabel('Piksel (Boylam)')
plt.ylabel('Piksel (Enlem)')
cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
cbar.set_label('Geri Saçılım Değişimi (dB)', fontsize=12)
plt.savefig('yangin_etki_haritasi.png', dpi=300, bbox_inches='tight')
plt.show()


profile.update({
    'height': target_rows,
    'width': target_cols,
    'dtype': rasterio.float32,
    'count': 1
})

with rasterio.open('yangin_etki_haritasi.tif', 'w', **profile) as dst:
   
    change_map_to_save = np.nan_to_num(log_ratio_change, nan=-9999.0)
    dst.write(change_map_to_save.astype(rasterio.float32), 1)
    dst.nodata = -9999.0

print("Etki haritası 'yangin_etki_haritasi.png' ve 'yangin_etki_haritasi.tif' olarak kaydedildi.")
