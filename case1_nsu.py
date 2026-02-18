import turtle
turtle.setup(width = 1400, height = 800)
turtle.tracer(0)

def shestiugolnik(x, y, a, color):
    turtle.up()
    turtle.setposition(x, y)
    turtle.setheading(0)
    turtle.down()
    turtle.fillcolor(color)
    turtle.begin_fill()
    
    for i in range(6):
        turtle.forward(a)
        turtle.left(60)
        
    turtle.end_fill()

def shestiugolnikW():
    shestiugolnik(-100, 200, 50, "yellow")

def trapezia(x, y, angle, top, bottom, side, color):
    turtle.up()
    turtle.setposition(x, y)
    turtle.setheading(0)
    turtle.down()
    turtle.fillcolor(color)
    turtle.begin_fill()
    
    turtle.forward(bottom)
    turtle.left(angle)
    turtle.forward(side)
    turtle.left(180-angle)
    turtle.forward(top)
    turtle.left(180-angle)
    turtle.forward(side)
    turtle.left(angle)
    
    turtle.end_fill()

def trapeziaW():
    trapezia(0, 200, 120, 60, 120, 60, "red")

def triangle(x, y, a1, s1, s2, color):
    turtle.up()
    turtle.setposition(x, y)
    turtle.setheading(0)
    turtle.down()
    turtle.fillcolor(color)
    turtle.begin_fill()
    
    turtle.forward(s1)
    turtle.left(180-a1)
    turtle.forward(s2)
    turtle.goto(x, y)
    
    turtle.end_fill()

def pryamougolnyitriangleW():
    triangle(120, 200, 60, 90, 90, "orange")

def square(x, y, a, color):
    turtle.up()
    turtle.setposition(x, y)
    turtle.setheading(0)
    turtle.down()
    turtle.fillcolor(color)
    turtle.begin_fill()
    
    turtle.forward(a)
    turtle.left(90)
    turtle.forward(a)
    turtle.left(90)
    turtle.forward(a)
    turtle.left(90)
    turtle.forward(a)
    
    turtle.end_fill()

def square1():
    square(210, 200, 80, "black")

def rectangle(x, y, a, b, color):
    turtle.up()
    turtle.setposition(x, y)
    turtle.setheading(0)
    turtle.down()
    turtle.fillcolor(color)
    turtle.begin_fill()
    
    turtle.forward(a)
    turtle.left(90)
    turtle.forward(b)
    turtle.left(90)
    turtle.forward(a)
    turtle.left(90)
    turtle.forward(b)
    turtle.left(90)
    
    turtle.end_fill()

def rectangle1():
    rectangle(290, 200, 80, 40, "purple")

def parallelogram(x, y, a, b, angel, color):
    turtle.up()
    turtle.setposition(x, y)
    turtle.setheading(0)
    turtle.down()
    turtle.fillcolor(color)
    turtle.begin_fill()
    
    turtle.forward(a)
    turtle.left(angel)
    turtle.forward(b)
    turtle.left(180-angel)
    turtle.forward(a)
    turtle.left(angel)
    turtle.forward(b)
    turtle.left(180-angel)
    
    turtle.end_fill()

def parallelogram1():
    parallelogram(410, 200, 90, 45, 150, "brown")

def romb(x, y, a, angle, color):
    turtle.up()
    turtle.setposition(x, y)
    turtle.setheading(90-angle/2)
    turtle.down()
    turtle.fillcolor(color)
    turtle.begin_fill()
    
    for i in range(2):
        turtle.forward(a)
        turtle.left(angle)
        turtle.forward(a)
        turtle.left(180-angle)
        
    turtle.end_fill()

def romb1():
    romb(0, 200, 80, 60, "dark cyan")

def pentagon(x, y, a, color):
    turtle.up()
    turtle.setposition(x, y)
    turtle.setheading(0)
    turtle.down()
    turtle.fillcolor(color)
    turtle.begin_fill()
    
    for i in range(5):
        turtle.forward(a)
        turtle.left(72)
        
    turtle.end_fill()

def pentagon1():
    pentagon(-200, 200, 60, "light coral")

#код к композициям
def Malevich_square():
    square(-650, -100, 100, "black")

def ring():
    pentagon(-495, -15, 40, "purple")
    shestiugolnik(-500, -100, 50, "yellow")
    square(-500, -80, 50, "white")

def house():
    rectangle(-400, -100, 120, 100, "coral")
    trapezia(-400, 0, 120, 60, 120, 60, "orange")
    square(-380, -50, 30, "blue")
    rectangle(-320, -100, 30, 70, "black")

def ship():
    trapezia(-230, -100, 60, 140, 120, 20, "yellow")
    rectangle(-175, -82, 15, 100, "blue")
    triangle(-160, -14, 45, 32, 45, "black")

def air_plane():
    parallelogram(-50, -100, 150, 45, 150, "brown")
    parallelogram(-20, -77, 35, 80, 140, "brown")
    parallelogram(-80, -150, 35, 80, 40, "brown")
    square(-50, -90, 7, 'aquamarine')
    square(-37, -90, 7, 'aquamarine')
    square(-24, -90, 7, 'aquamarine')
    square(-11, -90, 7, 'aquamarine')
    square(2, -90, 7, 'aquamarine')
    square(15, -90, 7, 'aquamarine')
    square(28, -90, 7, 'aquamarine')
    square(41, -90, 7, 'aquamarine')


def tree():
    rectangle(195, -100, 30, 60, "sienna")
    triangle(160, -90, 60, 100, 100, "green")
    triangle(170, -50, 60, 80, 80, "green")
    triangle(180, -20, 60, 60, 60, "green")

def car():
    rectangle(350, -100, 160, 50, "red")
    trapezia(380, -50, 120, 80, 120, 50, "dark red")
    romb(380, -130, 30, 60, "black")
    romb(470, -130, 30, 60, "black")

#композиции
Malevich_square()
ring()
house()
ship()
air_plane()
tree()
car()

# все фигуры 
pentagon1()
shestiugolnikW()
romb1()
trapeziaW()
pryamougolnyitriangleW()
square1()
rectangle1()
parallelogram1()

turtle.hideturtle()
turtle.update()
turtle.done()


