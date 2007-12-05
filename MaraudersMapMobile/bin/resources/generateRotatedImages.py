import Image

imageFile = 'gates.png'
numRotations = 24

image = Image.open(imageFile)
degrees = 360.0 / numRotations
for i in range(numRotations):
    image.rotate(i * degrees).save('gates_' + ('%03i' % (i * degrees)) + '.jpg')
