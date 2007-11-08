import Image

imageFile = 'gates.png'
numRotations = 16

image = Image.open(imageFile)
degrees = 360 / numRotations
for i in range(numRotations):
    image.rotate(i * degrees).save('gates_' + ('%03i' % (i * degrees)) + '.jpg')
