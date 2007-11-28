# mmmIcons.py
from graphics import *

print __name__
print "loading icons"

userIcon = Image.open("C:\\Data\\Images\\userIconCircle.jpg")
userIcon_mask = Image.new(userIcon.size, mode = 'L')
userIcon_mask.blit(Image.open("C:\\Data\\Images\\userIconCircle_mask.jpg"))

targetIcon = Image.open("C:\\Data\\Images\\star1.jpg")
targetIcon_mask = Image.new(targetIcon.size, mode = 'L')
targetIcon_mask.blit(Image.open("C:\\Data\\Images\\star_mask.jpg"))

targetLabel = Image.open("C:\\Data\\Images\\andyLabel.jpg")
targetLabel_mask = Image.new(targetLabel.size, mode = 'L')
targetLabel_mask.blit(Image.open("C:\\Data\\Images\\andyLabel_mask.jpg"))

#onebarsIcon = Image.open("C:\\Data\\Images\\1bars.jpg")
#onebarsIcon_mask = Image.new(onebarsIcon.size, mode = 'L')
#onebarsIcon_mask.blit(Image.open("C:\\Data\\Images\\1bars_mask.jpg"))

#twobarsIcon = Image.open("C:\\Data\\Images\\2bars.jpg")
#twobarsIcon_mask = Image.new(twobarsIcon.size, mode = 'L')
#twobarsIcon_mask.blit(Image.open("C:\\Data\\Images\\2bars_mask.jpg"))

#threebarsIcon = Image.open("C:\\Data\\Images\\3bars.jpg")
#threebarsIcon_mask = Image.new(threebarsIcon.size, mode = 'L')
#threebarsIcon_mask.blit(Image.open("C:\\Data\\Images\\3bars_mask.jpg"))

#fourbarsIcon = Image.open("C:\\Data\\Images\\4bars.jpg")
#fourbarsIcon_mask = Image.new(fourbarsIcon.size, mode = 'L')
#fourbarsIcon_mask.blit(Image.open("C:\\Data\\Images\\4bars_mask.jpg"))

fivebarsIcon = Image.open("C:\\Data\\Images\\5bars.jpg")
fivebarsIcon_mask = Image.new(fivebarsIcon.size, mode = 'L')
fivebarsIcon_mask.blit(Image.open("C:\\Data\\Images\\5bars_mask.jpg"))
