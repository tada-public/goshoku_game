import pygame
import sys
import random
import copy
import asyncio
from PIL import Image
GREEN = (0, 128, 0)
YELLOW = (255, 155, 0)
DARKGRAY = (64,64,64)
BOARD_SIZE=(5,4)
GRID_SIZE=(155,210)
CARD_SIZE=(145,200)
HEAD_SIZE=(52,211)
HEAD_SIZE_H=(252,49)
FULL_CARDS=BOARD_SIZE[0]*BOARD_SIZE[1]
SUKIMA=5
BAR_W=100
BAR_H=60
SIZE = (GRID_SIZE[0]*BOARD_SIZE[0],GRID_SIZE[1]*BOARD_SIZE[1])
FPS=30
INFO_RECT_CAND=[(GRID_SIZE[0]*BOARD_SIZE[0], 0, BAR_W, GRID_SIZE[1]*BOARD_SIZE[1]),(0,GRID_SIZE[1]*BOARD_SIZE[1], GRID_SIZE[0]*BOARD_SIZE[0]*2, BAR_H)]
SECTION_TIME=10 #sec
SECTION_TIME_SELECT=30 #sec
SECTION_TIME_RESULT=20 #sec
MOVE_TIME=0.1 #SEC
MOVE_FRAME=int(MOVE_TIME*FPS)
CPUAREA_RATE=1.5
CPUAREA_NUM=FULL_CARDS//2
BANDWIDTH=7
INVISIBLE_SIZE=(CARD_SIZE[0]-BANDWIDTH*2,CARD_SIZE[1]-BANDWIDTH*2)
INVISIBLE_TIME=2 #sec, completely invisible
FONT_SIZE_RESULT=74
STARTBTN_SIZE=[80, 50]
SLIDER_MIN_VALUE = 600# スライダー設定
SLIDER_MAX_VALUE = 1500# スライダー設定
SLIDER_STEP = 100# スライダー設定
SLIDER_WIDTH = 300
SLIDER_HEIGHT = 10
SLIDER_POS = (int(GRID_SIZE[0]*1), int(GRID_SIZE[1]*3)+50)  # スライダーのバーの左上座標
KNOB_RADIUS = 10

#colors=["あお","ぴんく","きー","みどり","おれんじ"]
#colors_kanji=["青札","桃札","黄札","緑札","橙札"]
#colors_eng=["BLUE","PINK","YELLOW","GREEN","ORANGE"]
colors_code=["#33CCFF","#FF99CC","#FFCC00","#33CC66","#FF9933"]
colors_code_V85=["#2badd9","#d982ad","#d9ad00","#2bad57","#d9822b"]
#colors_code_S30=["#c2f0ff","#ffe0f0","#fff0b3","#c7ffda","#ffe0c2"]
colors_code_S30_alpha=[(194,240,255),(255,224,240),(255,240,179),(199,255,218),(255,224,194)]
color_char=(250,250,250)

se_waka=[]
se={}
img = []
head_img = []
headh_img = []
background_image_g = pygame.image.load('pic/noise_image_g.png')  # 画像ファイルのパスを指定
background_image_y = pygame.image.load('pic/noise_image_y.png')  # 画像ファイルのパスを指定


class Karuta:
    def __init__(self):
        random.seed()
        self.board=[]*FULL_CARDS
        b=list(range(FULL_CARDS))
        random.shuffle(b)
        self.board=b
        self.board_2=[]*FULL_CARDS
        b=list(range(FULL_CARDS))
        random.shuffle(b)
        self.board_2=b
        self.hand=[]*FULL_CARDS
        h=list(range(FULL_CARDS))
        random.shuffle(h)
        self.hand=h
        self.hand_2=[]*FULL_CARDS
        h=list(range(FULL_CARDS))
        random.shuffle(h)
        self.hand_2=h
        self.read_cards=FULL_CARDS-3
        self.gamesize=(SIZE[0],SIZE[1])
        self.double_mode_flag=0
        self.invisible_flag=0
        self.draggingItemIndex=None
        self.drgOffsetX=0
        self.drgOffsetY=0
        self.drgCornerOffsetX=0
        self.drgCornerOffsetY=0
        self.char_flag=False
        self.char_mode_flag=True
        self.cpu_mode_flag=False
        self.cpuscore=0
        self.slider_dragging = False
        self.knob_x=SLIDER_POS[0]
        self.score=0
        self.score_2=0
        self.obtainedcard=0
        self.obtainedcard_2=0
        self.color=None
        self.color_2=None
        self.cpuframes=[SECTION_TIME*FPS]*self.read_cards
        self.moveflag=False
        self.move=[0,0,0,0,0] #[pos_x,pos_y,ith,MOVE_FRAME,IS_ME_OR_CPU]
        self.x0=0
        self.x0_2=GRID_SIZE[0]*BOARD_SIZE[0]
        self.y0=0
        self.info_rect=None
        self.card_rect=[None]*FULL_CARDS*2
        self.rotated_img=[None]*FULL_CARDS*2
        self.title_card_rect=[None]*BOARD_SIZE[0]
        self.wander_mode_flag=False
        cos_values = [1.00, 0.98, 0.94, 0.87, 0.77, 0.64, 0.50, 0.34, 0.17, 0.00,
                        -0.17, -0.34, -0.50, -0.64, -0.77, -0.87, -0.94, -0.98, -1.00, -0.98,
                        -0.94, -0.87, -0.77, -0.64, -0.50, -0.34, -0.17, 0.00, 0.17, 0.34,
                        0.50, 0.64, 0.77, 0.87, 0.94, 0.98]
        sin_values = [0.00, 0.17, 0.34, 0.50, 0.64, 0.77, 0.87, 0.94, 0.98, 1.00,
                        0.98, 0.94, 0.87, 0.77, 0.64, 0.50, 0.34, 0.17, 0.00, -0.17,
                        -0.34, -0.50, -0.64, -0.77, -0.87, -0.94, -0.98, -1.00, -0.98, -0.94,
                        -0.87, -0.77, -0.64, -0.50, -0.34, -0.17]
        points = []
        radius = 6  # 半径
        ang0 = 9  # 初期角度
        for i in range(20):
            angle_deg = ang0 + i * 18
            angle_deg = angle_deg % 360
            index = angle_deg // 10
            cos_value = cos_values[index]
            sin_value = sin_values[index]
            x = radius * cos_value
            y = radius * sin_value
            if 0<= x < 1:
                x = 1
            elif -1< x < 0:
                x = -1
            if 0<= y < 1:
                y = 1
            elif -1< y < 0:
                y = -1
            points.append([x, y])
        shuffled_points1 = copy.deepcopy(points)
        random.shuffle(shuffled_points1)
        shuffled_points2 = copy.deepcopy(points)
        random.shuffle(shuffled_points2)
        self.wander_ang = shuffled_points1 + shuffled_points2
        self.screen=None
        self.clock=None
        self.finish_flag=False
        self.color_prepared=False
        self.currentobtained=0
        self.currentfanfale=None
        self.result_text=None
        self.draftsc=None
        self.cpu_get_score=0

    def initialize(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(SIZE,pygame.RESIZABLE)
        self.draftsc = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pygame.display.set_caption("Goshoku_Hyakunin_Isshu")
        self.clock = pygame.time.Clock()

    def load_source(self):
        global se
        global se_waka
        global img
        global head_img
        se["binta01"] = pygame.mixer.Sound("ogg/binta01.ogg")
        se["maru"] = pygame.mixer.Sound("ogg/maru.ogg")
        se["atack"] = pygame.mixer.Sound("ogg/atack.ogg")
        se["ken"] = pygame.mixer.Sound("ogg/ken.ogg")
        se["shouri"] = pygame.mixer.Sound("ogg/sentou-syouri.ogg")
        se["shouri2"] = pygame.mixer.Sound("ogg/sentou-syouri2.ogg")
        se["shouri3"] = pygame.mixer.Sound("ogg/sentou-syouri3.ogg")
        se["shouri4"] = pygame.mixer.Sound("ogg/sentou-syouri4.ogg")
        se["shouri5"] = pygame.mixer.Sound("ogg/sentou-syouri5.ogg")
        se["bgm"] = pygame.mixer.Sound("ogg/harunoumi_s.ogg")
        for c in range(5):
            for i in range(20):
                se_waka.append(pygame.mixer.Sound("ogg/{}_{}.ogg".format(c,i)))
        COMBINED_CARD_PATH = 'pic/cards.png'
        COMBINED_HEAD_PATH = 'pic/heads.png'
        COMBINED_HEADH_PATH = 'pic/headsh.png'
        NUM_SETS = 5
        combined_card_img = Image.open(COMBINED_CARD_PATH).convert("RGBA")
        combined_head_img = Image.open(COMBINED_HEAD_PATH).convert("RGBA")
        combined_headh_img = Image.open(COMBINED_HEADH_PATH).convert("RGBA")
        for set_id in range(NUM_SETS):
            row = []
            head_row = []
            head_h_row = []
            for card_id in range(FULL_CARDS):
                cx = card_id * CARD_SIZE[0]
                cy = set_id * CARD_SIZE[1]
                cropped = combined_card_img.crop((cx, cy, cx + CARD_SIZE[0], cy + CARD_SIZE[1]))
                surface = self.pil_to_surface(cropped)
                row.append(surface)
                hx = card_id * HEAD_SIZE[0]
                hy = set_id * HEAD_SIZE[1]
                cropped = combined_head_img.crop((hx, hy, hx + HEAD_SIZE[0], hy + HEAD_SIZE[1]))
                surface = self.pil_to_surface(cropped)
                head_row.append(surface)
                hhx = card_id * HEAD_SIZE_H[0]
                hhy = set_id * HEAD_SIZE_H[1]
                cropped = combined_headh_img.crop((hhx, hhy, hhx + HEAD_SIZE_H[0], hhy + HEAD_SIZE_H[1]))
                surface = self.pil_to_surface(cropped)
                head_h_row.append(surface)
            img.append(row)
            head_img.append(head_row)
            headh_img.append(head_h_row)

    def pil_to_surface(self,pil_image):
        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()
        return pygame.image.fromstring(data, size, mode).convert_alpha()

    def get_posid(self,i):
        for j in range(FULL_CARDS):
            if self.board[j]==i:
                return j
        return 99
    def get_posid_2(self,i):
        for j in range(FULL_CARDS):
            if self.board_2[j]==i:
                return j
        return 99
    def set_cpuframes(self):
        read_cards_for_calc=20-3
        cpuallframe=(100*read_cards_for_calc-self.cpuscore)*int(FPS/10)
        cpuarea_cards=0
        for i in range(read_cards_for_calc):
            if self.hand[i]<CPUAREA_NUM:
                cpuarea_cards+=1
        splitframe=cpuallframe/(CPUAREA_RATE*(read_cards_for_calc-cpuarea_cards)+cpuarea_cards)
        for i in range(read_cards_for_calc):
            if self.card_rect[i].center[1]//GRID_SIZE[1] < 2:
                self.cpuframes[i]=int(splitframe)
            else:
                self.cpuframes[i]=int(splitframe*CPUAREA_RATE)
        err=sum(self.cpuframes) - cpuallframe
        if err != 0:
            for i in range(abs(err)):
                self.cpuframes[i%read_cards_for_calc]+=err/abs(err) #-1 or 1
        tiltfunc=[0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0,-0.1,-0.2,-0.3,-0.4,-0.5,-0.6,-0.7,-0.8]
        for i in range(read_cards_for_calc):
            self.cpuframes[i]+=int(tiltfunc[i]*FPS)
        if self.double_mode_flag:
            temp_list=self.cpuframes.copy()
            self.cpuframes=[]
            for i in range(read_cards_for_calc):
                self.cpuframes.append(temp_list[i])
                self.cpuframes.append(temp_list[i])

    def cpu_atack(self,ith,thisscore):
        se["atack"].play()
        self.moveflag=True
        x_id, y_id = self.card_rect[self.hand[ith]].center
        x_id //= GRID_SIZE[0]
        y_id //= GRID_SIZE[1]
        self.move=[x_id,y_id,self.hand[ith],MOVE_FRAME,0]
        self.card_rect[self.hand[ith]] = None
        self.cpu_get_score += thisscore
        print(f"cpuscore:{self.cpu_get_score}")
        if self.double_mode_flag and self.color==self.color_2:
            x_id, y_id = self.card_rect[self.hand[ith]+20].center
            x_id //= GRID_SIZE[0]
            y_id //= GRID_SIZE[1]
            self.move=[x_id,y_id,self.hand[ith]+20,MOVE_FRAME,0]
            self.card_rect[self.hand[ith]+20] = None            

    def draw_board(self,cnt,stage):
        if(cnt<0):
            cnt=0
        #self.draftsc.fill(DARKGRAY)
        pygame.draw.rect(self.draftsc, DARKGRAY, self.info_rect)
        self.draftsc.blit(background_image_g, (self.x0, self.y0), (0, 0, GRID_SIZE[0]*BOARD_SIZE[0], GRID_SIZE[1]*BOARD_SIZE[1]))
        card_num=FULL_CARDS
        if self.double_mode_flag:
            self.draftsc.blit(background_image_y, (self.x0_2, self.y0), (0, 0, GRID_SIZE[0]*BOARD_SIZE[0], GRID_SIZE[1]*BOARD_SIZE[1]))
            card_num=FULL_CARDS*2
        self.x0=0
        self.x0_2=GRID_SIZE[0]*BOARD_SIZE[0]
        self.y0=0
        for ii in range(card_num):
            if self.card_rect[ii] is not None:
                if(stage==2 and self.wander_mode_flag):
                    if ii < 20:
                        left_edge = self.x0
                    else:
                        left_edge = self.x0_2
                    right_edge = left_edge+GRID_SIZE[0]*BOARD_SIZE[0]
                    top_edge = self.y0
                    bottom_edge = top_edge+GRID_SIZE[1]*BOARD_SIZE[1]
                    if self.color_2 is not None and self.color != self.color_2:
                        left_edge = self.x0
                        right_edge = self.x0+GRID_SIZE[0]*BOARD_SIZE[0]*2
                    self.card_rect[ii].x += self.wander_ang[ii][0]
                    self.card_rect[ii].y += self.wander_ang[ii][1]
                    if self.card_rect[ii].left < left_edge:
                        self.card_rect[ii].left = left_edge
                        self.wander_ang[ii][0] *= -1
                        self.wander_ang[ii][1] += -1+ii%3
                        self.card_rect[ii].x += self.wander_ang[ii][0]
                    elif self.card_rect[ii].right > right_edge:
                        self.card_rect[ii].right = right_edge
                        self.wander_ang[ii][0] *= -1
                        self.wander_ang[ii][1] += -1+ii%3
                        self.card_rect[ii].x += self.wander_ang[ii][0]
                    if self.card_rect[ii].top < top_edge:
                        self.card_rect[ii].top = top_edge
                        self.wander_ang[ii][1] *= -1 
                        self.wander_ang[ii][0] += -1+ii%3
                        self.card_rect[ii].y += self.wander_ang[ii][1]
                    elif self.card_rect[ii].bottom > bottom_edge:
                        self.card_rect[ii].bottom = bottom_edge
                        self.wander_ang[ii][1] *= -1 
                        self.wander_ang[ii][0] += -1+ii%3
                        self.card_rect[ii].y += self.wander_ang[ii][1]
                if ii != self.draggingItemIndex:
                    self.draftsc.blit(self.rotated_img[ii], self.card_rect[ii].topleft)
                    if self.invisible_flag > 0:
                        self.draw_hidescr(ii,cnt,stage)
        if self.draggingItemIndex != None and self.drgCornerOffsetX != 0:
                self.draftsc.blit(self.rotated_img[self.draggingItemIndex], (self.drgCornerOffsetX,self.drgCornerOffsetY))
        if self.moveflag:
            if self.move[3]>1:
                temp_pos=(self.x0+self.move[0]*GRID_SIZE[0]+SUKIMA,self.y0+self.move[1]*GRID_SIZE[1]+SUKIMA)
                pos=(temp_pos[0]-(temp_pos[0]-int(self.gamesize[0]/2))/MOVE_FRAME*(MOVE_FRAME-self.move[3]+1),\
                     temp_pos[1]-(temp_pos[1]-self.gamesize[1]*self.move[4])/MOVE_FRAME*(MOVE_FRAME-self.move[3]+1))
                self.draftsc.blit(self.rotated_img[self.move[2]], pos)
                self.move[3]-=1
            elif self.move[3]:
                self.moveflag=False
                self.move=[0,0,0,0,0]

    def draw_board_text(self,cnt):
        font_size=24
        score_board_sukima=10
        font = pygame.font.Font(None, font_size)
        text=font.render("SCORE",True, color_char)
        self.draftsc.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+score_board_sukima))
        text=font.render("{}".format(self.score),True, color_char)
        self.draftsc.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+font_size+score_board_sukima))
        text=font.render("CARD",True, color_char)
        self.draftsc.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+font_size*2+score_board_sukima))
        text=font.render("{}".format(self.obtainedcard),True, color_char)
        self.draftsc.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+font_size*3+score_board_sukima))
        text=font.render("TIME",True, color_char)
        self.draftsc.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+font_size*5+score_board_sukima))
        text=font.render("{}".format(SECTION_TIME-int(cnt/FPS)),True, color_char)            
        self.draftsc.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+font_size*6+score_board_sukima))

    def draw_board_text_2(self,cnt):
        font_size=24
        score_board_sukima=10
        font = pygame.font.Font(None, font_size)
        currenttext="TIME: {}, SCORE SUM: {}, CARD SUM: {}".format(SECTION_TIME-int(cnt/FPS),self.score+self.score_2,self.obtainedcard+self.obtainedcard_2)
        currenttext_l="[LEFT] SCORE: {}, CARD: {}".format(self.score,self.obtainedcard)
        currenttext_r="[RIGHT] SCORE: {}, CARD: {}".format(self.score_2,self.obtainedcard_2)
        text=font.render(currenttext,True, color_char)
        self.draftsc.blit(text, (self.x0+score_board_sukima, self.y0+GRID_SIZE[1]*BOARD_SIZE[1]+score_board_sukima))
        text=font.render(currenttext_l,True, color_char)
        self.draftsc.blit(text, (self.x0+score_board_sukima, self.y0+GRID_SIZE[1]*BOARD_SIZE[1]+score_board_sukima+font_size))
        text=font.render(currenttext_r,True, color_char)
        #self.draftsc.blit(text, (self.x0_2+score_board_sukima, self.y0+GRID_SIZE[1]*BOARD_SIZE[1]+score_board_sukima+font_size))
        #print(f"{text.get_rect()}, {text.get_rect()[3]}")
        self.draftsc.blit(text, (self.x0_2+GRID_SIZE[0]*BOARD_SIZE[0]-(score_board_sukima+text.get_rect()[2]+200), self.y0+GRID_SIZE[1]*BOARD_SIZE[1]+score_board_sukima+font_size))

    def draw_dist_info(self):
        font_size=24
        score_board_sukima=10
        font = pygame.font.Font(None, font_size)
        if not self.double_mode_flag:
            text=font.render("Arrange",True, color_char)
            self.draftsc.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+score_board_sukima))
            text=font.render("the cards",True, color_char)
            self.draftsc.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+font_size+score_board_sukima))
            text=font.render("as you like",True, color_char)
            self.draftsc.blit(text, (self.x0+BOARD_SIZE[0]*GRID_SIZE[0]+score_board_sukima, self.y0+font_size*2+score_board_sukima))
        else:
            text=font.render("Arrange the cards as you like",True, color_char)
            self.draftsc.blit(text, (self.x0+score_board_sukima, self.y0+GRID_SIZE[1]*BOARD_SIZE[1]+score_board_sukima))

    def draw_startbtn(self,stage):
        font = pygame.font.Font(None, 24)
        if stage==0:
            x, y = BAR_W//2 + 10, GRID_SIZE[1]*BOARD_SIZE[1]-BAR_W
        else:
            if self.double_mode_flag:
                x, y = GRID_SIZE[0]*BOARD_SIZE[0]*2-BAR_W, GRID_SIZE[1]*BOARD_SIZE[1]+BAR_H//2
            else:
                x, y = GRID_SIZE[0]*BOARD_SIZE[0]+BAR_W//2, GRID_SIZE[1]*BOARD_SIZE[1]-BAR_H
        w, h = STARTBTN_SIZE[0],STARTBTN_SIZE[1]   
        button_color = 'azure1'
        button_color_edge = 'azure3'
        text_color = 'darkgreen'
        button_rect = pygame.Rect(self.x0+x-w//2+5, self.y0+y-h//2+5, w-10, h-10)
        self.button_rect_edge = pygame.Rect(self.x0 + x - w // 2, self.y0 + y - h // 2, w, h)
        pygame.draw.rect(self.draftsc, button_color_edge, self.button_rect_edge)
        pygame.draw.rect(self.draftsc, button_color, button_rect)
        text = font.render("START", True, text_color)
        text_rect = text.get_rect(center=(x, y))
        self.draftsc.blit(text, text_rect)

    def draw_board_char(self,cnt,ith):
        if cnt <= 0:
            #print("cnt<=0 in draw_board_char")
            return False
        font_size=24
        start_x = 0
        start_y = 0
        if head_img[self.color][self.hand[ith]] is None:
            #print(f"head_img is None in draw_board_char, ith:{ith}, hand[ith]:{self.hand[ith]}")
            return False
        img_w, img_h =head_img[self.color][self.hand[ith]].get_rect().size
        crop_width = img_w
        crop_height = min(cnt*(FPS//10)*2,img_h)
        if img_h <=0:
            #print(f"img_h <=0, img_h:{img_h}, ith:{ith}, hand[ith]:{self.hand[ith]}")
            return False
        crop_rect = pygame.Rect(start_x, start_y, crop_width, crop_height)
        try:
            cropped_image = head_img[self.color][self.hand[ith]].subsurface(crop_rect)
        except Exception as e:
            print(f"err, crop_width:{crop_width},crop_height:{crop_height} ith:{ith}, hand[ith]:{self.hand[ith]}: {e}")
        crop_center = (self.x0+GRID_SIZE[0]*BOARD_SIZE[0]+BAR_W//2, self.y0+SIZE[1]//2-font_size//2, font_size, font_size)
        display_x = crop_center[0] - crop_width // 2
        display_y = crop_center[1]
        self.draftsc.blit(cropped_image, (display_x, display_y))

    def draw_board_char_2(self,cnt,ith):
        if cnt <= 0:
            #print("cnt<=0 in draw_board_char_2")
            return False
        font_size=24
        thiscolor=self.color
        thisith=self.hand[ith]
        start_x = 0
        start_y = 0
        if self.color_2 is not None and self.color != self.color_2:
            if ith%2==0:
                thiscolor=self.color
                thisith=self.hand[ith]
            else:
                thiscolor=self.color_2
                thisith=self.hand[ith]-20
        if not(0 <= thisith < 20):
            #print("thisith is out of range in draw_board_char_2")
            return False
        elif headh_img[thiscolor][thisith] is None:
            print("headh_img is None in draw_board_char_2, ith:{ith}, hand[ith]:{self.hand[ith]}")
            return False
        img_w, img_h =headh_img[thiscolor][thisith].get_rect().size
        crop_width = min(cnt*(FPS//10)*2,img_w)
        crop_height = img_h
        crop_rect = pygame.Rect(start_x, start_y, crop_width, crop_height)
        cropped_image = headh_img[thiscolor][thisith].subsurface(crop_rect)
        crop_center = (self.x0+GRID_SIZE[0]*4+40, self.y0+SIZE[1]+BAR_H//2, font_size, font_size)
        display_x = crop_center[0]
        display_y = crop_center[1] - crop_height // 2
        self.draftsc.blit(cropped_image, (display_x, display_y))

    def draw_board_result(self,stage=3):
        self.display_result()
        self.draw_startbtn(stage)

    def draw_hidescr(self, card_id, cnt, stage):
        pos=self.card_rect[card_id].center
        if stage==2 and (self.invisible_flag==1 or (self.invisible_flag==2 and pos[1]//GRID_SIZE[1] >=2)):
            if cnt<INVISIBLE_TIME*FPS:
                alpha=255
            else:
                alpha=255-int(255/(SECTION_TIME-INVISIBLE_TIME)*(cnt/FPS-INVISIBLE_TIME))
            #pos=(self.x0+ gridpos[0] * GRID_SIZE[0]+SUKIMA+BANDWIDTH, self.y0+gridpos[1] * GRID_SIZE[1]+SUKIMA+BANDWIDTH)
            hidescr =pygame.Surface(INVISIBLE_SIZE,flags=pygame.SRCALPHA)
            if card_id<20:
                thiscolor=self.color
            else:
                thiscolor=self.color_2
            hidescr.fill((colors_code_S30_alpha[thiscolor][0],colors_code_S30_alpha[thiscolor][1],colors_code_S30_alpha[thiscolor][2],alpha))
            #self.draftsc.blit(hidescr,pos)
            hidescr_rect=hidescr.get_rect(center=pos)
            self.draftsc.blit(hidescr, hidescr_rect.topleft)

    def set_result(self):
        maxscore=max(self.score,self.score_2)
        winscore=17//2
        if self.cpuscore !=0:
            if self.obtainedcard > winscore or self.obtainedcard_2 > winscore:
                self.currentfanfale=se["shouri"]
                self.result_text = "You win!"
            else:
                self.currentfanfale=se["shouri2"]
                self.result_text = "Try again!"
        elif maxscore>=1400:
            self.currentfanfale=se["shouri"]
            self.result_text = "Fantastic!!"        
        elif maxscore>=1300:
            self.currentfanfale=se["shouri2"]
            self.result_text = "Congratulations!"
        elif maxscore>=1200:
            self.currentfanfale=se["shouri3"]
            self.result_text = "Good Job!"
        elif maxscore>=1100:
            self.currentfanfale=se["shouri4"]
            self.result_text = "Finish!"
        else:
            self.currentfanfale=se["shouri5"]
            self.result_text = "Finish..."

    def display_result(self):
        font = pygame.font.Font(None, FONT_SIZE_RESULT)
        text = font.render(self.result_text, True, YELLOW)
        cx, cy =SIZE[0] // 2, SIZE[1] // 2
        if self.double_mode_flag:
            cx, cy =SIZE[0], SIZE[1] // 2            
        text_rect = text.get_rect(center=(cx,cy))
        text_rect.move_ip(self.x0, self.y0)
        self.draftsc.blit(text, text_rect)
        self.char_flag=False
    
    def update(self,x,y,ith,thisscore):
        getcard=None
        if self.color_2 is None:
            if self.card_rect[self.hand[ith]].collidepoint(x, y):
                getcard=self.hand[ith]
                self.obtainedcard+=1
                self.score+=thisscore
        elif self.color_2 is not None and self.color==self.color_2:
            if self.card_rect[self.hand[ith]] is not None:
                if self.card_rect[self.hand[ith]].collidepoint(x, y):
                    getcard=self.hand[ith]
                    self.obtainedcard+=1
                    self.score+=thisscore
            if self.card_rect[self.hand[ith]+20] is not None:
                if self.card_rect[self.hand[ith]+20].collidepoint(x, y):
                    getcard=self.hand[ith]+20
                    self.obtainedcard_2+=1
                    self.score_2+=thisscore
        elif self.color_2 is not None and self.color!=self.color_2:
            if self.card_rect[self.hand[ith]].collidepoint(x, y):
                getcard=self.hand[ith]
                if getcard<20:
                    self.obtainedcard+=1
                    self.score+=thisscore
                else:
                    self.obtainedcard_2+=1
                    self.score_2+=thisscore
        if getcard is not None:
            se["binta01"].play()
            self.moveflag=True
            x_id, y_id = self.card_rect[getcard].center
            x_id //= GRID_SIZE[0]
            y_id //= GRID_SIZE[1]
            self.move=[x_id,y_id,getcard,MOVE_FRAME,1]
            self.card_rect[getcard] = None
            return True
        else:
            se["ken"].play()
            return False

    def reset_section(self,ith):
        pygame.mixer.stop()
        if self.hand[ith]<20:
            thiscolor=self.color
            thisith=self.hand[ith]
        else:
            thiscolor=self.color_2
            thisith=self.hand[ith]-20
        se_waka[thiscolor*20+thisith].play()
        self.char_flag=True

    def draw_select_board(self):
        #self.draftsc.fill(DARKGRAY)
        #pygame.draw.rect(self.draftsc, DARKGRAY, self.info_rect)
        self.draftsc.blit(background_image_g, (self.x0, self.y0), (0, 0, GRID_SIZE[0]*BOARD_SIZE[0], GRID_SIZE[1]*BOARD_SIZE[1]))
        font_size=32
        font = pygame.font.Font(None, font_size)
        card_represent=[5,13,3,4,8]
        for i in range(BOARD_SIZE[0]*1):
            gridpos=(i%BOARD_SIZE[0],1)
            centerpos=(self.x0+gridpos[0]*GRID_SIZE[0]+GRID_SIZE[0]//2, self.y0+gridpos[1]*GRID_SIZE[1]+GRID_SIZE[1]//2)
            self.title_card_rect[i]=img[i][card_represent[i]].get_rect(center=centerpos)
            self.draftsc.blit(img[i][card_represent[i]], self.title_card_rect[i].topleft)
        if not self.double_mode_flag:
            color_double_off, color_double_on = 'red', 'gray'
        else:
            color_double_off, color_double_on = 'gray', 'red'
        if not self.cpu_mode_flag:
            color_cpu_off, color_cpu_on = 'red', 'gray'
        else:
            color_cpu_off, color_cpu_on = 'gray', 'red'
        if self.invisible_flag==1:
            color_on, color_on2, color_off = 'red', 'gray', 'gray'
        elif self.invisible_flag==2:
            color_on, color_on2, color_off = 'gray', 'red', 'gray'
        else:
            color_on, color_on2, color_off = 'gray', 'gray', 'red'
        if not self.char_mode_flag:
            color_char_off, color_char_on = 'red', 'gray'
        else:
            color_char_off, color_char_on = 'gray', 'red'
        if not self.wander_mode_flag:
            color_wander_off, color_wander_on = 'red', 'gray'
        else:
            color_wander_off, color_wander_on = 'gray', 'red'
        box_size=24
        border_w=1
        small_font = pygame.font.Font(None, box_size)

        double_box_x=self.x0+GRID_SIZE[0]*0+box_size
        double_box_y=self.y0+int(GRID_SIZE[1]*2.5)+box_size
        self.double_rect_off = pygame.Rect(double_box_x, double_box_y+box_size, box_size, box_size)
        self.double_rect_on = pygame.Rect(double_box_x, double_box_y+int(box_size*2.5), box_size, box_size)
        pygame.draw.rect(self.draftsc, color_double_off, self.double_rect_off)
        pygame.draw.rect(self.draftsc, 'gray', self.double_rect_off, border_w)
        pygame.draw.rect(self.draftsc, color_double_on, self.double_rect_on)
        pygame.draw.rect(self.draftsc, 'gray', self.double_rect_on, border_w)
        text = small_font.render("double mode", True, 'white')
        text_rect = text.get_rect(midleft=(double_box_x, double_box_y))
        self.draftsc.blit(text, text_rect)
        text = small_font.render("OFF", True, 'white')
        self.text_double_rect_off = text.get_rect(midleft=(double_box_x+int(box_size*1.5), double_box_y+int(box_size*1.5)))
        self.draftsc.blit(text, self.text_double_rect_off)
        text = small_font.render("ON", True, 'white')
        self.text_double_rect_on = text.get_rect(midleft=(double_box_x+int(box_size*1.5), double_box_y+int(box_size*3)))
        self.draftsc.blit(text, self.text_double_rect_on)

        cpu_box_x=self.x0+GRID_SIZE[0]*1+box_size
        cpu_box_y=self.y0+int(GRID_SIZE[1]*2.5)+box_size
        self.cpu_rect_off = pygame.Rect(cpu_box_x, cpu_box_y+box_size, box_size, box_size)
        self.cpu_rect_on = pygame.Rect(cpu_box_x, cpu_box_y+int(box_size*2.5), box_size, box_size)
        pygame.draw.rect(self.draftsc, color_cpu_off, self.cpu_rect_off)
        pygame.draw.rect(self.draftsc, 'gray', self.cpu_rect_off, border_w)
        pygame.draw.rect(self.draftsc, color_cpu_on, self.cpu_rect_on)
        pygame.draw.rect(self.draftsc, 'gray', self.cpu_rect_on, border_w)
        text = small_font.render("CPU mode", True, 'white')
        text_rect = text.get_rect(midleft=(cpu_box_x, cpu_box_y))
        self.draftsc.blit(text, text_rect)
        text = small_font.render("OFF", True, 'white')
        self.text_cpu_rect_off = text.get_rect(midleft=(cpu_box_x+int(box_size*1.5), cpu_box_y+int(box_size*1.5)))
        self.draftsc.blit(text, self.text_cpu_rect_off)
        text = small_font.render("ON", True, 'white')
        self.text_cpu_rect_on = text.get_rect(midleft=(cpu_box_x+int(box_size*1.5), cpu_box_y+int(box_size*3)))
        self.draftsc.blit(text, self.text_cpu_rect_on)

        char_box_x=self.x0+GRID_SIZE[0]*3+box_size
        char_box_y=self.y0+int(GRID_SIZE[1]*2.5)+box_size
        self.char_rect_off = pygame.Rect(char_box_x, char_box_y+box_size, box_size, box_size)
        self.char_rect_on = pygame.Rect(char_box_x, char_box_y+int(box_size*2.5), box_size, box_size)
        pygame.draw.rect(self.draftsc, color_char_off, self.char_rect_off)
        pygame.draw.rect(self.draftsc, 'gray', self.char_rect_off, border_w)
        pygame.draw.rect(self.draftsc, color_char_on, self.char_rect_on)
        pygame.draw.rect(self.draftsc, 'gray', self.char_rect_on, border_w)
        text = small_font.render("readable mode", True, 'white')
        text_rect = text.get_rect(midleft=(char_box_x, char_box_y))
        self.draftsc.blit(text, text_rect)
        text = small_font.render("OFF", True, 'white')
        self.text_char_rect_off = text.get_rect(midleft=(char_box_x+int(box_size*1.5), char_box_y+int(box_size*1.5)))
        self.draftsc.blit(text, self.text_char_rect_off)
        text = small_font.render("ON", True, 'white')
        self.text_char_rect_on = text.get_rect(midleft=(char_box_x+int(box_size*1.5), char_box_y+int(box_size*3)))
        self.draftsc.blit(text, self.text_char_rect_on)

        box_x=self.x0+GRID_SIZE[0]*3+box_size
        box_y=self.y0+GRID_SIZE[1]*3+box_size
        self.inv_rect_off = pygame.Rect(box_x, box_y+box_size, box_size, box_size)
        self.inv_rect_on = pygame.Rect(box_x, box_y+int(box_size*2.5), box_size, box_size)
        self.inv_rect_on2 = pygame.Rect(box_x, box_y+int(box_size*4), box_size, box_size)
        pygame.draw.rect(self.draftsc, color_off, self.inv_rect_off)
        pygame.draw.rect(self.draftsc, 'gray', self.inv_rect_off, border_w)
        pygame.draw.rect(self.draftsc, color_on, self.inv_rect_on)
        pygame.draw.rect(self.draftsc, 'gray', self.inv_rect_on, border_w)
        pygame.draw.rect(self.draftsc, color_on2, self.inv_rect_on2)
        pygame.draw.rect(self.draftsc, 'gray', self.inv_rect_on2, border_w)
        text = small_font.render("invisible mode", True, 'white')
        text_rect = text.get_rect(midleft=(box_x, box_y))
        self.draftsc.blit(text, text_rect)
        text = small_font.render("OFF", True, 'white')
        self.text_inv_rect_off = text.get_rect(midleft=(box_x+int(box_size*1.5), box_y+int(box_size*1.5)))
        self.draftsc.blit(text, self.text_inv_rect_off)
        text = small_font.render("ON", True, 'white')
        self.text_inv_rect_on = text.get_rect(midleft=(box_x+int(box_size*1.5), box_y+int(box_size*3)))
        self.draftsc.blit(text, self.text_inv_rect_on)
        text = small_font.render("ON for my side", True, 'white')
        self.text_inv_rect_on2 = text.get_rect(midleft=(box_x+int(box_size*1.5), box_y+int(box_size*4.5)))
        self.draftsc.blit(text, self.text_inv_rect_on2)

        wander_box_x=self.x0+GRID_SIZE[0]*4+box_size
        wander_box_y=self.y0+int(GRID_SIZE[1]*2.5)+box_size
        self.wander_rect_off = pygame.Rect(wander_box_x, wander_box_y+box_size, box_size, box_size)
        self.wander_rect_on = pygame.Rect(wander_box_x, wander_box_y+int(box_size*2.5), box_size, box_size)
        pygame.draw.rect(self.draftsc, color_wander_off, self.wander_rect_off)
        pygame.draw.rect(self.draftsc, 'gray', self.wander_rect_off, border_w)
        pygame.draw.rect(self.draftsc, color_wander_on, self.wander_rect_on)
        pygame.draw.rect(self.draftsc, 'gray', self.wander_rect_on, border_w)
        text = small_font.render("wandering mode", True, 'white')
        text_rect = text.get_rect(midleft=(wander_box_x, wander_box_y))
        self.draftsc.blit(text, text_rect)
        text = small_font.render("OFF", True, 'white')
        self.text_wander_rect_off = text.get_rect(midleft=(wander_box_x+int(box_size*1.5), wander_box_y+int(box_size*1.5)))
        self.draftsc.blit(text, self.text_wander_rect_off)
        text = small_font.render("ON", True, 'white')
        self.text_wander_rect_on = text.get_rect(midleft=(wander_box_x+int(box_size*1.5), wander_box_y+int(box_size*3)))
        self.draftsc.blit(text, self.text_wander_rect_on)

        text=font.render("SELECT COLOR",True, color_char)
        text_rect = text.get_rect(center=(int(GRID_SIZE[0]*2.5), int(GRID_SIZE[1]*0.5)))
        text_rect.move_ip(self.x0, self.y0)
        self.draftsc.blit(text, text_rect)

    def draw_selected_colors(self):
        box_size=24
        small_font = pygame.font.Font(None, box_size)
        tx, ty = self.x0+box_size, self.y0+int(GRID_SIZE[1]*2.5)+int(box_size*5.5)
        text = small_font.render("selected colors: ", True, 'white')
        text_rect = text.get_rect(midleft=(tx, ty))
        self.draftsc.blit(text, text_rect)
        if self.color is not None:
            color_rect = pygame.Rect(self.x0+box_size, self.y0+int(GRID_SIZE[1]*2.5)+box_size*6, box_size, box_size)
            pygame.draw.rect(self.draftsc, colors_code[self.color], color_rect)
        if self.color_2 is not None:
            color_rect = pygame.Rect(self.x0+box_size*2.5, self.y0+int(GRID_SIZE[1]*2.5)+box_size*6, box_size, box_size)
            pygame.draw.rect(self.draftsc, colors_code[self.color_2], color_rect)

    def draw_slider(self, thiscpuscore):
        steps = (thiscpuscore - SLIDER_MIN_VALUE) // SLIDER_STEP
        ratio = steps / ((SLIDER_MAX_VALUE - SLIDER_MIN_VALUE) // SLIDER_STEP)
        self.knob_x= int(SLIDER_POS[0] + ratio * SLIDER_WIDTH)
        pygame.draw.rect(self.draftsc, 'gray', (SLIDER_POS[0], SLIDER_POS[1], SLIDER_WIDTH, SLIDER_HEIGHT))
        pygame.draw.circle(self.draftsc, 'white', (self.knob_x, SLIDER_POS[1] + SLIDER_HEIGHT // 2), KNOB_RADIUS)
        font = pygame.font.Font(None, 24)
        text = font.render(f"CPU Score: {self.cpuscore}", True, (255, 255, 255))
        self.draftsc.blit(text, (SLIDER_POS[0], SLIDER_POS[1] - 20))

    def update_cpuscore(self,this_knob_x):
        relative_x = this_knob_x - SLIDER_POS[0]
        ratio = relative_x / SLIDER_WIDTH
        steps = round(ratio * ((SLIDER_MAX_VALUE - SLIDER_MIN_VALUE) // SLIDER_STEP))
        value = SLIDER_MIN_VALUE + steps * SLIDER_STEP
        value = max(SLIDER_MIN_VALUE, min(SLIDER_MAX_VALUE, value))
        return value
    
    def reset_section_select(self):
        pygame.mixer.stop()
        se["bgm"].play()

    def sizecheck(self):
        w, h = pygame.display.get_surface().get_size()
        self.x0=int((w-self.gamesize[0])/2)
        self.x0_2=self.x0+GRID_SIZE[0]*BOARD_SIZE[0]
        self.y0=int((h-self.gamesize[1])/2)

    def card_click_check(self, x, y):
        for i in range(FULL_CARDS*2):
            if self.card_rect[i] is not None:
                if self.card_rect[i].collidepoint(x, y):
                    return i
        return 99
    
    def title_card_click_check(self, x, y):
        for c in range(BOARD_SIZE[0]):
            if self.title_card_rect[c].collidepoint(x, y):
                se["maru"].play()
                if self.color is None:
                    for i in range(FULL_CARDS):
                        posid=self.get_posid(i)
                        if posid < FULL_CARDS // 2:
                            self.rotated_img[i]=pygame.transform.rotate(img[c][i], 180)
                        else:
                            self.rotated_img[i]=img[c][i]
                        gridpos=(posid%BOARD_SIZE[0],posid//BOARD_SIZE[0])
                        centerpos=(self.x0+gridpos[0]*GRID_SIZE[0]+GRID_SIZE[0]//2, self.y0+gridpos[1]*GRID_SIZE[1]+GRID_SIZE[1]//2)
                        self.card_rect[i]=self.rotated_img[i].get_rect(center=centerpos)
                    self.color=c
                elif self.color_2 is None:
                    for i in range(FULL_CARDS):
                        posid=self.get_posid_2(i)
                        if posid < FULL_CARDS // 2:
                            self.rotated_img[20+i]=pygame.transform.rotate(img[c][i], 180)
                        else:
                            self.rotated_img[20+i]=img[c][i]
                        gridpos=(posid%BOARD_SIZE[0],posid//BOARD_SIZE[0])
                        centerpos=(self.x0_2+gridpos[0]*GRID_SIZE[0]+GRID_SIZE[0]//2, self.y0+gridpos[1]*GRID_SIZE[1]+GRID_SIZE[1]//2)
                        self.card_rect[20+i]=self.rotated_img[20+i].get_rect(center=centerpos)
                    self.color_2=c
                    if self.color != self.color_2:
                        temp_waka=self.hand.copy()
                        temp_waka_2=self.hand_2.copy()
                        self.hand=[]
                        self.read_cards=(20-3)*2
                        for ii in range(20):
                            self.hand.append(temp_waka[ii])
                            self.hand.append(temp_waka_2[ii]+20)
                return c
        se["ken"].play()
        return 99
    
    def show_loading_screen(self):
        font = pygame.font.Font(None, 24)
        self.draftsc.blit(background_image_g, (0, 0), (0, 0, SIZE[0], SIZE[1]))
        text = font.render("Goshoku Hyakunin Isshu ver. 0.5       Loading...", True, (255, 255, 255))
        self.draftsc.blit(text, (SIZE[0] // 2 - text.get_width() // 2, SIZE[1] // 2 - text.get_height() // 2))
        self.screen.blit(self.draftsc, (0, 0))
        pygame.display.flip()

async def main():
    game = Karuta()
    game.initialize()
    game.show_loading_screen()
    game.load_source()
    running = True
    cnt=0
    read_cnt=0
    stage=0
    while running:
        #game.sizecheck()
        pygame.event.pump()
        if stage==0:
            if cnt%(SECTION_TIME_SELECT*FPS)==0:
                game.reset_section_select()
                cnt = 0
            game.draw_select_board()
            if game.cpu_mode_flag:
                game.draw_slider(game.cpuscore)
            if game.double_mode_flag:
                game.draw_selected_colors()
                if game.color is not None and game.color_2 is not None:
                    game.draw_startbtn(stage)
                    game.color_prepared=True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    px, py = event.pos
                    clicked=game.title_card_click_check(px,py)
                    if (clicked in range(BOARD_SIZE[0]) and not game.double_mode_flag) \
                        or (game.color is not None and game.color_2 is not None and game.double_mode_flag and\
                            game.color_prepared and\
                            game.button_rect_edge.collidepoint(px, py)):
                        stage = 1
                        cnt = -1
                        if  not game.double_mode_flag:
                            game.gamesize=(GRID_SIZE[0]*BOARD_SIZE[0]+BAR_W,GRID_SIZE[1]*BOARD_SIZE[1]) 
                            game.screen = pygame.display.set_mode(game.gamesize, pygame.RESIZABLE)
                            game.draftsc = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
                            game.info_rect=INFO_RECT_CAND[0]
                        else:
                            game.gamesize=(GRID_SIZE[0]*BOARD_SIZE[0]*2,GRID_SIZE[1]*BOARD_SIZE[1]+BAR_H) 
                            game.screen = pygame.display.set_mode(game.gamesize, pygame.RESIZABLE)
                            game.draftsc = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
                            game.info_rect=INFO_RECT_CAND[1]
                        if game.cpu_mode_flag:
                            game.set_cpuframes()
                    elif game.double_rect_off.collidepoint(px, py) or game.text_double_rect_off.collidepoint(px, py):
                         game.double_mode_flag=False
                         game.color=None
                         game.color_2=None
                    elif game.double_rect_on.collidepoint(px, py) or game.text_double_rect_on.collidepoint(px, py):
                         game.double_mode_flag=True
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
                    elif game.wander_rect_off.collidepoint(px, py) or game.text_wander_rect_off.collidepoint(px, py):
                        game.wander_mode_flag=False
                    elif game.wander_rect_on.collidepoint(px, py) or game.text_wander_rect_on.collidepoint(px, py):
                        game.wander_mode_flag=True
                    elif game.cpu_rect_off.collidepoint(px, py) or game.text_cpu_rect_off.collidepoint(px, py):
                        game.cpu_mode_flag=False
                        game.cpuscore = 0
                    elif game.cpu_rect_on.collidepoint(px, py) or game.text_cpu_rect_on.collidepoint(px, py):
                        game.cpu_mode_flag=True
                        game.cpuscore = 1200
                    elif KNOB_RADIUS >= ((px - game.knob_x) ** 2 + (py - (SLIDER_POS[1] + SLIDER_HEIGHT // 2)) ** 2) ** 0.5:
                        game.slider_dragging = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    game.slider_dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if game.slider_dragging:
                        px, py = event.pos
                        px-=game.x0
                        py-=game.y0
                        this_knob_x = px
                        if px >= SLIDER_POS[0] + SLIDER_WIDTH:
                            this_knob_x=SLIDER_POS[0] + SLIDER_WIDTH
                        elif px <=SLIDER_POS[0]:
                            this_knob_x = SLIDER_POS[0]
                        game.cpuscore = game.update_cpuscore(this_knob_x)
                        steps = (game.cpuscore - SLIDER_MIN_VALUE) // SLIDER_STEP
                        ratio = steps / ((SLIDER_MAX_VALUE - SLIDER_MIN_VALUE) // SLIDER_STEP)
                        game.knob_x= int(SLIDER_POS[0] + ratio * SLIDER_WIDTH)
        elif stage==1:
            game.draw_board(cnt,stage)
            game.draw_dist_info()
            game.draw_startbtn(stage)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    px, py = event.pos
                    clicked=game.card_click_check(px, py)
                    if clicked < FULL_CARDS*2:
                        game.draggingItemIndex = clicked
                        game.drgCornerOffsetX = game.card_rect[clicked].topleft[0]
                        game.drgCornerOffsetY = game.card_rect[clicked].topleft[1]
                        game.drgOffsetX = px - game.drgCornerOffsetX
                        game.drgOffsetY = py - game.drgCornerOffsetY
                    elif game.button_rect_edge.collidepoint(px, py):
                        cnt = (SECTION_TIME-2)*FPS
                        game.draggingItemIndex=None
                        game.drgOffsetX=0
                        game.drgOffsetY=0
                        game.drgCornerOffsetX=0
                        game.drgCornerOffsetY=0
                        read_cnt=-1
                        se["maru"].play()
                        stage=2
                elif event.type == pygame.MOUSEMOTION:
                    if game.draggingItemIndex != None:
                        px, py = event.pos
                        game.drgCornerOffsetX=px - game.drgOffsetX
                        game.drgCornerOffsetY=py - game.drgOffsetY
                elif event.type == pygame.MOUSEBUTTONUP:
                    if game.draggingItemIndex != None:
                        px, py = event.pos
                        clicked=game.card_click_check(px, py)
                        #dragcheck
                        if clicked < FULL_CARDS*2:
                            game.card_rect[game.draggingItemIndex], game.card_rect[clicked] = game.card_rect[clicked], game.card_rect[game.draggingItemIndex] 
                            if (game.card_rect[game.draggingItemIndex][1]//GRID_SIZE[1]-1.5) * (game.card_rect[clicked][1]//GRID_SIZE[1]-1.5) < 0:
                                game.rotated_img[game.draggingItemIndex]=pygame.transform.rotate(game.rotated_img[game.draggingItemIndex], 180)
                                game.rotated_img[clicked]=pygame.transform.rotate(game.rotated_img[clicked], 180)
                        game.draggingItemIndex = None
                        game.drgCornerOffsetX=0
                        game.drgCornerOffsetY=0 
                        game.drgOffsetX=0
                        game.drgOffsetY=0
            if cnt==0:
                pass
            elif cnt==SECTION_TIME*FPS:
                cnt = -1
        elif stage==2:
            if cnt%(SECTION_TIME*FPS)==0:
                game.currentobtained=0
                allobtained=False
                if read_cnt+1 >= game.read_cards:
                    game.finish_flag=True
                    cnt=-1
                    game.set_result()
                    pygame.mixer.stop()
                    stage=3
                else:
                    read_cnt += 1
                    game.reset_section(read_cnt)
                    cnt = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    px,py = event.pos
                    #if game.card_rect[game.hand[read_cnt]] is not None:
                    #getcard=None
                    #ith=read_cnt
                    #if game.color_2 is None:
                    #    if game.card_rect[game.hand[ith]] is not None:
                    #        getcard=game.hand[ith]
                    #else: 
                    #    if game.color==game.color_2:
                    #        if game.card_rect[game.hand[ith]] is not None:
                    #            getcard=game.hand[ith]
                    #        elif game.card_rect[game.hand[ith]+20] is not None:
                    #            getcard=game.hand[ith]+20
                    #    else:
                    #        if game.card_rect[game.hand[ith]] is not None:
                    #            getcard=game.hand[ith]
                    getcard=1
                    if getcard is not None:
                        res=game.update(px,py,read_cnt,100-int(100/(SECTION_TIME*FPS)*cnt))
                        if res:
                            game.currentobtained+=1
                        if game.double_mode_flag and game.color == game.color_2:
                            if game.currentobtained==2:
                                allobtained=True
                        elif game.currentobtained==1:
                                allobtained=True
                        if allobtained:
                            cnt=(SECTION_TIME-2)*FPS
            if game.cpuscore!=0 and cnt==game.cpuframes[read_cnt] and game.card_rect[game.hand[read_cnt]] is not None:
                game.cpu_atack(read_cnt,100-int(100/(SECTION_TIME*FPS)*cnt))
                cnt=(SECTION_TIME-2)*FPS
            game.draw_board(cnt,stage)
            if not game.double_mode_flag:
                game.draw_board_text(cnt)
                if game.char_mode_flag:
                    if read_cnt>=0:
                        #print(f"{read_cnt}")
                        game.draw_board_char(cnt,read_cnt)
            else:
                game.draw_board_text_2(cnt)
                if game.char_mode_flag:
                    if read_cnt>=0:
                        game.draw_board_char_2(cnt,read_cnt)
        if stage==3:
            #game.display_result()
            game.draw_board_result()
            if cnt%SECTION_TIME_RESULT*FPS==0:
                if game.finish_flag:
                    game.currentfanfale.play()
                    game.finish_flag=False
                cnt=0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    px,py = event.pos
                    if game.button_rect_edge.collidepoint(px, py):
                        cnt=0
                        read_cnt=0
                        stage=0
                        pygame.mixer.stop()
                        se["maru"].play()
                        game = Karuta()
                        game.initialize()
                        continue
        game.screen.blit(game.draftsc, (0, 0))
        pygame.display.flip()
        game.clock.tick(FPS)
        await asyncio.sleep(0) 
        cnt += 1
    pygame.quit()
    sys.exit()

#asyncio.run(main())
if __name__ == "__main__": # 二重ループを起こさないように変更
    try:
        asyncio.run(main())
    except RuntimeError as e:
        # In some environments, an event loop might already be running.
        # This handles such cases.
        if "cannot run loop while another loop is running" in str(e):
            loop = asyncio.get_event_loop()
            loop.create_task(main())
        else:
            raise
