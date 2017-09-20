import os
import platform
import sys

import sip

# # switch on str in Python3
#
sip.setapi('str', 1)

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# import your own modules here

from PsyNeuLink.Components.Mechanisms.ProcessingMechanisms.IntegratorMechanism import IntegratorMechanism
from PsyNeuLink.Components.Mechanisms.ProcessingMechanisms.TransferMechanism import TransferMechanism
from PsyNeuLink.Library.Mechanisms.ProcessingMechanisms.IntegratorMechanisms.DDM import DDM
from PsyNeuLink.Components.Functions.Function import Logistic, Linear, Exponential

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        toolbarDockWidget = QDockWidget("Toolbar", self)
        toolbarDockWidget.setObjectName("ToolbarDockWidgetget")
        toolbarDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)

        # List of items to drag from
        self.palette = Palette()
        toolbarDockWidget.setWidget(self.palette)
        self.addDockWidget(Qt.LeftDockWidgetArea, toolbarDockWidget)

        # Canvas area to drag to
        self.canvas = CanvasView()
        self.setCentralWidget(self.canvas)

        # width, height of GUI window
        self.resize(1000,500)

# creating mechanism palette item widget
class MechanismPaletteItem(QListWidgetItem):
    def __init__(self, type_, parent=None):
        super(MechanismPaletteItem, self).__init__(parent)
        self.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "images/brain.png")))
        self.type_ = type_ + "_mechanism"
        self.item_name = type_
        self.setText(self.type_)


# creating palette widget
class Palette(QListWidget):
    def __init__(self, parent=None):
        super(Palette, self).__init__(parent)
        self.setDragEnabled(True)
        self.setViewMode(QListWidget.IconMode)
        self.addItem(MechanismPaletteItem("transfer"))
        self.addItem(MechanismPaletteItem("ddm"))
        self.addItem(MechanismPaletteItem("integrator"))


    def startDrag(self, dropActions):
        # item = selected palette item
        item = self.currentItem()
        icon = item.icon()
        name = item.item_name
        # storing icon image file name in mimeData
        data = QByteArray()
        string = str(item.type_)
        stream = QDataStream(data, QIODevice.WriteOnly)
        # stream << string
        mimeData = QMimeData()
        mimeData.setData("application/x-icon", data)

        drag = QDrag(self)
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
            # stream >> optName
            optName = str(stream)
            item = QGraphicsRectItem()
            # print(optName)
            # if (optName == "transfer_mechanism"):
            #     item = MechanismCanvasItem("transfer")
            # if (optName == "ddm_mechanism"):
            #     item = MechanismCanvasItem("ddm")
            # item = MechanismCanvasItem("images/brain.png")
            self.scene.addItem(item)
            item.setPos(event.pos())
            item.setBrush(QBrush(Qt.red, style =Qt.SolidPattern))
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

#########################################
class Button(QPushButton):
    def __init__(self, title, parent=None):
        super().__init__(title, parent)

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):

        super().mousePressEvent(e)

        if e.button() == Qt.LeftButton:
            print('press')

##########################################

# object to be created when a palette item is dropped on canvas
class CanvasItem(QPixmap):
    def __init__(self, imgFileName="images/brain.png", parent=QPixmap):
        super(CanvasItem, self).__init__(parent)
        # self.scale()
        # self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)


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
    def __init__(self, type_, parent=CanvasItem):
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