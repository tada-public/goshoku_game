import pygame
import sys
import random
import asyncio

GREEN = (0, 128, 0)
YELLOW = (255, 155, 0)
BOARD_SIZE=(5,4)
GRID_SIZE=(165,220)
CARD_SIZE=(145,200)
FULL_CARDS=BOARD_SIZE[0]*BOARD_SIZE[1]
READ_CARDS=FULL_CARDS-3
SUKIMA=5
BAR_W=100
SIZE = (GRID_SIZE[0]*BOARD_SIZE[0]+BAR_W,GRID_SIZE[1]*BOARD_SIZE[1])
FPS=30
SECTION_TIME=10 #sec
SECTION_TIME_SELECT=30 #sec
SECTION_TIME_RESULT=20 #sec
MOVE_TIME=0.1 #SEC
MOVE_FRAME=int(MOVE_TIME*FPS)
CPUAREA_RATE=1.5
CPUAREA_NUM=int(FULL_CARDS/2)
BANDWIDTH=7
INVISIBLE_SIZE=(CARD_SIZE[0]-BANDWIDTH*2,CARD_SIZE[1]-BANDWIDTH*2)
INVISIBLE_TIME=2 #sec, completely invisible
FONT_SIZE_RESULT=74
STARTBTN_POS=[GRID_SIZE[0]*BOARD_SIZE[0]+BAR_W//2, GRID_SIZE[1]*BOARD_SIZE[1]-BAR_W]
STARTBTN_SIZE=[80, 60]
colors=["あお","ぴんく","きー","みどり","おれんじ"]
colors_kanji=["青札","桃札","黄札","緑札","橙札"]
colors_eng=["BLUE","PINK","YELLOW","GREEN","ORANGE"]
colors_code=["#33CCFF","#FF99CC","#FFCC00","#33CC66","#FF9933"]
colors_code_V85=["#2badd9","#d982ad","#d9ad00","#2bad57","#d9822b"]
colors_code_S30=["#c2f0ff","#ffe0f0","#fff0b3","#c7ffda","#ffe0c2"]
colors_code_S30_alpha=[(194,240,255),(255,224,240),(255,240,179),(199,255,218),(255,224,194)]
color_char=(250,250,250)

pygame.init()
pygame.mixer.init()
volume=0.7
screen = pygame.display.set_mode(SIZE,pygame.RESIZABLE)
pygame.display.set_caption("Goshoku_Hyakunin_Isshu")
clock = pygame.time.Clock()
se_binta01 = pygame.mixer.Sound("ogg/binta01.ogg")
se_maru = pygame.mixer.Sound("ogg/maru.ogg")
se_atack = pygame.mixer.Sound("ogg/atack.ogg")
se_ken = pygame.mixer.Sound("ogg/ken.ogg")
se_shouri = pygame.mixer.Sound("ogg/sentou-syouri.ogg")
se_shouri2 = pygame.mixer.Sound("ogg/sentou-syouri2.ogg")
se_shouri3 = pygame.mixer.Sound("ogg/sentou-syouri3.ogg")
se_shouri4 = pygame.mixer.Sound("ogg/sentou-syouri4.ogg")
se_shouri5 = pygame.mixer.Sound("ogg/sentou-syouri5.ogg")
se_bgm = pygame.mixer.Sound("ogg/harunoumi_s.ogg")
se_waka=[]
for c in range(5):
    for i in range(20):
        se_waka.append(pygame.mixer.Sound("ogg/{}_{}.ogg".format(c,i)))
img=[[] for i in range(5)]
head_img=[[] for i in range(5)]
for c in range(5):
    for i in range(20):
        img[c].append(pygame.image.load("pic/{}_{}.png".format(c,i)).convert())
        head_img[c].append(pygame.image.load("pic/head_{}_{}.png".format(c,i)).convert_alpha())

background_image = pygame.image.load('pic/noise_image_g.png')  # 画像ファイルのパスを指定
class Karuta:
    def __init__(self):
        random.seed()
        self.board=[]*BOARD_SIZE[0]*BOARD_SIZE[1]
        b=list(range(BOARD_SIZE[0]*BOARD_SIZE[1]))
        random.shuffle(b)
        self.board=b
        self.hand=[]*BOARD_SIZE[0]*BOARD_SIZE[1]
        h=list(range(BOARD_SIZE[0]*BOARD_SIZE[1]))
        random.shuffle(h)
        self.hand=h
        self.invisible_flag=0
        self.draggingflag=False
        self.draggingItemIndex=None
        self.drgOffsetX=0
        self.drgOffsetY=0
        self.drgCornerOffsetX=0
        self.drgCornerOffsetY=0
        self.char_flag=False
        self.char_mode_flag=False
        self.cpuscore=0
        self.score=0
        self.obtainedcard=0
        self.col=0
        self.cpuframes=[SECTION_TIME*FPS]*READ_CARDS
        self.moveflag=False
        self.move=[0,0,0,0,0] #[pos_x,pos_y,ith,MOVE_FRAME,IS_ME_OR_CPU]
        self.x0=0
        self.y0=0

    def get_posid(self,i):
        for j in range(FULL_CARDS):
            if self.board[j]==i:
                return j
        return 99
    def get_posid_hand(self,ith):
        for j in range(FULL_CARDS):
            if self.board[j]==self.hand[ith]:
                return j
        return 99
    def set_cpuframes(self):
        cpuallframe=(100*READ_CARDS-self.cpuscore)*int(FPS/10)
        cpuarea_cards=0
        for i in range(READ_CARDS):
            if self.hand[i]<CPUAREA_NUM:
                cpuarea_cards+=1
        splitframe=cpuallframe/(CPUAREA_RATE*(READ_CARDS-cpuarea_cards)+cpuarea_cards)
        for i in range(READ_CARDS):
            if self.get_posid_hand(i) < CPUAREA_NUM:
                self.cpuframes[i]=int(splitframe)
            else:
                self.cpuframes[i]=int(splitframe*CPUAREA_RATE)
        err=sum(self.cpuframes) - cpuallframe
        if err != 0:
            err_e=[0]*READ_CARDS
            for i in range(abs(err)):
                self.cpuframes[i%READ_CARDS]+=err/abs(err) #-1 or 1
        tiltfunc=[0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0,-0.1,-0.2,-0.3,-0.4,-0.5,-0.6,-0.7,-0.8]
        for i in range(READ_CARDS):
            self.cpuframes[i]+int(tiltfunc[i]*FPS)

    def cpu_atack(self,ith):
        for i in range(BOARD_SIZE[0]*BOARD_SIZE[1]):
            if self.board[i] == self.hand[ith]:
                self.board[i] = None
                se_atack.play()
                self.moveflag=True
                self.move=[i%BOARD_SIZE[0],int(i/BOARD_SIZE[0]),ith,MOVE_FRAME,0]
        
    def draw_board(self,cnt,stage,ith):
        if(cnt<0):
            cnt=0
        screen.fill(GREEN)
        screen.blit(background_image, (self.x0, self.y0), (0, 0, GRID_SIZE[0]*BOARD_SIZE[0], GRID_SIZE[1]*BOARD_SIZE[1]))
        for i in range(FULL_CARDS):
            if self.board[i] is not None and i != self.draggingItemIndex:
                gridpos=(i%BOARD_SIZE[0],i//BOARD_SIZE[0])
                self.draw_card(gridpos, self.board[i],cnt,stage)
        if self.draggingItemIndex != None and self.drgCornerOffsetX != 0:
                screen.blit(self.this_img[self.board[self.draggingItemIndex]], (self.drgCornerOffsetX,self.drgCornerOffsetY))
        if self.moveflag:
            if self.move[3]>1:
                temp_pos=(self.x0+self.move[0]*GRID_SIZE[0]+SUKIMA,self.y0+self.move[1]*GRID_SIZE[1]+SUKIMA)
                pos=(temp_pos[0]-(temp_pos[0]-int(GRID_SIZE[0]*BOARD_SIZE[0]/2))/MOVE_FRAME*(MOVE_FRAME-self.move[3]+1),\
                     temp_pos[1]-(temp_pos[1]-SIZE[1]*self.move[4])/MOVE_FRAME*(MOVE_FRAME-self.move[3]+1))
                screen.blit(self.this_img[self.hand[self.move[2]]], pos)
                self.move[3]-=1
            elif self.move[3]:
                self.moveflag=False
                self.move=[0,0,0,0,0]
        font_size=18
        score_board_sukima=10
        font = pygame.font.Font('ipaexg.ttf', font_size)
        text=font.render("SCORE",True, color_char)
        screen.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+score_board_sukima))
        text=font.render("{}".format(self.score),True, color_char)
        screen.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+font_size+score_board_sukima))
        text=font.render("CARD",True, color_char)
        screen.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+font_size*2+score_board_sukima))
        text=font.render("{}".format(self.obtainedcard),True, color_char)
        screen.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+font_size*3+score_board_sukima))
        text=font.render("TIME",True, color_char)
        screen.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+font_size*5+score_board_sukima))
        if stage==1:
            text=font.render("inf.",True, color_char)
        else:
            text=font.render("{}".format(SECTION_TIME-int(cnt/FPS)),True, color_char)            
        screen.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+font_size*6+score_board_sukima))
        if(stage==2 and self.char_flag and self.char_mode_flag and ith < FULL_CARDS and cnt>(FPS//2)):
            start_x = 0
            start_y = 0
            img_w, img_h =head_img[self.col][self.hand[ith]].get_rect().size
            crop_width = img_w
            crop_height = min(cnt*(FPS//10)-(FPS//2),img_h)
            crop_rect = pygame.Rect(start_x, start_y, crop_width, crop_height)
            cropped_image = head_img[self.col][self.hand[ith]].subsurface(crop_rect)
            crop_center = (self.x0+GRID_SIZE[0]*BOARD_SIZE[0]+BAR_W//2, self.y0+SIZE[1]//2-font_size//2, font_size, font_size)
            display_x = crop_center[0] - crop_width // 2
            display_y = crop_center[1]
            screen.blit(cropped_image, (display_x, display_y))

    def draw_card(self, gridpos, card_id,cnt,stage):
        pos=(self.x0+gridpos[0] * GRID_SIZE[0]+SUKIMA, self.y0+gridpos[1] * GRID_SIZE[1]+SUKIMA)
        screen.blit(self.this_img[card_id], pos)
        if stage==2 and (self.invisible_flag==1 or (self.invisible_flag==2 and gridpos[1] >=2)):
            if cnt<INVISIBLE_TIME*FPS:
                alpha=255
            else:
                alpha=255-int(255/(SECTION_TIME-INVISIBLE_TIME)*(cnt/FPS-INVISIBLE_TIME))
            pos=(self.x0+ gridpos[0] * GRID_SIZE[0]+SUKIMA+BANDWIDTH, self.y0+gridpos[1] * GRID_SIZE[1]+SUKIMA+BANDWIDTH)
            hidescr =pygame.Surface(INVISIBLE_SIZE,flags=pygame.SRCALPHA)
            hidescr.fill((colors_code_S30_alpha[self.col][0],colors_code_S30_alpha[self.col][1],colors_code_S30_alpha[self.col][2],alpha))
            screen.blit(hidescr,pos)

    def display_result(self):
        font = pygame.font.Font('ipaexg.ttf', FONT_SIZE_RESULT)
        if self.cpuscore !=0:
            if self.obtainedcard > READ_CARDS/2:
                se_shouri.play()
                text = font.render("You win!", True, YELLOW)
            else:
                se_shouri2.play()
                text = font.render("Try again!", True, YELLOW)
        elif self.score>=1400:
            se_shouri.play()
            text = font.render("Fantastic!!", True, YELLOW)        
        elif self.score>=1300:
            se_shouri2.play()
            text = font.render("Congratulations!", True, YELLOW)
        elif self.score>=1200:
            se_shouri3.play()
            text = font.render("Good Job!", True, YELLOW)
        elif self.score>=1100:
            se_shouri4.play()
            text = font.render("Finish!", True, YELLOW)
        else:
            se_shouri5.play()
            text = font.render("Finish...", True, YELLOW)
        text_rect = text.get_rect(center=(SIZE[0] // 2, SIZE[1] // 2))
        text_rect.move_ip(self.x0, self.y0)
        screen.blit(text, text_rect)
        pygame.display.flip()
        self.char_flag=False

    
    def update(self,x,y,ith,thisscore):
        if self.board[BOARD_SIZE[0]*y+x] == self.hand[ith]:
            self.board[BOARD_SIZE[0]*y+x] = None
            se_binta01.play()
            self.score+=thisscore
            self.moveflag=True
            self.move=[x,y,ith,MOVE_FRAME,1]
            self.obtainedcard+=1
            return True
        else:
            se_ken.play()
            return False

    def reset_section(self,ith):
        pygame.mixer.stop()
        se_waka[self.col*20+self.hand[ith]].play()
        self.char_flag=True

    def draw_select_board(self):
        screen.fill(GREEN)
        screen.blit(background_image, (self.x0, self.y0), (0, 0, GRID_SIZE[0]*BOARD_SIZE[0], GRID_SIZE[1]*BOARD_SIZE[1]))
        font_size=24
        font = pygame.font.Font('ipaexg.ttf', font_size)
        for i in range(BOARD_SIZE[0]*1):
            gridpos=(i%BOARD_SIZE[0],1)
            pos=(self.x0+gridpos[0] * GRID_SIZE[0], self.y0+gridpos[1] * GRID_SIZE[1])
            rect = pygame.Rect(pos[0]+10, pos[1]+10, GRID_SIZE[0]-20, GRID_SIZE[1]-20)
            pygame.draw.rect(screen, colors_code_V85[i], rect, width=0)
            rect = pygame.Rect(pos[0]+15, pos[1]+15, GRID_SIZE[0]-30, GRID_SIZE[1]-30)
            pygame.draw.rect(screen, colors_code_S30[i], rect, width=0)
            text=font.render("{}".format(colors_eng[i]),True, colors_code_V85[i])
            text_rect = text.get_rect(center=(int(GRID_SIZE[0]*(i+0.5)), int(GRID_SIZE[1]*1.5)))
            text_rect.move_ip(self.x0, self.y0)
            screen.blit(text, text_rect)
        if self.invisible_flag==1:
            color_on = 'red'
            color_on2 = 'gray'
            color_off = 'gray'
        elif self.invisible_flag==2:
            color_on = 'gray'
            color_on2 = 'red'
            color_off = 'gray'
        else:
            color_on = 'gray'
            color_on2 = 'gray'
            color_off = 'red'
        if not self.char_mode_flag:
            color_char_off='red'
            color_char_on='gray'
        else:
            color_char_off='gray'
            color_char_on='red'
        box_size=16
        border_w=1
        small_font = pygame.font.Font('ipaexg.ttf', box_size)
        char_box_x=self.x0+GRID_SIZE[0]*4+box_size
        char_box_y=self.y0+int(GRID_SIZE[1]*2.5)+box_size
        self.char_rect_off = pygame.Rect(char_box_x, char_box_y+box_size, box_size, box_size)
        self.char_rect_on = pygame.Rect(char_box_x, char_box_y+int(box_size*2.5), box_size, box_size)
        pygame.draw.rect(screen, color_char_off, self.char_rect_off)
        pygame.draw.rect(screen, 'gray', self.char_rect_off, border_w)
        pygame.draw.rect(screen, color_char_on, self.char_rect_on)
        pygame.draw.rect(screen, 'gray', self.char_rect_on, border_w)
        text = small_font.render("readable mode", True, 'white')
        text_rect = text.get_rect(midleft=(char_box_x, char_box_y))
        screen.blit(text, text_rect)
        text = small_font.render("OFF", True, 'white')
        self.text_char_rect_off = text.get_rect(midleft=(char_box_x+int(box_size*1.5), char_box_y+int(box_size*1.5)))
        screen.blit(text, self.text_char_rect_off)
        text = small_font.render("ON", True, 'white')
        self.text_char_rect_on = text.get_rect(midleft=(char_box_x+int(box_size*1.5), char_box_y+int(box_size*3)))
        screen.blit(text, self.text_char_rect_on)

        box_x=self.x0+GRID_SIZE[0]*4+box_size
        box_y=self.y0+GRID_SIZE[1]*3+box_size
        self.inv_rect_off = pygame.Rect(box_x, box_y+box_size, box_size, box_size)
        self.inv_rect_on = pygame.Rect(box_x, box_y+int(box_size*2.5), box_size, box_size)
        self.inv_rect_on2 = pygame.Rect(box_x, box_y+int(box_size*4), box_size, box_size)
        pygame.draw.rect(screen, color_off, self.inv_rect_off)
        pygame.draw.rect(screen, 'gray', self.inv_rect_off, border_w)
        pygame.draw.rect(screen, color_on, self.inv_rect_on)
        pygame.draw.rect(screen, 'gray', self.inv_rect_on, border_w)
        pygame.draw.rect(screen, color_on2, self.inv_rect_on2)
        pygame.draw.rect(screen, 'gray', self.inv_rect_on2, border_w)
        text = small_font.render("invisible mode", True, 'white')
        text_rect = text.get_rect(midleft=(box_x, box_y))
        screen.blit(text, text_rect)
        text = small_font.render("OFF", True, 'white')
        self.text_inv_rect_off = text.get_rect(midleft=(box_x+int(box_size*1.5), box_y+int(box_size*1.5)))
        screen.blit(text, self.text_inv_rect_off)
        text = small_font.render("ON", True, 'white')
        self.text_inv_rect_on = text.get_rect(midleft=(box_x+int(box_size*1.5), box_y+int(box_size*3)))
        screen.blit(text, self.text_inv_rect_on)
        text = small_font.render("ON for my side", True, 'white')
        self.text_inv_rect_on2 = text.get_rect(midleft=(box_x+int(box_size*1.5), box_y+int(box_size*4.5)))
        screen.blit(text, self.text_inv_rect_on2)

        if self.cpuscore!=0:
            text=font.render("CPU MODE (CPU SCORE {})".format(self.cpuscore),True, color_char)
            text_rect = text.get_rect(center=(int(GRID_SIZE[0]*2.5), int(GRID_SIZE[1]*2.5)+font_size))
            text_rect.move_ip(self.x0, self.y0)
            screen.blit(text, text_rect)
        text=font.render("SELECT COLOR",True, color_char)
        text_rect = text.get_rect(center=(int(GRID_SIZE[0]*2.5), int(GRID_SIZE[1]*3.5)))
        text_rect.move_ip(self.x0, self.y0)
        screen.blit(text, text_rect)

    def reset_section_select(self):
        pygame.mixer.stop()
        se_bgm.play()
    def selected(self,x,y):
            if x in [0,1,2,3,4] and y in [1]:
                self.col = x
                se_maru.play()
                self.this_img=[]
                for i in range(FULL_CARDS):
                    if self.get_posid(i) < FULL_CARDS // 2:
                        self.this_img.append(pygame.transform.rotate(img[x][i], 180))
                    else:
                        self.this_img.append(img[x][i])
                return True
            else:
                se_ken.play()
                return False
    def sizecheck(self):
        w, h = pygame.display.get_surface().get_size()
        self.x0=int((w-SIZE[0])/2)
        self.y0=int((h-SIZE[1])/2)
    def draw_startbtn(self):
        font = pygame.font.Font('ipaexg.ttf', 18)
        x, y = GRID_SIZE[0]*BOARD_SIZE[0]+BAR_W//2, GRID_SIZE[1]*BOARD_SIZE[1]-BAR_W # ボタンの中心座標
        w, h = 80, 60   # ボタンの幅と高さ
        button_color = 'azure1'
        button_color_edge = 'azure3'
        text_color = 'darkgreen'
        button_rect = pygame.Rect(self.x0+x-w//2+5, self.y0+y-h//2+5, w-10, h-10)
        self.button_rect_edge = pygame.Rect(self.x0 + x - w // 2, self.y0 + y - h // 2, w, h)
        pygame.draw.rect(screen, button_color_edge, self.button_rect_edge)
        pygame.draw.rect(screen, button_color, button_rect)
        text = font.render("START", True, text_color)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)
async def main():
    game = Karuta()
    running = True
    cnt=0
    read_cnt=0
    stage=0
    while running:
        game.sizecheck()
        if stage==0:
            if cnt%(SECTION_TIME_SELECT*FPS)==0:
                game.reset_section_select()
                cnt = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x:
                        game.invisible_flag=(game.invisible_flag+1)%3
                    elif event.key == pygame.K_6:
                        game.cpuscore=600
                    elif event.key == pygame.K_7:
                        game.cpuscore=700
                    elif event.key == pygame.K_8:
                        game.cpuscore=800
                    elif event.key == pygame.K_9:
                        game.cpuscore=900
                    elif event.key == pygame.K_0:
                        game.cpuscore=1000
                    elif event.key == pygame.K_1:
                        game.cpuscore=1100
                    elif event.key == pygame.K_2:
                        game.cpuscore=1200
                    elif event.key == pygame.K_3:
                        game.cpuscore=1300
                    elif event.key == pygame.K_4:
                        game.cpuscore=1400
                    elif event.key == pygame.K_5:
                        game.cpuscore=1500
                    elif event.key == pygame.K_z:
                        game.cpuscore=0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    px, py = event.pos
                    px-=game.x0
                    py-=game.y0
                    x = px//GRID_SIZE[0]
                    y = py//GRID_SIZE[1]
                    if(0<=x<BOARD_SIZE[0] and y==1):
                        res=game.selected(x,y)
                        if res:
                            stage = 1
                            cnt = -1
                            if game.cpuscore!=0:
                                game.set_cpuframes()
                    elif game.inv_rect_off.collidepoint(px, py) or game.text_inv_rect_off.collidepoint(px, py):
                        game.invisible_flag=0
                    elif game.inv_rect_on.collidepoint(px, py) or game.text_inv_rect_on.collidepoint(px, py):
                        game.invisible_flag=1
                    elif game.inv_rect_on2.collidepoint(px, py) or game.text_inv_rect_on2.collidepoint(px, py):
                        game.invisible_flag=2
                    elif game.char_rect_off.collidepoint(px, py) or game.text_char_rect_off.collidepoint(px, py):
                        game.char_mode_flag=False
                    elif game.char_rect_on.collidepoint(px, py) or game.text_char_rect_on.collidepoint(px, py):
                        game.char_mode_flag=True
            game.draw_select_board()
        elif stage==1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    px, py = event.pos
                    px-=game.x0
                    py-=game.y0
                    #dragcheck
                    x=px//GRID_SIZE[0]
                    y=py//GRID_SIZE[1]
                    idx = y * BOARD_SIZE[0]+x
                    if 0<= idx < FULL_CARDS:
                        game.draggingItemIndex = idx
                        game.drgOffsetX = px - x * GRID_SIZE[0]
                        game.drgOffsetY = py - y * GRID_SIZE[1]
                        game.drgCornerOffsetX = x * GRID_SIZE[0]
                        game.drgCornerOffsetY = y * GRID_SIZE[1]
                    elif game.button_rect_edge.collidepoint(px, py):
                        cnt = (SECTION_TIME-2)*FPS
                        game.draggingItemIndex=None
                        game.drgOffsetX=0
                        game.drgOffsetY=0
                        game.drgCornerOffsetX=0
                        game.drgCornerOffsetY=0
                        se_maru.play()
                        stage=2
                elif event.type == pygame.MOUSEMOTION:
                    if game.draggingItemIndex != None:
                        px, py = event.pos
                        px-=game.x0
                        py-=game.y0
                        game.drgCornerOffsetX=px - game.drgOffsetX
                        game.drgCornerOffsetY=py - game.drgOffsetY
                elif event.type == pygame.MOUSEBUTTONUP:
                    if game.draggingItemIndex != None:
                        px, py = event.pos
                        px-=game.x0
                        py-=game.y0
                        #dragcheck
                        x=px//GRID_SIZE[0]
                        y=py//GRID_SIZE[1]
                        idx = y * BOARD_SIZE[0]+x
                        if 0 <= idx < FULL_CARDS:
                            game.board[game.draggingItemIndex],game.board[idx]=game.board[idx],game.board[game.draggingItemIndex]
                            if (game.draggingItemIndex -9.5) * (idx -9.5) < 0:
                                game.this_img[game.board[game.draggingItemIndex]]=pygame.transform.rotate(game.this_img[game.board[game.draggingItemIndex]], 180)
                                game.this_img[game.board[idx]]=pygame.transform.rotate(game.this_img[game.board[idx]], 180)
                        game.draggingItemIndex = None
                        game.drgCornerOffsetX=0
                        game.drgCornerOffsetY=0 
                        game.drgOffsetX=0
                        game.drgOffsetY=0
            if cnt==0:
                pass
            elif cnt==SECTION_TIME*FPS:
                cnt = -1
                #stage=2
            game.draw_board(cnt,stage,99)
            game.draw_startbtn()
        elif stage==2:
            if cnt%(SECTION_TIME*FPS)==0:
                read_cnt += 1
                if read_cnt > READ_CARDS:
                    game.display_result()
                    remaintime=SECTION_TIME_RESULT*FPS*10
                    for i in range(remaintime):
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                        clock.tick(FPS)
                        await asyncio.sleep(0) 
                    pygame.quit()
                    sys.exit()
                else:
                    game.reset_section(read_cnt-1)
                cnt = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    x-=game.x0
                    y-=game.y0
                    x //= GRID_SIZE[0]
                    y //= GRID_SIZE[1]
                    res=game.update(x,y,read_cnt-1,100-int(100/(SECTION_TIME*FPS)*cnt))
                    if res:
                        cnt=(SECTION_TIME-2)*FPS

            if game.cpuscore!=0 and cnt==game.cpuframes[read_cnt-1] and game.get_posid_hand(read_cnt-1) !=99:
                game.cpu_atack(read_cnt-1)
                cnt=(SECTION_TIME-2)*FPS
                #pygame.mixer.stop()
            game.draw_board(cnt,stage,read_cnt-1)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0) 
        cnt += 1
    pygame.quit()
    sys.exit()


asyncio.run(main())
    
