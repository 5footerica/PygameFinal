# left to do:
# Fix bump sound
# Animate player sprite
# Add labels
# Add NPCS
# Add shooting
# Add intro?
# Add user input for playing again

import pygame, random, sys
from pygame import *
from math import fabs

pygame.init()
lives = 3
score = 0
whatLevel = 1

WIN_WIDTH, WIN_HEIGHT = 640, 480                           # Defines size of window

DISPLAY = (WIN_WIDTH,WIN_HEIGHT)          # Display uses WIN_Width/Heigth as one variable
screen = pygame.display.set_mode(DISPLAY)

HALF_WIDTH = int(WIN_WIDTH / 2)           # To be used by camera
HALF_HEIGHT = int(WIN_HEIGHT / 2)

pygame.mixer.pre_init(44100, -16, 2, 2048)

pygame.init()

pygame.mixer.music.load('sounds/bgMusic.ogg')#load music
pygame.mixer.music.play(-1)
death = pygame.mixer.Sound('sounds/sizzle.ogg')
jump = pygame.mixer.Sound('sounds/jump.ogg')
door = pygame.mixer.Sound('sounds/door.ogg')
bump = pygame.mixer.Sound('sounds/bump.ogg')

def main():
    print """Welcome to this platformer game!
Use arrows to move around the screen, and spacebar to jump.
Find the door to get to the next level, and avoid a lava'y death!

Thank you for the semester, I learned a lot!
"""
    pygame.mixer.music.load('sounds/bgMusic.ogg')#load music
    pygame.mixer.music.play(-1)
    pygame.display.set_caption("Move with arrows")
    timer = pygame.time.Clock()
    background = pygame.Surface(screen.get_size())

    global lives
    print "Lives left: ", lives                                   # Prints lives at beginning of loop (label?)
    global score
    print "Total score: ", score
    
    up = down = left = right = running = False     # variables for moving player later

    entities = pygame.sprite.Group()               # sets properties of base sprites
    
    player = Player(32, 32,"images/stone.png")     # Creates instance of sprite from Player class
    
    platforms = []                                 # array to hold platform sprites
    x = y = 0                                      # starts are position 0,0 and read each character in array
    level = [
        "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "W                    LMMMMMMMMMR           W",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "W    LMMMMMMMMR                            W",
        "W                                          W",
        "W                          LMMMMMR         W",
        "W                                          W",
        "W                                          W",
        "W         LMMMMMR                          W",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "WLMMMMMMMMMMMMR              LMMMMR        W",
        "W                                          W",
        "W                                          W",
        "W                   S                      W",
        "W                   T                      W",
        "W              LMMMMMMMMMR                 W",
        "W                                          W",
        "GGGGGGGGGGGGGGFFFFFFFFFFFFFFFFFFGGGGGGGGGGGG",
        "HHHHHHHHHHHHHHEEEEEEEEEEEEEEEEEEHHHHHHHHHHHH",]

    level2 = [
        "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "WLMMMMMMMR                                 W",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "W                          LMMMMMMMMMMMMMMRW",
        "W                                          W",
        "W                                          W",
        "W                LMMMMMMMMMR               W",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "W        LMMMMMR                           W",
        "W                                          W",
        "W                                          W",
        "WLMMMR                                     W",
        "W                                          W",
        "W                                          S",
        "W     BBBBB  BBBBB  BBBBB  BBBBB  BBBBB    T",
        "GGGFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFGGGG",
        "HHHEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEHHHH",]

    level3 = [
        "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "WLMMMMMMMMMMMMMMR                          W",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "W                          LMMMMMMMMMMMMMMRW",
        "W                                          W",
        "W                                          W",
        "W                                          W",
        "WLMMMMMMMMR           LMMMMR               W",
        "W                                          W",
        "W                                          W",
        "W                               LMMMMMMMMMRW",
        "W                                          W",
        "W LMMMMR          S                        W",
        "W                 T                        W",
        "W                LMR                       W",
        "GFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFG",
        "HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEH",]
    # build the level
    global whatLevel
    if whatLevel == 1:
        for row in level:
            for col in row:                                  # will create a 32x32 platform
                if col == "G":
                    p = Platform(x, y,"images/ground.png")   # makes it a sprite of Platform class
                    platforms.append(p)                      # and add platform entity to sprite group
                    entities.add(p)
                if col == "H":
                    p = Platform(x, y,"images/ground2.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "W":
                    p = Platform(x, y,"images/wall.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "S":
                    p = Platform(x, y,"images/exitTop.png")
                    entities.add(p)
                if col == "T":
                    t = ExitBlock(x, y,"images/exitBottom.png")
                    platforms.append(t)
                    entities.add(t)
                if col == "L":
                    p = Platform(x, y,"images/LeftPlat2.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "M":
                    p = Platform(x, y,"images/MidPlat2.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "R":
                    p = Platform(x, y,"images/RightPlat2.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "C":
                    p = Platform(x, y,"images/cloud.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "F":                                 # Lava block that doesn't kill, makes player appear to sink in lava before dying
                    p = Platform(x, y,"images/lava.png")
                    entities.add(p)
                if col == "E":                                 # creates sprite of LavaBlock class, kills player 
                    e = LavaBlock(x, y, "images/lava2.png")
                    platforms.append(e)
                    entities.add(e)
                
                x += 32                                        # once column is finished, advance x by 32px
            y += 32                                            # once row is finished, advance y by 32px, reset x to 0 poisiton
            x = 0

    if whatLevel == 2:
        for row in level2:
            for col in row:                                  # will create a 32x32 platform
                if col == "G":
                    p = Platform(x, y,"images/ground.png")   # makes it a sprite of Platform class
                    platforms.append(p)                      # and add platform entity to sprite group
                    entities.add(p)
                if col == "H":
                    p = Platform(x, y,"images/ground2.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "B":
                    p = Platform(x, y,"images/Bridge.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "W":
                    p = Platform(x, y,"images/wall.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "S":
                    t = ExitBlock(x, y,"images/exitTop.png")
                    entities.add(t)
                if col == "T":
                    t = ExitBlock(x, y,"images/exitBottom.png")
 #                   door.play()
                    platforms.append(t)
                    entities.add(t)
                if col == "L":
                    p = Platform(x, y,"images/LeftPlat.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "M":
                    p = Platform(x, y,"images/MidPlat.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "R":
                    p = Platform(x, y,"images/RightPlat.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "C":
                    p = Platform(x, y,"images/cloud.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "F":                                 # Lava block that doesn't kill, makes player appear to sink in lava before dying
                    p = Platform(x, y,"images/lava.png")
                    entities.add(p)
                if col == "E":                                 # creates sprite of LavaBlock class, kills player 
                    e = LavaBlock(x, y, "images/lava2.png")
                    platforms.append(e)
                    entities.add(e)
                
                x += 32                                        # once column is finished, advance x by 32px
            y += 32                                            # once row is finished, advance y by 32px, reset x to 0 poisiton
            x = 0

    if whatLevel == 3:
        for row in level3:
            for col in row:                                  # will create a 32x32 platform
                if col == "G":
                    p = Platform(x, y,"images/ground.png")   # makes it a sprite of Platform class
                    platforms.append(p)                      # and add platform entity to sprite group
                    entities.add(p)
                if col == "H":
                    p = Platform(x, y,"images/ground2.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "W":
                    p = Platform(x, y,"images/wall.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "S":
                    t = ExitBlock(x, y,"images/exitTop.png")
                    entities.add(t)
                if col == "T":
                    t = ExitBlock(x, y,"images/exitBottom.png")
                    platforms.append(t)
                    entities.add(t)
                if col == "L":
                    p = Platform(x, y,"images/LeftPlat3.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "M":
                    p = Platform(x, y,"images/MidPlat3.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "R":
                    p = Platform(x, y,"images/RightPlat3.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "C":
                    p = Platform(x, y,"images/cloud.png")
                    platforms.append(p)
                    entities.add(p)
                if col == "F":                                 # Lava block that doesn't kill, makes player appear to sink in lava before dying
                    p = Platform(x, y,"images/lava.png")
                    entities.add(p)
                if col == "E":                                 # creates sprite of LavaBlock class, kills player 
                    e = LavaBlock(x, y, "images/lava2.png")
                    platforms.append(e)
                    entities.add(e)
                
                x += 32                                        # once column is finished, advance x by 32px
            y += 32                                            # once row is finished, advance y by 32px, reset x to 0 poisiton
            x = 0
    if whatLevel >= 4:
        win()
        
    # for the camera
    total_level_width  = len(level[0])*32                  # returns length of first level, [0], in array and times it by 32 = width of level
    total_level_height = len(level)*32                     # gives us height with same method
    camera = Camera(complex_camera, total_level_width, total_level_height)       # instance of camera class, pass wid/height, entities sprite group now contains plateform sprites + player
    entities.add(player)

    while 1:                                               # always true
        timer.tick(30)                                     # sets game speed

        for e in pygame.event.get():                       # when key is pressed/mouse is moved, go to event handler
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                pygame.quit()
                sys.exit()               # escape key
            # when key is pressed
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
                jump.play()
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYDOWN and e.key == K_SPACE:
                running = True
            # when key is released
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        # draw background
        bg = Surface((WIN_WIDTH,WIN_HEIGHT))
        if whatLevel == 1:
            BackGround = Background('images/background1.jpg', [-player.rect.x/2,-player.rect.y/3])
        if whatLevel == 2:
            BackGround = Background('images/background2.jpg', [-player.rect.x/2,-player.rect.y/3])
        if whatLevel == 3:
            BackGround = Background('images/background3.jpg', [-player.rect.x/2,-player.rect.y/3])
#        else:
#            BackGround = Background('images/background1.jpg', [-player.rect.x/2,-player.rect.y/3]) 
        bg.convert()
        screen.blit(BackGround.image, BackGround.rect)
        
        camera.update(player)                            # updates camera based on position of player

        player.update(up, down, left, right, running, platforms)    # update player, draw everything else
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        if lives == 0:
            dead()

        
        pygame.display.flip()

class Camera(object):
# sets camera for following target = player
# l = left, t = top, w= width, h = heigth 
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    # creates distances that are half a screen away from player left and top of current position
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h
    # makes sure camera does not go outside of width/height of screen
    l = min(0, l)                                  # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)          # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t)        # stop scrolling at the bottom
    t = min(0, t)                                  # stop scrolling at the top
    return Rect(l, t, w, h)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)        # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity): # is of type Entity, is a sprite, sets properties
    def __init__(self, x, y, imageString):         # sets x, y when initialixed (see player: 32 x 32)
        Entity.__init__(self) 
        self.xvel = 0                              # sets velocity
        self.yvel = 0
        self.onGround = False                      # Is player in the air?
        # sets visible part of sprite
        # sets the size of the visible surface, as opposed to size of object
        self.image = Surface((32,32))
        self.image = pygame.image.load(imageString).convert_alpha()
        # Sets player rect position of x,y and size of 32 x 32
        # 32 x 32 is the actual size of object, as opposed to what the surface is
        self.rect = Rect(x, y, 32, 32)

    def update(self, up, down, left, right, running, platforms):
        if up:                                     # check if true/false
            if self.onGround: self.yvel -= 10      # only jump if on the ground
        if down:
            pass
        if running:
            self.xvel = 12
        if left:                                   # goes left at -8 velocity
            self.xvel = -8
        if right:                                  # goes right at 8 velocity
            self.xvel = 8
        if not self.onGround:                      # if in air, increase y velocity until on ground
            self.yvel += 0.3                       # only accelerate with gravity if in the air
            if self.yvel > 100: self.yvel = 100    # max falling speed
        if not(left or right):
            self.xvel = 0
        self.rect.left += self.xvel                # increment in x direction
        self.collide(self.xvel, 0, platforms)      # do x-axis collisions
        self.rect.top += self.yvel                 # increment in y direction
        self.onGround = False;                     # assuming we're in the air
        self.collide(0, self.yvel, platforms)      # do y-axis collisions

    def collide(self, xvel, yvel, platforms):
        global lives
        global score
        global whatLevel
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, LavaBlock):
                    lives = lives - 1
                    death.play()
                    pygame.mixer.music.play(0)
                    print "You must try to avoid the lava!"
                    pygame.time.delay(1000)
                    main()
                if isinstance(p, ExitBlock):
                    score += 100
                    door.play()
                    pygame.time.delay(400)
                    whatLevel += 1
                    main()
                if xvel > 0:
 #                   pygame.mixer.music.play(-1)
                    self.rect.right = p.rect.left
                if xvel < 0:
#                    pygame.mixer.music.play(-1)
                    self.rect.left = p.rect.right
                if yvel > 0:
#                    pygame.mixer.music.play(-1)
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
#                    pygame.mixer.music.play(-1)
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                if fabs(yvel)>5 or fabs(xvel)>5:
                    bump.play()
                

class Platform(Entity):                             # is of Entity sprite, its property
    def __init__(self, x, y, imageString):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image = pygame.image.load(imageString).convert_alpha()
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class LavaBlock(Platform):
    def __init__(self, x, y, imageString):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image = pygame.image.load(imageString).convert_alpha()
        self.rect = Rect(x, y, 32, 32)

class ExitBlock(Platform):
    def __init__(self, x, y, imageString):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image = pygame.image.load(imageString).convert_alpha()
        self.rect = Rect(x, y, 32, 32)

def win():
    youWin = """Congratulations, you have have beaten this game! Would you like to play again?"""
    print youWin
    select = raw_input("Press y to play again, or n to quit: ")
    if select.lower() == "y":
        print "Here we go!"
        pygame.time.delay(600)
        reset()
    if select.lower() == "n":
        print "Well, thanks for playing!"
        pygame.time.delay(600)
        pygame.quit()
        sys.exit()
        
def dead():
    youLose = """Oh no! You've lost all of your lives... Would you like to play again? """
    print youLose
    select = raw_input("Press y to play again, or n to quit: ")
    if select.lower() == "y":
        print "Here we go!"
        pygame.time.delay(600)
        reset()
    if select.lower() == "n":
        print "Well, thanks for playing!"
        pygame.time.delay(600)
        pygame.quit()
        sys.exit()
    
def reset():
    global whatLevel
    global lives
    global score
    whatLevel = 1
    lives = 3
    score = 0
    main()

if __name__ == "__main__":
    main()
