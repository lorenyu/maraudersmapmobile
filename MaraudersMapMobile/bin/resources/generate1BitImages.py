import Image

imageFile = 'mapui1_mask.png'

image = Image.open(imageFile)
image.convert('1').save('mapui1_1bit.png')
