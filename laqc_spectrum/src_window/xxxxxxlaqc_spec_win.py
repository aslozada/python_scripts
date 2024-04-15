# -*- coding: utf-8 -*-
"""
Extract excited states and plot data for UV-VIS.

UNIFEI - Universidade Federal de Itajuba.
LaQC - Laboratorio de Quimica Computacional


entries = ['one', 'two', 'three']
model = QtGui.QStandardItemModel()
self.listFiles.setModel(model)

for i in entries:
    item = QtGui.QStandardItem(i)
    model.appendRow(item)


addWidget( widget, 0, 0, 2, 0, Qt::AlignHCenter );
has fromRow = 0, fromColumn = 0, rowSpan = 2 and columnSpan = 0. This
means it starts from row 0 and spans over two rows, i.e. it will be in
row 0 and 1 (Note: Two rows in total, not two additional rows). Also it
starts from column 0 with a span of 0 which I think means the column span
is ignored.


@author: Rogério Ribeiro Macêdo
"""
# pylint: disable=invalid-name
# pylint: disable=import-error
import sys
import os
try:
    from PyQt5 import QtGui, QtWidgets, QtCore
except ImportError as e:
    print('[!] The required Python libraries could not be imported:', file=sys.stderr)
    print(f'\t{e}')
    sys.exit(1)


class MainWindow(QtWidgets.QMainWindow):
    """Class main window."""

    def __init__(self, *args, **kwargs):
        """
        Initializate function of class.

        Parameters
        ----------
        *args : TYPE
            DESCRIPTION.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        super().__init__(*args, **kwargs)

        # Window propertis
        self.setWindowTitle("LaQC Spectrum Window")
        self.setWindowIcon(QtGui.QIcon('images/logo.png'))

        # Menu bar
        self.mainMenuBar()

        # Tool bar
        self.mainToolBar()

        # Status bar
        self.mainStatusBar()

        # Layout window
        self.layoutWindow()

    def layoutWindow(self):
        """
        Layout of window.

        Returns
        -------
        None.

        """
        # Background Window
        self.setAutoFillBackground(True)

        # Core Layout
        self.mainLayout = QtWidgets.QGridLayout()
        self.mainLayout.setObjectName("mainLayout")

        # Frames
        self.leftFrame = QtWidgets.QFrame()
        self.leftFrame.setStyleSheet(".QFrame {padding-top: 5px;padding-bottom: 5px;"
                                     "border:0.5px solid black;}")
        self.leftFrame.setObjectName("leftFrame")
        self.leftFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                     QtWidgets.QSizePolicy.Minimum)

        self.rightFrame = QtWidgets.QFrame()
        self.rightFrame.setObjectName("rightFrame")
        self.rightFrame.setStyleSheet(" .QFrame {padding-top: 5px;padding-bottom: 5px;border:0.5px solid black;}")
        self.rightFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                      QtWidgets.QSizePolicy.Minimum)

        # Adding widgets to lefFrame
        self.addWidgetsLeft()
        self.addWidgetsRight()

        # Adding frames to mainLayout
        self.mainLayout.addWidget(self.leftFrame, 0, 0, 1, 1)
        self.mainLayout.addWidget(self.rightFrame, 0, 1, 1, 1)

        # Initiating window widget
        self.window = QtWidgets.QWidget()
        self.window.setObjectName("window")
        self.window.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                  QtWidgets.QSizePolicy.Minimum)
        self.window.setLayout(self.mainLayout)

        # Central Widget
        self.setCentralWidget(self.window)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                           QtWidgets.QSizePolicy.Minimum)

    def addWidgetsRight(self):
        """
        Adding widgts to right frame.

        Returns
        -------
        None.

        """
        # Grid for widgets
        self.gridRightFrame = QtWidgets.QGridLayout()

        # Widgets
        self.labelOutputFiles = QtWidgets.QLabel("Output file(s)")

        # Add widgets to grid
        self.gridRightFrame.addWidget(self.labelOutputFiles, 0, 0)

        # Add layout to frame
        self.rightFrame.setLayout(self.gridRightFrame)

    def addWidgetsLeft(self):
        """
        Adding widgets to left frame.

        Returns
        -------
        None.

        """
        # Grid for widgets
        self.gridLeftFrame = QtWidgets.QGridLayout()
        self.gridLeftFrame.setObjectName("gridLeftFrame")
        self.gridLeftFrame.setRowMinimumHeight(3, 45)

        # Widgets
        self.labelOutputFiles = QtWidgets.QLabel("Output file(s)")
        self.labelOutputFiles.setObjectName("labelOutputFiles")

        # Horizontal Line
        self.horizontalLine = QtWidgets.QFrame()
        self.horizontalLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.horizontalLine.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLine.setStyleSheet("background: black")

        # List Files
        self.listFiles = QtWidgets.QListWidget()
        self.listFiles.setObjectName("listFiles")

        self.buttonSelectAll = QtWidgets.QPushButton("Select all")
        self.buttonSelectAll.setObjectName("buttonSelectAll")
        self.buttonSelectAll.setStatusTip('Select all the structures')
        self.buttonSelectAll.clicked.connect(self.on_click_selectAll)

        self.buttonUnselectAll = QtWidgets.QPushButton("Unselect all")
        self.buttonUnselectAll.setObjectName("buttonUnselectAll")
        self.buttonUnselectAll.setStatusTip('Unselect all the structures')

        # Group box for average
        self.groupBoxAverage = QtWidgets.QGroupBox("Average")
        self.groupBoxAverage.setStyleSheet(".QGroupBox {padding-top: 15px;padding-bottom: 5px;"
                                           "border:0.5px solid black;}")
        self.radioNone = QtWidgets.QRadioButton("&None")
        self.radioArithmetic = QtWidgets.QRadioButton("&Arithmetic")
        self.radioNone.setChecked(True)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.radioNone)
        self.vbox.addWidget(self.radioArithmetic)
        # self.vbox.addStretch(1)
        self.groupBoxAverage.setLayout(self.vbox)

        self.dataXMenu = QtWidgets.QComboBox()
        self.dataXMenu.addItems(["asdf", "asdfasdfsad", "awerwrwer"])

        # Add widgets to grid
        self.gridLeftFrame.addWidget(self.labelOutputFiles, 0, 0, 1, 2, alignment=QtCore.Qt.AlignTop)
        # self.gridLeftFrame.addWidget(self.horizontalLine, 1, 0, 1, 2, alignment=QtCore.Qt.AlignTop)
        self.gridLeftFrame.addWidget(self.listFiles, 2, 0, 1, 2, alignment=QtCore.Qt.AlignTop)
        self.gridLeftFrame.addWidget(self.buttonSelectAll, 3, 0, 15, 1,
                                     alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.gridLeftFrame.addWidget(self.buttonUnselectAll, 3, 1, 15, 1,
                                     alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
        self.gridLeftFrame.addWidget(self.groupBoxAverage, 4, 0, 1, 2, alignment=QtCore.Qt.AlignTop)
        self.gridLeftFrame.addWidget(self.dataXMenu, 5, 0, 1, 2, alignment=QtCore.Qt.AlignTop)

        # Add layout to frame
        self.leftFrame.setLayout(self.gridLeftFrame)

    def on_click_selectAll(self):
        """
        Select all.

        Returns
        -------
        None.

        """

    def mainMenuBar(self):
        """
        Meke the main menu bar.

        Returns
        -------
        None.

        """
        # Menu bar
        upperMenuBar = self.menuBar()

        # Menu file
        menuFile = upperMenuBar.addMenu("&File")

        # File -> Open
        openAction = QtWidgets.QAction(QtGui.QIcon("images/open.png"), "&Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip("Open file.")
        openAction.triggered.connect(self.selectDataFile)
        menuFile.addAction(openAction)

        # File -> Save
        saveAction = QtWidgets.QAction(QtGui.QIcon("images/save.png"), "&Save", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip("Save file.")
        menuFile.addAction(saveAction)

        # File -> Save as
        save_asAction = QtWidgets.QAction(QtGui.QIcon("images/save_as.png"), "&Save as", self)
        save_asAction.setStatusTip("Save as file.")
        menuFile.addAction(save_asAction)

        # Separator
        menuFile.addSeparator()

        # Exit option (File -> Exit)
        exitAction = QtWidgets.QAction(QtGui.QIcon('images/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+E')
        exitAction.setStatusTip('Exit')
        exitAction.triggered.connect(QtWidgets.qApp.quit)
        menuFile.addAction(exitAction)

        # Menu About
        menuAbout = upperMenuBar.addMenu("&About")

        # About -> Info
        infoAction = QtWidgets.QAction(QtGui.QIcon("images/info.png"), "&Info", self)
        infoAction.setShortcut("Ctrl+i")
        infoAction.setStatusTip("Info about the program.")
        infoAction.triggered.connect(self.aboutWindow)
        menuAbout.addAction(infoAction)

    def mainToolBar(self):
        """
        Make the main tool bar.

        Returns
        -------
        None.

        """
        # Toolbar
        toolbar = QtWidgets.QToolBar('Main toolbar')
        toolbar.setStyleSheet(".QToolBar {padding-top: 7px;padding-bottom: 7px;"
                              "border-bottom:1px solid black;"
                              "color:black;spacing:3px;}")

        # Bottom exit
        exitAction = QtWidgets.QAction(QtGui.QIcon('images/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+E')
        exitAction.setStatusTip('Exit')
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        # Bottom open
        openButtonAction = QtWidgets.QAction(QtGui.QIcon('images/open.png'), 'Open', self)
        openButtonAction.setShortcut('Ctrl+O')
        openButtonAction.setStatusTip('Open asdfsadf')
        openButtonAction.triggered.connect(self.selectDataFile)

        # Bottom save
        saveAction = QtWidgets.QAction(QtGui.QIcon('images/save.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save')
        # saveAction.triggered.connect(self.saveFile)

        # Adding elements
        self.addToolBar(toolbar)
        toolbar.addAction(exitAction)
        toolbar.addSeparator()
        toolbar.addAction(openAction)
        toolbar.addAction(saveAction)

    def mainStatusBar(self):
        """
        Make de main status bar.

        Returns
        -------
        None.

        """
        statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(statusBar)
        statusBar.setStyleSheet("padding-top: 10px;padding-bottom: 10px;border-top:0.5px solid black;"
                                "color:black;")
        # statusBar.showMessage("Are you ready!?")

    def selectDataFile(self):
        """
        Create a window that allows the user to select the file which will be read.

        Returns
        -------
        None.

        """
        openFile = QtWidgets.QFileDialog()
        openFile.setDirectory(os.getcwd())
        openFile.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        openFile.setNameFilter("Log (*.log)")
        openFile.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        if openFile.exec():
            self.selectedFileName = openFile.selectedFiles()
            if self.selectedFileName:
                # Adding files
                entries = self.selectedFileName
                model = QtGui.QStandardItemModel()
                self.listFiles.setModel(model)

                for i in entries:
                    item = QtGui.QStandardItem(i)
                    model.appendRow(item)
        else:
            print("Nao executado")

    def aboutWindow(self):
        """
        Create a pop-up window with information about the interface.

        Returns
        -------
        None.

        """
        infoMessage = QtWidgets.QMessageBox()
        infoMessage.setWindowTitle("About")
        infoMessage.setText("Application written in Python<br/><br/>\
                      Author: Rogério Ribeiro Macêdo<br/>\
                      Institution: Instituto de Física e Química. Chemistry and Physics Institute, University Federal of Itajubá<br/>\
                      Year: 2023 and 2024<br/> \
                      Last Modified data: September 11, 2023")
        infoMessage.setIcon(1)
        infoMessage.exec_()


def main():
    """
    Initialize the window.

    Returns
    -------
    None.

    """
    # Create the Qt Application
    application = QtWidgets.QApplication(sys.argv)
    # application.setFont(QtGui.QFont("Lato", 11, QtGui.QFont.Normal))

    # Create and show the principal window
    mainWindow = MainWindow()
    mainWindow.showMaximized()

    # Run the main Qt loop
    sys.exit(application.exec())


if __name__ == "__main__":
    main()
