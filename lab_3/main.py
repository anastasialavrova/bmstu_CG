from tkinter import *
from tkinter import messagebox
from math import fabs, ceil, radians, cos, sin, floor
import matplotlib.pyplot as plt
import time

# Знак числа
def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0


# ЦДА
def cda_test(ps, pf):
    dx = abs(pf[0] - ps[0])
    dy = abs(pf[1] - ps[1])
    if dx > dy:
        L = dx
    else:
        L = dy
    sx = (pf[0] - ps[0]) / L
    sy = (pf[1] - ps[1]) / L
    x = ps[0]
    y = ps[1]
    while abs(x - pf[0]) > 1 or abs(y - pf[1]) > 1:
        x += sx
        y += sy


def draw_line_cda(ps, pf, fill):
    dx = abs(pf[0] - ps[0])
    dy = abs(pf[1] - ps[1])
    if dx:
        tg = dy / dx
    else:
        tg = 0
    if dx > dy:
        steep = dx
    else:
        steep = dy
    sx = (pf[0] - ps[0]) / steep # step of x
    sy = (pf[1] - ps[1]) / steep # step of y
    x = ps[0]
    y = ps[1]
    stairs = []
    st = 1
    while abs(x - pf[0]) > 1 or abs(y - pf[1]) > 1:
        canvas.create_line(x, y, x + 1, y + 1, fill=fill)
        if (abs(int(x) - int(x + sx)) >= 1 and tg > 1) or (abs(int(y) - int(y + sy)) >= 1 >= tg):
            stairs.append(st)
            st = 0
        else:
            st += 1
        x += sx
        y += sy
    if st:
        stairs.append(st)
    return stairs


# БР вещественный для теста
def float_test(ps, pf):
    dx = pf[0] - ps[0]
    dy = pf[1] - ps[1]
    sx = sign(dx)
    sy = sign(dy)
    dy = abs(dy)
    dx = abs(dx)
    if dy >= dx:
        dx, dy = dy, dx
        pr = 1
    else:
        pr = 0
    m = dy / dx
    e = m - 1 / 2
    x = ps[0]
    y = ps[1]
    while x != pf[0] or y != pf[1]:
        if e >= 0:
            if pr == 1:
                x += sx
            else:
                y += sy
            e -= 1
        if e <= 0:
            if pr == 0:
                x += sx
            else:
                y += sy
        e += m

# Брезенхема с действительными коэффами
def draw_line_brez_float(ps, pf, fill):
    dx = pf[0] - ps[0]
    dy = pf[1] - ps[1]
    sx = sign(dx)
    sy = sign(dy)
    dy = abs(dy)
    dx = abs(dx)
    if dy >= dx:
        dx, dy = dy, dx
        steep = 1
    else:
        steep = 0
    tg = dy / dx # tангенс угла наклона
    e = tg - 1 / 2 # начальное значение ошибки
    x = ps[0] # начальный икс
    y = ps[1] # начальный игрек
    stairs = []
    st = 1
    while x != pf[0] or y != pf[1]:
        canvas.create_line(x, y, x + 1, y + 1, fill=fill)
        # выбираем пиксель
        if e >= 0:
            if steep == 1: # dy >= dx
                x += sx
            else: # dy < dx
                y += sy
            e -= 1 # отличие от целого
            stairs.append(st)
            st = 0
        if e <= 0:
            if steep == 0: # dy < dx
                x += sx
            else: # dy >= dx
                y += sy
            st += 1
            e += tg # отличие от целого

    if st:
        stairs.append(st)
    return stairs


# БР целый
def int_test(ps, pf):
    dx = pf[0] - ps[0]
    dy = pf[1] - ps[1]
    sx = sign(dx)
    sy = sign(dy)
    dy = abs(dy)
    dx = abs(dx)
    if dy >= dx:
        dx, dy = dy, dx
        pr = 1
    else:
        pr = 0
    m = 2 * dy
    e = m - dx
    ed = 2 * dx
    x = ps[0]
    y = ps[1]
    while x != pf[0] or y != pf[1]:
        if e >= 0:
            if pr == 1:
                x += sx
            else:
                y += sy
            e -= ed
        if e <= 0:
            if pr == 0:
                x += sx
            else:
                y += sy
        e += m


# Брезенхема с целыми коэффами
def draw_line_brez_int(ps, pf, fill):
    dx = pf[0] - ps[0]
    dy = pf[1] - ps[1]
    sx = sign(dx)
    sy = sign(dy)
    dy = abs(dy)
    dx = abs(dx)
    if dy >= dx:
        dx, dy = dy, dx
        steep = 1
    else:
        steep = 0
    e = 2 * dy - dx # отличие от вещественного (e = tg - 1 / 2) tg = dy / dx
    x = ps[0]
    y = ps[1]
    stairs = []
    st = 1
    while x != pf[0] or y != pf[1]:
        canvas.create_line(x, y, x + 1, y + 1, fill=fill)
        if e >= 0:
            if steep == 1:
                x += sx
            else:
                y += sy
            stairs.append(st)
            st = 0
            e -= 2 * dx # отличие от вещественного (e -= 1)
        if e <= 0:
            if steep == 0:
                x += sx
            else:
                y += sy
            st += 1
            e += 2 * dy # difference (e += tg)

    if st:
        stairs.append(st)
    return stairs


# Брезенхема со сглаживанием
def smoth_test(ps, pf):
    L = 100
    dx = pf[0] - ps[0]
    dy = pf[1] - ps[1]
    sx = sign(dx)
    sy = sign(dy)
    dy = abs(dy)
    dx = abs(dx)
    if dy >= dx:
        dx, dy = dy, dx
        pr = 1
    else:
        pr = 0
    m = dy / dx * L
    e = L / 2
    w = L - m
    x = ps[0]
    y = ps[1]
    while x != pf[0] or y != pf[1]:
        if e < w:
            if pr == 0:
                x += sx
            else:
                y += sy
            e += m
        elif e >= w:
            x += sx
            y += sy
            e -= w

def draw_line_brez_smoth(ps, pf, fill):
    I = 100
    fill = get_rgb_intensity(fill, I)
    dx = pf[0] - ps[0]
    dy = pf[1] - ps[1]
    sx = sign(dx)
    sy = sign(dy)
    dy = abs(dy)
    dx = abs(dx)
    if dy >= dx:
        dx, dy = dy, dx
        steep = 1 #
    else:
        steep = 0 #
    tg = dy / dx * I # тангенс угла наклона (умножаем на инт., чтобы не приходилось умножать внутри цикла
    e = I / 2 # интенсивность для высвечивания начального пикселя
    w = I - tg # пороговое значение
    x = ps[0]
    y = ps[1]
    stairs = []
    st = 1
    while x != pf[0] or y != pf[1]:
        canvas.create_line(x, y, x + 1, y + 1, fill=fill[round(e) - 1])
        if e < w:
            if steep == 0: # dy < dx
                x += sx # -1 if dx < 0, 0 if dx = 0, 1 if dx > 0
            else: # dy >= dx
                y += sy # -1 if dy < 0, 0 if dy = 0, 1 if dy > 0
            st += 1 # stepping
            e += tg
        elif e >= w:
            x += sx
            y += sy
            e -= w
            stairs.append(st)
            st = 0
    if st:
        stairs.append(st)
    return stairs

def vu_test(ps, pf):
    x1 = ps[0]
    x2 = pf[0]
    y1 = ps[1]
    y2 = pf[1]
    I = 100
    stairs = []
    #fills = get_rgb_intensity("black", I)
    if x1 == x2 and y1 == y2:
        flag = 1

    steep = abs(y2 - y1) > abs(x2 - x1)

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        tg = 1
    else:
        tg = dy / dx

    # first endpoint
    xend = round(x1)
    yend = y1 + tg * (xend - x1)
    xpx1 = xend
    ypx1 = int(yend)
    y = yend + tg

    # second endpoint
    xend = int(x2 + 0.5)
    yend = y2 + tg * (xend - x2)
    xpx2 = xend

    # main loop
    if steep:
        for x in range(xpx1, xpx2):

            y += tg
    else:
        for x in range(xpx1, xpx2):
            y += tg

def draw_line_vu(ps, pf, fill):
    x1 = ps[0]
    x2 = pf[0]
    y1 = ps[1]
    y2 = pf[1]
    I = 100
    stairs = []
    fills = get_rgb_intensity(fill, I)
    if x1 == x2 and y1 == y2:
        canvas.create_line(x1, y1, x1 + 1, y1 + 1, fill = fills[100])

    steep = abs(y2 - y1) > abs(x2 - x1)

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        tg = 1
    else:
        tg = dy / dx

    # first endpoint
    xend = round(x1)
    yend = y1 + tg * (xend - x1)
    xpx1 = xend
    y = yend + tg

    # second endpoint
    xend = int(x2 + 0.5)
    xpx2 = xend
    st = 0

    # main loop
    if steep:
        for x in range(xpx1, xpx2):
            canvas.create_line(int(y), x + 1, int(y) + 1, x + 2,
                               fill = fills[int((I - 1) * (abs(1 - y + int(y))))])
            canvas.create_line(int(y) + 1, x + 1, int(y) + 2, x + 2,
                               fill = fills[int((I - 1) * (abs(y - int(y))))])

            if (abs(int(x) - int(x + 1)) >= 1 and tg > 1) or \
                    (not 1 > abs(int(y) - int(y + tg)) >= tg):
                stairs.append(st)
                st = 0
            else:
                st += 1
            y += tg
    else:
        for x in range(xpx1, xpx2):
            #print((I - 1)*round(abs(1 - y + floor(y))))
            canvas.create_line(x + 1, int(y), x + 2, int(y) + 1,
                               fill = fills[round((I - 1) * (abs(1 - y + floor(y))))])
            #print((I - 1)*round(abs(y - floor(y))))
            canvas.create_line(x + 1, int(y) + 1, x + 2, int(y) + 2,
                               fill = fills[round((I - 1) * (abs(y - floor(y))))])

            if (abs(int(x) - int(x + 1)) >= 1 and tg > 1) or \
                    (not 1 > abs(int(y) - int(y + tg)) >= tg):
                stairs.append(st)
                st = 0
            else:
                st += 1
            y += tg
    return stairs


# Массив цветов одного оттенка разной интенсивности
def get_rgb_intensity(color, intensity):
    grad = []
    (r1, g1, b1) = canvas.winfo_rgb(color) # разложение цвета линни на составляющие ргб
    (r2, g2, b2) = canvas.winfo_rgb(bg_color) # разложение цвета фона на составляющие ргб
    r_ratio = float(r2 - r1) / intensity # получение шага интенсивности
    g_ratio = float(g2 - g1) / intensity
    b_ratio = float(b2 - b1) / intensity
    for i in range(intensity):
        nr = int(r1 + (r_ratio * i)) # заполнение массива разными оттенками
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        grad.append("#%4.4x%4.4x%4.4x" % (nr, ng, nb))
    grad.reverse()
    return grad


# Получение параметров для отрисовки
def draw(test_mode):
    choise = method_list.curselection()
    if len(choise) == 1:
        xs, ys = fxs.get(), fys.get()
        xf, yf = fxf.get(), fyf.get()
        if not xs and not ys:
            messagebox.showwarning('Ошибка ввода',
                                   'Не заданы координаты начала отрезка!')
        elif not xs or not ys:
            messagebox.showwarning('Ошибка ввода',
                                   'Не задана одна из координат начала отрезка!')
        elif not xf and not yf:
            messagebox.showwarning('Ошибка ввода',
                                   'Не заданы координаты конца отрезка!')
        elif not xf or not yf:
            messagebox.showwarning('Ошибка ввода',
                                   'Не задана одна из координат конца отрезка!')
        else:
            #try:
                xs, ys = round(float(xs)), round(float(ys))
                xf, yf = round(float(xf)), round(float(yf))
                if xs != xf or ys != yf:
                    if not test_mode:
                        funcs[choise[0]]([xs, ys], [xf, yf], fill=line_color)
                    else:
                        angle = fangle.get()
                        if angle:
                            try:
                                angle = int(angle)
                                if angle:
                                    test(1, choise[0], funcs[choise[0]], angle, [xs, ys], [xf, yf])
                                else:
                                    messagebox.showwarning('Ошибка ввода',
                                                           'Задано нулевое значение для угла поворота!')
                            except:
                                messagebox.showwarning('Ошибка ввода',
                                                      'Введено нечисловое значение для шага анализа!')
                        else:
                            messagebox.showwarning('Ошибка ввода',
                                                   'Не задано значение для шага анализа!')
                else:
                    messagebox.showwarning('Ошибка ввода',
                                           'Начало и конец отрезка совпадают!')
            #except:
                #messagebox.showwarning('Ошибка ввода',
                #                       'Нечисловое значение для параметров отрезка!')
    elif not len(choise):
        messagebox.showwarning('Ошибка ввода',
                               'Не выбран метод построения отрезка!')
    else:
        messagebox.showwarning('Ошибка ввода',
                               'Выбрано более одного метода простроения отрезка!')


# Получение параметров для анализа
def analyze(mode):
    #try:
        #length = len_line.get()
        length = 100
        if length:
            length = int(length)
        else:
            length = 100
        if not mode:
            time_bar(length)
        else:
            ind = method_list.curselection()
            if ind:
                if ind[-1] != 5:
                    smoth_analyze(ind, length)
                else:
                    messagebox.showwarning('Предупреждение',
                                           'Стандартный метод не может '
                                           'быть проанализирован на ступенчатость!')
            else:
                messagebox.showwarning('Предупреждение',
                                       'Не выбрано ни одного'
                                       'метода построения отрезка!')
    #except:
     #   messagebox.showwarning('Предупреждение',
    #                           'Введено нечисловое значение для длины отрезка!')


# замер времени
def test(flag, ind, method, angle, pb, pe):
    global line_color
    total = 0
    steps = int(360 // angle)
    for i in range(steps):
        cur1 = time.time()
        if flag == 0:
            method(pb, pe)
        else:
            method(pb, pe, fill=line_color)
        cur2 = time.time()
        turn_point(radians(angle), pe, pb)
        total += cur2 - cur1
    return total / steps


# гистограмма времени
def time_bar(length):
    close_plt()
    plt.figure(2, figsize=(9, 7))
    times = []
    angle = 1
    pb = [center[0], center[1]]
    pe = [center[0] + 100, center[1]]
    for i in range(5):
        times.append(test(0, i, test_funcs[i], angle, pb, pe))
    clean()
    Y = range(len(times))
    L = ('Digital\ndifferential\nanalyzer', 'Bresenham\n(real coeffs)',
         'Bresenham\n(int coeffs)', 'Bresenham\n(smooth)', 'Wu')
    plt.bar(Y, times, align='center')
    plt.xticks(Y, L)
    plt.ylabel("Work time in sec. (line len. " + str(length) + ")")
    plt.show()

# Поворот точки для сравнения ступенчатости
def turn_point(angle, p, center):
    x = p[0]
    p[0] = round(center[0] + (x - center[0]) * cos(angle) + (p[1] - center[1]) * sin(angle))
    p[1] = round(center[1] - (x - center[0]) * sin(angle) + (p[1] - center[1]) * cos(angle))

# Анализ ступечатости
def smoth_analyze(methods, length):
    close_plt()
    names = ('Digital\ndifferential\nanalyzer', 'Bresenham\n(real coeffs)',
             'Bresenham\n(int coeffs)', 'Bresenham\n(smooth)', 'Wu')
    plt.figure(1)
    plt.title("Stepping analysis")
    plt.xlabel("Angle")
    plt.ylabel("Number of steps(line length " + str(length) + ")")
    plt.grid(True)
    plt.legend(loc='best')

    for i in methods:
        max_len = []
        nums = []
        angles = []
        angle = 0
        step = 2
        pb = [center[0], center[1]]
        pe = [center[0] + length, center[1]]

        for j in range(90 // step):
            stairs = funcs[i](pb, pe, line_color)
            turn_point(radians(step), pe, pb)
            if stairs:
                max_len.append(max(stairs))
            else:
                max_len.append(0)
            nums.append(len(stairs))
            angles.append(angle)
            angle += step
        clean()
        plt.figure(1)
        plt.plot(angles, nums, label=names[i])
        plt.legend()
    plt.show()

# Оси координат
def draw_axes():
    color = 'gray'
    canvas.create_line(0, 2, 750, 2, fill="gray", arrow=LAST)
    canvas.create_line(2, 0, 2, 400, fill="gray", arrow=LAST)
    for i in range(50, 750, 50):
        canvas.create_text(i, 10, text=str(abs(i)), fill=color)
        canvas.create_line(i, 0, i, 5, fill=color)

    for i in range(25, 400, 25):
        canvas.create_text(15, i, text=str(abs(i)), fill=color)
        canvas.create_line(0, i, 5, i, fill=color)

# очистка канваса
def clean():
    canvas.delete("all")
    draw_axes()


# Список методов прорисовки отрезка
def fill_list(lst):
    lst.insert(END, "ЦД")
    lst.insert(END, "Брезенхем (float)")
    lst.insert(END, "Брезенхем (int)")
    lst.insert(END, "Брезенхем с устранением ступенчатости")
    lst.insert(END, "Ву")
    lst.insert(END, "Стандартный")


def set_bgcolor(color):
    global bg_color
    bg_color = color
    canvas.configure(bg=bg_color)


def set_linecolor(color):
    global line_color
    line_color = color
    lb_lcolor.configure(bg=line_color)

def close_plt():
    plt.figure(1)
    plt.close()
    plt.figure(2)
    plt.close()


root = Tk()
root.geometry('950x550')
root.resizable(0, 0)
root.title('Лабораторная работа №3')
color_menu = "#f0f0f0"

coords_frame = Frame(root, bg=color_menu, height=200, width=160)
coords_frame.place(x=770, y=0)

comparison_frame = Frame(root, bg=color_menu, height=180, width=160)
comparison_frame.place(x=770, y=200)

angle_frame = Frame(root, bg=color_menu, height=120, width=160)
angle_frame.place(x=770, y=380)

menu_frame = Frame(root, bg=color_menu, height=150, width=160)
menu_frame.place(x=0, y=400)

color_frame = Frame(root, bg=color_menu, height=150, width=160)
color_frame.place(x=160, y=400)

canv = Canvas(root, width=750, height=400, bg='white')
canvas = canv
canvas_test = canv
canv.place(x=0, y=0)
center = (375, 200)

# Список Алгоритмов
method_list = Listbox(coords_frame, selectmode=EXTENDED)
method_list.place(x=10, y=10, width=130, height=70)
fill_list(method_list)
funcs = (draw_line_cda, draw_line_brez_float, draw_line_brez_int,
         draw_line_brez_smoth, draw_line_vu, canvas.create_line)
test_funcs = (cda_test, float_test, int_test, smoth_test, vu_test)

lb1 = Label(coords_frame, bg=color_menu, text='Начало линии:')
lb2 = Label(coords_frame, bg=color_menu, text='Конец линии:')
lb1.place(x=3, y=85)
lb2.place(x=3, y=125)

lbx1 = Label(coords_frame, bg=color_menu, text='X:')
lby1 = Label(coords_frame, bg=color_menu, text='Y:')
lbx2 = Label(coords_frame, bg=color_menu, text='X:')
lby2 = Label(coords_frame, bg=color_menu, text='Y:')
lbx1.place(x=90, y=85)
lby1.place(x=90, y=105)
lbx2.place(x=90, y=125)
lby2.place(x=90, y=145)

fxs = Entry(coords_frame, bg="white")
fys = Entry(coords_frame, bg="white")
fxf = Entry(coords_frame, bg="white")
fyf = Entry(coords_frame, bg="white")
fxs.place(x=105, y=85, width=35)
fys.place(x=105, y=105, width=35)
fxf.place(x=105, y=125, width=35)
fyf.place(x=105, y=145, width=35)

btn_draw = Button(coords_frame, text=u"Построить", command=lambda: draw(0), width=140, height=25)
btn_draw.place(x=40, y=175, width=70, height=20)

lb_angle = Label(angle_frame, bg=color_menu, text="Угол поворота\n(в градусах):")
lb_angle.place(x=2, y=2)

fangle = Entry(angle_frame, bg="white")
fangle.place(x=30, y=40, width=25)

btn_viz = Button(angle_frame, text=u"Визуальный анализ", command=lambda: draw(1))
btn_viz.place(x=25, y=65, width=120, height=25)

#lb_len = Label(comparison_frame, bg=color_menu, text="Длина линии\n(по умолчанию 100):")
#lb_len.place(x=2, y=2)
#len_line = Entry(comparison_frame, bg="white")
#len_line.place(x=40, y=40, width=40)
btn_time = Button(comparison_frame, text=u"Сравнение времени\nпостроения", command=lambda: analyze(0))
btn_time.place(x=3, y=50, width=140, height=40)
btn_smoth = Button(comparison_frame, text=u"Сравнение\nступенчатости", command=lambda: analyze(1))
btn_smoth.place(x=3, y=110, width=140, height=40)

btn_clean = Button(menu_frame, text=u"Очистить экран", command=clean)
btn_clean.place(x=30, y=50, width=95)

# выбор цветов

line_color = 'black'
bg_color = 'white'

size = 15
white_line = Button(color_frame, bg="white", activebackground="white",
                    command=lambda: set_linecolor('white'))
white_line.place(x=15, y=30, height=size, width=size)
black_line = Button(color_frame, bg="yellow", activebackground="black",
                    command=lambda: set_linecolor("yellow"))
black_line.place(x=30, y=30, height=size, width=size)
red_line = Button(color_frame, bg="orange", activebackground="orange",
                  command=lambda: set_linecolor("orange"))
red_line.place(x=45, y=30, height=size, width=size)
orange_line = Button(color_frame, bg="red", activebackground="red",
                     command=lambda: set_linecolor("red"))
orange_line.place(x=60, y=30, height=size, width=size)
yellow_line = Button(color_frame, bg="purple", activebackground="purple",
                     command=lambda: set_linecolor("purple"))
yellow_line.place(x=75, y=30, height=size, width=size)
green_line = Button(color_frame, bg="darkblue", activebackground="darkblue",
                    command=lambda: set_linecolor("darkblue"))
green_line.place(x=90, y=30, height=size, width=size)
doger_line = Button(color_frame, bg="darkgreen", activebackground="darkgreen",
                    command=lambda: set_linecolor("darkgreen"))
doger_line.place(x=105, y=30, height=size, width=size)
blue_line = Button(color_frame, bg="black", activebackground="black",
                   command=lambda: set_linecolor("black"))
blue_line.place(x=120, y=30, height=size, width=size)

white_bg = Button(color_frame, bg="white", activebackground="white",
                  command=lambda: set_bgcolor("white"))
white_bg.place(x=15, y=110, height=size, width=size)
black_bg = Button(color_frame, bg="yellow", activebackground="yellow",
                  command=lambda: set_bgcolor("yellow"))
black_bg.place(x=30, y=110, height=size, width=size)
red_bg = Button(color_frame, bg="orange", activebackground="orange",
                command=lambda: set_bgcolor("orange"))
red_bg.place(x=45, y=110, height=size, width=size)
orange_bg = Button(color_frame, bg="red", activebackground="red",
                   command=lambda: set_bgcolor("red"))
orange_bg.place(x=60, y=110, height=size, width=size)
yellow_bg = Button(color_frame, bg="purple", activebackground="purple",
                   command=lambda: set_bgcolor("purple"))
yellow_bg.place(x=75, y=110, height=size, width=size)
green_bg = Button(color_frame, bg="darkblue", activebackground="darkblue",
                  command=lambda: set_bgcolor("darkblue"))
green_bg.place(x=90, y=110, height=size, width=size)
dodger_bg = Button(color_frame, bg="darkgreen", activebackground="darkgreen",
                   command=lambda: set_bgcolor("darkgreen"))
dodger_bg.place(x=105, y=110, height=size, width=size)
blue_bg = Button(color_frame, bg="black", activebackground="black",
                 command=lambda: set_bgcolor("black"))
blue_bg.place(x=120, y=110, height=size, width=size)

lb_line = Label(color_frame, bg=color_menu, text='Цвет линии (текущий:       ): ')
lb_line.place(x=2, y=5)
lb_lcolor = Label(color_frame, bg=line_color)
lb_lcolor.place(x=135, y=9, width=12, height=12)
lb_bg = Label(color_frame, bg=color_menu, text='Цвет фона: ')
lb_bg.place(x=2, y=80)

draw_axes()
root.mainloop()
