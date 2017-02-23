# -*- coding: utf-8 -*-
import sys
import pandas
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure


handata = pandas.read_csv("hanData_1464739200_1464825600.csv")
frames = pandas.read_csv("frames_1464739200_1464825600.csv")
x_handata = handata.Timestamp
y_handata = handata.Value
x_frames = frames.time
y_frames_min = frames.plat[:-1]
y_frames_max = frames.plat[1:]
transisiton_colors = []
for transition in frames.transition[1:]:
    if transition > 0:
        transisiton_colors.append("g")
    elif transition < 0:
        transisiton_colors.append("r")
    else:
        transisiton_colors.append("b")


class Plot(FigureCanvas):
    def __init__(self, parent=None, width=5, height=10, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.mpl_connect("resize_event", self._tight_layout)
        self.build_plot()
        self.setParent(parent)

    def _tight_layout(self, *args, **kwargs):
        self.fig.tight_layout()

    def build_plot(self):
        axes = self.fig.add_subplot(111)
        axes.plot(x_handata, y_handata, "b")
        axes.vlines(x_frames, y_frames_min, y_frames_max, colors=transisiton_colors)
        axes.set_xlabel("timestamps")
        axes.set_ylabel("amplitude")
        axes.grid(color="grey", linestyle="dotted", linewidth=0.25)
        self._tight_layout()


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
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.min_amp = QtWidgets.QLabel(self.centralWidget)
        self.min_amp.setObjectName("min_amp")
        self.horizontalLayout_2.addWidget(self.min_amp)
        self.min_amp_val = QtWidgets.QLabel(self.centralWidget)
        self.min_amp_val.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.min_amp_val.setObjectName("min_amp_val")
        self.horizontalLayout_2.addWidget(self.min_amp_val)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.max_amp = QtWidgets.QLabel(self.centralWidget)
        self.max_amp.setObjectName("max_amp")
        self.horizontalLayout_3.addWidget(self.max_amp)
        self.max_amp_val = QtWidgets.QLabel(self.centralWidget)
        self.max_amp_val.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.max_amp_val.setObjectName("max_amp_val")
        self.horizontalLayout_3.addWidget(self.max_amp_val)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.min_dur = QtWidgets.QLabel(self.centralWidget)
        self.min_dur.setObjectName("min_dur")
        self.horizontalLayout_4.addWidget(self.min_dur)
        self.max_dur_val_2 = QtWidgets.QLabel(self.centralWidget)
        self.max_dur_val_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.max_dur_val_2.setObjectName("max_dur_val_2")
        self.horizontalLayout_4.addWidget(self.max_dur_val_2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.max_dur = QtWidgets.QLabel(self.centralWidget)
        self.max_dur.setObjectName("max_dur")
        self.horizontalLayout_5.addWidget(self.max_dur)
        self.max_dur_val = QtWidgets.QLabel(self.centralWidget)
        self.max_dur_val.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.max_dur_val.setObjectName("max_dur_val")
        self.horizontalLayout_5.addWidget(self.max_dur_val)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.prev_day_button.raise_()
        self.next_day_button.raise_()
        self.save_button.raise_()
        self.min_amp_val.raise_()
        self.min_amp.raise_()
        self.plot.raise_()
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
        MainWindow.addToolBar(self.plot_toolbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TaggerTool"))
        self.prev_day_button.setText(_translate("MainWindow", "Previous day"))
        self.save_button.setText(_translate("MainWindow", "Save"))
        self.next_day_button.setText(_translate("MainWindow", "Next day"))
        self.min_amp.setText(_translate("MainWindow", "Min amp:"))
        self.min_amp_val.setText(_translate("MainWindow", "TextLabel"))
        self.max_amp.setText(_translate("MainWindow", "Max amp:"))
        self.max_amp_val.setText(_translate("MainWindow", "TextLabel"))
        self.min_dur.setText(_translate("MainWindow", "Min duration:"))
        self.max_dur_val_2.setText(_translate("MainWindow", "TextLabel"))
        self.max_dur.setText(_translate("MainWindow", "Max duration:"))
        self.max_dur_val.setText(_translate("MainWindow", "TextLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "&File"))
        self.menuAbout.setTitle(_translate("MainWindow", "Abo&ut"))
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
