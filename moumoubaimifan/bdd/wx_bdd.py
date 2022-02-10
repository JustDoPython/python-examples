from PIL import Image
import os

path = 'D:/bdd/'
tx_img = Image.open(os.path.join(path,'tx.jpg'))
bdd_img = Image.open(os.path.join(path,'bdd.png'))

tx_rgba = tx_img.convert('RGBA')
bdd_rgba = bdd_img.convert('RGBA')

tx_x, tx_y = tx_rgba.size
bdd_x, bdd_y = bdd_rgba.size

scale = 5
img_scale = max(tx_x / (scale * bdd_x), tx_y / (scale * bdd_y))
new_size = (int(bdd_x * img_scale), int(bdd_y * img_scale))
bdd = bdd_rgba.resize(new_size, resample=Image.ANTIALIAS)
bdd.show()

bdd_x, bdd_y = bdd.size
tx_rgba.paste(bdd, (tx_x - bdd_x, tx_y - bdd_y), bdd)
tx_rgba.show()

tx_rgba.save(os.path.join(path,'tx_bdd.png'))
