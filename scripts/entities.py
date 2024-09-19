#player
import math
import random

import pygame

from scripts.particle import Particle
from scripts.spark import Spark

class PhysicsEntity:
    def __init__(self,game,e_type,pos,size,anim_offset=(0,0)):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size 
        self.velocity=[0,0]
        self.flip = False
        self.bidanh = False# biij đánh
        self.attacking = False
          
        if self.type =='player':
            self.rectedit=(29,70,35,50)
            self.rectTuongTacEdit=(23,50,50,64)     
            self.rectAttack=(60,-55,130,175,55)        
        elif self.type =='phanthan':
            self.rectedit=(29,70,35,50)
            self.rectTuongTacEdit=(23,50,50,64)     
            self.rectAttack=(60,-55,130,175,55)  
        elif self.type == 'enemy':
            self.rectedit=(19,52,35,50)
            self.rectTuongTacEdit=(19,50,35,50)
            self.rectAttack=(43,45,50,75,40)
              
        elif self.type == 'cungthu':
            self.rectedit=(75,133,40,50)
            self.rectTuongTacEdit=(70,45,50,130)
            self.rectAttack=(70,45,50,75,-15)# cách cạnh rectphai,y,size,size,cách cạnh rect trái

        elif self.type == 'bosschim':
            self.rectedit=(170,255,50,50)
            self.rectTuongTacEdit=(165,100,70,200)
            self.rectAttack=(70,135,125,125,60)
             

        self.collision = {'up':False,'down':False,'right':False,'left':False}
        
        self.action=''
        self.anim_offset =anim_offset# chỉnh vị trí ảnh animation h chưa cần lắm

       
        self.set_action('idle')
        self.frame_movement =(0,0) #dichuyen len xuong trai phai
        self.can_move = True
       
      

    #rect attack
    def rectattack(self,offset=(0,0)):
        if not self.flip:
            return pygame.Rect(self.rect().x+self.rectAttack[0] + -offset[0], self.pos[1]+self.rectAttack[1]-offset[1],self.rectAttack[2],self.rectAttack[3])  
        else:
            return pygame.Rect(self.rect().x -self.rectAttack[4] -self.rectAttack[0]-10-offset[0], self.pos[1]+self.rectAttack[1]-offset[1],self.rectAttack[2],self.rectAttack[3])  


    #rect tuong tac
    def recttuongtac(self,offset=(0,0)):
        
        return pygame.Rect(self.pos[0]+self.rectTuongTacEdit[0]-offset[0], self.pos[1]+self.rectTuongTacEdit[1]-offset[1],self.rectTuongTacEdit[2],self.rectTuongTacEdit[3])  
    

    #tao coll\ison cho player xử lý va chạm 
    def rect(self,offset=(0,0)):
        
        return pygame.Rect(self.pos[0]+self.rectedit[0]-offset[0], self.pos[1]+self.rectedit[1]-offset[1],self.rectedit[2],self.rectedit[3])  
        
            

    #tao trang thai neu dang ở trong trạng thái nào mà lại thêm chuyển đôg mơi giống  thì không chuyển
    def set_action(self,action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type +'/'+ self.action].copy() #'player/idle'
            



    def update(self,tilemap,movement=(0,0)):
        self.collision = {'up':False,'down':False,'right':False,'left':False}

        if self.can_move:
            self.frame_movement = (movement[0]+ self.velocity[0],movement[1]+ self.velocity[1])
        else:
            self.frame_movement = (0,movement[1]+ self.velocity[1])
        #di chuyen trai phai speed
        self.pos[0]+=self.frame_movement[0]*5
        #di chuyen len
        self.pos[1]+=self.frame_movement[1]*5

        #xử lý trạm 
        entity_rect = self.rect()
        pos_rect = [entity_rect.x,entity_rect.y]
        
       # Xử lý va chạm trục X
        #xử lý trạm 
        entity_rect = self.rect()
        pos_rect = [entity_rect.x,entity_rect.y]
        
        for rect in tilemap.physics_rects_around(pos_rect,1):
            if entity_rect.colliderect(rect)  :# tránh vc nhảy sang
                if self.frame_movement[0] > 0  :  # Di chuyển sang phải
                    entity_rect.right = rect.left
                    self.collision['right'] = True
                    self.pos[0] =  entity_rect.x - self.rectedit[0]
                elif self.frame_movement[0] <  0 :  # Di chuyển sang trái
                    entity_rect.left = rect.right
                    self.collision['left'] = True
                    self.pos[0] =  entity_rect.x - self.rectedit[0]
                # Cập nhật lại vị trí theo trục X
                
                

       

        # Xử lý va chạm trục Y
        entity_rect = self.rect()
        pos_rect = [entity_rect.x,entity_rect.y]
        for rect in tilemap.physics_rects_around(pos_rect,2):
            if entity_rect.colliderect(rect):
                if self.frame_movement[1] > 0 :  # Rơi xuống (di chuyển xuống dưới)
                    entity_rect.bottom = rect.top
                    self.collision['down'] = True
                    self.pos[1] = entity_rect.y - self.rectedit[1]
                elif self.frame_movement[1] < 0  and self.frame_movement[0]==0:  # Nhảy lên (di chuyển lên trên)
                    entity_rect.top = rect.bottom
                    self.collision['up'] = True
                    self.pos[1] = entity_rect.y - self.rectedit[1]

                # Cập nhật lại vị trí theo trục Y
                

        #flip       
        if movement[0]>0:
            self.flip = False
        if movement[0]<0:
            self.flip = True


        if self.attacking:        
            self.can_move = False
            if self.animation.done:  
             self.can_move = True
             self.attacking = False
        


         # Điều chỉnh vận tốc rơi    
        self.velocity[1] = min (11,self.velocity[1]+0.2 )# rơi cành nhanh đến 1 điểm nhất định
        
        if self.collision['down'] or self.collision['up']:
            self.velocity[1]=0
            self.frame_movement=(0,0)


        self.animation.update()


    # lấy ảnh
    def render(self,surf,offset=(0,0)):# off set đẻ nhận vật luôn ở vị trí trung tâm camera
        #pygame.draw.rect(surf, (0, 0, 255), self.rectattack(offset), 2)  # Viền đỏ
        #pygame.draw.rect(surf, (0, 255, 0), self.recttuongtac(offset), 2)  # Viền xanh lá
       # pygame.draw.rect(surf, (255, 0, 0), self.rect(offset), 2)  # Viền đỏ
        surf.blit(pygame.transform.flip(self.animation.img(),self.flip,False),(self.pos[0]-offset[0]+self.anim_offset[0],self.pos[1]-offset[1]+self.anim_offset[1]))
                                             


class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)
        self.attacking = False
        self.walking = 0
        self.dan='projectile'
        
    def update(self, tilemap, movement=(0, 0)):
        if self.walking:# xử lý đi trên vùng ok , chạm trái phải thì lật
            if tilemap.solid_check((self.rect().centerx + (-20 if self.flip else 20), self.rect().centery+25)):
                if (self.collision['right'] or self.collision['left']):
                    self.flip = not self.flip
                    
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)

            if not self.walking:
                #kc giữa pl và en
                dis = (self.game.player.pos[0] - self.pos[0], self.game.player.pos[1] - self.pos[1])
                #kc Y <16
                if (abs(dis[1]) < 79):
                    # đang quay trái bắn trái nếu gặp
                    if (self.flip and dis[0] < 0):
                        self.game.projectiles.append([[self.rect().centerx - 45, self.rect().centery-15], -5, 0,'projectile'])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5 + math.pi, 2 + random.random()))
                    if (not self.flip and dis[0] > 0):
                        self.game.projectiles.append([[self.rect().centerx + 45, self.rect().centery-15], 5, 0,'projectile'])
                        for i in range(4):
                            self.game.sparks.append(Spark(self.game.projectiles[-1][0], random.random() - 0.5, 2 + random.random()))
           
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)
        
        super().update(tilemap, movement=movement)
        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
            
        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.sparks.append(Spark(self.rect().center, angle, 2 + random.random()))
                    #self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                self.game.sparks.append(Spark(self.rect().center, 0, 5+ random.random()))
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))
             
                return True
    #lắp súng
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset=offset)
        
        if self.flip:
            surf.blit(pygame.transform.flip(self.game.assets['gun'], True, False), (self.rect().centerx - 20 - self.game.assets['gun'].get_width() - offset[0], self.rect().centery-20 - offset[1]))
        else:
            surf.blit(self.game.assets['gun'], (self.rect().centerx + 20 - offset[0], self.rect().centery-20 - offset[1]))
            
        
    

class Player(PhysicsEntity):
    def __init__(self,game,pos,size):
        super().__init__(game,'player',pos,size)
        self.air_time =0# thời gian ở trong không trung không tiếp đất
        self.jumps =1
        self.dashing = 0
        self.phanthaning= False
        self.blocking = False
        self.attacking = False
        self.bidanh = False
        self.dead = False
        self.mana_max = 10
        self.mana=10
        self.stamina_max=10
        self.stamina= 10
        self.hp_max =10
        self.hp=10
        self.mana=50
        self.stamina = 50
        
      
        


    def update(self,tilemap,movement=(0,0)):
        super().update(tilemap, movement=movement)
        self.stamina= min(10,self.stamina+0.022)

        #va cham với enemy
        for enemycon in self.game.enemies:
            if self.recttuongtac().colliderect(enemycon.rectattack()):
                if enemycon.attacking and abs(self.dashing) <50 and enemycon.animation.doneToDoSomething :
                    if  not self.blocking:                      
                        self.game.sfx['boom'].play()              
                        if self.flip == False:
                            self.pos[0] +=5.5
                            self.pos[1] -=15                           
                        else:
                            self.pos[0] -=5.5 
                            self.pos[1] -=15                    
                        self.hp-=0.1
                        #self.game.sfx['bidanh'].play()
                        
                    else:
                        self.game.sfx['chamvukhi'].play()
                        
                        if self.stamina<1:
                            self.hp-=0.005
                        else:
                            self.stamina-=0.01*random.randint(5,20)

                        if enemycon.type =='bosschim':
                            self.game.screenshake = max(random.randint(25,40),self.game.screenshake)
                            if random.randint(0,100)<40:
                                dis_x = enemycon.rectattack().centerx - self.recttuongtac().centerx
                                #dis_y = enemycon.rectattack().centery - self.recttuongtac().centery

                                if dis_x >30:
                                    self.pos[0] += random.randint(10,150)  # Giảm tốc độ dịch chuyển
                                    self.pos[1] -= random.randint(20, 100)  # Giảm độ ngẫu nhiên trục y cho mượt hơn
                                    
                                # Xử lý va chạm khi đạn từ phải qua trái
                                if dis_x <-30:
                                    self.pos[0] -= random.randint(10,150)  # Giảm tốc độ dịch chuyển
                                    self.pos[1] -= random.randint(20, 100)  # Giảm độ ngẫu nhiên trục y
                        else:
                            self.game.screenshake = max(16,self.game.screenshake)
                    
        if self.attacking:
            self.set_action('attack')
            self.game.sfx['wukongvoicechieudai'].play()
            self.animation.framecuoi[0]= self.animation.img_duration *5+1
            self.animation.framecuoi[1]= self.animation.img_duration *3+1
            self.anim_offset=(-90,-75)
            self.can_move = False
            if self.animation.done:
             self.anim_offset=(0,0)
             
             self.can_move = True
             self.attacking = False

        

        if self.attacking==False:

            if self.phanthaning:
                self.can_move = False
                self.set_action('phanthanskill')
            else:            
                self.air_time += 1
                
                

                if self.collision['down']:
                    self.air_time = 0
                    self.jumps = 2
                
                if self.blocking :
                    
                    self.attacking= False
                    self.can_move = False
                    self.set_action('block')
                else:
                    self.can_move = True
                    
        if self.can_move:
            if self.air_time > 4:
                        self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')

        
        if self.action=='phanthanskill':
            if self.animation.done:
                self.game.add_player()
                self.phanthaning = False
                self.can_move = True
                '''
        if self.action == 'hurt' :
            
            if self.flip == False:
                self.pos[0] +=5.5
                self.pos[1] -=15
                
            else:
                self.pos[0] -=5.5 
                self.pos[1] -=15

            if self.attacking:
               self.attacking = False
            self.can_move = False
            if self.animation.done:
                self.hp-=1
                self.bidanh = False
                self.can_move = True
                '''
        #dash
        if abs(self.dashing) in {60, 50}:
            for i in range(20):
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 1
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particlewukong', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))                 
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)   
        if abs(self.dashing) >50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 7
            self.game.sfx['tocbien'].play()
            #self.velocity[1] = 0
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1 # hãm 
            pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particlewukong', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7))) 

        #hãm phanh
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 50:
            super().render(surf, offset=offset)
            
    def jump(self):
        
        if self.jumps and self.stamina>1.5:
            self.velocity[1]=-4
            self.jumps -= 1
            self.air_time = 5
            self.stamina-=1.5

    def attack(self):
       if not self.attacking and   not self.blocking and self.stamina>1:  # Chỉ bắt đầu tấn công nếu không đang tấn công
            self.attacking = True
            self.stamina-=1
            
    def dash(self):
        if  abs(self.dashing)==0 and not self.attacking and  not self.blocking and self.stamina>3.5:

            if self.flip:
                self.dashing = -60
                self.stamina-=3.5
            else:
                self.dashing = 60
                self.stamina-=3.5
    def skillphanthan(self):
        if not self.phanthaning and self.mana>2 :
            self.phanthaning = True
            
            
            
        

      