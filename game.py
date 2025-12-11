#import pygame
import threading
import random
import math
import pandas as pd
import tensorflow as tf
import pygame

kerasModel = tf.keras.models.load_model("model4.keras")

pygame.init()

PI = 3.14159265358979

screen_width = 200
screen_height = 200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flight Game")


surf = pygame.Surface((40, 40))
surf.fill((255, 255, 255, 0))
pygame.draw.rect(surf, (0, 0, 0), pygame.Rect(10, 15, 20, 10))

rotation = 0

running = True
def set_interval(func, sec):
    def func_wrapper():
        global running
        if (running):
            set_interval(func, sec)
            func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class Controls:
    def __init__(self):
        self.right = False
        self.left = False
        
        self.boost = False
        
    def run(self):
        True
        
    def getOutputs(self):
        return {
            "right": 1 if self.right else 0,
            "left": 1 if self.left else 0,
            "boost": 1 if self.boost else 0
        }

class Actor:
    def __init__(self, controls):
        self.controls = controls
        
        self.boost = 1
        self.rotation = (PI + 0.3)
        self.dx = 0
        self.dy = 0
        self.x = 0
        self.y = 0
        
        self.targetX = 0
        self.targetY = 0
        self.targetdx = 0
        self.targetdy = 0
        self.targetGood = True
    
    def draw(self):
        surfy = pygame.transform.rotate(surf, self.rotation * 180 / PI)
        screen.blit(surfy, ((200 - surfy.get_width() / 2 + self.dx)/2, (0 - surfy.get_height() / 2 + self.y)/2))
        
        if (self.targetGood):
            pygame.draw.rect(screen, (0, 150, 0), pygame.Rect((self.targetX - 10)/2, (self.targetY - 10)/2, 10, 10))
        else:
            pygame.draw.rect(screen, (150, 0, 0), pygame.Rect((self.targetX - 10)/2, (self.targetY - 10)/2, 10, 10))
    
    def run(self):
        self.targetX += self.targetdx - self.dx / 100
        self.targetY += self.targetdy
        
        self.targetX = min(max(self.targetX, 0), 400)
        self.targetY = min(max(self.targetY, 50), 350)
        
        hit = math.sqrt((200 + self.dx - self.targetX)**2 + (self.y - self.targetY)**2) < 30
        if (self.targetX <= 0 or hit):
            self.targetX = 400
            self.targetY = random.randrange(500, 3500) / 10
            self.targetdx = random.randrange(-200, -100) / 100
            self.targetdy = random.randrange(-300, 300) / 100
            self.targetGood = random.randrange(0, 2) >= 1
            
        if (self.controls.right):
            self.rotation -= 0.05
            if (self.rotation < PI / 2):
                self.rotation = PI / 2
        if (self.controls.left):
            self.rotation += 0.05
            if (self.rotation > 3 * PI / 2):
                self.rotation = 3 * PI / 2
        
        self.dy += 1
        
        self.dx *= 0.95
        self.dy *= 0.95
        
        speed = dist(0, 0, self.dx, self.dy)
        if (self.controls.boost):
            speed += 0.1
        
        tempX = self.dx / speed
        tempY = self.dy / speed
        rotX = math.cos(self.rotation - PI)
        rotY = math.sin(self.rotation - PI)
        
        dot = tempX * rotX + tempY * rotY
        speed = (dot + 0.05) * speed
        newDir = (math.atan2(self.dy, self.dx) + PI / 2 + self.rotation * 10) / 11
        if (self.controls.boost and self.boost > 0):
            speed += 5 / 8
            self.dy -= 1 / 16
            self.boost -= 1 / 256
        if (not self.controls.boost):
            self.boost += 1 / 256
        self.boost = min(max(self.boost, 0), 1)
        self.dx = math.cos(newDir - PI) * speed
        self.dy = math.sin(newDir - PI) * speed
        
        self.dy += 2
        
        self.dx = min(max(self.dx, -50), 50)
        self.dy = min(max(self.dy, -5), 5)
        
        self.x += self.dx
        self.y += self.dy
        
        self.y = min(max(self.y, 0), 400)
        
        if (self.y >= 400):
            self.dy = 0
            self.dx = 0
        self.dy = min(max(self.dy, -5), 5)
        self.rotation = (self.rotation % (2 * PI) + 2 * PI) % (2 * PI)
    
    def getState(self):
        return {
            "y": round(self.y / 400 * 256) / 256,
            "dy": round((self.dy + 5) / 10 * 256) / 256,
            "dx": round((self.dx + 50) / 100 * 256) / 256,
            "rotation": round((self.rotation - PI / 2) / PI * 256) / 256,
            "boost": round(self.boost * 256) / 256,
            "targetX": round(self.targetX / 400 * 256) / 256,
            "targetY": round((self.targetY - 50) / 300 * 256) / 256,
            "targetdx": round((self.targetdx + 2) * 256) / 256,
            "targetdy": round((self.targetdy + 3) / 6 * 256) / 256,
            "targetGood": 1 if self.targetGood else -1
        }

class Gamer:
    def __init__(self):
        self.controls = Controls()
        
        self.actor = Actor(self.controls)
    
    def draw(self):
        screen.fill((255, 255, 255))
        self.actor.draw()
        
        pygame.draw.rect(screen, (50, 200, 50), pygame.Rect(5, 5, self.actor.boost * 50, 10))
    
    def run(self):
        self.controls.run()
        
        current = self.actor.getState()
        inputs = kerasModel.predict(pd.DataFrame({"y":[current["y"]],"dy":[current["dy"]],"dx":[current["dx"]],"rotation":[current["rotation"]],"boost":[current["boost"]],"targetX":[current["targetX"]],"targetY":[current["targetY"]],"targetdx":[current["targetdx"]],"targetdy":[current["targetdy"]],"targetGood":[current["targetGood"]]}))[0]
        print(inputs)
        self.controls.left = random.randrange(0, 100) <= inputs[0] * 100
        self.controls.right = random.randrange(0, 100) <= inputs[1] * 100
        self.controls.boost = random.randrange(0, 100) <= inputs[2] * 100
        self.controls.left = 50 <= inputs[0] * 100
        self.controls.right = 50 <= inputs[1] * 100
        self.controls.boost = 50 <= inputs[2] * 100
        
        self.actor.run()
        
        if (self.actor.dx == 0 and self.actor.dy == 0):
            self.actor.y = 0
            self.actor.rotation = PI + 0.3
            self.actor.boost = 1
    
    def getState(self):
        return self.actor.getState()
        
    def getInputs(self):
        return self.controls.getOutputs()

game = Gamer()

def draw():
    global game
    
    game.draw()
    
    game.run()
    
    #screen.fill((255, 255, 255))
    
    #surfy = pygame.transform.rotate(surf, rotation * 3.14159 / 180)
    #screen.blit(surfy, (30-surfy.get_width() / 2, 30 - surfy.get_height() / 2))
    #pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 10, 20, 20))
    
    pygame.display.flip()

set_interval(draw, 0.166)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()