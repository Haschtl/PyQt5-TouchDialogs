from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import sys
from functools import partial

import pyqt_lib as pyqtlib

message_stylesheet = '''
QPushButton:focus {
	border: none;
	outline: none;
	background-color: none;
}

QPushButton
{
    color: #eff0f1;
    /*background-color: #31363b;*/
    background-color: #404347;
    border-width: 0px;
    border-color: #76797C;
    border-style: solid;
    padding: 5px;
    border-radius: 2px;
    outline: none;
    opacity: 50;
}

QPushButton:focus {
    background-color: #3daee9;
    color: white;
}

QPushButton:pressed
{
    background-color: #3daee9;
    padding-top: -15px;
    padding-bottom: -17px;
}

QPushButton:hover
{
    border: 1px solid #3daee9;
    color: #eff0f1;
}

GrowingTextEdit, GrowingTextEdit:hover, GrowingTextEdit:disabled
{
    background-color: rgba(49, 54, 59,70);
    color: #eff0f1;
    border-radius: 0px;
    border: 0px solid #76797C;
}

QLabel
{
    background-color: rgba(49, 54, 59,70);
    border: 0px solid black;
    color: white;
}
'''

def alert_message(parent, title='', text='', stylesheet="", okbutton="OK", cancelbutton="Abbrechen"):
    _popframe = TranslucentWidget(parent)
    _popframe.resize(QtWidgets.QDesktopWidget().availableGeometry().width(), QtWidgets.QDesktopWidget().availableGeometry().height())

    msg = message(title = title, text=[text], stylesheet=stylesheet, buttonIcons=['close_window', 'checkbox_checked'], icon="alert", height=400)
    pyqtlib.clickable(_popframe).connect(msg.cancel)
    retval, text = msg.exec_()
    print(retval)
    print(text)
    _popframe._onclose()
    if retval == 0:
        return False
    else:
        return True


def info_message(parent, title='', text='', stylesheet="", buttons=['OK'], icon="info"):
    _popframe = TranslucentWidget(parent)
    _popframe.resize(QtWidgets.QDesktopWidget().availableGeometry().width(), QtWidgets.QDesktopWidget().availableGeometry().height())

    msg = message(title = title, text=[text], stylesheet=stylesheet, buttonIcons=['checkbox_checked'], height=400, icon='info')
    pyqtlib.clickable(_popframe).connect(msg.cancel)
    retval, text = msg.exec_()
    _popframe._onclose()
    return retval


def item_message(self, title, text, items, stylesheet=""):

    item, ok = QtWidgets.QInputDialog.getItem(self, title,
                                              text, items, 0, False)
    return item, ok


def text_message(self, title, text, placeholdertext, stylesheet=""):
    text, ok = QtWidgets.QInputDialog.getText(
        self, title, text, QtWidgets.QLineEdit.Normal, placeholdertext)

    return text, ok


class message(QtWidgets.QDialog):
    def __init__(self, **kwargs):
        super(message, self).__init__()
        title = kwargs.get('title', None)
        text = kwargs.get('text', None)
        width = kwargs.get('width', 300)
        height = kwargs.get('height', 200)
        stylesheet = kwargs.get('stylesheet', None)
        if stylesheet:
            self.stylesheet = stylesheet
        else:
            self.stylesheet = message_stylesheet

        layout = QtWidgets.QVBoxLayout(self)
        if title:
            self.header = QtWidgets.QLabel()
            self.header.setAlignment(QtCore.Qt.AlignCenter)
            self.header.setFont(QtGui.QFont('SansSerif', 13))
            layout.addWidget(self.header)
        self.buttonLayout = QtWidgets.QHBoxLayout(self)
        self.textLayout = QtWidgets.QVBoxLayout(self)
        icon = kwargs.get('icon', None)
        if icon:
            label = QtWidgets.QLabel(self)
            #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            #label.setSizePolicy(sizePolicy)
            label.setFixedHeight(40)
            pyqtlib.set_Icon(label, icon, "QLabel")
            layout.addWidget(label)
        layout.insertLayout(1, self.textLayout)
        layout.insertLayout(2, self.buttonLayout)

        self.buttonNames = kwargs.get('buttons', None)
        self.buttonIcons = kwargs.get('buttonIcons', None)
        if self.buttonNames == None and self.buttonIcons == None:
            self.buttonNames = ["Abbrechen", "OK"]
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        if title:
            self.header.setText(title)
        if text:
            self.setTexts(text)
        # if info:
        #     self.text2.setPlainText(info)
        self.setStyleSheet(self.stylesheet)

        if icon:
            self.setDialogIcon(icon)
        # siw = pyqtlib.SoftInputWidget(self)
        # siw.show()
        self.resize(width, height)

        self.retValue = -1
        self.retText = ''

        self.buttons = []
        self.setButtons()

        x = (QtWidgets.QDesktopWidget().availableGeometry().width()-self.frameGeometry().width())/2
        y = (QtWidgets.QDesktopWidget().availableGeometry().height()-self.frameGeometry().height())/2
        self.move(x, y)

        self.show()

    def setButtons(self):
        if self.buttonNames:
            for name in self.buttonNames:
                #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                button = QtWidgets.QPushButton(name)
                #button.setSizePolicy(sizePolicy)
                button.setFixedHeight(40)
                button.clicked.connect(partial(self.buttonAction, len(self.buttons), button))
                self.buttonLayout.addWidget(button)
                self.buttons.append(button)
        if self.buttonIcons:
            for icon in self.buttonIcons:
                button = QtWidgets.QPushButton()
                pyqtlib.set_Icon(button, icon)
                button.setFixedHeight(40)
                button.clicked.connect(partial(self.buttonAction, len(self.buttons), button))
                self.buttonLayout.addWidget(button)
                self.buttons.append(button)

    def setTexts(self, texts):
        for text in texts:
            textEdit = GrowingTextEdit(text=text, stylesheet=self.stylesheet)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            textEdit.setSizePolicy(sizePolicy)
            textEdit.setEnabled(False)
            self.textLayout.addWidget(textEdit)

    def setDialogIcon(self, icon):
        pass

    def buttonAction(self, idx, button):
        # self._popframe._onclose()
        self.retValue = idx
        self.retText = button.text()
        self.accept()

    def cancel(self):
        self.retValue = 0
        self.retText = "Cancel"
        self.accept()

    def exec_(self):
        super(message, self).exec_()
        return self.retValue, self.retText


def easy_float_message(parent, default, min, max):
    _popframe = TranslucentWidget(parent)
    _popframe.resize(QtWidgets.QDesktopWidget().availableGeometry().width(), QtWidgets.QDesktopWidget().availableGeometry().height())
    numericDialog = float_message(default=default, min=min, max=max)
    pyqtlib.clickable(_popframe).connect(numericDialog.actionCancel)
    ok, value = numericDialog.exec_()
    _popframe._onclose()
    return ok, value


class float_message(QtWidgets.QDialog):
    def __init__(self, **kwargs):
        super(float_message, self).__init__()

        default = kwargs.get('default', 0)
        min = kwargs.get('min', 0)
        max = kwargs.get('max', 100)
        width = kwargs.get('width', 200)
        height = kwargs.get('height', 300)
        stylesheet = kwargs.get('stylesheet', None)
        uic.loadUi("float_message.ui", self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        if stylesheet:
            self.setStyleSheet(stylesheet)
        # siw = pyqtlib.SoftInputWidget(self)
        # siw.show()
        self.resize(width, height)
        self.setHoverIcons()
        self.setButtonCallbacks()

        x = (QtWidgets.QDesktopWidget().availableGeometry().width()-self.frameGeometry().width())/2
        y = (QtWidgets.QDesktopWidget().availableGeometry().height()-self.frameGeometry().height())/2
        self.move(x, y)
        
        if '.' in str(default):
            self.comma = len(str(default).split('.')[1])
            # self.commaButton.setChecked(True)
        elif ',' in str(default):
            self.comma = len(str(default).split(',')[1])
            # self.commaButton.setChecked(True)
        else:
            self.comma = -1
        self.doubleSpinBox.setRange(min, max)
        self.digitVal = default
        self.submit = False
        self.doubleSpinBox.setDecimals(self.comma+1)
        self.doubleSpinBox.setValue(default)

        self.show()

    def setHoverIcons(self):
        pyqtlib.set_Icon(self.cancelButton, "esc")
        pyqtlib.set_Icon(self.zeroButton, "0")
        pyqtlib.set_Icon(self.oneButton, "1")
        pyqtlib.set_Icon(self.twoButton, "2")
        pyqtlib.set_Icon(self.threeButton, "3")
        pyqtlib.set_Icon(self.fourButton, "4")
        pyqtlib.set_Icon(self.fiveButton, "5")
        pyqtlib.set_Icon(self.sixButton, "6")
        pyqtlib.set_Icon(self.sevenButton, "7")
        pyqtlib.set_Icon(self.eightButton, "8")
        pyqtlib.set_Icon(self.nineButton, "9")

        pyqtlib.set_Icon(self.submitButton, "enter")
        pyqtlib.set_Icon(self.backspaceButton, "backspace")
        pyqtlib.set_IconChecked(self.commaButton, "comma")

    def setButtonCallbacks(self):
        self.cancelButton.clicked.connect(self.actionCancel)
        self.zeroButton.clicked.connect(lambda: self.actionDigit(0))
        self.oneButton.clicked.connect(lambda: self.actionDigit(1))
        self.twoButton.clicked.connect(lambda: self.actionDigit(2))
        self.threeButton.clicked.connect(lambda: self.actionDigit(3))
        self.fourButton.clicked.connect(lambda: self.actionDigit(4))
        self.fiveButton.clicked.connect(lambda: self.actionDigit(5))
        self.sixButton.clicked.connect(lambda: self.actionDigit(6))
        self.sevenButton.clicked.connect(lambda: self.actionDigit(7))
        self.eightButton.clicked.connect(lambda: self.actionDigit(8))
        self.nineButton.clicked.connect(lambda: self.actionDigit(9))
        self.submitButton.clicked.connect(self.actionSubmit)
        self.backspaceButton.clicked.connect(self.actionBackspace)
        self.commaButton.clicked.connect(self.actionComma)

    def actionDigit(self, addValue):
        oldValue = self.doubleSpinBox.value()
        if self.comma < 0 or not self.commaButton.isChecked():
            newValue = oldValue*10 + addValue
        else:
            self.doubleSpinBox.setDecimals(self.comma+1)
            multiplier = 1 / 10 * 10 ** -self.comma
            newValue = oldValue + addValue * multiplier
            self.comma += 1
        self.doubleSpinBox.setValue(newValue)
        self.digitVal = self.doubleSpinBox.value()

    def actionSubmit(self):
        self.submit = True
        # self._popframe._onclose()
        self.accept()

    def actionCancel(self):
        self.submit = False
        # self._popframe._onclose()
        self.accept()

    def actionBackspace(self):
        oldValue = self.doubleSpinBox.value()
        if self.comma < 0:
            newValue = round(oldValue/10)
        else:
            self.comma -= 1
            if self.comma == 0:
                self.comma = -1
            self.doubleSpinBox.setDecimals(self.comma)
            newValue = round(oldValue, self.comma)
            if self.comma == -1:
                self.commaButton.setChecked(False)

        self.doubleSpinBox.setValue(newValue)
        self.digitVal = self.doubleSpinBox.value()

    def actionComma(self):
        if self.commaButton.isChecked():
            self.comma = 0
        else:
            self.doubleSpinBox.setDecimals(0)
            self.comma = -1

    def exec_(self):
        super(float_message, self).exec_()
        return self.submit, self.digitVal


class TranslucentWidgetSignals(QtCore.QObject):
    # SIGNALS
    CLOSE = QtCore.pyqtSignal()


class TranslucentWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TranslucentWidget, self).__init__(parent)

        # make the window frameless
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.fillColor = QtGui.QColor(30, 30, 30, 220)
        self.penColor = QtGui.QColor("#333333")

        self.popup_fillColor = QtGui.QColor(240, 240, 240, 255)
        self.popup_penColor = QtGui.QColor(200, 200, 200, 255)

        # self.close_btn = QtWidgets.QPushButton(self)
        # self.close_btn.setText("x")
        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setBold(True)

        self.SIGNALS = TranslucentWidgetSignals()

        self.move(0, 0)
        if parent:
            self.resize(parent.width(), parent.height())
        else:
            self.resize(800, 450)
        self.SIGNALS.CLOSE.connect(self._closepopup)
        self._popflag = True
        self.show()

    def _closepopup(self):
        self.close()
        self._popflag = False

    def paintEvent(self, event):
        # This method is, in practice, drawing the contents of
        # your window.

        # get current window size
        s = self.size()
        qp = QtGui.QPainter()

        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(self.penColor)
        qp.setBrush(self.fillColor)
        qp.drawRect(0, 0, s.width(), s.height())

        # drawpopup
        qp.setPen(self.popup_penColor)
        qp.setBrush(self.popup_fillColor)

        qp.end()

    def _onclose(self):
        self.SIGNALS.CLOSE.emit()

class GrowingTextEdit(QtWidgets.QTextEdit):
    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args)
        # self.document().contentsChanged.connect(self.sizeChange)
        text = kwargs.get('text', '')
        stylesheet = kwargs.get('stylesheet', None)
        self.heightMin = 40
        self.heightMax = 2000
        # self.sizeChange()
        self.setFontPointSize(10)
        #self.setFont(QtGui.QFont('SansSerif', 10))
        # self.setAttribute(103)
        #self.setFixedHeight(40)
        # self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.setMinimumHeight(28)
        # self.returnPressed.emit(self.enterEvent())
        #self.clicked2.connect(self.showPlainText)
        self.setText2(text)
        if stylesheet:
            self.setStyleSheet(stylesheet)


    def sizeChange2(self):
        # docHeight = self.document().size().height()
        # nlines = self.text().count('\n')
        # if nlines is 0:

        #     nlines = 1
        size = max(self.text.count('<br/>')+1, self.text.count('\n')+1)*(self.fontPointSize()*2) + self.contentsMargins().top()+self.contentsMargins().bottom()
        # size=self.document().size().height() + self.contentsMargins().top()+self.contentsMargins().bottom()
        if self.heightMin <= size <= self.heightMax:
            #self.setMinimumHeight((nlines-1)*34+40)
            self.setMinimumHeight(size)
            # self.setMinimumHeight(docHeight)
        if size<self.heightMin:
            self.setMinimumHeight(self.heightMin)
        if size>self.heightMax:
            self.setMinimumHeight(self.heightMax)
    #def mousePressEvent(self, event):
    #    if event.button() == QtCore.Qt.LeftButton: self.clicked.emit()
    #    else: super().mousePressEvent(event)

    def text(self):
        return self.toPlainText()
        #return self.originalText

    #def showPlainText(self):
    #    self.setText(self.originalText)

    def setText2(self, text):
        #self.originalText=text
        self.text=text
        self.setText(text)
        #self.setPlainText(markdown2.markdown(text))
        # docHeight = self.document().size().height()
        self.sizeChange2()
        # self.setMinimumHeight(40+(nlines-1)*25)

    #def setPlaceholderText(self, text):
    #    self.placeholderText = text

    # def paintEvent(self, _event):
    #     """
    #     Implements the same behavior as QLineEdit's setPlaceholderText()
    #     Draw the placeholder text when there is no text entered and the widget
    #     doesn't have focus.
    #     """
    #     if self.placeholderText and not self.hasFocus() and not self.toPlainText():
    #         painter = QtGui.QPainter(self.viewport())
    #
    #         color = self.palette().text().color()
    #         color.setAlpha(128)
    #         painter.setPen(color)
    #
    #         painter.drawText(self.geometry().topLeft(), self.placeholderText)
    #
    #     else:
    #         super(GrowingTextEdit, self).paintEvent(_event)

    # def focusInEvent(self, event):
    #     QtWidgets.QTextEdit.focusInEvent(self, event)

    # def returnPressed(self, text):
    #     pass

def example_main(type = 'float'):
    app = QtWidgets.QApplication(sys.argv)
    if type == 'float':
        numericDialog = float_message(default=10, min=0, max=1000)
        submit, digitVal = numericDialog.exec_()
        print("Submit:" + str(submit)+'\nValue: ' + str(digitVal))
    elif type == 'info':
        answer = info_message(None, 'Info','This is <b>HTML-formatted</b> info-text<br>Based on "message" from this library')
        print("Submit:" + str(answer))
    elif type == 'alert':
        answer = alert_message(None, 'Alert','This is an alert, which returns True or False<br>Based on "message" from this library')
        print("Submit:" + str(answer))
    elif type == 'all':
        numericDialog = float_message(default=10, min=0, max=1000)
        submit, digitVal = numericDialog.exec_()
        print("Submit:" + str(submit)+'\nValue: ' + str(digitVal))
        answer = info_message(None, 'Info','This is <b>HTML-formatted</b> info-text<br>Based on "message" from this library')
        print("Submit:" + str(answer))
        answer = alert_message(None, 'Alert','This is an alert, which returns True or False<br>Based on "message" from this library')
        print("Submit:" + str(answer))
        infoDialog = message(title = "Titel", text=['This is an example custom message'], buttons=['A','B','C','D'])
        answer, text = infoDialog.exec_()
        print("Submit:" + str(answer)+'\nValue: ' + str(text))
    else:
        infoDialog = message(title = "Titel", text=['This is an example custom message'], buttons=['A','B','C','D'])
        answer, text = infoDialog.exec_()
        print("Submit:" + str(answer)+'\nValue: ' + str(text))


if __name__ == '__main__':
    example_main('all')
