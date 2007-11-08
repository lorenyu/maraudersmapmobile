from math import floor, fmod, pi

#note: this assumes theta is in radians

def getMap(theta):
    theta = theta * (180/pi)
    print "theta is"
    print theta
    realValue = int(theta/16)
    modValue = fmod(theta, 16)
    finalValue = None

#Need this minus because first image starts at 0
    if modValue < 8:
        finalValue = realValue-1 #floorValue
    else:
        finalValue = realValue #floorValue + 1

    pictureValue = finalValue * 22
    fileName = "gates_"
    if pictureValue < 100:
        fileName += "0"

    fileName += `pictureValue`

    return "c\\Data\\Images\\" + fileName

print getMap(pi/4)


    
