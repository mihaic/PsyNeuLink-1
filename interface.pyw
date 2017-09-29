import os
import platform
import sys

import sip

# # switch on str in Python3
#
# sip.setapi('str', 1)

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# import your own modules here
#
# from PsyNeuLink.Functions.Process import *
# from PsyNeuLink.Functions.Mechanisms.ProcessingMechanisms.Transfer import *
# from PsyNeuLink.Functions.Mechanisms.ProcessingMechanisms.DDM import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        toolbarDockWidget = QDockWidget("Toolbar", self)
        toolbarDockWidget.setObjectName("ToolbarDockWidgetget")
        toolbarDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.palette= Palette()
        toolbarDockWidget.setWidget(self.palette)
        self.addDockWidget(Qt.LeftDockWidgetArea, toolbarDockWidget)

        self.canvas = CanvasView()
        self.setCentralWidget(self.canvas)

        self.resize(700,500)

# creating mechanism palette item widget
class MechanismPaletteItem(QListWidgetItem):
    def __init__(self, type_, parent=None):
        super(MechanismPaletteItem, self).__init__(parent)
        self.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images/brain.png")))
        self.type_ = type_ + "_mechanism"
        self.setText(self.type_)


# creating palette widget
class Palette(QListWidget):
    def __init__(self, parent=None):
        super(Palette, self).__init__(parent)
        self.setDragEnabled(True)
        self.setViewMode(QListWidget.IconMode)
        self.addItem(MechanismPaletteItem("transfer"))
        #  self.addItem(MechanismPaletteItem("ddm"))


    def startDrag(self, dropActions):
        item = self.currentItem()
        icon = item.icon()
        # storing icon image file name in mimeData
        # stream << string

        drag = QDrag(self)
        mimeData = QMimeData()
        mimeData.setText(item.text())
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QPoint(12, 12))
        drag.setPixmap(pixmap)

        # initiating drag, checking whether drag has succeededs
        if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
            self.takeItem(self.row(item))


# creating QGraphicsView subclass
class CanvasView(QGraphicsView):
    def __init__(self, parent=None):
        super(CanvasView, self).__init__(parent)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setAcceptDrops(True)


    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon"):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon"):
            data = event.mimeData().data("application/x-icon")
            stream = QDataStream(data, QIODevice.ReadOnly)
            optName = str()
            # stream >>  optName
            optName = str(optName)
            item = CanvasItem()
            print(optName)
            if (optName == "transfer_mechanism"):
                item = MechanismCanvasItem("transfer")
            if (optName == "ddm_mechanism"):
                item = MechanismCanvasItem("ddm")
            self.scene.addItem(item)
            item.setPos(event.pos())
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

class CanvasItem(QGraphicsPixmapItem):
    def __init__(self, imgFileName="images/brain.png", parent=None):
        super(CanvasItem, self).__init__(parent)
        # self.scale()
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)


class MechanismDialog(QDialog):
    def __init__(self, parent=None):
        super(MechanismDialog, self).__init__(parent)

        # for now, representing mechanism
        self.data = {
            "name":"transfer_mechanism_default",
            "kwExecuteMethod":"" ,
            "kwExecuteMethodParams":{
                "kwTransfer_Gain":0,
                "kwTransfer_Bias":0
            }}

        nameLabel = QLabel("Mechanism Instance Name")
        self.nameEdit = QLineEdit(self.data["name"])

        methodLabel = QLabel("kwExecuteMethod")
        self.kwExecuteMethodComboBox = QComboBox()
        self.kwExecuteMethodComboBox.addItem("Logistic")
        self.kwExecuteMethodComboBox.addItem("Linear")
        self.kwExecuteMethodComboBox.addItem("Exponential")

        executeMethodParamsLabel = QLabel("kwExecuteMethodParams")

        kwTransfer_GainLabel = QLabel("kwTransfer_Gain")
        self.kwTransfer_GainSpinBox = QSpinBox()

        kwTransfer_BiasLabel = QLabel("kwTransfer_Bias")
        self.kwTransfer_BiasSpinBox = QSpinBox()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        grid = QGridLayout()
        grid.addWidget(nameLabel, 0, 0)
        grid.addWidget(self.nameEdit, 0, 1)
        grid.addWidget(methodLabel, 1, 0)
        grid.addWidget(self.kwExecuteMethodComboBox, 1, 1)
        grid.addWidget(executeMethodParamsLabel, 2, 0)
        grid.addWidget(kwTransfer_GainLabel, 3, 0)
        grid.addWidget(self.kwTransfer_GainSpinBox, 3, 1)
        grid.addWidget(kwTransfer_BiasLabel, 4, 0)
        grid.addWidget(self.kwTransfer_BiasSpinBox, 4, 1)
        grid.addWidget(buttonBox, 5, 0)
        self.setLayout(grid)

        self.connect(buttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))

    def accept(self):
        self.new_data = {
            "name": str(self.nameEdit.text()), "kwExecuteMethod":self.kwExecuteMethodComboBox.itemText(self.kwExecuteMethodComboBox.currentIndex()),
            "kwExecuteMethodParams": {
                "kwTransfer_Gain":self.kwTransfer_BiasSpinBox.value(),
                "kwTransfer_Bias":self.kwTransfer_GainSpinBox.value()
            }
        }


#        try:
#            if len(decimal) == 0:
#                raise DecimalError, ("The decimal marker may not be "
#                                     "empty.")
#            if len(thousands) > 1:
#                raise ThousandsError, ("The thousands separator may "
#                                    "only be empty or one character.")
#            if len(decimal) > 1:
#                raise DecimalError, ("The decimal marker must be "
#                                     "one character.")
#            if thousands == decimal:
#                raise ThousandsError, ("The thousands separator and "
#                              "the decimal marker must be different.")
#            if thousands and thousands not in Punctuation:
#                raise ThousandsError, ("The thousands separator must "
#                                       "be a punctuation symbol.")
#            if decimal not in Punctuation:
#                raise DecimalError, ("The decimal marker must be a "
#                                     "punctuation symbol.")
#        except ThousandsError, e:
#            QMessageBox.warning(self, "Thousands Separator Error",
#                                unicode(e))
#            self.thousandsEdit.selectAll()
#            self.thousandsEdit.setFocus()
#            return
#        except DecimalError, e:
#            QMessageBox.warning(self, "Decimal Marker Error",
#                                unicode(e))
#            self.decimalMarkerEdit.selectAll()
#            self.decimalMarkerEdit.setFocus()
#            return
#
#        self.format["thousandsseparator"] = thousands
#        self.format["decimalmarker"] = decimal
#        self.format["decimalplaces"] = \
#                self.decimalPlacesSpinBox.value()
#        self.format["rednegatives"] = \
#                self.redNegativesCheckBox.isChecked()
        QDialog.accept(self)


class MechanismCanvasItem(CanvasItem):
    def __init__(self, type_, parent=None):
        super(MechanismCanvasItem, self).__init__(parent)
        self.pixmap = QPixmap("images/brain.png")
        self.setPixmap(self.pixmap)
        self.type_ = type_
        self.dialog = MechanismDialog()
        self.dialog.show()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PsyNeuLink")
    form = MainWindow()
    form.show()
    app.exec_()

main()





# import sys
# import PyQt5 as Qt
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QMainWindow
# from PyQt5.QtCore import QPoint, QTime, QMimeData
# from PyQt5.QtGui import QDrag
#
# class PNLComponent(QLabel):
#
#     def __init__(self,text):
#         super().__init__()
#         self.setText(text)
#         self.mouse_down = False
#         self.mouse_posn = QPoint()
#         self.mouse_time = QTime()
#
#
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.mouse_down = True
#             self.mouse_posn = event.pos()
#             self.mouse_time.start()
#         event.ignore()
#         super().mousePressEvent(event)
#
#     def mouseMoveEvent(self, event):
#         if self.mouse_down:
#             t = self.mouse_time.elapsed()
#             d = (event.pos() - self.mouse_posn).manhattanLength()
#             if t >= QApplication.startDragTime() or d >= QApplication.startDragDistance():
#                 self.movePNLComponent(Qt.CopyAction)
#                 event.accept()
#                 return
#         event.ignore()
#         super().mouseMoveEvent(event)
#
#     def movePNLComponent(self, actions):
#         drag = QDrag(self)
#         drag_icon = self.grab().scaledToHeight(50)
#         drag.setPixmap(drag_icon)
#         drag.setHotSpot(QPoint(drag_icon.width()/2, drag_icon.height()/2))
#
#         data_to_drag = QMimeData()
#         data_to_drag.setText(self.text())
#         drag.setMimeData(data_to_drag)
#
#         act = drag.exec(actions)
#         default_action = drag.defaultAction()
#
#         target_widget = drag.target()
#         source_widget = drag.source()
#
#         print("moved ", source_widget)
# # class Palette(QListWidget):
# #     def __init__(self, parent=None):
# #         super().__init__(parent)
# class MainWindow(QMainWindow):
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
#
#         self.addDockWidget()
#
# if __name__ == '__main__':
#     def main():
#         app = QApplication(sys.argv)
#         app.setApplicationName("PsyNeuLink")
#         form = MainWindow()
#         form.show()
#         app.exec_()

# import os
# import platform
# import sys
#
# import sip
#
# # # switch on str in Python3
# #
# sip.setapi('str', 1)
#
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
#
# # import your own modules here
#
# from PsyNeuLink.Components.Mechanisms.ProcessingMechanisms.IntegratorMechanism import IntegratorMechanism
# from PsyNeuLink.Components.Mechanisms.ProcessingMechanisms.TransferMechanism import TransferMechanism
# from PsyNeuLink.Library.Mechanisms.ProcessingMechanisms.IntegratorMechanisms.DDM import DDM
# from PsyNeuLink.Components.Functions.Function import Logistic, Linear, Exponential
#
# class MainWindow(QMainWindow):
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
#
#         toolbarDockWidget = QDockWidget("Toolbar", self)
#         toolbarDockWidget.setObjectName("ToolbarDockWidget")
#         toolbarDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
#
#         # List of items to drag from
#         self.palette = Palette()
#         toolbarDockWidget.setWidget(self.palette)
#         self.addDockWidget(Qt.LeftDockWidgetArea, toolbarDockWidget)
#
#         # Canvas area to drag to
#         self.canvas = CanvasView()
#         self.setCentralWidget(self.canvas)
#
#         # width, height of GUI window
#         self.resize(1000,500)
#
# # creating mechanism palette item widget
# class MechanismPaletteItem(QListWidgetItem):
#     def __init__(self, type_, parent=None):
#         super(MechanismPaletteItem, self).__init__(parent)
#         self.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images/brain.png")))
#         self.type_ = type_ + "_mechanism"
#         self.item_name = type_
#         self.setText(self.type_)
#
#
# # creating palette widget
# class Palette(QListWidget):
#     def __init__(self, parent=None):
#         super(Palette, self).__init__(parent)
#         self.setDragEnabled(True)
#         self.setViewMode(QListWidget.IconMode)
#         self.addItem(MechanismPaletteItem("transfer"))
#         self.addItem(MechanismPaletteItem("ddm"))
#         self.addItem(MechanismPaletteItem("integrator"))
#
#
#     def startDrag(self, dropActions):
#         # item = selected palette item
#         item = self.currentItem()
#         icon = item.icon()
#         name = item.item_name
#         # storing icon image file name in mimeData
#         data = QByteArray()
#         string = str(item.type_)
#         stream = QDataStream(data, QIODevice.WriteOnly)
#         # stream << string
#         mimeData = QMimeData()
#         mimeData.setData("application/x-icon", data)
#
#         drag = QDrag(self)
#         drag.setMimeData(mimeData)
#         pixmap = icon.pixmap(24, 24)
#         drag.setHotSpot(QPoint(12, 12))
#         drag.setPixmap(pixmap)
#
#         # initiating drag, checking whether drag has succeededs
#         if drag.exec_(Qt.MoveAction) == Qt.MoveAction:
#             self.takeItem(self.row(item))
#
#
# # creating QGraphicsView subclass
# class CanvasView(QGraphicsView):
#     def __init__(self, parent=None):
#         super(CanvasView, self).__init__(parent)
#         self.setDragMode(QGraphicsView.RubberBandDrag)
#         self.scene = QGraphicsScene(self)
#         self.setScene(self.scene)
#         self.setAcceptDrops(True)
#
#
#     def dragEnterEvent(self, event):
#         if event.mimeData().hasFormat("application/x-icon"):
#             event.accept()
#         else:
#             event.ignore()
#
#     def dragMoveEvent(self, event):
#         if event.mimeData().hasFormat("application/x-icon"):
#             event.setDropAction(Qt.CopyAction)
#             event.accept()
#         else:
#             event.ignore()
#
#     def dropEvent(self, event):
#         if event.mimeData().hasFormat("application/x-icon"):
#             data = event.mimeData().data("application/x-icon")
#             stream = QDataStream(data, QIODevice.ReadOnly)
#             print(stream)
#             optName = str()
#             # stream >> optName
#             optName = str(stream)
#             item = QLabel()
#             # print(optName)
#             # if (optName == "transfer_mechanism"):
#             #     item = MechanismCanvasItem("transfer")
#             # if (optName == "ddm_mechanism"):
#             #     item = MechanismCanvasItem("ddm")
#             # item = MechanismCanvasItem("images/brain.png")
#             self.scene.addItem(item)
#             item.setPos(event.pos())
#             # event.accept()
#             event.setDropAction(Qt.CopyAction)
#
#         else:
#             event.ignore()
#
# #########################################
# class Button(QPushButton):
#     def __init__(self, title, parent=None):
#         super().__init__(title, parent)
#
#     def mouseMoveEvent(self, e):
#
#         if e.buttons() != Qt.RightButton:
#             return
#
#         mimeData = QMimeData()
#
#         drag = QDrag(self)
#         drag.setMimeData(mimeData)
#         drag.setHotSpot(e.pos() - self.rect().topLeft())
#
#         dropAction = drag.exec_(Qt.MoveAction)
#
#     def mousePressEvent(self, e):
#
#         super().mousePressEvent(e)
#
#         if e.button() == Qt.LeftButton:
#             print('press')
#
# ##########################################
#
# # object to be created when a palette item is dropped on canvas
# class CanvasItem(QPixmap):
#     def __init__(self, imgFileName="images/brain.png", parent=QPixmap):
#         super(CanvasItem, self).__init__(parent)
#         # self.scale()
#         # self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
#
#
# class MechanismDialog(QDialog):
#     def __init__(self, parent=None):
#         super(MechanismDialog, self).__init__(parent)
#
#         # for now, representing mechanism
#         self.data = {
#             "name":"transfer_mechanism_default",
#             "kwExecuteMethod":"" ,
#             "kwExecuteMethodParams":{
#                 "kwTransfer_Gain":0,
#                 "kwTransfer_Bias":0
#             }}
#
#         nameLabel = QLabel("Mechanism Instance Name")
#         self.nameEdit = QLineEdit(self.data["name"])
#
#         methodLabel = QLabel("kwExecuteMethod")
#         self.kwExecuteMethodComboBox = QComboBox()
#         self.kwExecuteMethodComboBox.addItem("Logistic")
#         self.kwExecuteMethodComboBox.addItem("Linear")
#         self.kwExecuteMethodComboBox.addItem("Exponential")
#
#         executeMethodParamsLabel = QLabel("kwExecuteMethodParams")
#
#         kwTransfer_GainLabel = QLabel("kwTransfer_Gain")
#         self.kwTransfer_GainSpinBox = QSpinBox()
#
#         kwTransfer_BiasLabel = QLabel("kwTransfer_Bias")
#         self.kwTransfer_BiasSpinBox = QSpinBox()
#
#         buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
#
#         grid = QGridLayout()
#         grid.addWidget(nameLabel, 0, 0)
#         grid.addWidget(self.nameEdit, 0, 1)
#         grid.addWidget(methodLabel, 1, 0)
#         grid.addWidget(self.kwExecuteMethodComboBox, 1, 1)
#         grid.addWidget(executeMethodParamsLabel, 2, 0)
#         grid.addWidget(kwTransfer_GainLabel, 3, 0)
#         grid.addWidget(self.kwTransfer_GainSpinBox, 3, 1)
#         grid.addWidget(kwTransfer_BiasLabel, 4, 0)
#         grid.addWidget(self.kwTransfer_BiasSpinBox, 4, 1)
#         grid.addWidget(buttonBox, 5, 0)
#         self.setLayout(grid)
#
#         self.connect(buttonBox, SIGNAL("accepted()"), self, SLOT("accept()"))
#
#     def accept(self):
#         self.new_data = {
#             "name": str(self.nameEdit.text()), "kwExecuteMethod":self.kwExecuteMethodComboBox.itemText(self.kwExecuteMethodComboBox.currentIndex()),
#             "kwExecuteMethodParams": {
#                 "kwTransfer_Gain":self.kwTransfer_BiasSpinBox.value(),
#                 "kwTransfer_Bias":self.kwTransfer_GainSpinBox.value()
#             }
#         }
#
#
# #        try:
# #            if len(decimal) == 0:
# #                raise DecimalError, ("The decimal marker may not be "
# #                                     "empty.")
# #            if len(thousands) > 1:
# #                raise ThousandsError, ("The thousands separator may "
# #                                    "only be empty or one character.")
# #            if len(decimal) > 1:
# #                raise DecimalError, ("The decimal marker must be "
# #                                     "one character.")
# #            if thousands == decimal:
# #                raise ThousandsError, ("The thousands separator and "
# #                              "the decimal marker must be different.")
# #            if thousands and thousands not in Punctuation:
# #                raise ThousandsError, ("The thousands separator must "
# #                                       "be a punctuation symbol.")
# #            if decimal not in Punctuation:
# #                raise DecimalError, ("The decimal marker must be a "
# #                                     "punctuation symbol.")
# #        except ThousandsError, e:
# #            QMessageBox.warning(self, "Thousands Separator Error",
# #                                unicode(e))
# #            self.thousandsEdit.selectAll()
# #            self.thousandsEdit.setFocus()
# #            return
# #        except DecimalError, e:
# #            QMessageBox.warning(self, "Decimal Marker Error",
# #                                unicode(e))
# #            self.decimalMarkerEdit.selectAll()
# #            self.decimalMarkerEdit.setFocus()
# #            return
# #
# #        self.format["thousandsseparator"] = thousands
# #        self.format["decimalmarker"] = decimal
# #        self.format["decimalplaces"] = \
# #                self.decimalPlacesSpinBox.value()
# #        self.format["rednegatives"] = \
# #                self.redNegativesCheckBox.isChecked()
#         QDialog.accept(self)
#
#
# class MechanismCanvasItem(CanvasItem):
#     def __init__(self, type_, parent=CanvasItem):
#         super(MechanismCanvasItem, self).__init__(parent)
#         self.pixmap = QPixmap("images/brain.png")
#         self.setPixmap(self.pixmap)
#         self.type_ = type_
#         self.dialog = MechanismDialog()
#         self.dialog.show()
#
# def main():
#     app = QApplication(sys.argv)
#     app.setApplicationName("PsyNeuLink")
#     form = MainWindow()
#     form.show()
#     app.exec_()
#
# main()






# Tkinter:

#
# import tkinter as tk
#
# class Example(tk.Frame):
#     '''Illustrate how to drag items on a Tkinter canvas'''
#
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent)
#
#         # create a canvas
#         self.canvas = tk.Canvas(width=1000, height=400)
#         self.canvas.pack(side=tk.LEFT, fill="both", expand=True)
#
#         self.canvas2 = tk.Canvas(width=1000, height=400)
#         self.canvas2.pack(side=tk.LEFT, fill="both", expand=True)
#         # this data is used to keep track of an
#         # item being dragged
#         self._drag_data = {"x": 0, "y": 0, "item": None}
#
#         # create a couple of movable objects
#         self._create_token((100, 100), "blue")
#         self._create_token((200, 100), "red")
#         # self._create_drop_surface()
#         # add bindings for clicking, dragging and releasing over
#         # any object with the "token" tag
#         self.canvas.tag_bind("token", "<ButtonPress-1>", self.on_token_press)
#         self.canvas.tag_bind("token", "<ButtonRelease-1>", self.on_token_release)
#         self.canvas.tag_bind("token", "<B1-Motion>", self.on_token_motion)
#
#     def _create_drop_surface(self):
#         drop_surface = tk.Frame(text="Drop PNL Objects Here!")
#         drop_surface.pack()
#         drop_surface.place(x=200, y=225, anchor=tk.CENTER)
#     def _create_token(self, coord, color):
#         '''Create a token at the given coordinate in the given color'''
#         (x,y) = coord
#         self.canvas.create_rectangle(x-25, y-25, x+25, y+25,
#                                 outline=color, fill=color, tags="token")
#
#     def on_token_press(self, event):
#         '''Begining drag of an object'''
#         # record the item and its location
#         self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
#         self._drag_data["x"] = event.x
#         self._drag_data["y"] = event.y
#         config = self.canvas.itemconfig(self._drag_data["item"])
#         new_config = {key: config[key][-1] for key in config.keys()}
#         self.canvas.create_rectangle((event.x+25, event.y+25, event.x-25, event.y-25), **new_config)
#
#
#     def on_token_release(self, event):
#         '''End drag of an object'''
#         # reset the drag information
#         self._drag_data["item"] = None
#         self._drag_data["x"] = 0
#         self._drag_data["y"] = 0
#
#     def on_token_motion(self, event):
#         '''Handle dragging of an object'''
#         # compute how much the mouse has moved
#         delta_x = event.x - self._drag_data["x"]
#         delta_y = event.y - self._drag_data["y"]
#         # move the object the appropriate amount
#         self.canvas.move(self._drag_data["item"], delta_x, delta_y)
#         # record the new position
#         self._drag_data["x"] = event.x
#         self._drag_data["y"] = event.y
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     # create a toplevel menu
#
#     def hello():
#         print("hello!")
#
#
#     listbox = tk.Listbox(root)
#     listbox.pack()
#     def buttonAction(name):
#         print(name, " was clicked")
#     mylist = ['TransferMechanism', 'DDM', 'IntegratorMechanism']
#     for item in mylist:
#         button = tk.Button(root, text=item, command=lambda x=item: buttonAction(x))
#         listbox.insert(tk.END, button)
#     # display the menu
#     Example(root).pack(fill="both", expand=True)
#     root.mainloop()