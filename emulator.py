#
#   Code for GPS-Track emulator, needs some refactoring ;)
#

import pygame, sys, requests, json
from threading import Semaphore

pygame.init()

#### Variables
S_WiDTH = 700
S_HEIGHT = 601
SCREEN = pygame.display.set_mode((S_WiDTH, S_HEIGHT))
ICON = pygame.image.load("assets/wifi_icon.png")
BG = pygame.image.load("assets/GPS-Tracker.png").convert_alpha()
pygame.display.set_icon(ICON)
pygame.display.set_caption("GPS-Tracker")
FONT = pygame.font.Font('assets/LCDMN___.TTF', 30)
FPS = 60
clock = pygame.time.Clock()
FIRMWARE_Version = '0.000'
FIRMWARE_Version_Downloaded = '0.000'
S = Semaphore(16)
json_data = {} # ??
updated = False
device_power = False
device_on = False
run_update = False
run_once = True
Txtpos_List = [ (165, 205), (160, 220), (165, 255), (165, 295), (160, 314), (170, 352)]
Txt_list = [ 'YA_TEAM 1', '__________________________', "LATITUDE: 12.12345", "LONGITUDE: 42.12345", '__________________________', "FIRMWARE: " + FIRMWARE_Version ]

#### Functions and Classes
def load_local_json():
    with open("static/js/emulator.json", "r") as read_json:
        json_data = json.load(read_json)
        for p in json_data:
            FIRMWARE_Version = p['firmware']
    return FIRMWARE_Version

def save_local_json(txtIn):
    with open("static/js/emulator.json", "r") as write_json:
        data = json.load(write_json)
        for p in data:
            p['firmware'] = txtIn
    with open("static/js/emulator.json", "w") as write_json:
        json.dump(data, write_json)

def get_api_json():
    myJson = requests.get('https://ya-gps-tracker.herokuapp.com/api/v1/firmware') # Production Stage 1
    #myJson = requests.get('http://localhost:5000/api/v1/firmware') # Develop
    for i in myJson.json():
        tmp_str = i['firmware']
    jh.json_ver_memory2(tmp_str)

def print_default(txt_in, txtpos):
    txt = FONT.render(txt_in, True, (0,0,0)) 
    SCREEN.blit(txt, txtpos)

class Button():
    def __init__(self, color, x, y, width, height, text):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline = None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            pass

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

def loading_firmware():
    if run_update:
        txt = FONT.render('CHECK FOR UPDATE...', True, (0,0,0))
        SCREEN.blit(txt, Txtpos_List[3])
        get_api_json()
        FIRMWARE_Version = jh.json_ver_return1()
        FIRMWARE_Version_Downloaded = jh.json_ver_return2()
        FIRM_OLD = int(FIRMWARE_Version.replace('.', ''))
        FIRM_NEW = int(FIRMWARE_Version_Downloaded.replace('.', ''))
        if FIRM_NEW > FIRM_OLD and updated == False:
            loading_str1 = "DOWNLOADING:"
            loading_str2 = "@"
            jh.json_ver_memory1(FIRMWARE_Version_Downloaded)
            for i in range(0, 12):
                # loading_str2.append('X')
                loading_str2 += '@'
                txt = FONT.render(loading_str1 + loading_str2, True, (0,0,0))
                SCREEN.blit(txt, Txtpos_List[5])
                pygame.display.update()
                pygame.time.delay(200)
        else:
            for i in range(0, 12):
                txt = FONT.render('NO NEW FIRMWARE AVAILABLE', True, (0,0,0))
                SCREEN.blit(txt, Txtpos_List[5])
                pygame.display.update()
                pygame.time.delay(250)

class json_handler():
    def __init__(self):
        self.firmversion1 = ''
        self.firmversion2 = ''

    def __del__(self):
        pass

    def json_ver_memory1(self, str1):
        self.firmversion1 = str1

    def json_ver_memory2(self, str1):
        self.firmversion2 = str1
    
    def json_ver_return1(self):
        return self.firmversion1

    def json_ver_return2(self):
        return self.firmversion2

def default_screen():
    FIRMWARE_Version = jh.json_ver_return1()
    Txt_list[5] = "FIRMWARE: " + FIRMWARE_Version
    for index, t in enumerate(Txtpos_List):
        print_default(Txt_list[index], t)

#### MainLoop
jh = json_handler()
btn_start = Button((255,255,255), 140, 443, 110, 30, '')
btn_update = Button((255,255,255), 300, 443, 110, 30, '')
btn_stop = Button((255,255,255), 460, 443, 110, 30, '')
run = True
jrun = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            run = False
            save_local_json(jh.json_ver_return1())
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_start.isOver(pos):
                device_power = True
                device_on = True
                run_update = False
                while jrun:
                    jh.json_ver_memory1(load_local_json())
                    jrun = False
                default_screen()
            if btn_update.isOver(pos):
                device_on = False
                run_update = True
            if btn_stop.isOver(pos):
                device_power = False
                device_on = False
                run_update = False

    btn_start.draw(SCREEN)
    btn_update.draw(SCREEN)
    btn_stop.draw(SCREEN)
    SCREEN.fill((255,255,255))
    SCREEN.blit(BG, (0, 0))

    if device_on and run_update == False:
        default_screen()
    elif device_on == False and run_update == True and device_power == True:
        loading_firmware()
        run_update = False
        device_on = True

    pygame.display.update()

pygame.quit()
sys.exit()