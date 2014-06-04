
#coding: utf-8
import pygame
from pygame.locals import *
import os
import sys

SCR_RECT = Rect(0, 0, 640, 480)

class PyAction:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("�ؓ��K���i�[")
        
        # �摜�̃��[�h
        Kinniku.left_image = load_image("python.gif", -1)                     # ������
        Kinniku.right_image = pygame.transform.flip(Kinniku.left_image, 1, 0)  # �E����
        Kinniku.right_image2 = load_image("kinniku.png", -1)  # ���Ⴊ��
        Kinniku.right_image3 = load_image("gunner.png", -1)  # �\��
        Shot.image = load_image("shot.png",-1) # �e�e
        Enemy.image = load_image("enemy.png",-1) # �G
        
        # �O���[�v�쐬
        self.all = pygame.sprite.RenderUpdates()
        Enemies = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        Kinniku.containers = self.all
        Shot.containers = self.all,shots
        Enemy.containers = self.all,Enemies
        Kinniku()

        # ���C�����[�v
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            collision_detection(shots, Enemies)
            self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def update(self):

        self.all.update()
    
    def draw(self, screen):

        screen.fill((0,0,0))
        self.all.draw(screen)
    
    def key_handler(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

def collision_detection(shots, Enemies):
	 enemy_collided = pygame.sprite.groupcollide(Enemies, shots, True, True)

class Kinniku(pygame.sprite.Sprite):

    MOVE_SPEED = 5.0  # �ړ����x
    JUMP_SPEED = 8.0  # �W�����v�̏����x
    GRAVITY = 0.4     # �d�͉����x
    reload_time = 15  # �e�̃����[�h����
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.right_image
        self.rect = self.image.get_rect()
        self.rect.bottom = SCR_RECT.bottom
        self.reload_timer = 0
        
        # ���������_�̈ʒu�Ƒ��x
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.fpvx = 0.0
        self.fpvy = 0.0
        
        # �n�ʂɂ��邩�ǂ���
        self.on_floor = False
        
        # �G�ʉ߁i�Ƃ肠�����j
        Enemy((500,400))
        Enemy((1000,300))
    def update(self):

        # �L�[���͎擾
        pressed_keys = pygame.key.get_pressed()

        # ���E�㉺�ړ�
        if pressed_keys[K_RIGHT]:
            self.image = self.right_image
            self.rect = self.image.get_rect()
            self.fpvx = self.MOVE_SPEED
            self.on_floor = False
        elif pressed_keys[K_LEFT]:
            self.image = self.left_image
            self.rect = self.image.get_rect()
            self.fpvx = -self.MOVE_SPEED
            self.on_floor = False
        elif pressed_keys[K_DOWN]:
        	self.image = self.right_image2
        	self.rect = self.image.get_rect()
        	self.fpvy = self.JUMP_SPEED
        	self.on_floor = False
        else:
            self.fpvx = 0.0
        
        # �e������
        if pressed_keys[K_RSHIFT]:
        	self.image = self.right_image3
        	if self.reload_timer > 0:
        		self.reload_timer -= 1
        	else:
        		Shot(self.rect.center)
        		self.reload_timer = self.reload_time

        # �W�����v
        if pressed_keys[K_UP]:
            if self.on_floor:
                self.fpvy = - self.JUMP_SPEED
                self.on_floor = False
        
        # ���x���X�V
        if not self.on_floor:
            self.fpvy += self.GRAVITY
        
        # ���������_�̈ʒu���X�V
        self.fpx += self.fpvx
        self.fpy += self.fpvy
        
        # ���n���������ׂ�
        if self.fpy > SCR_RECT.height - self.rect.height and self.image != self.right_image2:
            self.fpy = SCR_RECT.height - self.rect.height
            self.fpvy = 0
            self.on_floor = True
        elif self.fpy > SCR_RECT.height - self.rect.height and self.image == self.right_image2:
        	self.rect = self.image.get_rect()
        	self.fpy = SCR_RECT.height - self.rect.height
        	self.fpvy = 0
        	self.on_floor = True
        
        # ���������_�̈ʒu�𐮐����W�ɖ߂�
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)

class Shot(pygame.sprite.Sprite):
	speed = 9
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.rect = self.image.get_rect()
		self.rect.center = pos
	
	def update(self):
		self.rect.move_ip(self.speed, 0)
		if self.rect.top < 0:
			self.kill()

class Enemy(pygame.sprite.Sprite):
	speed = 2
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.rect = self.image.get_rect()
		self.rect.center = pos
		
	def update(self):
		self.rect.move_ip(-self.speed, 0)

def load_image(filename, colorkey=None):
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

if __name__ == "__main__":
    PyAction()
