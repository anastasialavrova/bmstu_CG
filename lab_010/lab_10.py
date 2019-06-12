from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsScene, QMessageBox
from PyQt5.QtGui import QPen, QImage, QPixmap, QColor
from PyQt5.QtCore import Qt
from math import sin, cos, exp, sqrt, pi
from algo import floatHorizon

M = 50
shx = 750 / 2
shy = 750 / 2
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("mainwindow.ui", self)

        self.backgroundColor = QColor(Qt.white)
        self.drawColor = QColor(Qt.white)

        self.scene = QGraphicsScene(0, 0, 745, 745)
        self.scene.setBackgroundBrush(self.backgroundColor)
        self.mainview.setScene(self.scene)


        self.draw_all_btn.clicked.connect(lambda: draw(self))
        self.rotate_btn.clicked.connect(lambda: rotate(self))
        self.clear_all_btn.clicked.connect(lambda: clearAll(self))

        self.funcs.addItem("sin(x) * cos(z)")
        self.funcs.addItem("|sin(x) * sin(z)|")
        self.funcs.addItem("(x ^ 2 / 5 - z ^ 2 / 6) / 2")
        self.funcs.addItem("exp(sin(sqrt(x**2 + z**2)))")

        self.thetaOX = 0
        self.thetaOY = 0
        self.thetaOZ = 0


def clearAll(win):
    win.thetaOX = 0
    win.thetaOY = 0
    win.thetaOZ = 0
    win.scene.clear()


def isInt(num):
    try:
        val = int(num)
        return 1
    except:
        return 0


def isFloat(num):
    try:
        val = float(num)
        return 1
    except:
        return 0


def sign(x):
    if not x:
        return 0
    else:
        return int(x / abs(x))


def f1(x, z):
    return sin(x) * cos(z)


def f2(x, z):
    return abs(sin(x) * cos(z))


def f3(x, z):
    return ((x**2) / 5 - (z**2) / 6) / 2


def f4(x, z):
    return exp(sin(sqrt(x**2 + z**2)))


def rotate(win):
    tmpOX = win.delta_theta_OX_text.text()
    tmpOY = win.delta_theta_OY_text.text()
    tmpOZ = win.delta_theta_OZ_text.text()
    if tmpOX != '' and isInt(tmpOX):
        win.thetaOX += int(tmpOX)
    if tmpOY != '' and isInt(tmpOY):
        win.thetaOY += int(tmpOY)
    if tmpOZ != '' and isInt(tmpOZ):
        win.thetaOZ += int(tmpOZ)
    draw(win)


def draw(win):
    win.scene.clear()
    xMin = win.x_min_text.text()
    xMax = win.x_max_text.text()
    zMin = win.z_min_text.text()
    zMax = win.z_max_text.text()
    dX = win.delta_x_text.text()
    dZ = win.delta_z_text.text()
    if isInt(xMin) and isInt(xMax) and isInt(zMin) and isInt(zMax) and isFloat(dX) and isFloat(dZ) :
        xMin = int(xMin)
        xMax = int(xMax)
        zMin = int(zMin)
        zMax = int(zMax)
        dX = float(dX)
        dZ = float(dZ)
        if xMin >= -5 and xMax <= 5 and zMax <= 5 and zMin >= -5 and dX > 0 and dZ > 0:
            if win.funcs.currentText() == "sin(x) * cos(z)":
                f = f1
            elif win.funcs.currentText() == "|sin(x) * sin(z)|":
                f = f2
            elif win.funcs.currentText() == "(x ^ 2 / 5 - z ^ 2 / 6) / 2":
                f = f3
            elif win.funcs.currentText() == "exp(sin(sqrt(x**2 + z**2)))":
                f = f4
            else:
                msg = QMessageBox()
                msg.setInformativeText("Функция не выбрана!")
                msg.setWindowTitle("Ошибка!")
                msg.exec_()
                return

            win.scene, arr_pts = floatHorizon(win.scene.width(), win.scene.height(), xMin, xMax, dX,
                                     zMin, zMax, dZ, win.thetaOX, win.thetaOY, win.thetaOZ,
                                     f, win.scene, win.drawColor)
            for i in range(len(arr_pts)):
                win.scene.addLine(arr_pts[i][0],arr_pts[i][1], arr_pts[i][2],arr_pts[i][3], Qt.black)

            arr_pts.clear()

        else:
            msg = QMessageBox()
            msg.setInformativeText("Координаты должны принадлежать отрезку [-5, 5]\n"
                                   "и dX, dZ должны быть больше нуля!")
            msg.setWindowTitle("Ошибка!")
            msg.exec_()
            return
            
    else:
        msg = QMessageBox()
        msg.setInformativeText("Координаты должны быть целыми!")
        msg.setWindowTitle("Ошибка!")
        msg.exec_()
        return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
