from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsScene, QMessageBox
from PyQt5.QtGui import QPen, QImage, QPixmap, QColor
from PyQt5.QtCore import Qt
from math import sin, cos, exp, sqrt, pi


M = 50
shx = 750 / 2
shy = 750 / 2

def rotateX(x, y, z, teta):
    teta = teta * pi / 180
    buf = y
    y = cos(teta) * y - sin(teta) * z
    z = cos(teta) * z + sin(teta) * buf
    return x, y, z


def rotateY(x, y, z, teta):
    teta = teta * pi / 180
    buf = x
    x = cos(teta) * x - sin(teta) * z
    z = cos(teta) * z + sin(teta) * buf
    return x, y, z


def rotateZ(x, y, z, teta):
    teta = teta * pi / 180
    buf = x
    x = cos(teta) * x - sin(teta) * y
    y = cos(teta) * y + sin(teta) * buf
    return x, y, z


def tranform(x, y, z, tetax, tetay, tetaz):
    x, y, z = rotateX(x, y, z, tetax)
    x, y, z = rotateY(x, y, z, tetay)
    x, y, z = rotateZ(x, y, z, tetaz)
    x = M * x + shx
    y = M * y + shy
    return round(x), round(y)


def isVisible(top, bottom, x, y):
    if y < top[x] and y > bottom[x]:
        return 0
    if y >= top[x]:
        return 1
    return -1


# поиск пересечения
def findIntersect(x_prev, y_prev, x_curr, y_curr, horizon):
    resX = x_prev
    resY = y_prev
    arr_y1 = horizon[x_prev]
    arr_y2 = horizon[x_curr]
    dx = x_curr - x_prev
    dy_cur = y_curr - y_prev
    dy_prev = arr_y2 - arr_y1
    if dx == 0:
        resX = x_curr
        resY = horizon[resX]
    elif y_prev == arr_y1 and y_curr == arr_y2:
        resX = x_prev
        resY = y_prev
    else:
        m = dy_cur / dx
        if dy_cur != dy_prev:
            resX = x_prev - round((y_prev - arr_y1) * dx / (dy_cur - dy_prev))
            resY = round((resX - x_prev) * m + y_prev)
    return resX, resY

# 0 - не видима, -1 - ниже, 1 - выше
def floatHorizon(scene_width, scene_height, x_min, x_max, x_step, z_min, z_max, z_step,
                 tx, ty, tz, func, scene, drawColor):
    arr = []
    x_left = -1
    y_left = -1
    x_right = -1
    y_right = -1

    flag_first_r = True
    flag_first_l = True

    top = {x: 0 for x in range(1, int(scene_width) + 1)}
    bottom = {x: scene_height for x in range(1, int(scene_width) + 1)}

    z = z_max
    while z >= z_min:
        x_prev = x_min
        y_prev = func(x_prev, z)
        x_prev, y_prev = tranform(x_prev, y_prev, z, tx, ty, tz) # поворот и умножение (растягиваем и масштабирует)

        # Обрабатываем левое ребро (заносим в массив в верх и нижн горизомпнт значение бокового ребра)
        if not flag_first_l:
            top, bottom = horizon(x_prev, y_prev, x_left, y_left, top, bottom, scene, drawColor, arr)
            flag_first_l = False
        x_left = x_prev
        y_left = y_prev

        prevVisible = isVisible(top, bottom, x_prev, y_prev) # смотрим видимость предыдущей точки

        x = x_min
        while x <= x_max:
            y = func(x, z)
            x_curr, y_curr = tranform(x, y, z, tx, ty, tz)

            curVisible = isVisible(top, bottom, x_curr, y_curr)

            if prevVisible == curVisible and (prevVisible == -1 or prevVisible == 1):  # Текущая и предыдущая точки невидимы и находятся обе либо выше верхнего, либо ниже нижнего
                top, bottom = horizon(x_prev, y_prev, x_curr, y_curr, top, bottom, scene, drawColor, arr)
            else: # найдем точку пересечения
                if curVisible == 0:  #  Текущая точка не видима
                    if prevVisible != 0:  #  Предыдущая точка видима
                        if prevVisible == 1:  #  Предыдущая точка выше вырхнего горизонта
                            xIntersect, yIntersect = findIntersect(x_prev, y_prev, x_curr, y_curr, top)  # Пересечение с верхним горизонтом
                        else:  #  Предыдущая точка ниже нижнего горизонта
                            xIntersect, yIntersect = findIntersect(x_prev, y_prev, x_curr, y_curr, bottom)  #  Пересечение с нижним норизонтом
                        top, bottom = horizon(x_prev, y_prev, xIntersect, yIntersect, top, bottom, scene, drawColor, arr)  # Рисуем от предыдущей до пересечения
                elif curVisible == 1:  #  Текущая точка выше верхнего горизонта
                    if prevVisible == 0:  #  Предыдущая точка не видима
                        xIntersect, yIntersect = findIntersect(x_prev, y_prev, x_curr, y_curr, top)  #  Пересечение с верхним горизонтом
                        top, bottom = horizon(xIntersect, yIntersect, x_curr, y_curr, top, bottom, scene, drawColor, arr)  # Рисуем от пересечения до текущей
                    else:  #  Предыдущая точка видима
                        xIntersect, yIntersect = findIntersect(x_prev, y_prev, x_curr, y_curr, bottom)  #  Пересечение с нижним горизонтом
                        top, bottom = horizon(x_prev, y_prev, xIntersect, yIntersect, top, bottom, scene, drawColor, arr)  #  Рисуем от предыдущей до пересечения
                        xIntersect, yIntersect = findIntersect(x_prev, y_prev, x_curr, y_curr, top)  # Пересечение с верхним горизонтом
                        top, bottom = horizon(xIntersect, yIntersect, x_curr, y_curr, top, bottom, scene, drawColor, arr)  # Рисуем от пересечения до текущей
                else:  #  Текущая точка ниже нижнего горизонта
                    if prevVisible == 0:  #  Предыдущая точка  невидима
                        xIntersect, yIntersect = findIntersect(x_prev, y_prev, x_curr, y_curr, bottom)  # Пересечения с нижним горизонтом
                        top, bottom = horizon(xIntersect, yIntersect, x_curr, y_curr, top, bottom, scene, drawColor, arr)  # Рисуем от пересечения до текущей
                    else:  #  Предыдущая точка видима
                        xIntersect, yIntersect = findIntersect(x_prev, y_prev, x_curr, y_curr, top)  # Пересечение с верхним горизонтом
                        top, bottom = horizon(x_prev, y_prev, xIntersect, yIntersect, top, bottom, scene, drawColor, arr)  # Рисуем от предыдущей до пересечения
                        xIntersect, yIntersect = findIntersect(x_prev, y_prev, x_curr, y_curr, bottom)  # Пересечение с нижним горизонтом
                        top, bottom = horizon(xIntersect, yIntersect, x_curr, y_curr, top, bottom, scene, drawColor, arr)  # Рисуем от пересечения до текущей
            prevVisible = curVisible
            x_prev = x_curr
            y_prev = y_curr
            x += x_step

        # Обрабатываем правое ребро
        if not flag_first_r:
            top, bottom = horizon(x_right, y_right, x_curr, y_curr, top, bottom, scene, drawColor, arr)
            flag_first_r = False
            x_right = x_curr
            y_right = y_curr

        z -= z_step

    return scene, arr


# заполняем массивы горизонта (интерполяция)
def horizon(x1, y1, x2, y2, top, bottom, scene, drawColor, arr):
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1

    arr.append([x1, y1, x2, y2])

    if dx == 0: # чтобы не делить на 0
        top[x1] = max(y1, top[x1]) # заполняем массив горизонтов
        bottom[x1] = min(y1, bottom[x1])
    else:
        x_prev = x1
        y_prev = y1
        m = dy / dx # вычисляем наклон линии
        x = x1
        while x <= x2:
            y = round(m * (x - x1) + y1) # находим y с помощью интерполяции
            top[x] = max(top[x], y) # изменяем горизонты в случае чего
            bottom[x] = min(bottom[x], y)
            x_curr = x
            y_curr = y
            x_prev = x_curr
            y_prev = y_curr
            x += 1
    return top, bottom
