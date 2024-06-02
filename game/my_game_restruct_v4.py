import pygame
from pygame import display
import sys
import random
import math
import requests
import json
import os
from PIL import Image
from datetime import datetime

accounts = [('admin','password')]
class Airplane():
    def __init__(self, x, y):
        self.image = pygame.image.load('C:/Users/MSI/DE30-3nd-4/game/source/plane.png')  # 비행기 이미지 로드
        self.image = pygame.transform.scale(self.image, (37, 37)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

class Missile:
    def __init__(self, x, y):
        self.image = pygame.image.load('C:/Users/MSI/DE30-3nd-4/game/source/bullet_1.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -2
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.speed

class Ailens:
    def __init__(self, screen_width):
        self.image = pygame.image.load('C:/Users/MSI/DE30-3nd-4/game/source/enemy.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)  # x 위치 랜덤 설정
        self.rect.y = -30
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.speed

class Red_Aliens():
    def __init__(self, screen_width):
        self.image = pygame.image.load('C:/Users/MSI/DE30-3nd-4/game/source/red_enemy.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)  # x 위치 랜덤 설정
        self.rect.y = -30
        self.speed = 2
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.x += random.randrange(-3, 4)
        self.rect.y += self.speed


class Health_point:
    def __init__(self, x, y):
        self.image = pygame.image.load('C:/Users/MSI/DE30-3nd-4/game/source/hp.png')
        self.image = pygame.transform.scale(self.image, (40, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw_hp(self, screen, hp):
        font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 20)  # 폰트 설정
        text = font.render(f"X {hp:02}", True, (255, 255, 255))  # 체력 텍스트 렌더링
        screen.blit(self.image, self.rect)  # 이미지 그리기
        screen.blit(text, (self.rect.right, self.rect.centery - 7))  # 텍스트 그리기

class Pop:
    def __init__(self, x, y):
        self.image = pygame.image.load('vpop.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def draw_pause(screen, screen_width, screen_height):
    font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 100)  # 폰트 설정
    sub_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 30)

    paused_text = font.render("Paused", True, (255, 255, 255))
    back_to_menu_txt = sub_font.render("Back to Menu",True,(255,255,255))
    exit_txt = sub_font.render("Exit",True,(255,255,255))

    paused_rect = paused_text.get_rect(center=(screen_width // 2, screen_height // 2))
    back_to_menu_txt_rect = back_to_menu_txt.get_rect(center=(screen_width // 2, (screen_height // 2)+90))
    exit_txt_rect = exit_txt.get_rect(center=(screen_width // 2, (screen_height // 2)+140))

    screen.blit(paused_text, paused_rect)
    screen.blit(back_to_menu_txt, back_to_menu_txt_rect)
    screen.blit(exit_txt,exit_txt_rect)
    return back_to_menu_txt_rect, exit_txt_rect

def draw_score(screen, score, x, y):
    font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 20)  # 폰트 설정
    text = font.render(f"Score : {score:000005}", True, (255, 255, 255))  # 점수 텍스트 렌더링
    screen.blit(text, (x, y))  # 화면에 텍스트 그리기

def draw_time(screen, time, x, y):
    second = math.floor(time / 1000)
    minutes = math.floor(time / (1000 * 60))
    font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 20)  # 폰트 설정
    text = font.render(f"time : {minutes:02}:{second:02}", True, (255, 255, 255))  # 시간 텍스트 렌더링
    screen.blit(text, (x, y))

def draw_menu(screen, screen_width, screen_height,id):
    main_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 60) # 폰트 설정
    sub_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 40)
    mini_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 10)

    title_text = main_font.render("HeHeBalSsa", True, (255, 255, 255))
    start_text = sub_font.render("Game Start", True, (255, 255, 255))
    LB_text = sub_font.render("LeaderBoard",True,(255, 255, 255))
    user_info_text = sub_font.render("My Info",True,(255, 255, 255))
    exit_text = sub_font.render("Exit",True,(255,255,255))
    user_id_text = mini_font.render(f"user id : {id}",True,(255, 255, 255))

    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3))
    start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
    LB_rect = LB_text.get_rect(center=(screen_width // 2, (screen_height // 2) +50))
    user_info_rect = user_info_text.get_rect(center=(screen_width // 2, (screen_height // 2) +100))
    exit_rect = exit_text.get_rect(center=(screen_width//2,(screen_height//2)+ 150))
    user_id_rect = user_id_text.get_rect(center=(50,screen_height- 10))

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(LB_text,LB_rect)
    screen.blit(user_info_text,user_info_rect)
    screen.blit(exit_text,exit_rect)
    screen.blit(user_id_text,user_id_rect)
    return start_rect, LB_rect, user_info_rect, exit_rect, title_text,start_text,LB_text,user_info_text,exit_text,sub_font

def draw_leaderboard(screen, screen_width, screen_height, data):
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    leaderboard_bg = pygame.image.load('C:/Users/MSI/DE30-3nd-4/game/source/leaderboard_bg.jpg')
    leaderboard_bg = pygame.transform.scale(leaderboard_bg, (screen_width, screen_height))
    screen.blit(leaderboard_bg, (0, 0))
    
    main_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 60) # 폰트 설정
    sub_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 40)
    mini_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 20)

    back_text = mini_font.render("Back", True, (255, 255, 255))
    back_rect = back_text.get_rect(center=(screen_width // 2, screen_height- 20))
    screen.blit(back_text,back_rect)

    title_text = main_font.render("Leaderboard", True, (255, 255, 255))
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))

    y_offset = 150
    # 속성명 표시
    attribute_names = list(data[0].keys())
    attribute_names.remove('ranking')  # 이름은 생략
    attribute_names.insert(0, 'Rank')  # 순위 추가
    for idx, name in enumerate(attribute_names):
        rendered_text = mini_font.render(name, True, (255, 255, 255))
        screen.blit(rendered_text, (40 + idx * 150, y_offset - 10))

    y_offset += 45
    for entry in data:
        name = entry.get('name')
        ranking = entry.get('ranking')
        play_count = entry.get('play_count')
        best_score = entry.get('best_score')
        average_score = entry.get('average_score')

        # 항목 표시
        attributes = [ranking, name, best_score, average_score, play_count]
        str_attr = ["Ranking", "Name", "Play Count", "Best Score", "Average Score"]
        for idx, attr in enumerate(attributes):
            rendered_text = mini_font.render(str(attr), True, (255, 255, 255))
            screen.blit(rendered_text, (45 + idx * 155, y_offset))
        y_offset += 45
    # pygame.display.flip()
    return back_rect


def draw_my_info(screen,screen_width,screen_height,id):
    main_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 60) # 폰트 설정
    sub_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 40)
    mini_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 20)
    body = {
            "user_or_game_id": id
            }
    url = "http://218.50.12.225:8000/api/usergames/"
    response = requests.post(url,body)
    game_data = response.json()


    game_data = response.json()
    
    best_score_data = max(game['score'] for game in game_data)
    average_score_data = sum(game['score'] for game in game_data) / len(game_data)
    total_elapsed_time = sum(game['elapsed_time'] for game in game_data)
    average_elapsed_time = total_elapsed_time / len(game_data)
    total_kill_count = sum(game['kill_count'] for game in game_data) / len(game_data)
    max_kill_count = max(game['kill_count'] for game in game_data)
    last_play_time = max(datetime.fromisoformat(game['when_played']) for game in game_data)

    id_text = sub_font.render(f"ID : {id}",True,(255,255,255))

    best_score = mini_font.render(f"Best score : {best_score_data}", True, (255, 255, 255))
    average_score = mini_font.render(f"Average score : {average_score_data}", True, (255, 255, 255))

    total_elapsed_time_text = mini_font.render(f"Total Elapsed Time : {total_elapsed_time}", True, (255,255,255))
    average_elapsed_time = mini_font.render(f"Total Elapsed Time : {total_elapsed_time}", True, (255,255,255))

    total_kill_count_text = mini_font.render(f"Total Kill Count : {total_kill_count}",True, (255,255,255))
    max_kill_count_text = mini_font.render(f"Best Kill Count : {max_kill_count}",True,(255,255,255))

    last_play_time_text = mini_font.render(f"Latest Play Time : {last_play_time}",True,(255,255,255))

    back_text = mini_font.render("Back", True, (255, 255, 255))


    id_text_rect = id_text.get_rect(left=20, centery = (screen_height // 20)*3)
    best_score_rect = best_score.get_rect(left=20, centery = (screen_height // 20)*6)
    average_score_rect = average_score.get_rect(left=20, centery = (screen_height // 20)*7)
    total_elapsed_time_rect = total_elapsed_time_text.get_rect(left=20, centery = (screen_height // 20)*8)
    average_elapsed_rect = average_elapsed_time.get_rect(left=20, centery = (screen_height // 20)*9)
    total_kill_count_rect = total_kill_count_text.get_rect(left=20, centery = (screen_height // 20)*10)
    max_kill_count_rect = max_kill_count_text.get_rect(left=20, centery = (screen_height // 20)*11)
    last_play_time_rect = last_play_time_text.get_rect(left=20, centery = (screen_height // 20)*12)
    back_rect = back_text.get_rect(center=(screen_width // 2-100, screen_height // 3 + 300))

    screen.blit(id_text,id_text_rect)
    screen.blit(best_score,best_score_rect)
    screen.blit(average_score,average_score_rect)
    screen.blit(total_elapsed_time_text,total_elapsed_time_rect)
    screen.blit(average_elapsed_time,average_elapsed_rect)
    screen.blit(total_kill_count_text,total_kill_count_rect)
    screen.blit(max_kill_count_text,max_kill_count_rect)
    screen.blit(last_play_time_text,last_play_time_rect)
    screen.blit(back_text,back_rect)
    return back_rect

def login_page_login_and_legister(screen, screen_width, screen_height):
    main_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 40) # 폰트 설정
    sub_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 20)

    login_text = main_font.render("Login", True, (255, 255, 255))
    login_rect = login_text.get_rect(center=(screen_width // 2 , screen_height // 3 + 200))

    register_text = sub_font.render("Register", True, (255, 255, 255))
    register_rect = register_text.get_rect(center=(screen_width // 2, screen_height // 3 + 250))

    screen.blit(login_text, login_rect)
    screen.blit(register_text, register_rect)
    return login_rect, register_rect

def draw_register_page(screen, screen_width,screen_height):
    main_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 40) # 폰트 설정
    sub_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 20)

    create_account_text = main_font.render("Create Account", True, (255, 255, 255))
    back_text = sub_font.render("Back", True, (255, 255, 255))

    create_account_rect = create_account_text.get_rect(center=(screen_width // 2, screen_height // 3 + 200))
    back_text_rect = back_text.get_rect(center=(screen_width // 2, screen_height // 3 + 250))

    screen.blit(back_text,back_text_rect)
    screen.blit(create_account_text,create_account_rect)
    return create_account_rect, back_text_rect

class TextInputBox:
    def __init__(self, x, y, w, h, font, inactive_color=pygame.Color('dark grey'), active_color=pygame.Color('white'), is_password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = inactive_color
        self.color_active = active_color
        self.color = self.color_inactive
        self.font = font
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False
        self.is_password = is_password
        self.sub_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 20)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                display_text = "*" * len(self.text) if self.is_password else self.text
                self.txt_surface = self.font.render(display_text, True, self.color)

    def update(self):
        # 텍스트 입력 상자의 너비를 텍스트 길이에 맞춰 조정
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen,screen_width,screen_height):
        title_text = self.font.render("HeHeBalSsa", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen_width // 2 + 5, screen_height // 3 - 80))

        id_text = self.sub_font.render("id", True, (255, 255, 255))
        id_rect = title_text.get_rect(center=((screen_width // 2)-24, (screen_height // 3)+50))

        pw_text = self.sub_font.render("password", True, (255, 255, 255))
        pw_rect = title_text.get_rect(center=((screen_width // 2)-24, (screen_height // 3)+108))

        # 텍스트 입력 상자에 텍스트 그리기
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        screen.blit(title_text, title_rect)
        screen.blit(id_text, id_rect)
        screen.blit(pw_text, pw_rect)

        # 텍스트 입력 상자 그리기
        pygame.draw.rect(screen, self.color, self.rect, 2)
        
def load_gif_frames(file_path):
    pil_image = Image.open(file_path)
    frames = []
    try:
        while True:
            frame = pil_image.copy().convert("RGBA")
            mode = frame.mode
            size = frame.size
            data = frame.tobytes()
            surface = pygame.image.fromstring(data, size, mode)
            frames.append(surface)
            pil_image.seek(len(frames))
    except EOFError:
        pass
    return frames
def initialize_game(screen_width,screen_height):
    global plane, heart, enemies, missiles, enemy_timer, paused, is_game, hp, score
    # 비행기 객체 생성
    plane = Airplane(screen_width // 2, screen_height - 50)

    # 체력 아이콘 생성
    heart = Health_point(screen_width - 70, screen_height - 20)

    # 적 리스트
    enemies = []

    # 미사일 리스트
    missiles = []

    # 적 생성 시간 추적
    enemy_timer = pygame.time.get_ticks()

    # 일시정지 여부
    paused = False

    # # 게임 진행 여부
    # is_game = False

    # 초기 점수 및 체력 설정
    score = 0  
    hp = 3  

    # 무적 여부
    is_invincible = False
    invincible_start_time = 0
    invincible_duration = 10000

def main():
    pygame.init()
    pygame.display.init()
    global score, hp, plane, heart, enemies, missiles, enemy_timer, event_start_time, last_fired_time, paused, is_game, is_login_page, is_menu_page

    screen_width = 400
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    # 창 제목 설정
    pygame.display.set_caption("히히발싸")

    # 폰트 설정
    font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 30)

    # 로그인창 텍스트박스 생성
    id_box = TextInputBox(screen_width // 2 - 100, screen_height // 2 - 50, 200, 32, font)
    pw_box = TextInputBox(screen_width // 2 - 100, screen_height // 2 + 10 , 200, 32, font,is_password=True)
    boxes = [id_box, pw_box]

    # 레지스터창 텍스트박스 생성
    register_id_box = TextInputBox(screen_width // 2 - 100, screen_height // 2 - 50, 200, 32, font)
    register_pw_box = TextInputBox(screen_width // 2 - 100, screen_height // 2 + 10 , 200, 32, font,is_password=True)
    register_boxes = [register_id_box, register_pw_box]

    # GIF 로드
    gif_path = "C:/Users/MSI/DE30-3nd-4/game/source/gif_bg.gif"
    gif_frames = load_gif_frames(gif_path)
    current_frame = 0
    frame_delay = 5
    frame_counter = 0

    # 게임 관련 변수 초기화
    initialize_game(screen_width,screen_height)

    # 배경 설정
    game_bg = pygame.image.load('C:/Users/MSI/DE30-3nd-4/game/source/screen.jpg')
    game_bg = pygame.transform.scale(game_bg, (screen_width, screen_height))

    menu_bg = pygame.image.load('C:/Users/MSI/DE30-3nd-4/game/source/menu.jpg')
    menu_bg = pygame.transform.scale(menu_bg, (screen_width, screen_height))

    # 화면 흔들림 관련 변수
    shake_duration = 200  # 흔들림 지속 시간 (ms)
    shake_intensity = 5  # 흔들림 강도 (pixel)
    shake_start_time = 0  # 흔들림 시작 시간

    # 발사체 쿨타임
    missile_cooldown = 400
    last_fired_time = 0

    # 로그인 화면 여부
    is_login_page = True

    # 레지스터 화면 여부
    is_register_page = False

    # 메뉴 화면 여부
    is_menu_page = False

    # 게임 진행 여부
    is_game = False

    # 리더보드 화면 여부
    is_LB = False

    # 개인정보 화면 여부
    is_myinfo = False

    # 게임 오버 여부
    is_game_over = False

    # 일시정지 여부
    paused = False

    login_failed = False
    fail_message_time = 0
    shake = False
    shake_duration = 0
    shake_start_time = 0

    register_failed = False
    register_fail_message_time = 0

    # 게임 루프
    clock = pygame.time.Clock()
    running = True
    
    while running:
        shake_offset_x = 0
        shake_offset_y = 0

        if is_login_page or is_register_page:
            frame_counter += 1
            if frame_counter >= frame_delay:
                current_frame = (current_frame + 1) % len(gif_frames)
                frame_counter = 0

            screen.blit(gif_frames[current_frame], (0, 0))
            # pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if is_login_page:
                for box in boxes:
                    box.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if login_rect.collidepoint(mouse_pos):
                        # 로그인 로직
                        username = str(id_box.text)
                        password = str(pw_box.text)
                        json_data = {
                            "name": username,
                            "password": password
                        }
                        url = "http://218.50.12.225:8000/api/login/"
                        try:
                            response = requests.post(url, json=json_data)
                            print(f"Response: {response.status_code}, {response.text}")
                            if response.status_code == 200:
                                user_id = response.json().get("user_or_game_id")
                                print("Login successful")
                                is_login_page = False
                                is_menu_page = True
                            else:
                                print("Login failed")
                                login_failed = True
                                fail_message_time = pygame.time.get_ticks()
                                shake = True
                                shake_duration = 500  # 화면 흔들림 지속 시간 (밀리초)
                                shake_start_time = pygame.time.get_ticks()
                        except requests.RequestException as e:
                            print(f"Request failed: {e}")
                            login_failed = True
                            fail_message_time = pygame.time.get_ticks()
                            shake = True
                            shake_duration = 500
                            shake_start_time = pygame.time.get_ticks()
                    if register_rect.collidepoint(mouse_pos):
                        is_login_page = False
                        is_register_page = True
            elif is_register_page:
                for box in register_boxes:
                    box.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if create_account_rect.collidepoint(mouse_pos):
                        username = str(register_id_box.text)
                        password = str(register_pw_box.text)
                        json_data = {
                            "name": username,
                            "password": password
                        }
                        url = "http://218.50.12.225:8000/api/register/"
                        response = requests.post(url, json=json_data)
                        if response.status_code == 200:
                            print("Account created")
                            # print(username,password)
                            # accounts.append((username, password))
                            is_register_page = False
                            is_login_page = True
                        elif response.status_code == 409:
                            print("same id already exist",response.status_code)
                            # print(username,password)
                            register_failed = True
                            register_fail_message_time = pygame.time.get_ticks()
                        else:
                            print("Register failed with status code:", response.status_code)
                            # print(username,password)
                            register_failed = True
                            register_fail_message_time = pygame.time.get_ticks()

                    if back_text_rect.collidepoint(mouse_pos):
                        is_register_page = False
                        is_login_page = True

        if shake and pygame.time.get_ticks() - shake_start_time < shake_duration:
            shake_offset_x = pygame.time.get_ticks() % 10 - 5
            shake_offset_y = pygame.time.get_ticks() % 10 - 5
            screen.blit(screen, (shake_offset_x, shake_offset_y))
        else:
            shake = False
            shake_offset_x = 0
            shake_offset_y = 0

        if is_login_page:
            login_rect, register_rect = login_page_login_and_legister(screen, screen_width, screen_height)
            for box in boxes:
                box.update()
                box.draw(screen, screen_width, screen_height)
        elif is_register_page:
            create_account_rect, back_text_rect = draw_register_page(screen, screen_width, screen_height)
            for box in register_boxes:
                box.update()
                box.draw(screen, screen_width, screen_height)

        # 로그인 실패 시 메시지 표시
        if login_failed:
            fail_duration = 2000 
            if pygame.time.get_ticks() - fail_message_time < fail_duration:
                fail_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 30)
                fail_text = fail_font.render("Login Failed", True, (255, 0, 0))
                screen.blit(fail_text, (screen_width // 2 - fail_text.get_width() // 2, screen_height // 2 + 50))
            else:
                login_failed = False
        if register_failed:
            register_fail_duration = 2000 
            if pygame.time.get_ticks() - register_fail_message_time < register_fail_duration:
                fail_font = pygame.font.Font('C:/Users/MSI/DE30-3nd-4/game/source/ARCADE.TTF', 30)
                fail_text = fail_font.render("Same ID Already Exist", True, (255, 0, 0))
                screen.blit(fail_text, (screen_width // 2 - fail_text.get_width() // 2, screen_height // 2 + 50))
            else:
                register_failed = False
        if is_login_page or is_register_page:
            pygame.display.flip()
            clock.tick(30)

        if is_menu_page:
            screen.blit(menu_bg, (0, 0))
            start_rect, LB_rect, user_info_rect, exit_rect, title_text,start_text,LB_text,user_info_text,exit_text,sub_font = draw_menu(screen, screen_width, screen_height,user_id)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_rect.collidepoint(mouse_pos):
                        initialize_game(screen_width,screen_height)
                        is_menu_page = False
                        is_game = True
                        is_LB = False
                        is_myinfo = False
                    elif exit_rect.collidepoint(mouse_pos):
                        running = False
                    elif LB_rect.collidepoint(mouse_pos):
                        is_menu_page = False
                        is_game = False
                        is_LB = True
                        is_myinfo = False
                    elif user_info_rect.collidepoint(mouse_pos):
                        is_menu_page = False
                        is_game = False
                        is_LB = False
                        is_myinfo = True
        if is_menu_page == False and is_LB:
            # URL 및 데이터 가져오기
            url = "http://218.50.12.225:8000/api/leaderboard/"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                sorted_data = sorted(data, key=lambda x: x['ranking'])
            except requests.RequestException as e:
                print(f"Request failed: {e}")
                sorted_data = []
            screen.blit(menu_bg, (0, 0))
            back_rect = draw_leaderboard(screen, screen_height, screen_width, sorted_data)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type ==pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_rect.collidepoint(mouse_pos):
                        screen_width = 400
                        screen_height = 600
                        screen = pygame.display.set_mode((screen_width, screen_height))
                        is_LB = False
                        is_menu_page = True
        elif is_menu_page == False and is_myinfo:
            screen.blit(menu_bg, (0, 0))
            back_rect = draw_my_info(screen, screen_height, screen_width,user_id)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type ==pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_rect.collidepoint(mouse_pos):
                        is_myinfo = False
                        is_menu_page = True

        elif is_menu_page == False and is_game == True:
            event_start_time = pygame.time.get_ticks()
            play_time = pygame.time.get_ticks() - event_start_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and event_start_time - last_fired_time > missile_cooldown:
                        missile = Missile(plane.rect.centerx, plane.rect.top)
                        missiles.append(missile)
                        last_fired_time = event_start_time
                    if event.key == pygame.K_p and not paused:
                        paused = True
                        paused_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_p and paused:
                        paused = False
                        event_start_time -= paused_time
            if paused:
                back_to_menu_txt_rect, exit_txt_rect = draw_pause(screen, screen_width, screen_height)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if back_to_menu_txt_rect.collidepoint(mouse_pos):
                            paused = False
                            is_menu_page = True
                        elif exit_txt_rect.collidepoint(mouse_pos):
                            running = False
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and plane.rect.left > 0:
                    plane.move(-plane.speed, 0)
                if keys[pygame.K_RIGHT] and plane.rect.right < screen_width:
                    plane.move(plane.speed, 0)
                if keys[pygame.K_UP] and plane.rect.top > 0:
                    plane.move(0, -plane.speed)
                if keys[pygame.K_DOWN] and plane.rect.bottom < screen_height:
                    plane.move(0, plane.speed)

                screen.blit(game_bg, (0, 0))

                plane.draw(screen)

                heart.draw_hp(screen, hp)

                if event_start_time - enemy_timer > 300 and is_menu_page == False:
                    enemy = Ailens(screen_width)
                    if event_start_time >= 30000:
                        red_enemy = Red_Aliens(screen_width)
                        enemies.append(red_enemy)
                    enemies.append(enemy) 
                    enemy_timer = event_start_time

                for e in enemies[:]:
                    e.update()
                    e.draw(screen)
                    if e.rect.y > screen_height:
                        enemies.remove(e)

                    if pygame.sprite.collide_mask(plane, e):
                        hp -= 1
                        enemies.remove(e)
                        if hp == -1:
                            is_menu_page = True
                            is_game = False
                            is_game_over = True
                            hp = 3

                        shake_start_time = event_start_time

                    for missile in missiles[:]:
                        if pygame.sprite.collide_mask(missile, e):
                            enemies.remove(e)
                            missiles.remove(missile)
                            score += 10

                for missile in missiles[:]:
                    missile.update()
                    missile.draw(screen)
                    if missile.rect.bottom < 0:
                        missiles.remove(missile)

                if event_start_time - shake_start_time < shake_duration:
                    shake_offset_x = random.randint(-shake_intensity, shake_intensity)
                    shake_offset_y = random.randint(-shake_intensity, shake_intensity)
                    screen.blit(game_bg, (shake_offset_x, shake_offset_y))

                draw_score(screen, score, screen_width - 130, 10)
                draw_time(screen, event_start_time, 10, screen_height - 30)
                if is_game_over:
                    game_data = {
                                "user_or_game_id": user_id,
                                "when_played": datetime.now().isoformat(),
                                "kill_count": int(score/10),
                                "elapsed_time": event_start_time,
                                "score": score
                                }
                    url = "http://218.50.12.225:8000/api/savegame/"
                    response = requests.post(url, json=game_data)

                    key_data = {
                    "SECRET_KEY": "7276"
                    }
                    url = "http://218.50.12.225:8000/api/update/"
                    response = requests.post(url, json=key_data)
                    is_game_over = False
        pygame.display.flip()
        clock.tick(300)




    pygame.quit()
    sys.exit()

screen_width = 400
screen_height = 600
if __name__ == "__main__":
    main()
    initialize_game(screen_width,screen_height)
