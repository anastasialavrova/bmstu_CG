from tkinter import *
from tkinter import messagebox as mb
import math


arr = [[0 for j in range(2)] for i in range(20)]

def but_func():
    global n, arr
    if ((not point_str.get().count(' ') == 1) or (point_str.get() \
                                                          .split()[0].replace('-', '', 1).replace('.', '',
                                                                                                  1).isdigit() == False) \
            or (point_str.get().split()[0].find('-') > 0) or (point_str.get() \
                                                                      .split()[1].replace('-', '', 1).replace('.', '',
                                                                                                              1).isdigit() == False) \
            or (point_str.get().split()[1].find('-') > 0)):
        mb.showerror("Ошибка", "Неккоректный ввод.")
    else:
        l.insert(END, "№" + str(n+1) + ":  " + point_str.get())
        entry.delete(0, END)
        arr[n][0] = l.get(n).split()[1]
        arr[n][1] = l.get(n).split()[2]
        n += 1


def but_func_2():
    global n
    l.delete(0, END)
    n = 0


x_max = 940
x_min = 0
y_max = 730
y_min = 0
x1_m = 0
x2_m = 0
x3_m = 0
y1_m = 0
y2_m = 0
y3_m = 0
xo_m = 0
yo_m = 0
xb_1 = 0
xb_2 = 0
xb_3 = 0
yb_1 = 0
yb_2 = 0
yb_3 = 0


def but_func_3():
    global x_max, x_min, y_max, y_min, x1_m, x2_m, x3_m, y1_m, y2_m, y3_m, xo_m, yo_m
    global xb_1, xb_2, xb_3, yb_1, yb_2, yb_3
    a_m = 0
    b_m = 0
    c_m = 0
    min_sum = 0
    flag = 0
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):

                # координаты точек треугольника
                x1 = float(l.get(i).split()[1])
                y1 = float(l.get(i).split()[2])
                x2 = float(l.get(j).split()[1])
                y2 = float(l.get(j).split()[2])
                x3 = float(l.get(k).split()[1])
                y3 = float(l.get(k).split()[2])

                print(x1, ";", y1, " ", x2, ";", y2, " ", x3, ";", y3, "\n")

                # длины сторон треугольника
                a = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                b = math.sqrt((x2 - x3)**2 + (y2 - y3)**2)
                c = math.sqrt((x3 - x1)**2 + (y3 - y1)**2)

                eps = 0.0000001

                print(a, " ", b, " ", c, "\n")

                if((math.fabs(a+b - c) > eps) and (math.fabs(c+b - a) > eps) and (math.fabs(a+c - b) > eps)):

                    print("!", n, "\n")

                    # точка пересечения биссектрис
                    x_o = (a*x3 + b*x1 + c*x2)/(a+b+c)
                    y_o = (a*y3 + b*y1 + c*y2)/(a+b+c)

                    if (flag == 0):
                        min_sum = x_o + y_o
                        x1_m = x1
                        x2_m = x2
                        x3_m = x3
                        y1_m = y1
                        y2_m = y2
                        y3_m = y3
                        xo_m = x_o
                        yo_m = y_o
                        a_m = a
                        b_m = b
                        c_m = c
                        flag = 1
                    else:
                        if (min_sum > (x_o + y_o)):
                            min_sum = x_o + y_o
                            x1_m = x1
                            x2_m = x2
                            x3_m = x3
                            y1_m = y1
                            y2_m = y2
                            y3_m = y3
                            xo_m = x_o
                            yo_m = y_o
                            a_m = a
                            b_m = b
                            c_m = c

                print("------------------\n")

    eps = 0.0000001

    if (n <= 2):
        mb.showerror("Ошибка", "Недостаточное количество точек")
    else:
        if ((math.fabs(a_m + b_m - c_m) > eps) and (math.fabs(c_m + b_m - a_m) > eps) and (math.fabs(a_m + c_m - b_m) > eps)):
            lm1 = (a_m/b_m)
            xb_1 = (x1_m + lm1*x3_m) / (1 + lm1)
            yb_1 = (y1_m + lm1 * y3_m) / (1 + lm1)

            lm2 = (c_m/a_m)
            xb_2 = (x3_m + lm2*x2_m) / (1 + lm2)
            yb_2 = (y3_m + lm2 * y2_m) / (1 + lm2)

            lm3 = (b_m/c_m)
            xb_3 = (x2_m + lm3 * x1_m)/ (1 + lm3)
            yb_3 = (y2_m + lm3 * y1_m) / (1 + lm3)
            draw(x1_m, x2_m, x3_m, y1_m, y2_m, y3_m, xb_1, xb_2, xb_3, yb_1, yb_2, yb_3, xo_m, yo_m)
        else:
            mb.showerror("Ошибка", "Треугольник вырожден")


def draw(x1_m, x2_m, x3_m, y1_m, y2_m, y3_m, xb_1, xb_2, xb_3, yb_1, yb_2, yb_3, x_om, y_om):

    coord_x = [x1_m, x2_m, x3_m, xb_1, xb_2, xb_3, xo_m]
    coord_y = [y1_m, y2_m, y3_m, yb_1, yb_2, yb_3, yo_m]
    coord_x2 = [x1_m, x2_m, x3_m, xb_1, xb_2, xb_3, xo_m]
    coord_y2 = [y1_m, y2_m, y3_m, yb_1, yb_2, yb_3, yo_m]

    for i in range (len(coord_x2)):
        coord_x2[i] = float('{:.2f}'.format(coord_x2[i]))
        coord_y2[i] = float('{:.2f}'.format(coord_y2[i]))


    margin = 100
    panel_s = 700
    scale = (700 - margin*2)/max(max(coord_x)-min(coord_x), max(coord_y) - min(coord_y))

    mn_x = min(coord_x)
    mx_y = max(coord_y)
    for i in range (len(coord_x)):
        coord_x[i] = (coord_x[i] - mn_x) * scale + margin

    for i in range (len(coord_y)):
        coord_y[i] = (mx_y - coord_y[i]) * scale + margin

    w.delete("all")

    w.create_text(coord_x[0]+5, coord_y[0]+5, text=str("("+ str(coord_x2[0])+", "+str(coord_y2[0]) +")"),
                      anchor="n", justify=LEFT, fill='dark blue')
    w.create_text(coord_x[1] + 5, coord_y[1] + 5, text=str("(" + str(coord_x2[1]) + ", " + str(coord_y2[1]) + ")"),
                  anchor="n", justify=LEFT, fill='dark blue')
    w.create_text(coord_x[2] + 5, coord_y[2] + 5, text=str("(" + str(coord_x2[2]) + ", " + str(coord_y2[2]) + ")"),
                  anchor="n", justify=LEFT, fill='dark blue')
    w.create_text(coord_x[6] + 5, coord_y[6] + 5, text=str("(" + str(coord_x2[6]) + ", " + str(coord_y2[6]) + ")"),
                  anchor="n", justify=LEFT, fill='dark blue')

    w.create_line(coord_x[0], coord_y[0], coord_x[1], coord_y[1])
    w.create_line(coord_x[1], coord_y[1], coord_x[2], coord_y[2])
    w.create_line(coord_x[0], coord_y[0], coord_x[2], coord_y[2])

    w.create_line(coord_x[0], coord_y[0], coord_x[4], coord_y[4])
    w.create_line(coord_x[1], coord_y[1], coord_x[3], coord_y[3])
    w.create_line(coord_x[2], coord_y[2], coord_x[5], coord_y[5])


def but_clear():
    w.delete("all")


def delete_by_index():
    global n
    print(n, "\n")
    n -= 1;
    print(n, "\n")
    selection = l.curselection()
    l.delete(selection[0])


def change_by_index():
    global n
    if ((not xy_str.get().count(' ') == 1) or (xy_str.get() \
                                                          .split()[0].replace('-', '', 1).replace('.', '',
                                                                                                  1).isdigit() == False) \
            or (xy_str.get().split()[0].find('-') > 0) or (xy_str.get() \
                                                                      .split()[1].replace('-', '', 1).replace('.', '',
                                                                                                              1).isdigit() == False) \
            or (xy_str.get().split()[1].find('-') > 0) or (ind_str.get().isdigit() == False)):
        mb.showerror("Ошибка", "Неккоректный ввод.")
    else:
        n_str = ind_str.get()
        n_i = int(n_str)
        print(n_i, " ", n, "\n")
        if (n_i > n):
            mb.showerror("Ошибка", "Неккоректный ввод (индекс)")
        else:
            l.delete(n_i-1)
            l.insert(n_i-1, "№" + n_str + ":  " + xy_str.get())
            entry2.delete(0, END)
            entry3.delete(0, END)



n = 0
root = Tk()
root.geometry('1130x720')
point_str = StringVar()
points_str = StringVar()
rad_str = StringVar()
label1 = Label(text="Введите координаты точки:")
label1.place(x=750, y=40)
entry = Entry(textvariable=point_str, width=25)
entry.place(x=750, y=70)
but = Button(text="Добавить точку", command=but_func)
but.place(x=750, y=100)
l = Listbox(height=20, width=25)
l.place(x=750, y=150)
but = Button(text="Удалить все точки", command=but_func_2)
but.place(x=750, y=490)

but2 = Button(text="Удалить выбранную точку", command=delete_by_index)
but2.place(x=750, y=520)

but = Button(text="Решить", width=15, command=but_func_3)
but.place(x=750, y=600)
w = Canvas(root, width=700, height=700, bg='white')
w.place(x=10, y=10)
#but = Button(text="Очистить поле", command=but_clear)
#but.place(x=450, y=760)

ind_str = StringVar()
xy_str = StringVar()

label2 = Label(text="Введите индекс точки:")
label2.place(x=950, y=70)
entry2 = Entry(textvariable=ind_str, width=25)
entry2.place(x=950, y=90)

label3 = Label(text="Введите координаты:")
label3.place(x=950, y=110)
entry3 = Entry(textvariable=xy_str, width=25)
entry3.place(x=950, y=130)

but3 = Button(text="Изменить точку", command=change_by_index)
but3.place(x=950, y=170)

m = Menu(root)
root.config(menu=m)
root.mainloop()