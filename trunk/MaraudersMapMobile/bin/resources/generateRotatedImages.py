import Image

imageFile = 'gates.png'
numRotations = 16

image = Image.open('gates.png')
for i in range(16):
    image.rotate(i * degrees).save('gates_' + ('%03i' % (i * degrees)) + '.jpg')
