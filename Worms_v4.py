'''golubenko98@gmail.com'''
from tkinter import Tk, Canvas
import random, math

# x и y - координаты центра круга
class Circle(object):
    def __init__(self,x,y,r,color):
        self.x=x
        self.y=y
        self.r=r # радиус
        self.color=color
        self.pict=canvas.create_oval([x-r,y+r], [x+r,y-r], fill=color, width=0)

    # Перемещает круг в точку (x;y)
    def Move(self,x,y):
        self.x=x
        self.y=y
        canvas.delete(self.pict)
        self.pict=canvas.create_oval([x-self.r,y+self.r], [x+self.r,y-self.r], fill=self.color, width=0)

    # Удаляет круг
    def __del__(self):
        canvas.delete(self.pict)

class Worm(object):
    delay=10 # Сколько времени проходит между двумя вызовами метода Step() (милисекунды)
    def __init__(self,x,y,v=5,length=7,r=10,colors=['green', 'yellow'], sex=True, strength=10):
        self.v=v
        self.angle=random.randint(1,360)
        self.length=length
        self.sex = sex
        self.strength = strength
        self.colors=colors # Цвета кружков, из которых состоит червяк
        self.fertile=50 if not sex else 1000 # Сколько раз червяк может ...
        self.old = 60000 - 55000 * len(Moving.worms) / 40
        self.fert_rec=self.old // 5 # Через сколько времени червяк сможет породить червяка (милисекунды)
        LenCol=len(colors)
        self.worm=[Circle(x,y,abs(strength/10),colors[i%LenCol]) for i in range(length)]

    def Step(self):
        if self.fert_rec > 0: # Восстановление после порождения нового червяка
            self.fert_rec-=Worm.delay
        if self.old <= 0:
            Moving.deleteWorm(self)
            return
        self.old-=Worm.delay
        width=canvas.winfo_width()
        height=canvas.winfo_height()
        self.angle+=random.randint(-45,45)
        vx = self.v * math.cos(math.radians(self.angle))
        vy = self.v * math.sin(math.radians(self.angle))
        if height-self.worm[0].r <= self.worm[0].y: # отскок от нижнего края
            self.angle=-90
        elif self.worm[0].r >= self.worm[0].y: # отскок от верхнего края
            self.angle=90
        if width-self.worm[0].r <= self.worm[0].x: # отскок от правого края
            self.angle=180
        elif self.worm[0].r >= self.worm[0].x: # отскок от левого края
            self.angle=0
        for i in range(self.length-1,0,-1):
            self.worm[i].Move(self.worm[i-1].x, self.worm[i-1].y)
        self.worm[0].Move(self.worm[0].x+vx, self.worm[0].y+vy)

    def whoWillBorn(s1, s2):
        return random.randint(0, s1) >= random.randint(0, s2)

    def meet(worm_1,worm_2):
        if worm_1.fertile and worm_1.fert_rec<=0 and worm_2.fertile and worm_2.fert_rec<=0:
            children=[Worm((worm_1.worm[0].x + worm_2.worm[0].x)//2, \
                (worm_1.worm[0].y + worm_2.worm[0].y)//2, v=(worm_1.v+worm_2.v)//2,\
                length=(worm_1.length+worm_2.length)//2,\
                r=(worm_1.worm[0].r+worm_2.worm[0].r)//2,\
                colors=worm_1.colors if Worm.whoWillBorn(worm_1.strength, worm_2.strength) else worm_2.colors,
                sex = random.random() < 0.5,\
                strength = random.randint(int((worm_1.strength + worm_2.strength)/2),\
                   int((worm_1.strength + worm_2.strength)/2 + 40)) \
                    if worm_1.colors != worm_2.colors else \
                    random.randint(int((worm_1.strength + worm_2.strength)/2) - 40,\
                   int((worm_1.strength + worm_2.strength)/2)))
                    for i in range(random.randint(1,7))]
            worm_1.fertile-=1
            worm_1.fert_rec=5000 if not worm_1.sex else 10
            worm_2.fertile-=1
            worm_2.fert_rec=5000 if not worm_2.sex else 10
            return children
        return False

    # Если головы двух червяков соприкасаются, и оба червяка готовы к порождению, то появляется новый червяк
    def Contact(worm_1,worm_2):
        if (worm_1.worm[0].x - worm_2.worm[0].x)**2 + (worm_1.worm[0].y - worm_2.worm[0].y)**2 <= (worm_1.worm[0].r + worm_2.worm[0].r)**2:
            if worm_1.sex == worm_2.sex and worm_1.colors != worm_2.colors:
                if worm_1.strength > worm_2.strength and worm_2.fert_rec <= 0:
                    Moving.deleteWorm(worm_2)
                elif worm_2.strength > worm_1.strength and worm_1.fert_rec <= 0:
                    Moving.deleteWorm(worm_1)
            elif worm_1.sex != worm_2.sex:
                return Worm.meet(worm_1,worm_2)

class Moving(object):
    avg = 0
    delay=15
    time=-delay
    worms=[]
    colors=['red','orange','yellow','green','light blue','blue','purple']
    @staticmethod
    def Run():
        Moving.time+=Moving.delay
        for e in Moving.worms:
            e.Step()
        ln = len(Moving.worms)
        if ln > 0:
            a = sum([e.strength for e in Moving.worms])/ln
            if a != Moving.avg:
                print(a, ln)
                Moving.avg = a
            Moving.WormsContact()
        root.after(Moving.delay, Moving.Run)

    @staticmethod
    def deleteWorm(worm):
        Moving.worms.pop(Moving.worms.index(worm))

    # Содаётся мир червяков
    @staticmethod
    def Start():
        Worm.delay=Moving.delay
        Moving.Run()

    # Левая кнопка мыши - появление нового червяка
    @staticmethod
    def Button_1(event):
        random.shuffle(Moving.colors)
        newWorm = Worm(event.x, event.y, v=random.randint(2,7), length=random.randint(1,30), r=random.randint(10,20), colors=Moving.colors[:], sex = random.random() < 0.5, strength = random.randint(20,300))
        Moving.worms.append(newWorm)

    # Заносит в список worms всех новых червяков
    @staticmethod
    def WormsContact():        
        ln_worms=len(Moving.worms)
        children = None
        for i in range(ln_worms):
            for j in range(ln_worms):
                if i != j:
                    try:
                        children=Worm.Contact(Moving.worms[i], Moving.worms[j])
                    except Exception:
                        pass
                    if children:
                        for child in children:
                            Moving.worms.append(child)

width = 1000
height = 1000
background = "white"
root = Tk()
canvas = Canvas(root, width=width, height=height, background=background)
canvas.pack()
root.bind('<Button-1>',Moving.Button_1)
Moving.Start()
root.mainloop()
