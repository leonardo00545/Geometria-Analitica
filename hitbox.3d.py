from ursina import *
import random

# ============================================================
# INICIAR JOGO
# ============================================================

app = Ursina()

window.title = 'Simulador de Hitbox 3D'
window.borderless = False
window.fullscreen = False

# ============================================================
# CHÃO
# ============================================================

ground = Entity(
    model='plane',
    scale=(50,1,50),
    texture='white_cube',
    texture_scale=(50,50),
    color=color.gray,
    collider='box'
)

# ============================================================
# PLAYER
# ============================================================

player = Entity(
    model='quad',
    texture='mario.png',
    scale=(2,3),
    position=(0,1.5,0)
)

player.collider = BoxCollider(
    player,
    center=(0,-0.2,0),
    size=(1.2,2.4,0.2)
)

# ============================================================
# HITBOX PLAYER
# ============================================================

player_hitbox = Entity(
    parent=player,
    model='cube',
    scale=(1.2,2.4,0.2),
    color=color.rgba(0,255,0,60),
    wireframe=True
)

# ============================================================
# CÂMERA
# ============================================================

camera.position = (0,12,-15)
camera.rotation_x = 35

# ============================================================
# OBSTÁCULOS
# ============================================================

obstaculos = []

for i in range(8):

    obj = Entity(

        model='cube',

        color=color.azure,

        scale=(
            random.uniform(1,2),
            random.uniform(1,3),
            random.uniform(1,2)
        ),

        position=(
            random.uniform(-10,10),
            1,
            random.uniform(-10,10)
        ),

        collider='box'
    )

    hitbox = Entity(

        parent=obj,

        model='cube',

        scale=(1.05,1.05,1.05),

        color=color.rgba(0,255,0,60),

        wireframe=True
    )

    obj.hitbox_visual = hitbox

    obj.velocidade = Vec3(0,0,0)

    obj.altura_original = obj.y

    obstaculos.append(obj)

# ============================================================
# CONFIGURAÇÕES
# ============================================================

velocidade = 5

gravidade = 20

forca_pulo = 8

velocidade_y = 0

no_chao = False

# Liga e desliga a física

fisica_objetos = True

# ============================================================
# UPDATE
# ============================================================

def update():

    global velocidade_y
    global no_chao

    # ----------------------------
    # MOVIMENTO
    # ----------------------------

    if held_keys['w']:
        player.z += velocidade * time.dt

    if held_keys['s']:
        player.z -= velocidade * time.dt

    if held_keys['a']:
        player.x -= velocidade * time.dt

    if held_keys['d']:
        player.x += velocidade * time.dt

    # ----------------------------
    # GRAVIDADE
    # ----------------------------

    velocidade_y -= gravidade * time.dt

    player.y += velocidade_y * time.dt

    # ----------------------------
    # CHÃO
    # ----------------------------

    if player.y <= 1.5:

        player.y = 1.5

        velocidade_y = 0

        no_chao = True

    else:

        no_chao = False

    # ----------------------------
    # FÍSICA DOS OBJETOS
    # ----------------------------

    for obj in obstaculos:

        obj.position += obj.velocidade * time.dt

        obj.y = obj.altura_original

        obj.velocidade.y = 0

        obj.velocidade *= 0.90

    # ----------------------------
    # COLISÕES
    # ----------------------------

    colidindo = False

    for obj in obstaculos:

        resultado = player.intersects(
            obj,
            ignore=[player_hitbox]
        )

        if resultado.hit:

            colidindo = True

            obj.hitbox_visual.color = color.red

            # EMPURRÃO

            direcao = Vec3(

                obj.x - player.x,

                0,

                obj.z - player.z

            )

            if fisica_objetos:

                if direcao.length() > 0:

                    direcao = direcao.normalized()

                    obj.velocidade += direcao * 8

        else:

            obj.hitbox_visual.color = color.rgba(
                0,255,0,60
            )


    # ----------------------------
    # HITBOX PLAYER
    # ----------------------------

    if colidindo:

        player_hitbox.color = color.rgba(
            255,0,0,120
        )

    else:

        player_hitbox.color = color.rgba(
            0,255,0,60
        )

# ============================================================
# INPUT
# ============================================================

def input(key):

    global velocidade_y
    global fisica_objetos

    # PULO

    if key == 'space':

        if no_chao:

            velocidade_y = forca_pulo

    # LIGAR / DESLIGAR FÍSICA

    if key == 'f':

        fisica_objetos = not fisica_objetos

        if fisica_objetos:

            botao_fisica.text = "Fisica ON"

            botao_fisica.color = color.green

        else:

            botao_fisica.text = "Fisica OFF"

            botao_fisica.color = color.red

# ============================================================
# LUZ
# ============================================================

DirectionalLight()

AmbientLight(
    color=color.rgba(
        180,
        180,
        180,
        255
    )
)

# ============================================================
# BOTÃO DA FÍSICA
# ============================================================

botao_fisica = Button(

    text='Fisica ON',

    color=color.green,

    scale=(0.22,0.08),

    position=(0.72,0.42)
)

def alternar_fisica():

    global fisica_objetos

    fisica_objetos = not fisica_objetos

    if fisica_objetos:

        botao_fisica.text = "Fisica ON"

        botao_fisica.color = color.green

    else:

        botao_fisica.text = "Fisica OFF"

        botao_fisica.color = color.red

botao_fisica.on_click = alternar_fisica

# ============================================================
# TEXTO
# ============================================================

Text(

    text=
"""
W A S D -> mover

SPACE -> pular

F -> ligar/desligar física

Botão verde = física ligada

Botão vermelho = física desligada

VERDE = sem colisão

VERMELHO = colisão

Objetos podem ser empurrados
""",

    position=(-0.85,0.45),

    scale=1.1
)

# ============================================================
# EXECUTAR
# ============================================================

app.run()