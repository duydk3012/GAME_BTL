import pygame
import math
import os
import random
import sys
from scripts.utils import load_image,load_images,Animation
from scripts.entities import PhysicsEntity,Player,Enemy
from scripts.cungthu import CungThu
from scripts.bosschim import BossChim
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.phanthan import PhanThan
import pygame
import pygame
from moviepy.editor import VideoFileClip


#make your game its own object
class Game:
    def __init__(self):
        pygame.init()
       
        # đặt tên ứng dụng
        pygame.display.set_caption('BLACK MYTH WUKONG')
        self.screen = pygame.display.set_mode((1200,800))
        #tốc đọ khung hình
        self.clock = pygame.time.Clock() 

        #dichuyen
        self.movement =[False,False]
       
        #load_image
        self.assets={
            'decor':load_images('tiles/decor',(50,50),(0,0,0)),# trả về 1 mảng ảnh png  
            'grass':load_images('tiles/grass',(50,50),(0,0,0)),
            'grass2':load_images('tiles/grass2',(50,50),(255,255,255)),
            'large_decor':load_images('tiles/large_decor',None,(0,0,0),5),
            'stone':load_images('tiles/stone',(50,50),(0,0,0)),
            'stone2':load_images('tiles/grass2',(50,50),(255,255,255)),

            'player':load_image('entities/player.png',(95,125),(255,255,255)),
            'background':load_image('background.png',(1200,800)),
            'tree':load_images('tiles/tree',None,(255,255,255),5),
            'clouds':load_images('clouds',None,(0,0,0)),
            
            'enemy/idle': Animation(load_images('entities/enemy/idle',(75, 100),(0,0,0)), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run',(75,100),(0,0,0)), img_dur=4),

            'cungthu/idle': Animation(load_images('entities/cungthu/idle',(200, 200),(255,255,255)), img_dur=6),
            'cungthu/run': Animation(load_images('entities/cungthu/run',(200,200),(255,255,255)), img_dur=4),
            'cungthu/attack': Animation(load_images('entities/cungthu/attack',(200,200),(255,255,255)), img_dur=9,loop=False),
            'cungthu/attackngoi': Animation(load_images('entities/cungthu/attackngoi',(200,200),(255,255,255)), img_dur=5,loop=False),
            'cungthu/attackgan': Animation(load_images('entities/cungthu/attackgan',(200,200),(255,255,255)), img_dur=7,loop=False),
            'cungthu/attackchuanbigandam': Animation(load_images('entities/cungthu/attackchuanbigandam',(200,200),(255,255,255)), img_dur=15,loop=False),
            'cungthu/attackgandam': Animation(load_images('entities/cungthu/attackgandam',(200,200),(255,255,255)), img_dur=7,loop=False),
            'cungthu/hurt': Animation(load_images('entities/cungthu/hurt',(200,200),(255,255,255)), img_dur=17,loop=False),
            'cungthu/die': Animation(load_images('entities/cungthu/die',(200,200),(255,255,255)), img_dur=12,loop=False),
            

            'bosschim/idle': Animation(load_images('entities/bosschim/idle',(400, 400),(255,255,255)), img_dur=10),
            'bosschim/walk': Animation(load_images('entities/bosschim/walk',(400,400),(255,255,255)), img_dur=4),
            'bosschim/attackkiemchuanbi': Animation(load_images('entities/bosschim/attackiemchuanbi',(400,400),(255,255,255)), img_dur=15,loop=False),
            'bosschim/attackkiem': Animation(load_images('entities/bosschim/attackkiem',(400,400),(255,255,255)), img_dur=5,loop=False),
            'bosschim/attackgan': Animation(load_images('entities/bosschim/attackgan',(400,400),(255,255,255)), img_dur=9,loop=False),
            'bosschim/hurt': Animation(load_images('entities/bosschim/hurt',(400,400),(255,255,255)), img_dur=7,loop=False),
            'bosschim/die': Animation(load_images('entities/bosschim/die',(400,400),(255,255,255)), img_dur=12,loop=False),
            'bosschim/win': Animation(load_images('entities/bosschim/win',(400,400),(255,255,255)), img_dur=31,loop=True),
            'bosschim/tipcan': Animation(load_images('entities/bosschim/tipcan',(400,400),(255,255,255)), img_dur=6,loop=True),

            'player/idle':Animation(load_images('entities/player/idle',(95,125),(255,255,255)),img_dur=15),
            'player/run':Animation(load_images('entities/player/run',(95,125),(255,255,255)),img_dur=10),
            'player/phanthanskill':Animation(load_images('entities/player/phanthanskill',(95,125),(255,255,255)),img_dur=12,loop=False),
            'player/jump':Animation(load_images('entities/player/jump',(95,125),(255,255,255))),
            'player/block':Animation(load_images('entities/player/block',(95,125),(255,255,255))),
            'player/hurt':Animation(load_images('entities/player/hurt',(95,125),(255,255,255)),img_dur=8,loop=False),
            
            'player/attack':Animation(load_images('entities/player/attack',(300,300),(255,255,255)),img_dur=5,loop=False),
            'particle/leaf': Animation(load_images('particles/leaf',(40,40),(0,0,0)), img_dur=30, loop=False),
            'particle/particle': Animation(load_images('particles/particle',(50,50),(0,0,0)), img_dur=12, loop=False),
            'particle/particlewukong': Animation(load_images('particles/particlewukong',(50,50),(0,0,0)), img_dur=12, loop=False),


            'phanthan/idle':Animation(load_images('entities/player/idle',(95,125),(255,255,255)),img_dur=15),
            'phanthan/run':Animation(load_images('entities/player/run',(95,125),(255,255,255)),img_dur=10),
            'phanthan/jump':Animation(load_images('entities/player/jump',(95,125),(255,255,255))),
            'phanthan/hurt':Animation(load_images('entities/player/hurt',(95,125),(255,255,255)),img_dur=8,loop=False),

            #'player/slide':Animation(load_images('entities/player/slide',(95,125),(255,255,255))),
            'phanthan/attack':Animation(load_images('entities/player/attack',(300,300),(255,255,255)),img_dur=6,loop=False),
            'phanthan/die':Animation(load_images('entities/player/die',(200,200),(0,0,0)),img_dur=10,loop=False),


            'gun': load_image('gun.png',(25,25),(0,0,0)),
            'projectile': load_image('projectile.png',(20,15),(0,0,0)),
            'cungten1': load_image('cungten1.png',(80,6),(0,0,0)),
            'cungten2': load_image('cungten2.png',(80,6),(255,255,255)),
            'kiemnangluong1': load_image('kimnl1.png',(100,180),(0,0,0)),
            'kiemnangluong2': load_image('kimnl2.png',(100,180),(0,0,0)),
            
            #'intro':Animation(load_images('tiles/batdau',(1200,800)),img_dur=10,loop=False)
            'intro':load_image('intro.png',(1200,800)),
            
        }
        self.sfx={
            'chuyencanh':pygame.mixer.Sound('data/sfx/chuyencanh.mp3'),
            'chamvukhi':pygame.mixer.Sound('data/sfx/chamvukhi.mp3'),
            'tocbien':pygame.mixer.Sound('data/sfx/tocbien.mp3'),
            'tocbienquai':pygame.mixer.Sound('data/sfx/tocbienquai.mp3'),
            'bidanh':pygame.mixer.Sound('data/sfx/bidanh.mp3'),
            'wukongvoicechieudai':pygame.mixer.Sound('data/sfx/wukongvoicechieudai.mp3'),
            'boom':pygame.mixer.Sound('data/sfx/boom.mp3')
        }
        self.sfx['chuyencanh'].set_volume(0.01)
        self.sfx['boom'].set_volume(0.01)
        self.sfx['tocbien'].set_volume(0.5)
        self.sfx['tocbienquai'].set_volume(5.1)
        self.sfx['bidanh'].set_volume(7)
        self.sfx['chamvukhi'].set_volume(5.1)
        self.sfx['wukongvoicechieudai'].set_volume(1.1)

        self.clip = VideoFileClip("data/demo.mp4")
        self.show_intro_video()  # Play the intro video

        

        
        #clouds1
        self.clouds1 = Clouds(self.assets['clouds'],count = 2)
    
        
        self.level = 0
        self.load_level(self.level)


        #clouds
        self.clouds = Clouds(self.assets['clouds'],count = 9)
        #soluongphanthan
        self.anhem=4
    
    def show_intro_video(self):
        # Play the intro video
        intro_duration = self.clip.duration  # Get the duration of the video
        start_time = pygame.time.get_ticks()
        pygame.mixer.music.load('data/intro.mp3')
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)
        while True:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) / 1000.0

            if elapsed_time >= intro_duration:
                break  # Exit after the video duration

            # Get the frame corresponding to the elapsed time
            frame = self.clip.get_frame(elapsed_time)

            # Convert the frame to a Pygame surface
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            # Blit the frame onto the screen
            self.screen.blit(pygame.transform.scale(frame_surface, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(30)  # Set the frame rate

            # Handle events (e.g., for skipping the video)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Skip the video by pressing space
                        return
    def load_level(self, map_id):

        self.sfx['chuyencanh'].play()

        
        #khaibao image player va tilemap
        self.player = Player(self,(400,-1700),(95,125))
       
        self.tilemap = Tilemap(self,tile_size=50)
      

        self.tilemap.load(str(map_id) + '.json')
        # hịu ứng lá rơi  nhờ extract map để bik vị trí spawwn
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(50 + tree['pos'][0],50  + tree['pos'][1], 100, 130))
        for tree in self.tilemap.extract([('tree', 0)], keep=True):
            self.leaf_spawners.append(pygame.Rect(150 + tree['pos'][0],150  + tree['pos'][1], 500, 1000))  
        for tree in self.tilemap.extract([('tree', 1)], keep=True):
            self.leaf_spawners.append(pygame.Rect(150 + tree['pos'][0],150  + tree['pos'][1], 500, 1000))   

        #enemy
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1),('spawners', 2),('spawners', 3)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time =0
            if spawner['variant'] == 1:
                self.enemies.append(Enemy(self, spawner['pos'], (75, 100)))
            if spawner['variant'] == 2:
                self.enemies.append(CungThu(self, spawner['pos'], (75, 100)))
            if spawner['variant'] == 3:
                self.enemies.append(BossChim(self, spawner['pos'], (75, 100)))
            
        self.projectiles = [] #đạn bắn
        self.particles = []
        self.sparks = []   #hiệu ứng
        self.scroll =[0,0]
        self.dead = 0
        self.phanthans=[]  #skill

        self.screenshake=0 #rung lắc
        self.transition =-30


    # Hàm vẽ thanh máu
    def draw_health_bar(self,screen, x, y, current_hp, max_hp,color=(0,0,0),width=200,height=20):
        # Kích thước của thanh máu
        bar_width = width
        bar_height = height
        # Tính toán chiều rộng của thanh máu dựa trên HP
        fill_width = int((current_hp / max_hp) * bar_width)

        # Màu sắc
        bar_color = color  # Màu đỏ cho thanh máu
        background_color = (128, 128, 128)  # Màu xám cho viền

        # Vẽ thanh máu nền (màu xám)
        pygame.draw.rect(screen, background_color, (x, y, bar_width, bar_height))
        # Vẽ thanh máu thực sự (màu đỏ)
        pygame.draw.rect(screen, bar_color, (x, y, fill_width, bar_height))
    def add_player(self):
        if self.player.flip:
            x = self.player.pos[0]-  random.randint(75,150)# Tạo khoảng cách giữa các nhân vật
        else:
            x = self.player.pos[0]+  random.randint(75,150)
        y = self.player.pos[1] -  random.randint(0,100)        
        new_player = PhanThan(self, (x, y), (95,125) )
        if len(self.phanthans) <self.anhem :
            self.player.mana-=5
            self.phanthans.append(new_player)
            self.sfx['tocbienquai'].play()
            for i in range(30):
                angle = random.random() * math.pi * 2
                speed = random.random() * 2
                self.sparks.append(Spark(new_player.rect().center, angle, 2 + random.random()))
                self.particles.append(Particle(self, 'particle', new_player.rect().center, velocity=[math.cos(angle + math.pi) * speed , math.sin(angle + math.pi) * speed ], frame=random.randint(0, 7)))

    
    def run(self):
        current_music = None
        # Giả sử bạn đã có lớp Animation và đã tạo đối tượng animation với hình ảnh intro
       
        while True:
            # Kiểm tra và phát nhạc phù hợp với level hiện tại

            if self.level == 0 and current_music != 'intro':
                self.anhem=0

                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/intro.mp3')
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1) # Phát nhạc lặp lại
                current_music = 'intro'
            elif self.level == 1 and current_music != 'khoidau':
                self.anhem=4
                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/khoidau.mp3')
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                current_music = 'khoidau'

           
            #camera theo player
            self.scroll[0]+=(self.player.rect().centerx-self.screen.get_width()/2-self.scroll[0])/50
            self.scroll[1]+=(self.player.rect().centery-self.screen.get_height()/2-self.scroll[1])/3
            render_scroll =(int(self.scroll[0]),int(self.scroll[1]))

        
            #BG
            if self.level ==0 :
                
                self.screen.blit(self.assets['intro'],(0,0))
                render_scroll=(0,0)
            else:
                self.screen.blit(self.assets['background'],(0,0))
                

                
            self.screenshake = max(0,self.screenshake-1)

            
            #cloud
            self.clouds.update()
            self.clouds.render(self.screen,offset = render_scroll)

            #tilemap
            self.tilemap.render(self.screen,offset = render_scroll)

            #đạn
            # [[x, y], direction, timer,loaidan] cáu tạo projectile
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1 #timer
                img = self.assets[ projectile[3]]
                self.screen.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1])) # chia chia là lấy center 

                # check xem chạm tile map thì mất 
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    if  projectile[3] =='kiemnangluong1' or projectile[3] =='kiemnangluong2':
                        self.screenshake = max(40,self.screenshake)
                        for i in range(20):
                            self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 5 + random.random()))
                    else:
                        for i in range(10):
                            self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))

                #bay lâu quá cx cút        
                elif projectile[2] > 1360:
                    self.projectiles.remove(projectile)

                # chạm người đang ko dang dash cx cút
                elif abs(self.player.dashing) < 50:
                    if  projectile[3] =='kiemnangluong1' or projectile[3] =='kiemnangluong2':
                        if self.player.recttuongtac().collidepoint(projectile[0][0]+random.randint(-5,5),projectile[0][1]+random.randint(-45,45)) :
                            if not self.player.blocking:
                                self.projectiles.remove(projectile)
                                self.player.hp-=1
                                self.sfx['bidanh'].play()
                                self.screenshake = max(20,self.screenshake)
                                for i in range(30):
                                    angle = random.random() * math.pi * 2
                                    speed = random.random() * 5
                                    self.sparks.append(Spark(self.player.rect().center, angle, 3 + random.random()))
                                    #self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed , math.sin(angle + math.pi) * speed ], frame=random.randint(0, 7)))
                            else:
                                self.player.stamina-=1.5
                                self.screenshake = max(random.randint(16,60),self.screenshake)
                                self.sfx['chamvukhi'].play()
                                self.projectiles.remove(projectile)
                                for i in range(10):
                                    self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 5 + random.random()))
                    elif self.player.recttuongtac().collidepoint(projectile[0]) and not self.player.blocking: #cho biết điểm pos của đạn có nằm trong hình chữ nhật hay không.
                        # còn thêm colliderList nữa
                        self.projectiles.remove(projectile)
                        self.player.hp-=1
                        self.sfx['bidanh'].play()
                        self.screenshake = max(16,self.screenshake)
                        for i in range(10):
                                    self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                    elif self.player.recttuongtac().collidepoint(projectile[0]) and  self.player.blocking:
                        self.projectiles.remove(projectile)
                        self.sfx['chamvukhi'].play()
                        self.player.stamina-=1
                        for i in range(10):
                            self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))

                    
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.screen, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)              
            #ênmy
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                
                enemy.render(self.screen, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)
                else:
                    if enemy.type=='bosschim'and self.player.pos[0]>2800 and self.player.pos[0]<5300  and enemy.mainBoss==True:
                        self.draw_health_bar(self.screen,500,  700,enemy.hp, enemy.hp_max,(255,0,0),500,20)

            #phanthan
            for phanthan in self.phanthans.copy():
                kill = phanthan.update(self.tilemap, (0, 0))
                phanthan.render(self.screen, offset=render_scroll)
                if kill:
                         self.phanthans.remove(phanthan)
                    
               

            #la roi
            for rect in self.leaf_spawners:
                if random.random() * 2500000 < rect.width * rect.height: # NHÂN SỐ CÀNG TO TỶ LỆ RA CẰNG THẤP
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.screen, offset=render_scroll)
                if particle.type == 'leaf':
                    # Chuyển động nhẹ theo trục x để tạo hiệu ứng dao động gió
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.5  # Tăng nhẹ tần suất dao động
                    #cham vô vùng tấn công của anime
                    for entity in self.enemies:
                        if entity.attacking and entity.animation.doneToDoSomething and random.randint(0, 100) < 80:
                            dis_x = entity.rectattack().centerx - particle.pos[0]
                            dis_y = entity.rectattack().centery - particle.pos[1]
                            if dis_x < 60 and dis_x >= -200 and abs(dis_y) <= 150:
                                particle.pos[0] += min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y cho mượt hơn
                                
                            # Xử lý va chạm khi đạn từ phải qua trái
                            if dis_x > -60 and dis_x <= 200 and abs(dis_y) <= 150:
                                particle.pos[0] -= min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y
                    # người chơi tấn công
                    if self.player.attacking == True:
                        if self.player.animation.doneToDoSomething and random.randint(0, 100) < 80:
                            dis_x = self.player.rectattack().centerx - particle.pos[0]
                            dis_y = self.player.rectattack().centery - particle.pos[1]
                            if dis_x < 60 and dis_x >= -200 and abs(dis_y) <= 150:
                                particle.pos[0] += min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y cho mượt hơn
                                
                            # Xử lý va chạm khi đạn từ phải qua trái
                            if dis_x > -60 and dis_x <= 200 and abs(dis_y) <= 150:
                                particle.pos[0] -= min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y
                    #phanthan dánh
                    for entity in self.phanthans:
                        if entity.attacking and entity.animation.doneToDoSomething and random.randint(0, 100) < 80:
                            dis_x = entity.rectattack().centerx - particle.pos[0]
                            dis_y = entity.rectattack().centery - particle.pos[1]
                            if dis_x < 60 and dis_x >= -200 and abs(dis_y) <= 150:
                                particle.pos[0] += min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y cho mượt hơn
                                
                            # Xử lý va chạm khi đạn từ phải qua trái
                            if dis_x > -60 and dis_x <= 200 and abs(dis_y) <= 150:
                                particle.pos[0] -= min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y
                    # người chơi dash
                    if abs(self.player.dashing) >30  and random.randint(0, 100) < 80:
                            dis_x = self.player.recttuongtac().centerx - particle.pos[0]
                            dis_y = self.player.recttuongtac().centery - particle.pos[1]
                            if dis_x < 60 and dis_x >= -200 and abs(dis_y) <= 150:
                                particle.pos[0] += min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y cho mượt hơn
                                
                            # Xử lý va chạm khi đạn từ phải qua trái
                            if dis_x > -60 and dis_x <= 200 and abs(dis_y) <= 150:
                                particle.pos[0] -= min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y

                    for dan in self.projectiles:
                        if random.randint(0, 100) < 65:
                            dis_x = dan[0][0] - particle.pos[0]
                            dis_y = dan[0][1] - particle.pos[1]
                            discao = 0
                            disxa =0
                            if dan[3] =='kiemnangluong1' or dan[3] =='kiemnangluong2':
                                discao=200
                                disxa = 200
                            else:
                                discao=40
                                disxa =120
                            # Xử lý va chạm khi đạn từ trái qua phải
                           
                            if dis_x < 20 and dis_x >= -1*disxa and abs(dis_y) <= discao:
                                particle.pos[0] += min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y cho mượt hơn
                                
                            # Xử lý va chạm khi đạn từ phải qua trái
                            if dis_x > -20 and dis_x <= disxa and abs(dis_y) <= discao:
                                particle.pos[0] -= min(30, abs(dis_x) / 1.1)  # Giảm tốc độ dịch chuyển
                                particle.pos[1] -= random.randint(-150, 150)  # Giảm độ ngẫu nhiên trục y

                if kill:
                    self.particles.remove(particle)
          

           #player
            if self.player.hp>0 :
                self.player.update(self.tilemap,(self.movement[1]-self.movement[0],0))
                self.player.render(self.screen,offset = render_scroll)
            else:
                self.sfx['boom'].play()
                for i in range(4):
                    angle = random.random() * math.pi * 2.2
                    speed = random.random() *2
                   # self.sparks.append(Spark(self.player.recttuongtac().center, angle,1+random.random()))
                    self.particles.append(Particle(self, 'particlewukong', (self.player.rect().centerx+4,self.player.rect().centery-6.5), velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                    
            #CO CHE LOAD MAP
            if not len(self.enemies):
                self.transition+=1
                if self.transition >30:
                    self.level=min(self.level+1,len(os.listdir('data/maps'))-1)
                    self.load_level(self.level)
            if self.transition<0:
                self.transition+=1

            

            if self.player.air_time>130 or self.player.hp<=0:
                self.player.hp -=1
                if self.player.air_time >200 or  self.player.hp <-200 :
                    self.player.air_time+=2
                    self.transition = min(30,self.transition+1)
                if self.player.air_time > 300 or  self.player.hp <-500 :
                    self.load_level(self.level)
              

           
            

            #cloud1
            self.clouds1.update()
            self.clouds1.render(self.screen,(render_scroll[0]*3,3*render_scroll[1]))
             #thanh máu
            if self.level!=0:
                self.draw_health_bar(self.screen, 50, 650, self.player.hp, self.player.hp_max,(220, 220, 220))
                self.draw_health_bar(self.screen, 50, 675, self.player.mana, self.player.mana_max,(0, 0, 139),40,10)
                self.draw_health_bar(self.screen, 50, 695, self.player.stamina, self.player.stamina_max,(255, 255, 0),150,10)
         
            #print(self.tilemap.physics_rects_around(self.player.pos))
            for event in pygame.event.get(): #get the input,click , keosv..vv
                if event.type == pygame.QUIT: #click dau X để thoát
                    pygame.quit()

                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                        
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                        
                    if event.key == pygame.K_UP:
                        self.player.jump()
                        for i in range(20):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 2 + 1
                            pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                            self.particles.append(Particle(self, 'particlewukong', self.player.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))                 
                    if event.key == pygame.K_DOWN:
                        
                        self.player.blocking = True
                        
                        
                    if event.key == pygame.K_c:
                        self.player.attack()
                        
                               
                    if event.key == pygame.K_x:
                        
                        self.player.skillphanthan()

                        
                    if event.key == pygame.K_z:
                        self.player.dash()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    #if event.key == pygame.K_q:
                        #self.phanthan = False
                    if event.key == pygame.K_DOWN:
                        self.player.blocking = False
            # hiệu ứng chuyển map
            if self.transition:
                transition_surf = pygame.Surface(self.screen.get_size())
                pygame.draw.circle(transition_surf,(255,255,255),(self.screen.get_width()//2,self.screen.get_height()//2),(30 - abs(self.transition))*8)
                transition_surf.set_colorkey((255,255,255))
                self.screen.blit(transition_surf,(0,0))

            #rung lắc
            screenshake_offset = (random.random()*self.screenshake - self.screenshake/2,random.random()*self.screenshake - self.screenshake/2)   
            self.screen.blit(pygame.transform.scale(self.screen,self.screen.get_size()),screenshake_offset)    
            pygame.display.update()
            self.clock.tick(60) # duy trì tốc độ 60FPS
Game().run()