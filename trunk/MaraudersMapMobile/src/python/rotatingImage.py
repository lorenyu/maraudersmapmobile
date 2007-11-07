import appuifw, key_codes, glcanvas, e32
from gles import *
from graphics import *

#vertices = array(GL_BYTE, 3, [
#    -1,1,1,  1,1,1,  1,-1,1,  -1,-1,1,
#    -1,1,-1, 1,1,-1, 1,-1,-1, -1,-1,-1 ])
#triangles = array(GL_UNSIGNED_BYTE, 3, [
#    1,0,3, 1,3,2, 2,6,5, 2,5,1, 7,4,5, 7,5,6,
#    0,4,7, 0,7,3, 5,4,0, 5,0,1, 3,7,6, 3,6,2 ])
vertices = array(GL_BYTE, 3, [
    -1,-1,0, 1,-1,0, 1,1,0, -1,1,0])
quads = array(GL_UNSIGNED_BYTE, 3, [
    0,1,2, 0,2,3])
texcoords = array(GL_FLOAT, 2, [
    0,0, 1,0, 1,1, 0,1])
colors = array(GL_UNSIGNED_BYTE, 4, [
    0,255,0,255, 0,0,255,255, 0,255,0,255, 255,0,0,255,
    0,0,255,255, 255,0,0,255, 0,0,255,255, 0,255,0,255 ])

running = 1
turning_axis = 0
texture = None

def resize():
    #Resize handler
    glViewport(0, 0, canvas.size[0], canvas.size[1])
    aspect = float(canvas.size[1]) / float(canvas.size[0])
    glMatrixMode( GL_PROJECTION )
    glLoadIdentity()
    glFrustumf( -1.0, 1.0, -1.0*aspect, 1.0*aspect, 3.0, 1000.0 )
    
def initgl():
    global render
    #Initializes OpenGL and sets up the rendering environment
    glClearColor( 0.0, 0.0, 0.0, 1.0 )# Set the screen background color.
    glEnable( GL_CULL_FACE  )# Enable back face culling.
    resize()# Initialize viewport and projection.
    glMatrixMode( GL_MODELVIEW )
    glEnableClientState( GL_VERTEX_ARRAY )# Enable vertex arrays.
    glVertexPointerb(vertices)# Set array pointers.
    glEnableClientState( GL_TEXTURE_COORD_ARRAY )
    glTexCoordPointerf(texcoords)
    #glEnableClientState( GL_COLOR_ARRAY ) # Enable color arrays.
    #glColorPointerub(colors )# Set color pointers.
    glShadeModel( GL_SMOOTH )# Set the initial shading mode
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_FASTEST )# no perspective correction
    loadTexture()
    
def loadTexture():
    global texture
    
    texture = glGenTextures(1)    

    glBindTexture(GL_TEXTURE_2D, texture)
	
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    #glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, TEX_W, TEX_H, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex)
    image = Image.open("C:\\Data\\Images\\nerd.jpg")
    w, h = image.size
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, image)

def drawbox(aSizeX, aSizeY, aSizeZ):
    #Draws a box with triangles.Scales the box to the given size using glScalef.
    glScalef( aSizeX, aSizeY, aSizeZ )
    
    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
    glBindTexture(GL_TEXTURE_2D, texture)
    
    glDrawElementsub(GL_TRIANGLES, quads)
    
    glDisable(GL_TEXTURE_2D)
    
    #glDrawElementsub( GL_TRIANGLES, triangles )

def redraw(frame):
    global turning_axis
    #Draws & animates the objects. The frame number determines the amount of rotation.
    iFrame = frame
    glMatrixMode( GL_MODELVIEW )
    cameraDistance = 100
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    
    # Animate and draw box
    glLoadIdentity() # brand new coordinate system, so translate then rotate!
    #gl translate x - zooming in and out (pushing back in space)
    glTranslatex( 0 , 0 , -cameraDistance << 16)
    drawbox( 15.0, 15.0, 15.0 )

def set_exit():
    global running, canvas
    canvas=None
    running = 0

def keys(event):
    global turning_axis
    if event['keycode'] == key_codes.EKeyDownArrow: turning_axis = 1
    elif event['keycode'] == key_codes.EKeyRightArrow: turning_axis = 2
    elif event['keycode'] == key_codes.EKeyLeftArrow: turning_axis = 3
    elif event['keycode'] == key_codes.EKeyUpArrow: turning_axis = 0

appuifw.app.exit_key_handler=set_exit
appuifw.app.screen = 'normal'
canvas=glcanvas.GLCanvas(redraw_callback=redraw, event_callback=keys, resize_callback=resize)
appuifw.app.body=canvas
initgl()

while running:
    canvas.drawNow()
    e32.ao_sleep(0.0001)


