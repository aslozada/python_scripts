# -*- coding: utf-8 -*-
"""
Extract excited states and plot data for UV-VIS.

UNIFEI - Universidade Federal de Itajuba.
LaQC - Laboratorio de Quimica Computacional

Author.....: Rogério Ribeiro Macêdo
Last update: 29/09/2023

"""
# pylint: disable=invalid-name
# pylint: disable=import-error
import sys
try:
    from PyQt5 import QtGui, QtWidgets, QtCore
    from pathlib import Path
    import os
    import platform
    import math
    import numpy as np
    import matplotlib
    matplotlib.use('Qt5Agg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

    # Classes use in this project
    import classMessageBox
    import classTabOptionsGraph
except ImportError as e:
    print('[!] The required Python libraries could not be imported:', file=sys.stderr)
    print(f'\t{e}')
    sys.exit(1)

# Constants
A = 1.30629744736E8
FACT1 = 1.0E7
FACT2 = 1.0E0
SIGMA = 3099.6
MSG_TITLE = "LaQC Spectrum"

typeFit = ['Gaussian', 'Lorentzian']


class mplCustomizedToolbar(NavigationToolbar):
    """Modify the default matplotlib toolbar."""

    # Button that will appear in toolbar
    toolitems = [
        t for t in NavigationToolbar.toolitems
        if t[0] in ('Home', 'Pan', 'Zoom', 'Save')
    ]

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super(mplCustomizedToolbar, self).__init__(*args, **kwargs)
        self.layout().takeAt(4)


class MplCanvas(FigureCanvas):
    """Class that create."""

    def __init__(self, parent=None, width=9.0, height=6.0, dpi=72):
        """Initialize the class."""
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class MainWindow(QtWidgets.QMainWindow):
    """Class main window."""

    def __init__(self):
        """
        Class init.

        Returns
        -------
        None.

        """
        super().__init__()

        # Message box
        self.msgbox = classMessageBox.MessageBox()

        self.initUI()

    def initUI(self):
        """
        Widgets init.

        Returns
        -------
        None.

        """
        # Propriedades da jenala
        self.setWindowTitle("LaQC Spectrun")
        self.setWindowIcon(QtGui.QIcon('images/logo_laqc.jpg'))

        # Menu bar
        self.mainMenuBar()

        # Tool bar
        self.mainToolBar()

        # Status bar
        self.mainStatusBar()

        # window layout
        self.windowLayout()

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
        menuFile.setStyleSheet("QMenu {icon-size: 32px;}")

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

    def selectDataFile(self):
        """
        Create a window that allows the user to select the file which will be read.

        Returns
        -------
        None.

        """
        # File dialog
        openFile = QtWidgets.QFileDialog()
        openFile.setDirectory(os.getcwd())
        openFile.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        openFile.setNameFilter("Log (*.log)")
        openFile.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        if openFile.exec():
            self.selectedFileName = openFile.selectedFiles()
            if self.selectedFileName:
                # Getting file
                entries = self.selectedFileName

                for i in entries:
                    # Adjusting the separator
                    i = self.selectedFileName = QtCore.QDir.toNativeSeparators(i)

                    # Search if the entry exist in the list
                    match_itens = self.listFiles.findItems(i, QtCore.Qt.MatchContains)

                    # If item is not in the list add it.
                    if len(match_itens) == 0:
                        item = QtWidgets.QListWidgetItem(i)
                        self.listFiles.addItem(item)

            # Select first item
            self.current_item_row = 0
            self.listFiles.setCurrentRow(0)
            self.current_item = self.listFiles.currentItem().text()

    def mainToolBar(self):
        """
        Make the main tool bar.

        Returns
        -------
        None.

        """
        # Toolbar
        toolbar = QtWidgets.QToolBar('Main toolbar')
        toolbar.setStyleSheet(".QToolBar {padding-top: 27px;padding-bottom: 27px;"
                              "border-bottom:1px solid black;"
                              "color:black;spacing:5px;}")
        toolbar.setFloatable(False)
        toolbar.setMovable(False)
        toolbar.setIconSize(QtCore.QSize(32, 32))

        # Bottom exit
        exitAction = QtWidgets.QAction(QtGui.QIcon('images/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+E')
        exitAction.setStatusTip('Exit')
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        # Bottom open
        openAction = QtWidgets.QAction(QtGui.QIcon('images/open.png'), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open')
        openAction.triggered.connect(self.selectDataFile)

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
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("padding-top: 5px;padding-bottom: 5px;border-top:0.5px solid black;"
                                     "color:black;")
        self.statusBar.showMessage("Ready!?")

    def windowLayout(self):
        """
        Windows Layout.

        Returns
        -------
        None.

        """
        # Principal
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setObjectName("mainLayout")

        # Frames
        self.setLeftFrame()
        self.setRightFrame()

        # Adding frames to mainLayout
        self.mainLayout.addWidget(self.leftFrame)
        self.mainLayout.addWidget(self.rightFrame)
        self.mainLayout.setStretchFactor(self.leftFrame, 1)
        self.mainLayout.setStretchFactor(self.rightFrame, 1)

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

    def get_separador(self):
        """
        Captura o separador de caminho de acordo com o sistema operacional.

        Returns
        -------
        separador : string
            Caracter separador.
        """
        separador = "/"
        sistema_operacional = platform.system()
        if sistema_operacional == 'Linux':
            separador = "/"
        else:
            separador = "\\"

        return separador

    def setLeftFrame(self):
        """Left Frame."""
        # Frame
        self.leftFrame = QtWidgets.QFrame()
        self.leftFrame.setObjectName("leftFrame")
        self.leftFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                     QtWidgets.QSizePolicy.Minimum)

        # Layout frame
        self.boxLeftLayout = QtWidgets.QVBoxLayout()
        self.boxLeftLayout.setObjectName("boxLeftLayout")

        # Widgets

        # List files and buttons
        self.listFilesFrame = QtWidgets.QGroupBox("Output file(s)")
        self.listFilesFrame.setObjectName("listFilesFrame")
        self.listFilesGrid = QtWidgets.QGridLayout()

        self.listFiles = QtWidgets.QListWidget()
        self.listFiles.setObjectName("listFiles")
        self.listFiles.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listFiles.clicked.connect(self.listfiles_clicked)
        self.listFiles.itemSelectionChanged.connect(self.selectionChanged)
        self.listFiles.addItem("C:\\Users\\rogerio\\Documents\\dados_debora\\poptd_cargatddft_mc_20000160.log")
        # self.listFiles.addItem(r"C:\Users\rogerio\Documents\dados_debora\poptd_cargatddft_mc_20000240.log")
        # self.listFiles.addItem(r"C:\Users\rogerio\Documents\dados_debora\poptd_cargatddft_mc_20000800.log")
        self.listFilesGrid.addWidget(self.listFiles, 0, 0, 5, 1)

        self.btnSelectAll = QtWidgets.QPushButton("Select all")
        self.btnSelectAll.setObjectName("btnSelectAll")
        self.btnSelectAll.setStatusTip('Select all the structures')
        self.btnSelectAll.clicked.connect(self.on_click_selectAll)

        self.btnUnselect = QtWidgets.QPushButton("Unselect")
        self.btnUnselect.setObjectName("btnUnselect")
        self.btnUnselect.setStatusTip('Select all the structures')
        self.btnUnselect.clicked.connect(self.on_click_unselectAll)

        self.btnDelete = QtWidgets.QPushButton("Delete")
        self.btnDelete.setObjectName("btnDelete")
        self.btnDelete.setStatusTip('Delete the selected item')
        self.btnDelete.clicked.connect(self.on_click_delete)

        self.btnCalculate = QtWidgets.QPushButton("Calculate")
        self.btnCalculate.setObjectName("btnCalculate")
        self.btnCalculate.setStatusTip('Calculate the UV-VIS spectrum')
        self.btnCalculate.clicked.connect(self.on_click_calculate)

        self.listFilesGrid.addWidget(self.btnSelectAll, 0, 1)
        self.listFilesGrid.addWidget(self.btnUnselect, 1, 1)
        self.listFilesGrid.addWidget(self.btnDelete, 2, 1)
        self.listFilesGrid.addWidget(self.btnCalculate, 4, 1)

        self.listFilesGrid.setColumnStretch(0, 6)
        self.listFilesGrid.setColumnStretch(1, 1)

        self.listFilesFrame.setLayout(self.listFilesGrid)

        # UV-Vis Options and Type of Average
        self.optionsUVAvgWid = QtWidgets.QFrame()
        self.optionsUVAvgWid.setObjectName("optionsUVAvgWid")
        self.optionsUVAvgLay = QtWidgets.QHBoxLayout()
        self.optionsUVAvgLay.setSpacing(4)  # Space between cells
        self.optionsUVAvgLay.setContentsMargins(0, 0, 0, 0)  # Margins
        self.optionsUVAvgWid.setLayout(self.optionsUVAvgLay)

        # UV-Vis Options and Type of Average -> UV-Vis Options
        self.optUVVis = QtWidgets.QGroupBox("UV-Vis options")
        self.optUVVis.setObjectName("optUVVis")
        self.optUVVisGrid = QtWidgets.QGridLayout()
        self.optUVVis.setLayout(self.optUVVisGrid)
        self.lblTypeFit = QtWidgets.QLabel("Type of fit")
        self.combTypeFit = QtWidgets.QComboBox()
        self.combTypeFit.addItems(typeFit)
        self.lblWaveNumb = QtWidgets.QLabel("Wave numbers")
        self.lblWaveInte = QtWidgets.QLabel("Wave intervals")
        self.edtWaveFrom = QtWidgets.QLineEdit()
        self.edtWaveFrom.setText("100")
        self.edtWaveFrom.setInputMask("900")
        self.lblTo = QtWidgets.QLabel("to")
        self.edtWaveTo = QtWidgets.QLineEdit()
        self.edtWaveTo.setText("800")
        self.edtWaveTo.setInputMask("900")
        self.edtInterval = QtWidgets.QLineEdit()
        self.edtInterval.setText("0.5")
        self.edtInterval.setInputMask("9.00")
        self.optUVVisGrid.addWidget(self.lblTypeFit, 0, 0, 1, 1)
        self.optUVVisGrid.addWidget(self.combTypeFit, 0, 1, 1, 2)
        self.optUVVisGrid.addWidget(self.lblWaveNumb, 1, 0, 1, 3)
        self.optUVVisGrid.addWidget(self.lblWaveInte, 1, 3, 1, 1)
        self.optUVVisGrid.addWidget(self.edtWaveFrom, 2, 0)
        self.optUVVisGrid.addWidget(self.lblTo, 2, 1)
        self.optUVVisGrid.addWidget(self.edtWaveTo, 2, 2)
        self.optUVVisGrid.addWidget(self.edtInterval, 2, 3)

        # UV-Vis Options and Type of Average -> Type of Average
        self.groupAverage = QtWidgets.QGroupBox("Type of average")
        self.groupAverage.setObjectName("groupAverage")
        self.groupAverageLayout = QtWidgets.QVBoxLayout()
        self.groupAverage.setLayout(self.groupAverageLayout)
        self.radioButtonNone = QtWidgets.QRadioButton("None")
        self.radioButtonArith = QtWidgets.QRadioButton("Arithmetic")
        self.groupAverageLayout.addWidget(self.radioButtonNone)
        self.groupAverageLayout.addWidget(self.radioButtonArith)
        self.radioButtonArith.setChecked(True)
        self.optionsUVAvgLay.addWidget(self.optUVVis)
        self.optionsUVAvgLay.addWidget(self.groupAverage)
        self.optionsUVAvgLay.setStretchFactor(self.optUVVis, 1)
        self.optionsUVAvgLay.setStretchFactor(self.groupAverage, 1)

        # Tab Options Axes
        self.tabOptAxes = classTabOptionsGraph.TabOptionsGraph()
        self.tabOptAxes.setEnabled(False)

        # Botton Update
        self.btnUpdate = QtWidgets.QPushButton("Update")
        self.btnUpdate.setObjectName("btnUpdate")
        self.btnUpdate.setEnabled(False)
        self.btnUpdate.setStatusTip('Update graph')
        self.btnUpdate.clicked.connect(self.on_click_update)

        # Adding widgets
        self.boxLeftLayout.addWidget(self.listFilesFrame)
        self.boxLeftLayout.addWidget(self.optionsUVAvgWid)
        self.boxLeftLayout.addWidget(self.tabOptAxes)
        # self.boxLeftLayout.addWidget(self.groupOptionsAxes)

        # Add a spacer
        # self.boxLeftLayout.addStretch()

        # Adding button update
        self.boxLeftLayout.addWidget(self.btnUpdate)

        # Adding layout to frame
        self.leftFrame.setLayout(self.boxLeftLayout)

    def verify_waves(self):
        """
        Verify if values of waves and interval are valid.

        Returns
        -------
        validation : bool
            True, correct values.
            False, incorrect values.
        """
        validation = True
        try:
            wave_from = int(self.edtWaveFrom.text().strip())
            wave_to = int(self.edtWaveTo.text().strip())
            interval = float(self.edtInterval.text().strip())
            if wave_to <= wave_from:
                validation = False
            if interval <= 0.0:
                validation = False
        except ValueError:
            validation = False

        return validation

    def on_click_calculate(self):
        """Calculate UV-VIS."""
        if len(self.listFiles.selectedItems()) >= 1:
            if self.verify_waves():
                # List of select files
                log_files = [i.text() for i in self.listFiles.selectedItems()]

                # Extract data from gaussian (make input.dat)
                self.extract_data_gaussian(log_files)

                # Wave and interval waves
                wave_numbers_interval = float(self.edtInterval.text())
                wave_numbers = list(np.arange(int(self.edtWaveFrom.text().strip()),
                                              int(self.edtWaveTo.text().strip())+1,
                                              wave_numbers_interval))

                # Type of Average
                type_of_average = 'Arithmetic'
                for radioButton in self.groupAverage.findChildren(QtWidgets.QRadioButton):
                    if radioButton.isChecked():
                        type_of_average = radioButton.text()

                # Fit gaussian
                dataX, dataY, dataLegends = self.fit_gaussian(type_of_average, wave_numbers)
                self.listLegends = [dataLegends[i] for i in dataLegends]
                self.dataLegends = dataLegends
                self.dataX = dataX
                self.dataY = dataY

                # Adjust widgets that specific limits for x and y axis
                min_y = 0
                max_y = 0
                for i in range(0, len(dataX)):
                    # Ploting data
                    if min_y > min(dataY[i]):
                        min_y = min(dataY[i])
                    if max_y < max(dataY[i]):
                        max_y = max(dataY[i])

                self.tabOptAxes.edtXMinValue.setText(str(int(min(self.dataX[0]))))
                self.tabOptAxes.edtXMaxValue.setText(str(int(max(self.dataX[0]))))
                self.tabOptAxes.edtYMinValue.setText(str(round(min_y)))
                self.tabOptAxes.edtYMaxValue.setText(str(round(max_y)))

                # Plot data in graph
                self.plot(dataX, dataY, self.listLegends)

                # Enabled options
                self.tabOptAxes.setEnabled(True)

                # Info about legends
                self.info_about_legends()
                self.tabOptAxes.tabLegendPopulate(self.listLegends)

                self.btnUpdate.setEnabled(True)
            else:
                self.msgbox.showError(MSG_TITLE, "Verify values of waves and interval.")
        else:
            self.msgbox.showInfo(MSG_TITLE, "Select some file to be calculated.")

    def info_about_legends(self):
        """Info about legends."""
        # Make a list of all legends present in the graph
        legends = [self.canvas.axes.get_legend()]
        # Dict of all legends present in the graph
        self.dict_legends = {'Legends': dict()}
        for i, legend in enumerate(legends):
            dict_legend = dict()
            for j, obj in enumerate(legend.get_texts()):
                dict_obj = dict()
                dict_fp = dict()
                text = obj.get_text()
                position = obj.get_position()
                color = obj.get_color()
                dict_obj.update({'Text': text,
                                 'Position': tuple(position),
                                 'Color': color})
                obj_fp = obj.get_font_properties()
                dict_fp.update({'Font_Name': obj_fp.get_name()})
                fontconfig_pattern = obj_fp.get_fontconfig_pattern()
                font_properties = str.split(fontconfig_pattern, ":")
                for fp in font_properties:
                   if len(fp.split("=")) > 1:
                       if not (fp.strip() == ''):
                           key, value = fp.split("=")
                           dict_fp.update({str.title(key): value})
                dict_fp.update({'fontconfig_pattern': fontconfig_pattern})
                dict_obj.update({'Font_Properties': dict_fp})
                dict_legend.update({'Text_Object_{}'.format(j+1): dict_obj})
            self.dict_legends['Legends'].update({'Legend_{}'.format(i): {'Legend_Object': legend,
                                                                         'Contents': dict_legend}})
        print(self.dict_legends)

    def get_name_file(self, log_file):
        """Return the file name."""
        pos_log = log_file.index(".log")
        name_file = ""
        for i in range(pos_log, 0, -1):
            if log_file[i] == self.get_separador():
                name_file = log_file[i+1:pos_log]
                break

        return name_file

    def get_name_files(self, log_files):
        """Return the files name."""
        listLegends = []
        for log in log_files:
            pos_log = log.index(".log")
            for i in range(pos_log, 0, -1):
                if log[i] == self.get_separador():
                    listLegends.append(log[i+1:pos_log])
                    break

        return listLegends

    def plot(self, dataX, dataY, dataLegend):
        """Plot data graph."""
        # discards the old graph
        self.canvas.axes.clear()

        for i in range(0, len(dataX)):
            self.canvas.axes.plot(dataX[i],
                                  dataY[i],
                                  linewidth='1.5',
                                  label=dataLegend[i])

        # font2 = {'family':'serif','color':'darkred','size':12}
        # prop = {'ylabel': self.tabOptAxes.edtYAxis.text().strip(),
        #         'xlabel': self.tabOptAxes.edtXAxis.text().strip(),
        #         'title': self.tabOptAxes.edtTitle.text().strip()
        #         }
        # self.canvas.axes.update(prop)
        self.canvas.axes.set_title(self.tabOptAxes.edtTitle.text().strip(),
                                   pad=20,
                                   fontdict={'size': 14})
        self.canvas.axes.set_xlabel(self.tabOptAxes.edtXAxis.text().strip(),
                                    labelpad=20,
                                    fontdict={'size': 14})
        self.canvas.axes.set_xlim(int(self.tabOptAxes.edtXMinValue.text()),
                                  int(self.tabOptAxes.edtXMaxValue.text()))
        self.canvas.axes.set_ylabel(self.tabOptAxes.edtYAxis.text().strip(),
                                    labelpad=20,
                                    fontdict={'size': 14})
        self.canvas.axes.set_ylim(int(self.tabOptAxes.edtYMinValue.text()),
                                  int(self.tabOptAxes.edtYMaxValue.text()))
        # self.canvas.axes.update()

        # Config legend
        self.canvas.axes.legend(title='Legend',
                                title_fontsize='medium',
                                fontsize='medium',
                                alignment='center',
                                edgecolor='black',
                                fancybox=True,
                                prop={'size': 11},
                                frameon=False)

        # refresh canvas
        self.canvas.draw()

    def on_click_update(self):
        """Update options."""
        try:
            # Verify limits
            int(self.tabOptAxes.edtXMinValue.text())
            int(self.tabOptAxes.edtYMinValue.text())
            float(self.tabOptAxes.edtYMinValue.text())
            float(self.tabOptAxes.edtYMaxValue.text())

            # Legends
            for i in range(0, self.tabOptAxes.legendLayout.count()):
                if isinstance(self.tabOptAxes.legendLayout.itemAt(i).widget(), QtWidgets.QLineEdit):
                    obj_name = self.tabOptAxes.legendLayout.itemAt(i).widget().objectName()
                    obj_text = self.tabOptAxes.legendLayout.itemAt(i).widget().text()
                    self.dataLegends[obj_name] = obj_text

            self.listLegends = [self.dataLegends[i] for i in self.dataLegends]
            self.plot(self.dataX, self.dataY, self.listLegends)
        except ValueError:
            self.msgbox.showError(MSG_TITLE, "Verify limits of axis")

    def on_click_delete(self):
        """Delete the selected item."""
        if len(self.listFiles.selectedItems()) >= 1:
            for item in self.listFiles.selectedItems():
                self.listFiles.takeItem(self.listFiles.row(item))

    def listfiles_clicked(self):
        """List view clicked."""
        self.current_item_row = self.listFiles.currentRow()
        self.current_item = self.listFiles.currentItem().text()

    def selectionChanged(self):
        """List view changed selection."""
        try:
            # Necessary to the last item
            if self.listFiles.count() > 0:
                self.current_item = self.listFiles.currentItem().text()
        except AttributeError:
            pass

    def on_click_unselectAll(self):
        """
        Select all.

        Returns
        -------
        None.

        """
        self.listFiles.clearSelection()
        self.current_item = ""
        self.current_item_row = -1

        # Unabled options
        self.groupAverage.setEnabled(False)

        # Clear data from graph
        self.canvas.axes.cla()

        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def on_click_selectAll(self):
        """
        Select all.

        Returns
        -------
        None.

        """
        self.listFiles.selectAll()
        self.current_item = ""
        self.current_item_row = -1

    def setRightFrame(self):
        """Right Frame."""
        # Frame
        self.rightFrame = QtWidgets.QFrame()
        self.rightFrame.setObjectName("rightFrame")
        self.rightFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                      QtWidgets.QSizePolicy.Minimum)

        # Layout
        self.boxRightLayout = QtWidgets.QVBoxLayout()
        self.boxRightLayout.setObjectName("boxRightLayout")

        # Matplotlib graph
        self.mplGraphFrame = QtWidgets.QWidget()
        self.canvas = MplCanvas(self, width=5, height=4, dpi=72)
        self.cid = self.canvas.fig.canvas.mpl_connect('button_press_event',
                                                      self.clickIntegral)
        # self.mplToolbar = mplCustomizedToolbar(self.canvas, self.mplGraphFrame)
        self.mplToolbar = NavigationToolbar(self.canvas, self.mplGraphFrame)
        self.current_item_row = -1
        self.current_item = ""

        # self.mplToolbar = NavigationToolbar(self.canvas, self.mplGraphFrame)

        # Adding widgets
        self.boxRightLayout.addWidget(self.mplToolbar)
        self.boxRightLayout.addWidget(self.canvas)

        # Adding layout to frame
        self.rightFrame.setLayout(self.boxRightLayout)

    def clickIntegral(self, event):
        """When click on graph."""
        print("clickIntegral")

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
                      Institution: Chemistry and Physics Institute, University Federal of Itajubá<br/>\
                      Year: 2022 and 2023<br/> \
                      Last Modified data: September 29, 2023")
        infoMessage.setIcon(1)
        infoMessage.exec_()

    def fit_gaussian(self, type_of_average, wave_numbers):
        """
        Ajuste gaussian.

        Parameters
        ----------
        type_of_average : TYPE
            DESCRIPTION.
        wave_numbers : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        average = {}
        dataX = []
        dataY = []
        dataLegend = {}

        try:
            f_spectrum_gaussian = open("spectrum_gaussian.dat", "w")

            with open("input.dat", "r") as f_input:
                m_valor = int(f_input.readline())
                n_valor = [int(i) for i in f_input.readline().split(" ")]
                files_name = [i for i in f_input.readline().split(" ")]

                maxn = max(n_valor)
                eigenvalue = [[0.0]*maxn for i in np.arange(0, m_valor)]
                strength = [[0.0]*maxn for i in np.arange(0, m_valor)]

                for j in range(0, m_valor):
                    for i in range(0, n_valor[j]):
                        read_line = f_input.readline()
                        if (read_line.strip()) != "":
                            values = [float(i) for i in read_line.split("  ")]
                            eigenvalue[j][i] = values[0]
                            strength[j][i] = values[1]
            f_input.close()

            for j in range(0, m_valor):
                valorX = []
                valorY = []

                for nm_valor in wave_numbers:
                    spectrum = 0.0
                    for i in range(0, n_valor[j]):
                        if type_of_average == 'Arithmetic':
                            spectrum = spectrum + A * \
                                (strength[j][i] / (FACT1/SIGMA)) * math.exp(-(((1.0/nm_valor) -
                                                                               (1.0/eigenvalue[j][i]))/(FACT2/SIGMA))**2)

                    f_spectrum_gaussian.write(f"{nm_valor:<4f}   {spectrum:>6.10f}\n")
                    valorX.append(nm_valor)
                    valorY.append(spectrum)

                    if nm_valor in average:
                        average[nm_valor] = average[nm_valor] + spectrum
                    else:
                        average[nm_valor] = spectrum

                f_spectrum_gaussian.write("\n")
                dataX.append(valorX)
                dataY.append(valorY)

                # Get the name of a log file was just calculated
                dataLegend[self.get_name_file(files_name[j])] = self.get_name_file(files_name[j])

            f_spectrum_gaussian.close()

            # Calculating and saving average
            if type_of_average == 'Arithmetic':
                for key in average.keys():
                    average[key] = average[key] / m_valor

            with open("average_spectrum.dat", "w") as f_average:
                for key, value in average.items():
                    f_average.write(f"{key:<4f}   {value:>6.10f}\n")
            f_average.close()
            # print("Arquivo average_spectrum.dat gerado!")

            return dataX, dataY, dataLegend
        except OSError as msg_err:
            print(f"Erro: {msg_err}")
        except ZeroDivisionError:
            print(f"Divisão por zero: {A} * ({strength[j][i]} / "
                  "({fact1}/{sigma})) * math.exp(-(((1.0/{nm})-"
                  "(1.0/{eigenvalue[j][i]}))/({fact2}/{sigma}))**2)")

    def extract_data_gaussian(self, list_log):
        """
        Extraindo dados de estados excitados no arquivo de saída do Gaussian.

        Returns
        -------
        None.

        """
        excited_states = []
        list_num_excited_state = []
        try:
            # Extracting data
            for log in list_log:

                self.statusBar.showMessage(f" - Extraindo estado excitado do arquivo: {log}")

                # if normal_termination(local_log):
                num_excited_state = 0
                with open(log, "r") as f_arquivo:

                    secao_encontrada = False

                    for line in f_arquivo:
                        txt_linha = line.strip()

                        if txt_linha.startswith("(Enter /scr/programs/g09/l914.exe)"):
                            secao_encontrada = True
                        else:
                            if txt_linha.startswith("Leave Link") and secao_encontrada:
                                break

                        if secao_encontrada:
                            if txt_linha.startswith("Excited State"):
                                num_excited_state = num_excited_state + 1

                                # restante da linha
                                restante = txt_linha.split(":")[1]

                                resto = []
                                for i in restante.split(" "):
                                    if i != "":
                                        resto.append(i)
                                comprimento_onda = resto[3]
                                forca_oscilador = resto[5].replace("f=", "")
                                excited_states.append([comprimento_onda, forca_oscilador])

                    list_num_excited_state.append(num_excited_state)
                    f_arquivo.close()

            # Saving data
            f_input = open("input.dat", "w")
            f_input.write(f"{len(list_log):<4d}\n")
            f_input.write(f'{" ".join(str(i) for i in list_num_excited_state)}\n')

            # Name for files log
            f_input.write(f'{" ".join(i for i in list_log)}\n')

            for item in excited_states:
                f_input.write(f'{"  ".join(str(i) for i in item)}\n')
            f_input.close()
            self.statusBar.showMessage("")
        except OSError as msg_err:
            self.msgbox.showError(MSG_TITLE, msg_err)
            # print(f" + Erro: {msg_err}")


def main(exist_style=True):
    """
    Principal function.

    Returns
    -------
    None.

    """
    # Create the Qt Application
    application = QtWidgets.QApplication(sys.argv)

    if exist_style:
        application.setStyleSheet(Path('styles.qss').read_text())
    else:
        print("File 'styles.qss' dont's exist. Using standard styles.")

    # Create and show the principal window
    mainWindow = MainWindow()
    mainWindow.showMaximized()

    # Run the main Qt loop
    sys.exit(application.exec())


if __name__ == "__main__":
    main(Path('styles.qss').exists())
