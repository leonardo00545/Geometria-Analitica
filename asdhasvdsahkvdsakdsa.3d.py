


# INSTALAÇÃO:
# pip install ursina

from ursina import *
import random


# INICIAR JOGO

app = Ursina()

window.title = 'Simulador de Hitbox 3D'
window.borderless = False
window.fullscreen = False


# CHÃO


ground = Entity(
    model='plane',
    scale=(50,1,50),
    texture='white_cube',
    texture_scale=(50,50),
    color=color.gray,
    collider='box'
)


# PLAYER


player = Entity(

    model='quad',

    texture='player.png',

    scale=(2,3),

    position=(0,1.5,0),

    collider='box'
)


# HITBOX VISUAL PLAYER


player_hitbox = Entity(

    parent=player,

    model='cube',

    scale=(1.2,1.1,0.3),

    color=color.rgba(0,255,0,60),

    wireframe=True
)


# CÂMERA


camera.position = (0,12,-15)
camera.rotation_x = 35


# OBSTÁCULOS


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

    obstaculos.append(obj)

# VELOCIDADE


velocidade = 5


# UPDATE


def update():

    # Movimento

    if held_keys['w']:
        player.z += velocidade * time.dt

    if held_keys['s']:
        player.z -= velocidade * time.dt

    if held_keys['a']:
        player.x -= velocidade * time.dt

    if held_keys['d']:
        player.x += velocidade * time.dt

    # Sempre olhar para câmera

    player.rotation_y = camera.rotation_y

    colidindo = False

    for obj in obstaculos:

        resultado = player.intersects(obj)

        if resultado.hit:

            colidindo = True

            obj.hitbox_visual.color = color.rgba(
                255,0,0,120
            )

        else:

            obj.hitbox_visual.color = color.rgba(
                0,255,0,60
            )

    if colidindo:

        player_hitbox.color = color.rgba(
            255,0,0,120
        )

    else:

        player_hitbox.color = color.rgba(
            0,255,0,60
        )

# ============================================================
# LUZ
# ============================================================

DirectionalLight()

AmbientLight(
    color=color.rgba(180,180,180,255)
)


# TEXTO


Text(

    text=
"""
W A S D -> mover

VERDE = sem colisão
VERMELHO = colisão
"""
,

    position=(-0.85,0.45),

    scale=1.1
)

# ============================================================
# EXECUTAR
# ============================================================

app.run()