# -*- coding: utf-8 -*-
import sys
import pandas
from PyQt5 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection


handata = pandas.read_csv("hanData_1464739200_1464825600.csv")
frames = pandas.read_csv("frames_1464739200_1464825600.csv")
x_handata = handata.Timestamp
y_handata = handata.Value


def get_frames(min_amp=None, max_amp=None):
    if min_amp and max_amp:
        filtered_frames = frames[
            (abs(frames.transition) <= int(max_amp)) & (abs(frames.transition) >= int(min_amp))
        ]
    elif min_amp and not max_amp:
        filtered_frames = frames[abs(frames.transition) >= int(min_amp)]
    elif not min_amp and max_amp:
        filtered_frames = frames[abs(frames.transition) <= int(max_amp)]
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


def get_rectangles(min_amp, max_amp, min_duration=None, max_duration=None):
    prev_x_frame = 0
    prev_color = ""
    rectangles = []
    coords = ()
    if not min_duration and max_duration:
        expression = lambda width: width <= int(max_duration)
    elif not max_duration and min_duration:
        expression = lambda width: width >= int(min_duration)
    elif max_duration and min_duration:
        expression = lambda width: int(min_duration) <= width <= int(max_duration)
    for x_frame, y_frame_min, y_frame_max, transition_color in zip(*get_frames(min_amp, max_amp)):
        width = x_frame - prev_x_frame
        if transition_color == "g" and prev_color != "g":
            coords = (x_frame, y_frame_min)
            prev_x_frame = x_frame
            height_g = y_frame_max - y_frame_min
        elif transition_color == "r" and coords and expression(width):
            height_r = y_frame_min - y_frame_max
            height = max(height_r, height_g)
            rectangles.append(Rectangle(coords, width, height, fill=False, edgecolor="g", linewidth=5))
        prev_color = transition_color
    return rectangles


class Plot(FigureCanvas):

    def __init__(self, parent=None, width=5, height=10, dpi=100):
        self.axes = None
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.mpl_connect("resize_event", self._tight_layout)
        self.build_plot()
        self.setParent(parent)

    def _tight_layout(self, *args, **kwargs):
        self.fig.tight_layout()

    def build_plot(self):
        self.axes = self.fig.add_subplot(111)
        self.axes.plot(x_handata, y_handata, "b")
        self.axes.set_xlabel("timestamps")
        self.axes.set_ylabel("amplitude")
        self.axes.grid(color="grey", linestyle="dotted", linewidth=0.25)
        self._tight_layout()

    def _clean_plot(self):
        for frame in self.axes.findobj(match=LineCollection):
            frame.remove()
        for rectangle in self.axes.findobj(match=Rectangle):
            try:
                rectangle.remove()
            except NotImplementedError:
                pass
        self.draw_idle()

    def filter_amp(self, min_amp, max_amp):
        x_frames, y_frames_min, y_frames_max, transisiton_colors = get_frames(min_amp, max_amp)
        self._clean_plot()
        self.axes.vlines(x_frames, y_frames_min, y_frames_max, colors=transisiton_colors, linewidth=5)

    def draw_pairs(self, min_duration, max_duration, min_amp, max_amp):
        self._clean_plot()
        for rectangle in get_rectangles(min_amp, max_amp, min_duration, max_duration):
            self.axes.add_patch(rectangle)


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
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.duration_min = QtWidgets.QLabel(self.centralWidget)
        self.duration_min.setObjectName("duration_min")
        self.horizontalLayout_4.addWidget(self.duration_min)
        self.duration_min_input = QtWidgets.QLineEdit(self.centralWidget)
        self.duration_min_input.setValidator(QtGui.QIntValidator())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.duration_min_input.sizePolicy().hasHeightForWidth())
        self.duration_min_input.setSizePolicy(sizePolicy)
        self.duration_min_input.setObjectName("duration_min_input")
        self.horizontalLayout_4.addWidget(self.duration_min_input)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.duration_max = QtWidgets.QLabel(self.centralWidget)
        self.duration_max.setObjectName("duration_max")
        self.horizontalLayout_6.addWidget(self.duration_max)
        self.duration_max_input = QtWidgets.QLineEdit(self.centralWidget)
        self.duration_max_input.setValidator(QtGui.QIntValidator())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.duration_max_input.sizePolicy().hasHeightForWidth())
        self.duration_max_input.setSizePolicy(sizePolicy)
        self.duration_max_input.setObjectName("duration_max_input")
        self.horizontalLayout_6.addWidget(self.duration_max_input)
        self.verticalLayout.addLayout(self.horizontalLayout_6)

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
        min_duration = self.duration_min_input.text()
        max_duration = self.duration_max_input.text()
        if max_amp and min_amp and int(max_amp) <= int(min_amp):
            self.showDialog("Minimal amplititude cannot be greater or equal to maximal")
        if min_duration and max_duration and int(min_duration) >= int(max_duration):
            self.showDialog("Minimal duration cannot be greater or equal to maximal")
        if (min_duration or max_duration) and not min_amp and not max_amp:
            self.showDialog("Enter amplitude values")
        if not min_duration and not max_duration and (min_amp or max_amp):
            self.plot.filter_amp(min_amp, max_amp)
        if (min_duration or max_duration) and (min_amp or max_amp):
            self.plot.draw_pairs(min_duration, max_duration, min_amp, max_amp)

    def showDialog(self, text):
        msg = QtWidgets.QMessageBox(self.centralWidget)
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(text)
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
        self.duration_min.setText(_translate("MainWindow", "Min duration:"))
        self.duration_max.setText(_translate("MainWindow", "Max duration:"))
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
