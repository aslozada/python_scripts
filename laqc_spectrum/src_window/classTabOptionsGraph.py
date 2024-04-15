# -*- coding: utf-8 -*-
"""
Class Tab Options Graph.

@author: rogerio
"""
from PyQt5 import QtWidgets, QtCore, QtGui


class TabOptionsGraph(QtWidgets.QTabWidget):
    """Class Tab Option Graph."""

    def __init__(self, parent=None):
        """Init class."""
        super().__init__(parent)

        # Creating tabs
        self.tabAxes = QtWidgets.QWidget()
        self.tabLegend = QtWidgets.QScrollArea()

        # Adding widgets in tabs
        self.tabAxesUI()
        self.tabLegendUI()

        # Adding tabs
        self.addTab(self.tabAxes, "Axes")
        self.addTab(self.tabLegend, "Legend")

    def tabAxesUI(self):
        """Widgets in tabAxes."""
        self.axesLayout = QtWidgets.QVBoxLayout()

        # Title
        self.lblTitleWidget = QtWidgets.QWidget()
        self.lblTitleLayout = QtWidgets.QHBoxLayout()
        self.lblTitleWidget.setLayout(self.lblTitleLayout)
        self.lblTitle = QtWidgets.QLabel("Graph title")
        self.edtTitle = QtWidgets.QLineEdit()
        self.edtTitle.setText("Graph title")
        self.lblTitleLayout.addWidget(self.lblTitle)
        self.lblTitleLayout.addWidget(self.edtTitle)

        # GroupBox X-Axis
        self.groupXAxisGrpBox = QtWidgets.QGroupBox("X-Axis")
        self.groupXAxisGrpBox.setObjectName("groupXAxisGrpBox")
        self.groupXAxisLayout = QtWidgets.QGridLayout()
        self.groupXAxisGrpBox.setLayout(self.groupXAxisLayout)
        self.lblXAxis = QtWidgets.QLabel("Label")
        self.edtXAxis = QtWidgets.QLineEdit()
        self.edtXAxis.setObjectName("edtXAxis")
        self.edtXAxis.setText("X")
        self.lblXMinValue = QtWidgets.QLabel("Min")
        self.edtXMinValue = QtWidgets.QLineEdit()
        self.edtXMinValue.setObjectName("editXMinValue")
        self.edtXMinValue.setText('100')
        self.lblXMaxValue = QtWidgets.QLabel("Max")
        self.edtXMaxValue = QtWidgets.QLineEdit()
        self.edtXMaxValue.setObjectName("editXMaxValue")
        self.edtXMinValue.setText('800')

        # GroupBox X-Axis -> adding widgets
        self.groupXAxisLayout.addWidget(self.lblXAxis, 0, 0)
        self.groupXAxisLayout.addWidget(self.edtXAxis, 0, 1)
        self.groupXAxisLayout.addWidget(self.lblXMinValue, 1, 0)
        self.groupXAxisLayout.addWidget(self.edtXMinValue, 1, 1)
        self.groupXAxisLayout.addWidget(self.lblXMaxValue, 2, 0)
        self.groupXAxisLayout.addWidget(self.edtXMaxValue, 2, 1)

        # GroupBox Y-Axis
        self.groupYAxisGrpBox = QtWidgets.QGroupBox("Y-Axis")
        self.groupYAxisGrpBox.setObjectName("groupYAxisGrpBox")
        self.groupYAxisLayout = QtWidgets.QGridLayout()
        self.groupYAxisGrpBox.setLayout(self.groupYAxisLayout)
        self.lblYAxis = QtWidgets.QLabel("Label")
        self.edtYAxis = QtWidgets.QLineEdit()
        self.edtYAxis.setObjectName("edtYAxis")
        self.edtYAxis.setText("Y")
        self.lblYMinValue = QtWidgets.QLabel("Min")
        self.edtYMinValue = QtWidgets.QLineEdit()
        self.edtYMinValue.setObjectName("editYMinValue")
        self.lblYMaxValue = QtWidgets.QLabel("Max")
        self.edtYMaxValue = QtWidgets.QLineEdit()
        self.edtYMaxValue.setObjectName("editYMaxValue")

        # GroupBox Y-Axis -> adding widgets
        self.groupYAxisLayout.addWidget(self.lblYAxis, 0, 0)
        self.groupYAxisLayout.addWidget(self.edtYAxis, 0, 1)
        self.groupYAxisLayout.addWidget(self.lblYMinValue, 1, 0)
        self.groupYAxisLayout.addWidget(self.edtYMinValue, 1, 1)
        self.groupYAxisLayout.addWidget(self.lblYMaxValue, 2, 0)
        self.groupYAxisLayout.addWidget(self.edtYMaxValue, 2, 1)

        # Group Axis Layout
        self.groupAxisWidget = QtWidgets.QWidget()
        self.groupAxisLayout = QtWidgets.QHBoxLayout()
        self.groupAxisWidget.setLayout(self.groupAxisLayout)
        self.groupAxisLayout.addWidget(self.groupXAxisGrpBox)
        self.groupAxisLayout.addWidget(self.groupYAxisGrpBox)

        # Adjust stretch
        self.groupAxisLayout.setStretchFactor(self.groupXAxisGrpBox, 1)
        self.groupAxisLayout.setStretchFactor(self.groupYAxisGrpBox, 1)

        # Adding widgets
        self.axesLayout.addWidget(self.lblTitleWidget)
        self.axesLayout.addWidget(self.groupAxisWidget)

        # Stretch
        self.axesLayout.addStretch()

        # Adding space
        # self.axesLayout.setRowStretch(self.axesLayout.rowCount(), 1)
        # self.axesLayout.setColumnStretch(self.axesLayout.columnCount(), 1)

        self.tabAxes.setLayout(self.axesLayout)

    def tabLegendUI(self):
        """Widgets in tabLegend."""
        self.legendWidget = QtWidgets.QWidget()
        self.legendLayout = QtWidgets.QGridLayout()
        self.legendWidget.setLayout(self.legendLayout)
        self.tabLegend.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tabLegend.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tabLegend.setWidgetResizable(True)
        self.tabLegend.setWidget(self.legendWidget)

    def tabLegendPopulate(self, itensLegend):
        """Create label/edit for legend."""
        # Excluding all widgets
        for i in range(0, self.legendLayout.count()):
            self.legendLayout.itemAt(i).widget().deleteLater()

        # Widgets
        self.listLegends = []
        for i in itensLegend:
            label = QtWidgets.QLabel(i)
            label.setObjectName('lbl' + i)
            edit = QtWidgets.QLineEdit()
            edit.setObjectName(i)
            edit.setText(i)
            self.listLegends.append([label, edit])

        # Adding widgets
        row = 0
        col = 0
        for i in self.listLegends:
            self.legendLayout.addWidget(i[0], row, col)
            self.legendLayout.addWidget(i[1], row, col+1)
            row += 1

        # Adding space
        self.legendLayout.setRowStretch(self.legendLayout.rowCount(), 1)
        # self.legendLayout.setColumnStretch(self.legendLayout.columnCount(), 1)
