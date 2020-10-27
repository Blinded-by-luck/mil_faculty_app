import pyglet
from pyglet.gl import *
import sys
sys.path.insert(0, '../Test app')

import Test



def load_cursor(filename):
    image = pyglet.image.load(filename)
    return pyglet.window.ImageMouseCursor(image)


key = pyglet.window.key
canvas_pyglet = []
window = pyglet.window.Window(630, 500, style='dialog')
times = pyglet.font.load('Times New Roman', 16)
animation = pyglet.image.load_animation('bubbles.gif')
animSprite = pyglet.sprite.Sprite(animation)

cursor =load_cursor("curs.png")
window.set_mouse_cursor(cursor=cursor)
r, g, b, alpha = 0.5, 0.5, 0.8, 0.5
pyglet.gl.glClearColor(r, g, b, alpha)


canvas_pyglet.append(pyglet.text.Label(f"Симулятор Проба",
                                font_name='Copperplate Cyrillic',
                                font_size=35,
                                x=window.width /2, y = window.height/2,
                                anchor_x='center', anchor_y='center'))
canvas_pyglet.append(pyglet.text.Label('нажмите Enter для запуска системы',
                                font_name='Copperplate Cyrillic',
                                font_size=20,
                                x=window.width//2, y=50,
                                anchor_x='center', anchor_y='center'))

@window.event
def on_draw():
    window.clear()
    animSprite.draw()
    canvas_pyglet[0].draw()
    canvas_pyglet[1].draw()

@window.event
def on_key_press(symbol, modifier):
    if symbol == key.ESCAPE:
        exit()
    if symbol == key.ENTER:
        window.close()
        Test.main()
        # здесь писать слк

if __name__ == '__main__':
    pyglet.app.run()