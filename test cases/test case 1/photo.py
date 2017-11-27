import PIL
from PIL import Image
import imagehash

hash1 = imagehash.phash(Image.open('test 1.jpg'))
print(hash1)

