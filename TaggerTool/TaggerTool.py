# -*- coding: utf-8 -*-
import sys
import pandas
from PyQt5 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure


handata = pandas.read_csv("hanData_1464739200_1464825600.csv")
frames = pandas.read_csv("frames_1464739200_1464825600.csv")
x_handata = handata.Timestamp
y_handata = handata.Value


def get_frames(min_amp=None, max_amp=None):
    if min_amp and max_amp:
        filtered_frames = frames[
            (frames.plat <= int(max_amp)) & (frames.plat >= int(min_amp))
        ]
    elif min_amp and not max_amp:
        filtered_frames = frames[frames.plat >= int(min_amp)]
    elif not min_amp and max_amp:
        filtered_frames = frames[frames.plat <= int(max_amp)]
    elif not min_amp and not max_amp:
        filtered_frames = frames
    x_frames = filtered_frames.time
    y_frames_max = filtered_frames.plat
    y_min_indexes = filtered_frames.index - 1
    y_frames_min = frames.iloc[y_min_indexes].plat
    transition_colors = []
    for transition in filtered_frames.transition:
        if transition > 0:
            transition_colors.append("g")
        elif transition < 0:
            transition_colors.append("r")
        else:
            transition_colors.append("b")
    return x_frames, y_frames_min, y_frames_max, transition_colors


class Plot(FigureCanvas):
    def __init__(self, parent=None, width=5, height=10, dpi=100):
        self.frames = None
        self.axes = None
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.mpl_connect("resize_event", self._tight_layout)
        self.build_plot()
        self.setParent(parent)

    def _tight_layout(self, *args, **kwargs):
        self.fig.tight_layout()

    def build_plot(self):
        x_frames, y_frames_min, y_frames_max, transisiton_colors = get_frames()
        self.axes = self.fig.add_subplot(111)
        self.axes.plot(x_handata, y_handata, "b")
        self.frames = self.axes.vlines(x_frames, y_frames_min, y_frames_max, colors=transisiton_colors)
        self.axes.set_xlabel("timestamps")
        self.axes.set_ylabel("amplitude")
        self.axes.grid(color="grey", linestyle="dotted", linewidth=0.25)
        self._tight_layout()

    def update_plot(self, min_amp=None, max_amp=None):
        x_frames, y_frames_min, y_frames_max, transisiton_colors = get_frames(min_amp, max_amp)
        self.frames.remove()
        self.draw_idle()
        self.frames = self.axes.vlines(x_frames, y_frames_min, y_frames_max, colors=transisiton_colors)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.prev_day_button = QtWidgets.QPushButton(self.centralWidget)
        self.prev_day_button.setObjectName("prev_day_button")
        self.horizontalLayout.addWidget(self.prev_day_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.save_button = QtWidgets.QPushButton(self.centralWidget)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.next_day_button = QtWidgets.QPushButton(self.centralWidget)
        self.next_day_button.setObjectName("next_day_button")
        self.horizontalLayout.addWidget(self.next_day_button)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.plot = Plot(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot.sizePolicy().hasHeightForWidth())
        self.plot.setSizePolicy(sizePolicy)
        self.plot.setObjectName("plot")
        self.gridLayout.addWidget(self.plot, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.min_amp = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.min_amp.sizePolicy().hasHeightForWidth())
        self.min_amp.setSizePolicy(sizePolicy)
        self.min_amp.setObjectName("min_amp")
        self.horizontalLayout_2.addWidget(self.min_amp)
        self.min_amp_input = QtWidgets.QLineEdit(self.centralWidget)
        self.min_amp_input.setValidator(QtGui.QIntValidator())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.min_amp_input.sizePolicy().hasHeightForWidth())
        self.min_amp_input.setSizePolicy(sizePolicy)
        self.min_amp_input.setObjectName("min_amp_input")
        self.horizontalLayout_2.addWidget(self.min_amp_input)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.max_amp = QtWidgets.QLabel(self.centralWidget)
        self.max_amp.setObjectName("max_amp")
        self.horizontalLayout_3.addWidget(self.max_amp)
        self.max_amp_input = QtWidgets.QLineEdit(self.centralWidget)
        self.max_amp_input.setValidator(QtGui.QIntValidator())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.max_amp_input.sizePolicy().hasHeightForWidth())
        self.max_amp_input.setSizePolicy(sizePolicy)
        self.max_amp_input.setObjectName("max_amp_input")
        self.horizontalLayout_3.addWidget(self.max_amp_input)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.submit_button = QtWidgets.QPushButton(self.centralWidget)
        self.submit_button.clicked.connect(self.handleButton)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submit_button.sizePolicy().hasHeightForWidth())
        self.submit_button.setSizePolicy(sizePolicy)
        self.submit_button.setBaseSize(QtCore.QSize(0, 0))
        self.submit_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.submit_button.setObjectName("submit_button")
        self.horizontalLayout_5.addWidget(self.submit_button)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menuBar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menuBar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())
        self.plot_toolbar = NavigationToolbar(self.plot, MainWindow)
        self.plot_toolbar.setObjectName("Matplolib toolbar")
        MainWindow.addToolBar(self.plot_toolbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def handleButton(self):
        min_amp = self.min_amp_input.text()
        max_amp = self.max_amp_input.text()
        if max_amp and min_amp and int(max_amp) <= int(min_amp):
            self.showDialog()
        else:
            self.plot.update_plot(min_amp, max_amp)

    def showDialog(self):
        msg = QtWidgets.QMessageBox(self.centralWidget)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Minimal amplititude cannot be greater or equal to maximal")
        msg.setWindowTitle("TaggerTool message")
        msg.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TaggerTool"))
        self.prev_day_button.setText(_translate("MainWindow", "Previous day"))
        self.save_button.setText(_translate("MainWindow", "Save"))
        self.next_day_button.setText(_translate("MainWindow", "Next day"))
        self.label.setText(_translate("MainWindow", "Filter amplitude"))
        self.min_amp.setText(_translate("MainWindow", "Min amp:"))
        self.max_amp.setText(_translate("MainWindow", "Max amp:"))
        self.submit_button.setText(_translate("MainWindow", "Submit"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuAbout.setTitle(_translate("MainWindow", "Abo&ut"))
        self.plot_toolbar.setWindowTitle(_translate("MainWindow", "Matplolib toolbar"))
        self.actionExit.setText(_translate("MainWindow", "&Exit"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
