import pygame
import os
from game import Game
import pickle
import random
import sys


pygame.init()
pygame.font.init()

WIDTH = 1200
HEIGHT = 700
card_size_x = 120
card_size_y = 180

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Black Jack")

# Import Music
bgm = pygame.mixer.music.load("sound/bg_music.wav")
click_sound = pygame.mixer.Sound("sound/click.wav")
coin_sound = pygame.mixer.Sound("sound/coins_clinking.wav")
no_sound = pygame.mixer.Sound("sound/no.wav")
ding_sound = pygame.mixer.Sound("sound/ding_ding.wav")
drum_sound = pygame.mixer.Sound("sound/DRUMROLL.WAV")
card_sound = pygame.mixer.Sound("sound/card.wav")
cheer_sound = pygame.mixer.Sound("sound/horray_fireworks.wav")
stand_sound = pygame.mixer.Sound("sound/complete.wav")
card_shuffle_sound = pygame.mixer.Sound("sound/card_shuffle.wav")

# Import Images
my_image = {}
for dirpath, dirname, filenames in os.walk("images"):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)
        try:
            my_image[filename] = pygame.image.load(file_path)
        except:
            print("unsupported file", filename)


def msg2screen(txt, x, y, color, size):
    screen_txt = pygame.font.SysFont(None, size).render(txt, True, color)
    screen.blit(screen_txt, (int(x), int(y)))


def screen_blit(img, x, y, transform_size=None):
    if not transform_size:
        screen.blit(my_image[img], (int(x), int(y)))
    else:
        transform_pic = pygame.transform.scale(my_image[img], (transform_size[0], transform_size[1]))
        screen.blit(transform_pic, (int(x), int(y)))


def save_data():
    profile = {
        "name": user.name,
        "profile_pic": user.profile_img
    }
    with open("profile_setting.txt", "wb") as f:
        f.write(pickle.dumps(profile))

    coin_dict = {
        "Eva": user.coin,
        game.players[1].name: game.players[1].coin,
        game.players[2].name: game.players[2].coin,
    }
    if game.final:
        with open("coin_history.txt", "wb") as f:
            f.write(pickle.dumps(coin_dict))


clicked = False


def event():
    global mouse_position, click_position, exit_main, game, clicked, run, play_again
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save profile changes
            save_data()
            run = False
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_position = pygame.mouse.get_pos()
            game.click = True
            clicked = True
            print(click_position)
        else:
            click_position = (-1, -1)
            game.click = False
            clicked = False

        if event.type == pygame.MOUSEMOTION:
            mouse_position = pygame.mouse.get_pos()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                exit_main = True


def main_page():
    global exit_main, mouse_position, setting

    screen_blit("bg1.jpg", 0, 0, (WIDTH, HEIGHT))

    # Mouse over Play
    try:
        mouse_position
    except:
        mouse_position = (-1,-1)
    if 590 < mouse_position[0] < 770 and 330 < mouse_position[1] < 390:
        enlargement = 30
        msg2screen("Play!", WIDTH / 2 - enlargement / 2, HEIGHT / 2 - 20 - enlargement / 2, (255, 255, 255),
                   100 + enlargement)

    else:
        msg2screen("Play!", WIDTH / 2, HEIGHT / 2 - 20, (255, 255, 255), 100)

    # Mouse click Play
    if 590 < click_position[0] < 770 and 330 < click_position[1] < 390:
        click_sound.play()
        exit_main = True

    # Mouse over Setting
    if 590 < mouse_position[0] < 786 and 429 < mouse_position[1] < 496:
        enlargement = 30
        msg2screen("Setting", WIDTH / 2 - 25 - enlargement / 2, HEIGHT / 2 + 90 - enlargement / 2, (255, 255, 255),
                   100 + enlargement)

    else:
        msg2screen("Setting", WIDTH / 2 - 25, HEIGHT / 2 + 90, (255, 255, 255), 80)

    if 590 < click_position[0] < 786 and 429 < click_position[1] < 496:
        click_sound.play()
        exit_main = True
        setting = True


attempt_to_change_name = False
display_image = False

highlight_img = False
selection = None



def setting_page():
    global exit_main, mouse_position, click_position, game, attempt_to_change_name, display_image, game, selection, setting
    screen_blit("setting_page.jpg", 0, 0, (WIDTH, HEIGHT))
    msg2screen("Profile", 100, 20, (255, 125, 0), 70)
    msg2screen("Player's name: ", 100, 100, (255, 255, 255), 70)
    msg2screen("Coin amount: ", 100, 180, (255, 255, 255), 70)
    msg2screen(f"{int(user.coin)}", 500, 180, (125, 255, 0), 70)
    msg2screen("Profile image: ", 100, 260, (255, 255, 255), 70)

    # Change user name
    if 500 < click_position[0] < 600 and 100 < click_position[1] < 150:
        msg2screen(f"{user.name}", 500, 100, (125, 255, 0), 90)
        if not attempt_to_change_name:
            user.name = '|'
        attempt_to_change_name = True
        msg2screen("Please Enter your user name:", 500, 40, (125, 255, 0), 70)

        user.name = input_val(user.name).capitalize()

    elif 500 < mouse_position[0] < 600 and 100 < mouse_position[1] < 150:
        if attempt_to_change_name:
            msg2screen("Please Enter your user name:", 500, 40, (125, 255, 0), 70)

            try:
                user.name = input_val(user.name).capitalize()
            except:
                pass

        msg2screen(f"{user.name}", 500, 100, (125, 255, 0), 90)
    else:
        msg2screen(f"{user.name}", 500, 100, (125, 255, 0), 70)

    # Change the profile image
    if 500 < click_position[0] < 560 and 260 < click_position[1] < 320:
        display_image = True

    elif 500 < mouse_position[0] < 560 and 260 < mouse_position[1] < 320:
        screen_blit(user.profile_img, 500, 260, (80, 80))
    else:
        screen_blit(user.profile_img, 500, 260, (60, 60))

    if display_image:
        msg2screen("Please choose your profile image:", 100, 330, (255, 200, 200), 50)
        x_start = 20
        for i in range(9):
            img_selection = i + 1
            if x_start < click_position[0] < x_start + 80 and 400 < click_position[1] < 480:
                draw_square(255, 125, 0, x_start, 400, 100)
                if img_selection != 9 and img_selection != 7:
                    screen_blit(f"choice{img_selection}.jpg", x_start, 400, (100, 100))
                    user.profile_img = f"choice{img_selection}.jpg"
                elif img_selection == 7:
                    screen_blit("choice7.png", x_start, 400, (100, 100))
                    user.profile_img = "choice7.png"
                else:
                    screen_blit("Eva_profile.JPG", x_start, 400, (100, 100))
                    user.profile_img = "Eva_profile.JPG"
                selection = i + 1
            elif x_start < mouse_position[0] < x_start + 80 and 400 < mouse_position[1] < 480:
                if selection == i + 1:
                    draw_square(255, 125, 0, x_start, 400, 100)
                if img_selection != 9 and img_selection != 7:
                    screen_blit(f"choice{img_selection}.jpg", x_start, 400, (100, 100))
                elif img_selection == 7:
                    screen_blit("choice7.png", x_start, 400, (100, 100))
                else:
                    screen_blit("Eva_profile.JPG", x_start, 400, (100, 100))
            else:
                if selection == i + 1:
                    draw_square(255, 125, 0, x_start, 400, 80)
                if img_selection != 9 and img_selection != 7:
                    screen_blit(f"choice{img_selection}.jpg", x_start, 400, (80, 80))
                elif img_selection == 7:
                    screen_blit("choice7.png", x_start, 400, (80, 80))
                else:
                    screen_blit("Eva_profile.JPG", x_start, 400, (80, 80))
            x_start += 120

    # Quit Button
    if 1070 < click_position[0] < 1170 and 620 < click_position[1] < 670:
        save_data()
        exit_main = False
        setting = False
    elif 1070 < mouse_position[0] < 1170 and 620 < mouse_position[1] < 670:
        msg2screen("Quit", WIDTH - 120, HEIGHT - 70, (255, 255, 255), 70)
    else:
        msg2screen("Quit", WIDTH - 120, HEIGHT - 70, (255, 255, 255), 50)


def read_profile_data():
    global game
    with open("profile_setting.txt", "rb") as f:
        profile_data = pickle.loads(f.read())
    user.name = profile_data["name"]
    user.profile_img = profile_data["profile_pic"]


def input_val(string):
    if string == "|":
        string = ""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                return string + "a"
            elif event.key == pygame.K_b:
                return string + "b"
            elif event.key == pygame.K_c:
                return string + "c"
            elif event.key == pygame.K_d:
                return string + "d"
            elif event.key == pygame.K_e:
                return string + "e"
            elif event.key == pygame.K_f:
                return string + "f"
            elif event.key == pygame.K_g:
                return string + "g"
            elif event.key == pygame.K_h:
                return string + "h"
            elif event.key == pygame.K_i:
                return string + "i"
            elif event.key == pygame.K_j:
                return string + "j"
            elif event.key == pygame.K_k:
                return string + "k"
            elif event.key == pygame.K_l:
                return string + "l"
            elif event.key == pygame.K_m:
                return string + "m"
            elif event.key == pygame.K_n:
                return string + "n"
            elif event.key == pygame.K_o:
                return string + "o"
            elif event.key == pygame.K_p:
                return string + "p"
            elif event.key == pygame.K_q:
                return string + "q"
            elif event.key == pygame.K_r:
                return string + "r"
            elif event.key == pygame.K_s:
                return string + "s"
            elif event.key == pygame.K_t:
                return string + "t"
            elif event.key == pygame.K_u:
                return string + "u"
            elif event.key == pygame.K_v:
                return string + "v"
            elif event.key == pygame.K_w:
                return string + "w"
            elif event.key == pygame.K_x:
                return string + "x"
            elif event.key == pygame.K_y:
                return string + "y"
            elif event.key == pygame.K_z:
                return string + "z"
            elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                string = string[0:len(string) - 1]
                return string
            elif event.key == pygame.K_RETURN:
                return True
    if string == "":
        string = "|"
    return string


def draw_square(r, g, b, start_x, start_y, width=50):
    pygame.draw.line(screen, (r, g, b), (start_x, start_y), (start_x + width, start_y), 3)
    pygame.draw.line(screen, (r, g, b), (start_x, start_y), (start_x, start_y + width), 3)
    pygame.draw.line(screen, (r, g, b), (start_x + width, start_y + width), (start_x, start_y + width), 3)
    pygame.draw.line(screen, (r, g, b), (start_x + width, start_y + width), (start_x + width, start_y), 3)


def highlight(player, color=None):
    if not color:
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    else:
        r, g, b = color[0], color[1], color[2]

    if player == game.players[1]:
        draw_square(r, g, b, 200, 70)

    elif player == game.players[2]:
        draw_square(r, g, b, 950, 70)


    else:
        draw_square(r, g, b, 400, HEIGHT - 100)


def automatical_attribute(player):
    coin_list = player.computer_attribute(game, game.base)
    if coin_list == [0, 0, 0, 0, 0]:
        player.stand = True
        stand_sound.play()
    else:
        for i in range(5):
            if i == 0:
                for _ in range(int(coin_list[i])):
                    game.pool_token.append("1000_token.png")
            elif i == 1:
                for _ in range(int(coin_list[i])):
                    game.pool_token.append("500_token.png")
            elif i == 2:
                for _ in range(int(coin_list[i])):
                    game.pool_token.append("100_token.png")
            elif i == 3:
                for _ in range(int(coin_list[i])):
                    game.pool_token.append("20_token.png")
            elif i == 4:
                for _ in range(int(coin_list[i])):
                    game.pool_token.append("10_token.png")
        coin_sound.play()


played = False
play_sound = False
game_loop_count = 0

def game_page():
    global click_position, mouse_position, game, exit_main, played, game_loop_count

    # bgm
    if not played:
        pygame.mixer.music.play(-1)
        played = True

    DISPLAY_SPACE = 100

    screen_blit("bg2.jpg", 0, 0, (WIDTH, HEIGHT))

    # Player profile pic and coin
    screen_blit(user.profile_img, 400, HEIGHT - 100, (50, 50))
    screen_blit("coin.jpg", 390, HEIGHT - 40, (20, 20))
    msg2screen(f"{int(user.coin)}", 415, HEIGHT - 35, (255, 125, 0), 20)

    screen_blit(f"{game.players[1].name}_profile.JPG", 200, 70, (50, 50))
    screen_blit("coin.jpg", 190, 130, (20, 20))
    msg2screen(f"{int(game.players[1].coin)}", 215, 135, (255, 125, 0), 20)

    screen_blit(f"{game.players[2].name}_profile.JPG", 200 + 750, 70, (50, 50))
    screen_blit("coin.jpg", 190 + 750, 130, (20, 20))
    msg2screen(f"{int(game.players[2].coin)}", 215 + 750, 135, (255, 125, 0), 20)

    for player in game.players:
        if player.is_busted():
            idx = game.players.index(player)

            if idx == 1:
                if not game.final:
                    msg2screen("Busted", 200, 30, (255, 255, 255), 30)
            elif idx == 2:
                if not game.final:
                    msg2screen("Busted", 965, 30, (255, 255, 255), 30)
        else:
            idx = game.players.index(player)
            if player.stand:
                if idx == 0:
                    if not game.final:
                        msg2screen("Stand", 400, HEIGHT - 60, (255, 255, 255), 30)
                elif idx == 1:
                    if not game.final:
                        msg2screen("Stand", 200, 30, (255, 255, 255), 30)
                else:
                    if not game.final:
                        msg2screen("Stand", 965, 30, (255, 255, 255), 30)

    # Display cards on deck
    i = 0
    if 400 < mouse_position[0] < 750 and 50 < mouse_position[1] < 180:
        display_size_x = card_size_x
        display_size_y = card_size_y
    else:
        display_size_x = int(card_size_x * 0.75)
        display_size_y = int(card_size_y * 0.75)

    for card in game.Card.cards:
        i += 5
        x = WIDTH / 2 - 200 + i
        y = HEIGHT / 2 - 300
        screen_blit("red_back.png", x, y, (display_size_x, display_size_y))

    # If game finished, reveal the card
    game_finished = True
    for player in game.players:
        if player.stand == False and not player.is_busted():
            game_finished = False

    # Display cards on players' hand
    for player in game.players:
        index = game.players.index(player)
        if index == 0:
            x = 300
            y = HEIGHT - 300
            for card in player.cards:
                screen_blit(f"{card[1]}{card[0][0]}.png", x, y, (card_size_x, card_size_y))
                x += DISPLAY_SPACE * 1.5

        elif index == 1:
            x = 100
            y = 200
            if not game_finished:
                for card in player.cards:
                    if player.cards.index(card) == 0:
                        screen_blit("yellow_back.png", x, y, (int(card_size_x * 0.75), int(card_size_y * 0.75)))
                    else:
                        screen_blit(f"{card[1]}{card[0][0]}.png", x, y,
                                    (int(card_size_x * 0.75), int(card_size_y * 0.75)))
                    x += DISPLAY_SPACE
            else:
                for card in player.cards:
                    screen_blit(f"{card[1]}{card[0][0]}.png", x, y, (int(card_size_x * 0.75), int(card_size_y * 0.75)))
                    x += DISPLAY_SPACE


        else:
            x = WIDTH - 400
            y = 200
            if not game_finished:
                for card in player.cards:
                    if player.cards.index(card) == 0:
                        screen_blit("purple_back.png", x, y, (int(card_size_x * 0.75), int(card_size_y * 0.75)))
                    else:
                        screen_blit(f"{card[1]}{card[0][0]}.png", x, y,
                                    (int(card_size_x * 0.75), int(card_size_y * 0.75)))
                    x += DISPLAY_SPACE
            else:
                for card in player.cards:
                    screen_blit(f"{card[1]}{card[0][0]}.png", x, y, (int(card_size_x * 0.75), int(card_size_y * 0.75)))
                    x += DISPLAY_SPACE

    # Gamble token
    event()
    if WIDTH - 300 < mouse_position[0] < WIDTH - 300 + 70 and HEIGHT - 200 < mouse_position[1] < HEIGHT - 200 + 70:
        screen_blit("10_token.png", WIDTH - 300, HEIGHT - 200, (80, 80))
    else:
        screen_blit("10_token.png", WIDTH - 300, HEIGHT - 200, (70, 70))
    if WIDTH - 300 < click_position[0] < WIDTH - 300 + 70 and HEIGHT - 200 < click_position[1] < HEIGHT - 200 + 70:
        game.pool_token.append("10_token.png")
        click_position = (-1, -1)
        game.deduct_coins(10)
        user.attribute_pool = True
        game.pool += 10
        user.round_coin += 10
        coin_sound.play()

    if WIDTH - 220 < mouse_position[0] < WIDTH - 220 + 70 and HEIGHT - 200 < mouse_position[1] < HEIGHT - 200 + 70:
        screen_blit("20_token.png", WIDTH - 220, HEIGHT - 200, (80, 80))
    else:
        screen_blit("20_token.png", WIDTH - 220, HEIGHT - 200, (70, 70))
    if WIDTH - 220 < click_position[0] < WIDTH - 220 + 70 and HEIGHT - 200 < click_position[1] < HEIGHT - 200 + 70:
        game.pool_token.append("20_token.png")
        click_position = (-1, -1)
        game.deduct_coins(20)
        user.attribute_pool = True
        game.pool += 20
        user.round_coin += 20
        coin_sound.play()

    if WIDTH - 140 < mouse_position[0] < WIDTH - 140 + 70 and HEIGHT - 200 < mouse_position[1] < HEIGHT - 200 + 70:
        screen_blit("100_token.png", WIDTH - 140, HEIGHT - 200, (80, 80))
    else:
        screen_blit("100_token.png", WIDTH - 140, HEIGHT - 200, (70, 70))
    if WIDTH - 140 < click_position[0] < WIDTH - 140 + 70 and HEIGHT - 200 < click_position[1] < HEIGHT - 200 + 70:
        game.pool_token.append("100_token.png")
        click_position = (-1, -1)
        game.deduct_coins(100)
        user.attribute_pool = True
        game.pool += 100
        user.round_coin += 100
        coin_sound.play()

    if WIDTH - 260 < mouse_position[0] < WIDTH - 260 + 70 and HEIGHT - 100 < mouse_position[1] < HEIGHT - 100 + 70:
        screen_blit("500_token.png", WIDTH - 260, HEIGHT - 100, (80, 80))
    else:
        screen_blit("500_token.png", WIDTH - 260, HEIGHT - 100, (70, 70))
    if WIDTH - 260 < click_position[0] < WIDTH - 260 + 70 and HEIGHT - 100 < click_position[1] < HEIGHT - 100 + 70:
        game.pool_token.append("500_token.png")
        click_position = (-1, -1)
        game.deduct_coins(500)
        user.attribute_pool = True
        game.pool += 500
        user.round_coin += 500
        coin_sound.play()

    if WIDTH - 180 < mouse_position[0] < WIDTH - 180 + 70 and HEIGHT - 100 < mouse_position[1] < HEIGHT - 100 + 70:
        screen_blit("1000_token.png", WIDTH - 180, HEIGHT - 100, (80, 80))
    else:
        screen_blit("1000_token.png", WIDTH - 180, HEIGHT - 100, (70, 70))
    if WIDTH - 180 < click_position[0] < WIDTH - 180 + 70 and HEIGHT - 100 < click_position[1] < HEIGHT - 100 + 70:
        game.pool_token.append("1000_token.png")
        click_position = (-1, -1)
        game.deduct_coins(1000)
        user.attribute_pool = True
        game.pool += 1000
        user.round_coin += 1000
        coin_sound.play()

    # Pool display
    x = 430
    y = 220
    space = 30
    for img in game.pool_token:
        if x >= 750:
            x = 430
            y += space
        screen_blit(img, x, y, (70, 70))
        x += space

    # Display card value
    if not user.is_busted():
        msg2screen(f"Your current card value is: {user.value}", WIDTH / 2 - 40, HEIGHT - 50, (255, 255, 255), 30)
    else:
        if not game.final:
            msg2screen(f"BUSTED!", WIDTH / 2 - 40, HEIGHT - 50, (255, 255, 255), 40)

    # Check the base
    if user.round_coin > game.base:
        game.base = user.round_coin

    # card shuffle sound
    if game_loop_count < 30:
        card_shuffle_sound.play()
    if game_loop_count < 60:
        msg2screen("shuffling...", 777, 94, (200,255,200), 30)



    # Turn:
    # Add card
    if not game_finished:
        highlight(game.turn)

        if game.turn == user:
            msg2screen(f"It's your turn! ", 620, 614, (255, 255, 255), 40)
            if game.turn.is_busted() or game.turn.stand:
                if user.finish_attribute:
                    user.round_coin = 0
                    game.next_turn()

            else:
                if 400 < click_position[0] < 750 and 50 < click_position[1] < 180:
                    if user.round_coin >= game.base:
                        game.add_cards()
                        click_position = (-1, -1)
                        user.response = "Hit"
                        card_sound.play()
                    else:
                        no_sound.play()

                # Stand Bottom
                event()
                if 100 < mouse_position[0] < 200 and 600 < mouse_position[1] < 640:
                    screen_blit("dark_btn.png", 100, 600, (120, 60))
                    if not game.final:
                        msg2screen("Stand", 120, 610, (255, 255, 255), 35)
                else:
                    screen_blit("dark_btn.png", 100, 600, (100, 50))
                    if not game.final:
                        msg2screen("Stand", 120, 610, (255, 255, 255), 30)
                if 90 < click_position[0] < 230 and 590 < click_position[1] < 670:
                    user.response = "Stand"
                    user.stand = True
                    stand_sound.play()
                    user.finish_attribute = True
                    click_position = (-1,-1)

                if user.response:
                    if user.response == "Hit":
                        user.response = None
                        user.attribute_pool = False
                        user.finish_attribute = True
                        user.round_coin = 0
                        game.next_turn()

        # Check computer term
        else:
            if game.turn.is_busted():
                if user.round_coin > game.base:
                    game.base = user.round_coin
                game.next_turn()
            elif game.turn.stand:
                automatical_attribute(game.turn)
                game.next_turn()
            else:
                if game.turn.thinking == 0:
                    if game.turn.analysis_result():
                        automatical_attribute(game.turn)
                        if not game.turn.quit:
                            card_sound.play()
                            game.add_cards(game.turn)

                    else:
                        game.turn.stand = True
                        stand_sound.play()
                    game.next_turn()
                    game.turn.thinking = 100
                else:
                    game.turn.thinking -= 1

    # Base msg
    if not game.final:
        msg2screen(f"At least {int(game.base)} coins are required to continue", WIDTH / 2 - 200, 20, (255, 255, 255), 30)

    # Check winner
    if game_finished:
        score = {}
        for player in game.players:
            if not player.is_busted() and not player.quit:
                score[f"{player.name}"] = player.value
        if len(score) == 0:
            msg = "There's no winner"
            msg2screen(msg, WIDTH / 2 - 250, HEIGHT / 2, (255, 125, 0), 60)
        else:
            best = 0
            for name in score:
                if score[name] > best:
                    best = score[name]
                    best_name = [name]
                elif score[name] == best:
                    best_name.append(name)

            if len(best_name) == 1:
                msg = f"The winner is {best_name[0]}!!!"
            else:
                names = ''
                for n in best_name:
                    if best_name.index(n) != 0:
                        names += f",{n}"
                    else:
                        names += n
                msg = f"The winners are {names}!!!"

            msg2screen(msg, WIDTH / 2 - 250, HEIGHT / 2, (255, 125, 0), 60)
            for name in best_name:
                for player in game.players:
                    if player.name == name:
                        game.winner.append(player)
    # Game final
    global play_sound
    game.money_result()
    if game.final:
        for winner in game.winner:
            highlight(winner)
        if not play_sound:
            cheer_sound.play()
            drum_sound.play()
            play_sound = True
        msg2screen(f"Card Value:{game.players[1].value}", 44, 77, (255,255,255), 20)
        msg2screen(f"Card Value:{game.players[2].value}", 1050, 77, (255,255,255), 20)
        save_data()
        restart()

    game_loop_count += 1


def restart():
    global play_again, game, user, attempt_to_change_name, display_image, highlight_img
    global selection, played, play_sound, exit_main, setting, game_loop_count,click_position

    # Main menu
    if 30 < click_position[0] < 230 and 520 < click_position[1] < 570:
        play_again = True
        game = Game(["Eva", "Sean", "Computer"])
        user = game.players[0]

        # general setting
        game = Game(["Eva", "Sean", "Computer"])
        user = game.players[0]
        attempt_to_change_name = False
        display_image = False
        highlight_img = False
        selection = None
        played = False
        play_sound = False
        exit_main = False
        setting = False
        game_loop_count = 0

        read_profile_data()
        click_position = (-1,-1)


    elif 30 < mouse_position[0] < 230 and 520 < mouse_position[1] < 570:
        msg2screen("Main menu", 30, 520, (255, 200, 200), 90)
    else:
        msg2screen("Main menu", 30, 520, (255, 200, 200), 70)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                play_again = True
                save_data()
    # Play again
    if 30 < click_position[0] < 230 and 620 < click_position[1] < 670:
        play_again = True
        game = Game(["Eva", "Sean", "Computer"])
        user = game.players[0]

        # general setting
        game = Game(["Eva", "Sean", "Computer"])
        user = game.players[0]
        attempt_to_change_name = False
        display_image = False
        highlight_img = False
        selection = None
        played = False
        play_sound = False
        exit_main = True
        setting = False
        game_loop_count = 0

        read_profile_data()
        click_position = (-1,-1)

    elif 30 < mouse_position[0] < 230 and 620 < mouse_position[1] < 670:
        msg2screen("Play again!", 30, HEIGHT - 70, (255, 200, 200), 90)
    else:
        msg2screen("Play again!", 30, HEIGHT - 70, (255, 200, 200), 70)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                play_again = True
                save_data()





exit_main = False
setting = False
game = Game(["Eva", "Sean", "Computer"])

user = game.players[0]
read_profile_data()

play_again = True

run = True
while run:
    event()
    if not exit_main:
        main_page()
    elif setting:
        setting_page()
    else:
        game_page()
    pygame.display.flip()




