from tkinter import *
from tkinter import messagebox
import copy
from math import cos, sin, pi, sqrt


def draw_points(points):
    # обводка canvas
    Can.create_rectangle(3, 3, can_w, can_h - 2)

    for line in points[0]:
        Can.create_line(line)

    # эллипсы
    for oval in points[1]:
        Can.create_line(oval)


def get_default_points(ox, oy):
    points = [[], []]

    #
    points[0].append([[ox + 20, oy - 130], [ox - 20, oy - 130]])

    #
    points[0].append([[ox + 20, oy + 93], [ox + 20, oy + 160]])
    points[0].append([[ox - 20, oy + 93], [ox - 20, oy + 160]])

    points[0].append([[ox + 20, oy + 160], [ox + 40, oy + 160]])
    points[0].append([[ox - 20, oy + 160], [ox - 40, oy + 160]])

    #
    points[0].append([[ox + 50, oy], [ox + 110, oy - 80]])
    points[0].append([[ox + 50, oy - 30], [ox + 110, oy - 80]])

    points[0].append([[ox - 50, oy], [ox - 110, oy - 80]])
    points[0].append([[ox - 50, oy - 30], [ox - 110, oy - 80]])

    #
    points[0].append([[ox + 20, oy - 199.5], [ox + 30, oy - 250]])
    points[0].append([[ox - 20, oy - 199.5], [ox - 30, oy - 250]])
    points[0].append([[ox + 30, oy - 250], [ox + 50, oy - 250]])
    points[0].append([[ox - 30, oy - 250], [ox - 50, oy - 250]])

    #
    body = get_ellipse([ox, oy], 50, 100)
    for i in range(len(body)):
        points[1].append(body[i])

    #
    face = get_ellipse([ox, oy-150], 50, 50)
    for i in range(len(face)):
        points[1].append(face[i])

    #
    eye1 = get_ellipse([ox - 20, oy - 170], 8, 5)
    for i in range(len(eye1)):
        points[1].append(eye1[i])

    eye2 = get_ellipse([ox + 20, oy - 170], 8, 5)
    for i in range(len(eye2)):
        points[1].append(eye2[i])


    return points


def get_ellipse(centre, a, b):
    ellipse = []
    num = 200
    step = abs(a) * 2 / num

    for i in range(num):
        x = -a + step * i
        y = sqrt((1 - (x ** 2) / (a ** 2)) * b ** 2)
        x1 = -a + step * (i + 1)
        y1 = sqrt((1 - (x1 ** 2) / (a ** 2)) * b ** 2)
        ellipse.append([[x + centre[0], y + centre[1]], [x1 + centre[0], y1 + centre[1]]])
    for i in range(num):
        x = -a + step * i
        y = -sqrt((1 - (x ** 2) / (a ** 2)) * b ** 2)
        x1 = -a + step * (i + 1)
        y1 = -sqrt((1 - (x1 ** 2) / (a ** 2)) * b ** 2)
        ellipse.append([[x + centre[0], y + centre[1]], [x1 + centre[0], y1 + centre[1]]])

    return ellipse


def draw_axis():
    Can.create_line([OX, 0], [OX, can_h - 3])
    Can.create_line([0, OY], [can_w, OY])
    Can.create_polygon([OX, 3], [OX - 5, 13], [OX + 5, 13])
    Can.create_polygon([can_w, OY], [can_w - 10, OY - 5], [can_w - 10, OY + 5])
    Can.create_text(OX + 15, 10, text="Y", font=Font)
    Can.create_text(can_w - 10, OY - 15, text="X", font=Font)


def move(dx, dy):
    try:
        dx = float(dx.get())
        dy = float(dy.get())
    except ValueError:
        messagebox.showinfo("Внимание", "Неверные данные!")
        return -1

    ActionsStack.append(copy.deepcopy(ActionsStack[-1]))
    for form in ActionsStack[-1]:
        for figure in form:
            for coord in figure:
                coord[0] += dx
                coord[1] += -dy

    rebuild_scene()


def rebuild_scene():
    Can.delete("all")
    draw_points(ActionsStack[-1])
    draw_axis()


def reset():
    ActionsStack.append(get_default_points(OX, OY))
    rebuild_scene()


def cancel():
    if len(ActionsStack) > 1:
        ActionsStack.pop(-1)
        rebuild_scene()


def scale(kx, ky, xc, yc):
    try:
        kx = float(kx.get())
        ky = float(ky.get())
        xc = float(xc.get())
        yc = -float(yc.get())
    except ValueError:
        messagebox.showinfo("Внимание", "Неверные данные!")
        return -1

    ActionsStack.append(copy.deepcopy(ActionsStack[-1]))
    for form in ActionsStack[-1]:
        for figure in form:
            for coord in figure:
                coord[0] = (coord[0] - xc - OX) * kx + xc + OX
                coord[1] = (coord[1] - yc - OY) * ky + yc + OY

    rebuild_scene()


def turn(xc, yc, angle):
    try:
        xc = float(xc.get())
        yc = -float(yc.get())
        angle = float(angle.get())
    except ValueError:
        messagebox.showinfo("Внимание", "Неверные данные!")
        return -1

    ActionsStack.append(copy.deepcopy(ActionsStack[-1]))
    for form in ActionsStack[-1]:
        for figure in form:
            for coord in figure:
                coord[0] -= OX
                coord[1] -= OY
                new_x = xc + (coord[0] - xc) * d_cos(angle) + (coord[1] - yc) * d_sin(angle)
                new_y = yc - (coord[0] - xc) * d_sin(angle) + (coord[1] - yc) * d_cos(angle)
                coord[0] = new_x
                coord[1] = new_y
                coord[0] += OX
                coord[1] += OY

    rebuild_scene()


def d_cos(a):
    return cos(a * pi / 180)


def d_sin(a):
    return sin(a * pi / 180)


# Tkinter
def move_UI():
    move_UI = Toplevel(root)
    move_UI.title('Перенос')
    move_UI.geometry('270x120')
    move_UI.resizable(False, False)
    move_UI.grab_set()
    move_UI.focus_set()

    MoveDxVar = StringVar()
    MoveDyVar = StringVar()

    MoveName = Label(move_UI, text="Перенос:", font=Font).grid(row=0, column=0, columnspan=4)
    MoveDx = Label(move_UI, text="dx:", font=Font).grid(row=1, column=0)
    MoveDy = Label(move_UI, text="dy:", font=Font).grid(row=1, column=2)

    MoveDxEntry = Entry(move_UI, width=EntryW, textvariable=MoveDxVar).grid(row=1, column=1)
    MoveDyEntry = Entry(move_UI, width=EntryW, textvariable=MoveDyVar).grid(row=1, column=3)

    MoveButton = Button(move_UI, text="Выполнить", font=Font, command=lambda: move(MoveDxVar, MoveDyVar)).grid(row=2,
                                                                                                               column=1,
                                                                                                               columnspan=2)
    move_UI.bind('<Return>', lambda event: move(MoveDxVar, MoveDyVar))


def scale_UI():
    scale_UI = Toplevel(root)
    scale_UI.title('Масштабирование')
    scale_UI.geometry('250x160')
    scale_UI.resizable(False, False)
    scale_UI.grab_set()
    scale_UI.focus_set()
    ScaleKxVar = StringVar()
    ScaleKyVar = StringVar()
    ScaleXcVar = StringVar()
    ScaleYcVar = StringVar()

    ScaleName = Label(scale_UI, text="Масштабирование:", font=Font).grid(row=0, column=0, columnspan=4)
    ScaleKx = Label(scale_UI, text="Kx:", font=Font).grid(row=1, column=0)
    ScaleKy = Label(scale_UI, text="Ky:", font=Font).grid(row=1, column=2)
    ScaleXc = Label(scale_UI, text="Xc:", font=Font).grid(row=2, column=0)
    ScaleYc = Label(scale_UI, text="Yc:", font=Font).grid(row=2, column=2)

    ScaleKxEntry = Entry(scale_UI, width=EntryW, textvariable=ScaleKxVar).grid(row=1, column=1)
    ScaleKyEntry = Entry(scale_UI, width=EntryW, textvariable=ScaleKyVar).grid(row=1, column=3)
    ScaleXcEntry = Entry(scale_UI, width=EntryW, textvariable=ScaleXcVar).grid(row=2, column=1)
    ScaleYcEntry = Entry(scale_UI, width=EntryW, textvariable=ScaleYcVar).grid(row=2, column=3)

    ScaleButton = Button(scale_UI, text="Выполнить",
                         command=lambda: scale(ScaleKxVar, ScaleKyVar, ScaleXcVar, ScaleYcVar), font=Font).grid(row=3,
                                                                                                                column=1,
                                                                                                                columnspan=2)
    scale_UI.bind('<Return>', lambda event: scale(ScaleKxVar, ScaleKyVar, ScaleXcVar, ScaleYcVar))


def turn_UI():
    turn_UI = Toplevel(root)
    turn_UI.title('Поворот')
    turn_UI.geometry('350x160')
    turn_UI.resizable(False, False)
    turn_UI.grab_set()
    turn_UI.focus_set()

    TurnXcVar = StringVar()
    TurnYcVar = StringVar()
    TurnAngleVar = StringVar()

    TurnName = Label(turn_UI, text="Поворот:", font=Font).grid(row=0, column=0, columnspan=4)
    TurnXc = Label(turn_UI, text="Xc:", font=Font).grid(row=1, column=0)
    TurnYc = Label(turn_UI, text="Yc:", font=Font).grid(row=1, column=2)
    TurnAngle = Label(turn_UI, text="Угол:\n(в градусах)", font=Font).grid(row=2, column=0)

    TurnXcEntry = Entry(turn_UI, width=EntryW, textvariable=TurnXcVar).grid(row=1, column=1)
    TurnYcEntry = Entry(turn_UI, width=EntryW, textvariable=TurnYcVar).grid(row=1, column=3)
    TurnAngleEntry = Entry(turn_UI, width=EntryW, textvariable=TurnAngleVar).grid(row=2, column=1)

    TurnButton = Button(turn_UI, text="Выполнить", command=lambda: turn(TurnXcVar, TurnYcVar, TurnAngleVar),
                        font=Font).grid(row=3, column=1, columnspan=2)
    turn_UI.bind('<Return>', lambda event: turn(TurnXcVar, TurnYcVar, TurnAngleVar))


# Main window
root = Tk()
root.resizable(False, False)
can_h = 600
can_w = 800
but_h = 70

root.geometry(str(1100) + "x" + str(700))
root.title("Лабораторная работа № 2")
Font = "Arial 16"
EntryW = 10
Can = Canvas(root, height=can_h, width=can_w, bg='white')
Can.place(x=0, y=but_h)

OX = can_w / 2
OY = can_h / 2
ActionsStack = []

move_button = Button(root, text="Перенос", command=lambda: move_UI(), font=Font).place(x=910, y=140)
scale_button = Button(root, text="Масштабирование", command=lambda: scale_UI(), font=Font).place(x=865, y=210)
scale_button = Button(root, text="Поворот", command=lambda: turn_UI(), font=Font).place(x=910, y=280)

SettingsResetButton = Button(root, text="Восстановить", command=lambda: reset(), font=Font).place(x=890, y=420)
SettingsCancelButton = Button(root, text="Отменить", command=lambda: cancel(), font=Font).place(x=910, y=350)

# Main programm
Points = get_default_points(OX, OY)
draw_axis()
draw_points(Points)
ActionsStack.append(Points)

root.mainloop()
