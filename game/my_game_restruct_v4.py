import pygame
from pygame import display
import sys
import random
import math
import requests
import json
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PROJECT.settings")





def send_json_data(url, json_data):
    try:
        headers = {'Content-Type': 'application/json'}  # JSON 형식의 데이터를 보낸다는 것을 명시
        response = requests.post(url, headers=headers, json=json_data)
        
        # HTTP 상태 코드 확인
        if response.status_code == 200:
            print("JSON 데이터 전송 성공!")
            print("응답:")
            print(response.text)
        else:
            print("JSON 데이터 전송 실패:", response.status_code)
    except Exception as e:
        print("오류 발생:", e)

class Airplane():
    def __init__(self, x, y):
        self.image = pygame.image.load('C:/Users/Playdata/Desktop/plane.png')  # 비행기 이미지 로드
        self.image = pygame.transform.scale(self.image, (37, 37)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 0.8
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

class Missile:
    def __init__(self, x, y):
        self.image = pygame.image.load('C:/Users/Playdata/Desktop/bullet_1.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -1
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.speed

class Ailens:
    def __init__(self, screen_width):
        self.image = pygame.image.load('C:/Users/Playdata/Desktop/enemy.png')
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
    def __init__(self,screen_width):
        self.image = pygame.image.load('C:/Users/Playdata/Desktop/red_enemy.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)  # x 위치 랜덤 설정
        self.rect.y = -30
        self.speed = 2
        self.mask = pygame.mask.from_surface(self.image)
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def update(self):
        self.rect.x += random.randrange(-3,4) 
        self.rect.y += self.speed


class Health_point:
    def __init__(self, x, y):
        self.image = pygame.image.load('C:/Users/Playdata/Desktop/hp.png')
        self.image = pygame.transform.scale(self.image, (40, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw_hp(self, screen, hp):
        font = pygame.font.Font('C:/Users/Playdata/Desktop/ARCADE.TTF', 20)  # 폰트 설정
        text = font.render(f"X {hp:02}", True, (255, 255, 255))  # 체력 텍스트 렌더링
        screen.blit(self.image, self.rect)  # 이미지 그리기
        screen.blit(text, (self.rect.right, self.rect.centery - 7))  # 텍스트 그리기

class Pop:
    def __init__(self, x, y):
        self.image = pygame.image.load('C:/Users/Playdata/Desktop/pop.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def draw_pause(screen, screen_width, screen_height):
    font = pygame.font.Font('C:/Users/Playdata/Desktop/ARCADE.TTF', 100)  # 폰트 설정
    sub_font = pygame.font.Font('C:/Users/Playdata/Desktop/ARCADE.TTF', 30)

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
    font = pygame.font.Font('C:/Users/Playdata/Desktop/ARCADE.TTF', 20)  # 폰트 설정
    text = font.render(f"Score : {score:000005}", True, (255, 255, 255))  # 점수 텍스트 렌더링
    screen.blit(text, (x, y))  # 화면에 텍스트 그리기

def draw_time(screen, time, x, y):
    second = math.floor(time / 1000)
    minutes = math.floor(time / (1000 * 60))
    font = pygame.font.Font('C:/Users/Playdata/Desktop/ARCADE.TTF', 20)  # 폰트 설정
    text = font.render(f"time : {minutes:02}:{second:02}", True, (255, 255, 255))  # 시간 텍스트 렌더링
    screen.blit(text, (x, y))

def draw_menu(screen, screen_width, screen_height):
    main_font = pygame.font.Font('C:/Users/Playdata/Desktop/ARCADE.TTF', 60)  # 폰트 설정
    sub_font = pygame.font.Font('C:/Users/Playdata/Desktop/ARCADE.TTF', 40)

    title_text = main_font.render("HeHeBalSsa", True, (255, 255, 255))
    start_text = sub_font.render("Game Start", True, (255, 255, 255))
    LB_text = sub_font.render("LeaderBoard",True,(255, 255, 255))
    user_info_text = sub_font.render("My Info",True,(255, 255, 255))
    exit_text = sub_font.render("Exit",True,(255,255,255))

    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3))
    start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
    LB_rect = LB_text.get_rect(center=(screen_width // 2, (screen_height // 2) +50))
    user_info_rect = user_info_text.get_rect(center=(screen_width // 2, (screen_height // 2) +100))
    exit_rect = exit_text.get_rect(center=(screen_width//2,(screen_height//2)+ 150))

    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(LB_text,LB_rect)
    screen.blit(user_info_text,user_info_rect)
    screen.blit(exit_text,exit_rect)
    return start_rect, LB_rect, user_info_rect, exit_rect, title_text,start_text,LB_text,user_info_text,exit_text,sub_font

class TextInputBox:
    def __init__(self, x, y, w, h, font, inactive_color=pygame.Color('grey'), active_color=pygame.Color('white')):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = inactive_color
        self.color_active = active_color
        self.color = self.color_inactive
        self.font = font
        self.text = ''
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 입력 상자를 클릭하면 활성화
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            # 색상 변경
            self.color = self.color_active if self.active else self.color_inactive
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)  # 엔터키를 누르면 입력된 텍스트를 출력
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # 백스페이스를 누르면 마지막 글자 삭제
                else:
                    self.text += event.unicode  # 다른 키를 누르면 텍스트 추가
                # 텍스트 렌더링
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # 텍스트 입력 상자의 너비를 텍스트 길이에 맞춰 조정
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # 텍스트 입력 상자에 텍스트 그리기
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # 텍스트 입력 상자 그리기
        pygame.draw.rect(screen, self.color, self.rect, 2)

def main():
    response = requests.get("192.168.0.40:8000/api/register/")
    pygame.init()
    score = 0  # 초기 점수
    hp = 3  # 초기 체력

    # 창 크기 설정
    screen_width = 400
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))

    # 창 제목 설정
    pygame.display.set_caption("히히발싸")


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

    clock = pygame.time.Clock()

    # 일시정지 여부
    paused = False

    # 프로그램 실행 여부
    running = True

    # 로그인 화면 여부
    is_login_page = True

    # 메뉴 화면 여부
    in_menu = False

    # 게임 진행 여부
    is_game = False

    # 리더보드 화면 여부
    is_LB = False

    # 개인정보 화면 여부
    is_myinfo = False

    # 배경 설정
    game_bg = pygame.image.load('C:/Users/Playdata/Desktop/screen.jpg')
    game_bg = pygame.transform.scale(game_bg, (screen_width,screen_height))

    menu_bg = pygame.image.load('C:/Users/Playdata/Desktop/menu.jpg')
    menu_bg = pygame.transform.scale(menu_bg, (screen_width,screen_height))

    login_bg = pygame.image.load('C:/Users/Playdata/Desktop/login_page.jpg')
    login_bg = pygame.transform.scale(login_bg, (screen_width,screen_height))

    # 화면 흔들림 관련 변수
    shake_duration = 200  # 흔들림 지속 시간 (ms)
    shake_intensity = 5  # 흔들림 강도 (pixel)
    shake_start_time = 0  # 흔들림 시작 시간

    # 발사체 쿨타임
    missile_cooldown = 400
    last_fired_time = 0

    # 시관 관련 변수
    play_time = None

    while running:
        event_start_time = pygame.time.get_ticks()
        
        shake_offset_x = 0
        shake_offset_y = 0

        if is_login_page:
            screen.blit(login_bg,(0,0))
            font = pygame.font.Font('C:/Users/Playdata/Desktop/ARCADE.TTF', 60)
            id_box = TextInputBox(100,200,100,20,font)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                id_box.handle_event(event)
                id_box.update()
                id_box.draw(screen)
            pygame.display.flip()

        else:
            if in_menu:
                screen.blit(menu_bg, (0, 0))  # 메뉴 화면 배경색
                start_rect, LB_rect, user_info_rect, exit_rect, title_text,start_text,LB_text,user_info_text,exit_text,sub_font = draw_menu(screen, screen_width, screen_height)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if start_rect.collidepoint(mouse_pos):
                            # start_text = sub_font.render("Game Start", True, (0, 255, 0))
                            in_menu = False
                            is_game = True
                            is_LB = False
                            is_myinfo = False
                            # title_text = sub_font.render("Game Start", True, (255, 255, 255))
                        # if LB_rect.collidepoint(mouse_pos):
                        #     in_menu = False
                        #     is_game = False
                        #     is_LB = True
                        #     is_myinfo = False
                        # if user_info_rect.collidepoint(mouse_pos):
                        #     in_menu = False
                        #     is_game = False
                        #     is_LB = False
                        #     is_myinfo = True
                        if exit_rect.collidepoint(mouse_pos):
                            running = False

            elif in_menu == False and is_game == True:
                play_time = (pygame.time.get_ticks() - event_start_time)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif pygame.key.get_pressed()[pygame.K_q]:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and play_time - last_fired_time > missile_cooldown:  
                            missile = Missile(plane.rect.centerx, plane.rect.top)
                            missiles.append(missile)
                            last_fired_time = play_time
                        if event.key == pygame.K_p and not paused:
                            paused = True
                            paused_time = pygame.time.get_ticks()
                        elif event.key == pygame.K_p and paused:
                            paused = False
                            play_time -= paused_time
                if paused:
                    back_to_menu_txt_rect, exit_txt_rect = draw_pause(screen, screen_width, screen_height)
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if back_to_menu_txt_rect.collidepoint(mouse_pos):
                                paused = False
                                in_menu = True
                            elif exit_txt_rect.collidepoint(mouse_pos):
                                running = False
                else:
                    # 키 입력으로 이동
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT] and plane.rect.left > 0:
                        plane.move(-plane.speed, 0)
                    if keys[pygame.K_RIGHT] and plane.rect.right < screen_width:
                        plane.move(plane.speed, 0)
                    if keys[pygame.K_UP] and plane.rect.top > 0:
                        plane.move(0, -plane.speed)
                    if keys[pygame.K_DOWN] and plane.rect.bottom < screen_height:
                        plane.move(0, plane.speed)


                    # 화면 채우기
                    screen.blit(game_bg, (0, 0))

                    # 비행기 그리기
                    plane.draw(screen)

                    # 체력 아이콘 그리기
                    heart.draw_hp(screen, hp)

                    # 일정 시간마다 적 생성
                    if play_time - enemy_timer > 300 and in_menu == False:
                        enemy = Ailens(screen_width)
                        if play_time >= 10000:
                            red_enemy = Red_Aliens(screen_width)
                            enemies.append(red_enemy)
                        enemies.append(enemy) 
                        enemy_timer = play_time  # 현재 시간으로 업데이트

                    # 적 업데이트 및 그리기
                    for e in enemies[:]: 
                        e.update()
                        e.draw(screen)
                        if e.rect.y > screen_height:
                            enemies.remove(e)

                        # 마스크를 사용하여 충돌 감지
                        if pygame.sprite.collide_mask(plane, e):
                            hp -= 1
                            enemies.remove(e)
                            if hp == -1:
                                in_menu = True
                                hp = 3
                                play_time = pygame.time.get_ticks()

                            # 화면 흔들림 효과
                            shake_start_time = event_start_time

                        for missile in missiles[:]:
                            if pygame.sprite.collide_mask(missile, e):
                                enemies.remove(e)
                                missiles.remove(missile)
                                score += 10

                    # 미사일 업데이트 및 그리기
                    for missile in missiles[:]:
                        missile.update()
                        missile.draw(screen)
                        if missile.rect.bottom < 0:
                            missiles.remove(missile)

                    # 화면 흔들림 효과 적용
                    if play_time - shake_start_time < shake_duration:
                        shake_offset_x = random.randint(-shake_intensity, shake_intensity)
                        shake_offset_y = random.randint(-shake_intensity, shake_intensity)
                        screen.blit(game_bg, (shake_offset_x, shake_offset_y))

                    draw_score(screen, score, screen_width - 130, 10)
                    draw_time(screen, play_time, 10, screen_height - 30)

                # 화면 업데이트
                pygame.display.flip()
                clock.tick(300)  # 프레임 속도 설정

        # # 게임 종료
        # pygame.quit()
        # sys.exit()

# if __name__ == "__main__":
#     main()
    

url = 'http://192.168.0.40:8000/api/register/'
data_to_send = {
    "name" : "newUserName",
    "password" : "newUserPW",
    "best_score" : 0,
    "average_score" : 0,
    "play_count" : 0
}



def 
url = "http://192.168.0.40:8000/api/signin/"
data = {
    "name" : "newUserName",
    "password" : "newUserPW",
    "best_score" : 0,
    "average_score" : 0,
    "play_count" : 0
}
response = requests.post(url, json=data)
print(response.json())