import pygame
import random

bloco = 40
qtd_caracteres = 0
qtd_linhas = 0
width = bloco * qtd_linhas
height = bloco * qtd_caracteres
mapa = []
filename = "mapa2.txt"
pygame.font.init()
player_x = 100
player_y = 100

play = "jogando"
pontos_para_vitoria = 5
fps = 10

tempo_acumulado_vilao = 0
tempo_acumulado_vilao_2 = 0
tempo_acumulado_vilao_3 = 0
tempo_acumulado_vilao_4 = 0

vilao_indice_frame = 0
vilao_indice_frame_2 = 0
vilao_indice_frame_3 = 0
vilao_indice_frame_4 = 0

vilao_tempo_animacao = 0
vilao_tempo_animacao_2 = 0
vilao_tempo_animacao_3 = 0
vilao_tempo_animacao_4 = 0


player = {
    "vida": 3,
    "pontuacao": 0,
    "velocidade": 5,
    "x": 50,
    "y": 50,
    "collided": False,
    "width": bloco,
    "height": bloco,
    "direcao": 1,
}

pedra = {
    "width": bloco,
    "height": bloco,
    "x": 0,
    "y": 0
}

pesca = {
    "width": bloco,
    "height": bloco,
    "x": 0,
    "y": 0,
    "collected": False,
}

vilao = {
    "width": bloco*1.5,
    "height": bloco*1.5,
    "x": 0,
    "y": 0,
    "img": "gyarados",
    "direcao": None,
    "velocidade_passo": bloco,
    "passos_restantes": 0,
    "minimo_de_passos": 3,
    "intervalo_passos_do_vilao": 500,
}

vilao_2 = {
    "width": bloco,
    "height": bloco,
    "x": 0,
    "y": 0,
    "img": "carvanha",
    "direcao": None,
    "velocidade_passo": 5,
    "minimo_de_passos": 15,
    "passos_restantes": 0,
    "intervalo_passos_do_vilao": 0,
}

vilao_3 = {
    "width": bloco,
    "height": bloco,
    "x": 0,
    "y": 0,
    "img": "carvanha",
    "direcao": None,
    "velocidade_passo": 5,
    "minimo_de_passos": 15,
    "passos_restantes": 0,
    "intervalo_passos_do_vilao": 0,
}

vilao_4 = {
    "width": bloco*1.5,
    "height": bloco*1.5,
    "x": 0,
    "y": 0,
    "img": "lapras",
    "direcao": None,
    "velocidade_passo": 10,
    "minimo_de_passos": 10,
    "passos_restantes": 0,
    "intervalo_passos_do_vilao": 0,
    "ativo": False 
}

sudo = {
    "width": bloco,
    "height": bloco,
    "x": int(width/2 - bloco/2),
    "y": int(height/2 - bloco/2),
}

pedras = []
agua = []

def define_tamanho_janela(filename):
    global qtd_caracteres, qtd_linhas, width, height
    global mapa
    file = open(filename, "r")
    qtd_caracteres = len(file.readline().strip())
    qtd_linhas = len(file.readlines()) + 1
    file.close()
    width = bloco * qtd_caracteres
    height = bloco * qtd_linhas

def load_mapa(filename):
    global mapa
    mapa = []
    file = open(filename, "r")
    i = 0
    for line in file.readlines():
        mapa.append([])
        for j in line:
            mapa[i].append(j)
        i = i + 1
    file.close()
    
def check_box_collision(x1, y1, w1, h1, x2, y2, w2, h2):
   return (x1 < x2 + w2) and (x2 < x1 + w1) and (y1 < y2 + h2) and (y2 < y1 + h1)

def pega_agua():
    global agua
    agua = []
    for i in range(qtd_linhas):
        for j in range(qtd_caracteres):
            if mapa[i][j] == "A":
                agua.append((j, i))

def spawna_pesca():
    global pesca
    tile_x, tile_y = random.choice(agua)
    
    pesca["x"] = tile_x * bloco
    pesca["y"] = tile_y * bloco
    pesca["collected"] = False

def spawna_vilao(vilao):
    if not agua:
        return
        
    tile_x, tile_y = random.choice(agua)
    vilao["x"] = tile_x * bloco + (bloco - vilao["width"]) // 2
    vilao["y"] = tile_y * bloco + (bloco - vilao["height"]) // 2
    vilao["direcao"] = random.randint(0, 3)
    vilao["passos_restantes"] = 2

def get_vilao_tile_pos(vilao):
    tile_x = int((vilao["x"] + vilao["width"] / 2) // bloco)
    tile_y = int((vilao["y"] + vilao["height"] / 2) // bloco)
    return tile_x, tile_y

def move_vilao(vilao):
    if vilao["passos_restantes"] <= 0:
        vilao["direcao"] = random.randint(0, 3)
        vilao["passos_restantes"] = random.randint(vilao["minimo_de_passos"], int(vilao["minimo_de_passos"] + vilao["minimo_de_passos"] * 1/2))

    old_x = vilao["x"]
    old_y = vilao["y"]
    
    if vilao["direcao"] == 0:
        vilao["y"] -= vilao["velocidade_passo"]
    elif vilao["direcao"] == 1:
        vilao["y"] += vilao["velocidade_passo"]
    elif vilao["direcao"] == 2:
        vilao["x"] -= vilao["velocidade_passo"]
    elif vilao["direcao"] == 3:
        vilao["x"] += vilao["velocidade_passo"]
        
    new_tile_x, new_tile_y = get_vilao_tile_pos(vilao)
    
    posicao_valida = False
    
    if 0 <= new_tile_y < len(mapa) and 0 <= new_tile_x < len(mapa[new_tile_y]):
        if mapa[new_tile_y][new_tile_x].strip() == "A":
            posicao_valida = True

    

    if posicao_valida:
        vilao["passos_restantes"] -= 1
    else:
        vilao["x"] = old_x
        vilao["y"] = old_y
        vilao["passos_restantes"] = 0

def update_vilao(dt, vilao, tempo_acumulado_vilao):
    if vilao.get("ativo") == False:
        return tempo_acumulado_vilao
    
    tempo_acumulado_vilao += dt
    if tempo_acumulado_vilao >= vilao["intervalo_passos_do_vilao"]:
        move_vilao(vilao)
        tempo_acumulado_vilao -= vilao["intervalo_passos_do_vilao"]
        
    if check_box_collision(player["x"], player["y"], player["width"], player["height"], vilao["x"], vilao["y"], vilao["width"], vilao["height"]):
        player["vida"] -= 1
        spawna_vilao(vilao)
    return tempo_acumulado_vilao

def update_pesca():
    if not pesca["collected"]:
        if check_box_collision(player["x"], player["y"], player["width"], player["height"], pesca["x"], pesca["y"], pesca["width"], pesca["height"]):
            pesca["collected"] = True
            spawna_pesca()
            player["pontuacao"] += 1

def carregar_imagens_pesca():
    global pesca_animacao
    pesca_animacao = []
    for i in range(1, 3):
        img = pygame.image.load(f"magi_{i}.png")
        img = pygame.transform.scale(img, (sudo["width"], sudo["height"]))
        pesca_animacao.append(img)

def carregar_imagens_player():
    global player_esquerdo_lado, player_direito_lado, player_costa, player_frente
    player_esquerdo_lado_1 = pygame.image.load("mario_lado_1.png")
    player_esquerdo_lado_1 = pygame.transform.scale(player_esquerdo_lado_1, (bloco, bloco))
    player_esquerdo_lado_2 = pygame.image.load("mario_lado_2.png")
    player_esquerdo_lado_2 = pygame.transform.scale(player_esquerdo_lado_2, (bloco, bloco))
    player_esquerdo_lado = [player_esquerdo_lado_1, player_esquerdo_lado_2]

    player_direito_lado_1 = pygame.transform.flip(player_esquerdo_lado_1, flip_x=True, flip_y=False)
    player_direito_lado_2 = pygame.transform.flip(player_esquerdo_lado_2, flip_x=True, flip_y=False) 
    player_direito_lado = [player_direito_lado_1, player_direito_lado_2]

    player_costa_1 = pygame.image.load("mario_costa_1.png")
    player_costa_1 = pygame.transform.scale(player_costa_1, (bloco, bloco))
    player_costa_2 = pygame.image.load("mario_costa_2.png")
    player_costa_2 = pygame.transform.scale(player_costa_2, (bloco, bloco))
    player_costa_3 = pygame.image.load("mario_costa_3.png")
    player_costa_3 = pygame.transform.scale(player_costa_3, (bloco, bloco))
    player_costa = [player_costa_1, player_costa_2, player_costa_3]

    player_frente_1 = pygame.image.load("mario_frente_1.png")
    player_frente_1 = pygame.transform.scale(player_frente_1, (bloco, bloco))
    player_frente_2 = pygame.image.load("mario_frente_2.png")
    player_frente_2 = pygame.transform.scale(player_frente_2, (bloco, bloco))
    player_frente = [player_frente_1, player_frente_2]

def carregar_imagens_sudo():
    global sudo_animacao_360
    sudo_animacao_360 = []
    for i in range(1, 7):
        img = pygame.image.load(f"sudo_{i}.png")
        img = pygame.transform.scale(img, (sudo["width"], sudo["height"]))
        sudo_animacao_360.append(img)
        
    frame_5_invertido = pygame.transform.flip(sudo_animacao_360[2], flip_x=True, flip_y=False) 
    frame_6_invertido = pygame.transform.flip(sudo_animacao_360[3], flip_x=True, flip_y=False)
    
    sudo_animacao_360.append(frame_5_invertido)
    sudo_animacao_360.append(frame_6_invertido)

def reset():
    global player, vilao
    global player_indice_frame, player_tempo_animacao
    global pesca_indice_frame, pesca_tempo_animacao
    global sudo_indice_frame, sudo_tempo_animacao

    player["vida"] = 3
    player["pontuacao"] = 0
    player["x"] = 50
    player["y"] = 50
    player["collided"] = False
    player["direcao"] = 1

    vilao["width"] = bloco*1.5
    vilao["height"] = bloco*1.5
    vilao["img"] = "gyarados"
    vilao["intervalo_passos_do_vilao"] = 500
    vilao["height"] = bloco*1.5

    vilao_2["width"] = bloco
    vilao_2["height"] = bloco
    vilao_2["img"] = "carvanha"
    vilao_2["intervalo_passos_do_vilao"] = 50
    vilao_2["velocidade_passo"] = 5
    vilao_2["minimo_de_passos"] = 15

    vilao_3["width"] = bloco
    vilao_3["height"] = bloco
    vilao_3["img"] = "carvanha"
    vilao_3["intervalo_passos_do_vilao"] = 50
    vilao_3["velocidade_passo"] = 5
    vilao_3["minimo_de_passos"] = 15

    vilao_4["ativo"] = False

    player_indice_frame = 0
    player_tempo_animacao = 0

    sudo_indice_frame = 0
    sudo_tempo_animacao = 0

    pesca_indice_frame = 0
    pesca_tempo_animacao = 0

def load():
    global clock
    global agua_img
    global tempo_acumulado_vilao, tempo_acumulado_vilao_2, tempo_acumulado_vilao_3, tempo_acumulado_vilao_4, vilao, vilao_2, vilao_3, vilao_4
    global play
    global sudo
    
    reset()

    agua_img = pygame.image.load("water.png")
    carregar_imagens_player()
    carregar_imagens_sudo()
    carregar_imagens_pesca()

    clock = pygame.time.Clock()
    define_tamanho_janela(filename)
    load_mapa(filename)
    sudo["x"] = int(width / 2 - sudo["width"] / 2)
    sudo["y"] = int(height / 2 - sudo["height"] / 2)
    pega_agua()
    spawna_pesca()
    spawna_vilao(vilao)
    spawna_vilao(vilao_2)
    spawna_vilao(vilao_3)
    tempo_acumulado_vilao = 0
    tempo_acumulado_vilao_2 = 0
    tempo_acumulado_vilao_3 = 0
    tempo_acumulado_vilao_4 = 0
    play = "jogando"

def mostra_vida(screen):
    global player
    coracao_img = pygame.image.load("heart.png")
    coracao_img = pygame.transform.scale(coracao_img, (30, 30))
    espacamento = 5
    largura_coracao = coracao_img.get_width()
    for i in range(player["vida"]):
        x_pos = (width - 10) - (largura_coracao * (i + 1)) - (espacamento * i)
        screen.blit(coracao_img, (x_pos, 10))

def mostra_pontos(screen):
    fonte_pontuacao = pygame.font.SysFont('Arial', 30)
    superficie_texto = fonte_pontuacao.render(f"Pontos: {player['pontuacao']}", True, (0, 0, 0))
    screen.blit(superficie_texto, (10, 10))

def desenha_avatar(screen):
    global player, player_tempo_animacao, fps, player_indice_frame, player_costa
    imgs = []

    if player["direcao"] == 0:
        imgs = player_costa
    elif player["direcao"] == 1:
        imgs = player_frente
    elif player["direcao"] == 2:
        imgs = player_direito_lado
    elif player["direcao"] == 3:
        imgs = player_esquerdo_lado

    if not imgs:
        return

    if player_indice_frame >= len(imgs):
        player_indice_frame = 0
    player_tempo_animacao += 1
    
    if player_tempo_animacao >= fps:
        player_tempo_animacao = 0
        player_indice_frame += 1
        if player_indice_frame >= len(imgs):
            player_indice_frame = 0

    screen.blit(imgs[player_indice_frame], (player["x"], player["y"]))

def desenha_pesca(screen):
    global pesca_animacao, pesca_indice_frame, pesca_tempo_animacao
    if not pesca["collected"]:
        imgs = pesca_animacao
    
        if not imgs:
            return

        if pesca_indice_frame >= len(imgs):
            pesca_indice_frame = 0
        pesca_tempo_animacao += 1
        
        if pesca_tempo_animacao >= fps+3:
            pesca_tempo_animacao = 0
            pesca_indice_frame += 1
            if pesca_indice_frame >= len(imgs):
                pesca_indice_frame = 0

        screen.blit(imgs[pesca_indice_frame], (pesca["x"], pesca["y"]))

def desenha_vilao(screen, vilao, tempo_animacao, indice_frame):
    global fps

    if vilao.get("ativo") == False:
        return tempo_animacao, indice_frame
    
    vilao_esquerdo_lado_1 = pygame.image.load(f"{vilao['img']}_lado_1.png")
    vilao_esquerdo_lado_1 = pygame.transform.scale(vilao_esquerdo_lado_1, (vilao["width"], vilao["height"]))
    vilao_esquerdo_lado_2 = pygame.image.load(f"{vilao['img']}_lado_2.png")
    vilao_esquerdo_lado_2 = pygame.transform.scale(vilao_esquerdo_lado_2, (vilao["width"], vilao["height"]))
    vilao_esquerdo_lado = [vilao_esquerdo_lado_1, vilao_esquerdo_lado_2]

    vilao_direito_lado_1 = pygame.transform.flip(vilao_esquerdo_lado_1, flip_x=True, flip_y=False)
    vilao_direito_lado_2 = pygame.transform.flip(vilao_esquerdo_lado_2, flip_x=True, flip_y=False) 
    vilao_direito_lado = [vilao_direito_lado_1, vilao_direito_lado_2]

    vilao_costa_1 = pygame.image.load(f"{vilao['img']}_costa_1.png")
    vilao_costa_1 = pygame.transform.scale(vilao_costa_1, (vilao["width"], vilao["height"]))
    vilao_costa_2 = pygame.image.load(f"{vilao['img']}_costa_2.png")
    vilao_costa_2 = pygame.transform.scale(vilao_costa_2, (vilao["width"], vilao["height"]))
    vilao_costa = [vilao_costa_1, vilao_costa_2]

    vilao_frente_1 = pygame.image.load(f"{vilao['img']}_frente_1.png")
    vilao_frente_1 = pygame.transform.scale(vilao_frente_1, (vilao["width"], vilao["height"]))
    vilao_frente_2 = pygame.image.load(f"{vilao['img']}_frente_2.png")
    vilao_frente_2 = pygame.transform.scale(vilao_frente_2, (vilao["width"], vilao["height"]))
    vilao_frente = [vilao_frente_1, vilao_frente_2]

    imgs = []

    if vilao["direcao"] == 0:
        imgs = vilao_costa
    elif vilao["direcao"] == 1:
        imgs = vilao_frente
    elif vilao["direcao"] == 2:
        imgs = vilao_esquerdo_lado
    elif vilao["direcao"] == 3:
        imgs = vilao_direito_lado

    if not imgs:
        return 

    if indice_frame >= len(imgs):
        indice_frame = 0

    tempo_animacao += 1
    
    if tempo_animacao >= fps:
        tempo_animacao = 0
        indice_frame += 1 
        
        if indice_frame >= len(imgs):
            indice_frame = 0

    screen.blit(imgs[indice_frame], (vilao["x"], vilao["y"]))
    return tempo_animacao, indice_frame

def desenha_agua(bloco_x, bloco_y):
    screen.blit(agua_img, (bloco_x, bloco_y))

def desenha_sudo(screen):
    global sudo, fps, sudo_indice_frame, sudo_tempo_animacao

    imgs = sudo_animacao_360
    
    if not imgs:
        return

    if sudo_indice_frame >= len(imgs):
        sudo_indice_frame = 0
    sudo_tempo_animacao += 1
    
    if sudo_tempo_animacao >= fps+3:
        sudo_tempo_animacao = 0
        sudo_indice_frame += 1
        if sudo_indice_frame >= len(imgs):
            sudo_indice_frame = 0

    screen.blit(imgs[sudo_indice_frame], (sudo["x"], sudo["y"]))

def update(dt):
    global player, pesca, play, vilao, tempo_acumulado_vilao, vilao_2, tempo_acumulado_vilao_2, vilao_3, tempo_acumulado_vilao_3, vilao_4, tempo_acumulado_vilao_4
    keys = pygame.key.get_pressed()

    colisao = False
    old_x = player["x"]
    old_y = player["y"]

    if keys[pygame.K_UP]:
        player["y"] -= player["velocidade"]
        player["direcao"] = 0
    if keys[pygame.K_DOWN]:
        player["y"] += player["velocidade"]
        player["direcao"] = 1
    if keys[pygame.K_LEFT]:
        player["x"] -= player["velocidade"]
        player["direcao"] = 2
    if keys[pygame.K_RIGHT]:
        player["x"] += player["velocidade"]
        player["direcao"] = 3

    max_x = width - player["width"]
    if player["x"] < 0:
        player["x"] = 0
    elif player["x"] > max_x:
        player["x"] = max_x

    max_y = height - player["height"]
    if player["y"] < 0:
        player["y"] = 0
    elif player["y"] > max_y:
        player["y"] = max_y
    
    for pedra in pedras:
        if check_box_collision(player["x"], player["y"], player["width"], player["height"], pedra["x"], pedra["y"], pedra["width"], pedra["height"]):
            player["x"] = old_x
            colisao = True
            break

    for pedra in pedras:
        if check_box_collision(player["x"], player["y"], player["width"], player["height"], pedra["x"], pedra["y"], pedra["width"], pedra["height"]):
            player["y"] = old_y
            colisao = True
            break

    player["collided"] = colisao
    
    update_pesca()

    if player["pontuacao"] >= pontos_para_vitoria * 60/100:
        if not vilao_4["ativo"]:
            vilao_4["ativo"] = True
            spawna_vilao(vilao_4)

        vilao["intervalo_passos_do_vilao"] = 150
        vilao["img"] = "shiny"
        vilao["width"] = bloco*2
        vilao["height"] = bloco*2
        vilao_2["intervalo_passos_do_vilao"] = 20
        vilao_2["img"] = "sharpedo"
        vilao_2["width"] = bloco*1.5
        vilao_2["height"] = bloco*1.5
        vilao_3["intervalo_passos_do_vilao"] = 20
        vilao_3["img"] = "sharpedo"
        vilao_3["width"] = bloco*1.5
        vilao_3["height"] = bloco*1.5

    tempo_acumulado_vilao = update_vilao(dt, vilao, tempo_acumulado_vilao)
    tempo_acumulado_vilao_2 = update_vilao(dt, vilao_2, tempo_acumulado_vilao_2)
    tempo_acumulado_vilao_3 = update_vilao(dt, vilao_3, tempo_acumulado_vilao_3)
    tempo_acumulado_vilao_4 = update_vilao(dt, vilao_4, tempo_acumulado_vilao_4)

    if player["vida"] <= 0:
        play = "gameover"
    elif player["pontuacao"] >= pontos_para_vitoria:
        play = "vitoria"
        
def draw_screen(screen):
    global pedras, vilao, vilao_tempo_animacao, vilao_indice_frame, vilao_2, vilao_tempo_animacao_2, vilao_indice_frame_2, vilao_indice_frame_3, vilao_tempo_animacao_3,vilao_indice_frame_4, vilao_tempo_animacao_4
    pedras = []
    pedras = []
    screen.fill((255,255,255))
    for i in range(qtd_linhas):
        for j in range(qtd_caracteres):
            color = (0,0,0)
            bloco_x = j * bloco
            bloco_y = i * bloco
            if mapa[i][j] == "P":
                color = (230,235,134)
                nova_pedra = {
                    "width": bloco,
                    "height": bloco,
                    "x": bloco_x,
                    "y": bloco_y
                }
                pedras.append(nova_pedra)
                pygame.draw.rect(screen, color, ((bloco_x), (bloco_y), bloco, bloco))
            elif mapa[i][j] == "G":
                color = (39,153,0)
                pygame.draw.rect(screen, color, ((bloco_x), (bloco_y), bloco, bloco))
            elif mapa[i][j] == "A":
                color = (63,125,232)
                pygame.draw.rect(screen, color, ((bloco_x), (bloco_y), bloco, bloco))

    desenha_pesca(screen)
    desenha_avatar(screen)
    vilao_tempo_animacao, vilao_indice_frame = desenha_vilao(screen, vilao, vilao_tempo_animacao, vilao_indice_frame)
    vilao_tempo_animacao_2, vilao_indice_frame_2 = desenha_vilao(screen, vilao_2, vilao_tempo_animacao_2, vilao_indice_frame_2)
    vilao_tempo_animacao_3, vilao_indice_frame_3 = desenha_vilao(screen, vilao_3, vilao_tempo_animacao_3, vilao_indice_frame_3)
    vilao_tempo_animacao_4, vilao_indice_frame_4 = desenha_vilao(screen, vilao_4, vilao_tempo_animacao_4, vilao_indice_frame_4)
    mostra_pontos(screen)
    mostra_vida(screen)
    desenha_sudo(screen)

def draw_win_screen(screen):
    pelicula = pygame.Surface((width, height), pygame.SRCALPHA)
    pelicula.fill((0, 0, 0, 180))
    screen.blit(pelicula, (0, 0))

    font_win = pygame.font.SysFont('Arial', 60, bold=True)
    text_win = font_win.render("VITÓRIA! Você é um Mestre Pescador!", True, (255, 255, 0))
    text_rect = text_win.get_rect(center=(width // 2, height // 2 - 50))
    screen.blit(text_win, text_rect)

    font_replay = pygame.font.SysFont('Arial', 30)
    text_replay = font_replay.render("Pressione ENTER para jogar novamente", True, (255, 255, 255))
    text_replay_rect = text_replay.get_rect(center=(width // 2, height // 2 + 50))
    screen.blit(text_replay, text_replay_rect)

def draw_game_over_screen(screen):
    pelicula = pygame.Surface((width, height), pygame.SRCALPHA)
    pelicula.fill((150, 0, 0, 180))
    screen.blit(pelicula, (0, 0))

    fonte = pygame.font.SysFont('Arial', 80, bold=True)
    texto = fonte.render("GAME OVER", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(width // 2, height // 2 - 50))
    screen.blit(texto, texto_rect)

    fonte_replay = pygame.font.SysFont('Arial', 30)
    text_replay = fonte_replay.render("Pressione ENTER para tentar novamente", True, (255, 255, 255))
    text_replay_rect = text_replay.get_rect(center=(width // 2, height // 2 + 50))
    screen.blit(text_replay, text_replay_rect)

def main_loop(screen):
    global clock
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                break
            if (play == "vitoria" or play == "gameover") and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    load()

        clock.tick(60)
        dt = clock.get_time()
        draw_screen(screen)
        if play == "jogando":
            update(dt)
        elif play == "vitoria":
            draw_win_screen(screen)
        elif play == "gameover":
            draw_game_over_screen(screen)
        pygame.display.update()

pygame.init()
pygame.mixer.init()
load()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Joguinho")
main_loop(screen)
pygame.quit()