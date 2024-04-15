# -*- coding: utf-8 -*-
"""
Class Message Box.

@author: rogerio
"""
from PyQt5 import QtWidgets


class MessageBox(QtWidgets.QMessageBox):
    """
    Show message box.

        Stadard button
        QMessageBox.Ok
        QMessageBox.Open
        QMessageBox.Save
        QMessageBox.Cancel
        QMessageBox.Close
        QMessageBox.Yes
        QMessageBox.No
        QMessageBox.Abort
        QMessageBox.Retry
        QMessageBox.Ignore
    """

    def __init__(self, parent=None):
        """Init class."""
        super().__init__(parent)

    def showInfo(self, title, text):
        """Show info dialog."""
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QtWidgets.QMessageBox.Information)
        self.standard_button = QtWidgets.QMessageBox.Ok
        self.setStandardButtons(self.standard_button)
        return self.execute()

    def showWarning(self, title, text):
        """Show warning dialog."""
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QtWidgets.QMessageBox.Warning)
        self.standard_button = QtWidgets.QMessageBox.Ok
        self.setStandardButtons(self.standard_button)
        return self.execute()

    def showError(self, title, text):
        """Show error dialog."""
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QtWidgets.QMessageBox.Critical)
        self.standard_button = QtWidgets.QMessageBox.Ok
        self.setStandardButtons(self.standard_button)
        return self.execute()

    def showAskYesNo(self, title, text):
        """Show questioning dialog (yes/no)."""
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QtWidgets.QMessageBox.Question)
        self.standard_button = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        self.setStandardButtons(self.standard_button)
        return self.execute()

    def showAskYesNoCancel(self, title, text):
        """Show questiongin dialog (yes/no/cancel)."""
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QtWidgets.QMessageBox.Question)
        self.standard_button = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
        self.setStandardButtons(self.standard_button)
        return self.execute()

    def showAskSave(self, title, text):
        """Show save dialog."""
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QtWidgets.QMessageBox.Question)
        self.standard_button = QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
        self.setStandardButtons(self.standard_button)
        return self.execute()

    def showAskOpen(self, title, text):
        """Show open dialog."""
        self.setWindowTitle(title)
        self.setText(text)
        self.setIcon(QtWidgets.QMessageBox.Question)
        self.standard_button = QtWidgets.QMessageBox.Open | QtWidgets.QMessageBox.No
        self.setStandardButtons(self.standard_button)
        return self.execute()

    def execute(self):
        """Execute dialog."""
        self.exec_()
        msg_returned = str(self.clickedButton().text()).replace('&', '')
        return msg_returned
