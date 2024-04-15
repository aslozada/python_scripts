# -*- coding: utf-8 -*-
"""
UNIFEI - Universidade Federal de Itajuba.

LaQC - Laboratorio de Quimica Computacional

Permite modificações em lote dos arquivos de input do Gaussian

Autor............: Rogério Ribeiro Macêdo
Criado em........: 17 de dezembro de 2022
Última alteração.: 27 de setembro de 2023

Versão 0.4

Observações:

    1) type_section: indica a seção do arquivo de entrada (input) que está sendo lida:
        - https://gaussian.com/input/#:~:text=The%20basic%20structure%20of%
        20a,options%20(blank%20line%20terminated)
"""
# pylint: disable=invalid-name
# pylint: disable=import-error
import sys
try:
    from PyQt5 import QtGui, QtWidgets, QtCore
    import platform
    import os
    from pathlib import Path
    import argparse
except ImportError as e:
    print('[!] As bibliotecas Python necessárias não puderam ser importadas:', file=sys.stderr)
    print(f'\t{e}')
    sys.exit(1)

# Tamanho da linha de texto no prompt de comando
TAM_TEXTO = 45


class MainWindow(QtWidgets.QMainWindow):
    """Class main window."""

    def __init__(self):
        """
        Inicializa a classe.

        Returns
        -------
        None.

        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Inicializa widgets.

        Returns
        -------
        None.

        """
        # Propriedades da jenala
        self.setWindowTitle("LaQC Mod Window")
        self.setWindowIcon(QtGui.QIcon('imagens/logo_laqc.jpg'))
        self.resize(550, 250)
        self.centralizar()

        # Barra de menu
        self.barraMenu()

        # Barra de status
        self.barraStatus()

        # Usar ou não o arquivo de configuração
        if self.usar_config():
            self.buscarArqConf()
            if self.arq_conf:
                self.dict_alteracoes = ler_arq_conf(self.arq_conf[0])
            else:
                print('Não escolheu')

        # Layout window
        self.layoutWindow()

    def layoutWindow(self):
        """
        Contruindo o layout da janela.

        Returns
        -------
        None.

        """
        # Principal
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setObjectName("mainLayout")

        # Frames
        self.setParametrosFrame()
        self.setCamadasFrame()
        self.setFreezeFrame()

        # Adding frames to mainLayout
        self.mainLayout.addWidget(self.parametrosFrame)
        self.mainLayout.addWidget(self.camadasFrame)
        self.mainLayout.addWidget(self.freezeFrame)

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

    def setFreezeFrame(self):
        """Configura o frame de 'freeze'."""
        self.freezeFrame = QtWidgets.QFrame()
        self.freezeFrame.setStyleSheet(".QFrame {padding-top: 5px;padding-bottom: 5px;"
                                       "border:0.5px solid black;}")
        self.freezeFrame.setObjectName("freezeFrame")
        self.freezeFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                       QtWidgets.QSizePolicy.Minimum)

    def setCamadasFrame(self):
        """Configura o frame de camadas."""
        self.camadasFrame = QtWidgets.QFrame()
        self.camadasFrame.setStyleSheet(".QFrame {padding-top: 5px;padding-bottom: 5px;"
                                        "border:0.5px solid black;}")
        self.camadasFrame.setObjectName("camadasFrame")
        self.camadasFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                        QtWidgets.QSizePolicy.Minimum)

    def setParametrosFrame(self):
        """Configura o frame de parâmetros."""
        # Frame
        self.parametrosFrame = QtWidgets.QFrame()
        self.parametrosFrame.setStyleSheet(".QFrame {padding-top: 5px;padding-bottom: 5px;"
                                           "border:0.5px solid black;}")
        self.parametrosFrame.setObjectName("parametrosFrame")
        self.parametrosFrame.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Minimum)

        # Layout
        self.gridParamFrame = QtWidgets.QGridLayout()
        self.gridParamFrame.setObjectName("gridParamFrame")

        # Widgets
        self.labelOriArq = QtWidgets.QLabel("Local de origem dos arquivos")
        self.editOriArq = QtWidgets.QTextEdit()

        # Adicionando widgets ao grid
        self.gridParamFrame.addWidget(self.labelOriArq, 0, 0, 1, 1, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
        self.gridParamFrame.addWidget(self.editOriArq, 0, 1, 1, 1, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
        
        # Adicionando layout ao frame
        self.parametrosFrame.setLayout(self.gridParamFrame)

    def buscarArqConf(self):
        """
        Diálogo para buscar arquivo de <arquivo>.conf.

        Returns
        -------
        None.

        """
        # Caminho e nome do arquivo de <arquivo>.conf
        arquivo = ""
        self.arq_conf = ""

        openFile = QtWidgets.QFileDialog()
        openFile.setDirectory(os.getcwd())
        openFile.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        openFile.setNameFilter("Conf (*.conf)")
        openFile.setViewMode(QtWidgets.QFileDialog.ViewMode.List)
        if openFile.exec():
            arquivo = openFile.selectedFiles()
            if arquivo:
                self.arq_conf = arquivo
            else:
                self.arq_conf = ""

    def usar_config(self):
        """
        Mostra diálogo para saber se usará ou não o arquivo de configuração.

        Returns
        -------
        resposta : bool
            True, usará arquivo; False, não usará arquivo.

        """
        resposta = False

        dlg = QtWidgets.QMessageBox(self)
        dlg.setWindowTitle("LaQC")
        dlg.setText("Usar arquivo de configuração?")
        dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        dlg.setIcon(QtWidgets.QMessageBox.Question)
        button = dlg.exec()

        if button == QtWidgets.QMessageBox.Yes:
            resposta = True

        return resposta

    def barraStatus(self):
        """
        Barra de status.

        Returns
        -------
        None.

        """
        statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(statusBar)
        statusBar.setStyleSheet("padding-top: 10px;padding-bottom: 10px;border-top:0.5px solid black;"
                                "color:black;")
        statusBar.showMessage("Tudo pronto!")

    def barraMenu(self):
        """
        Menu principal.

        Returns
        -------
        None.

        """
        menu = self.menuBar()
        menu.setObjectName("menuPrincipal")

        # Menu Arquivo
        arquivoMenu = menu.addMenu("&Arquivo")
        arquivoMenu.setObjectName("arquivoMenu")

        # Arquivo -> Sair
        sairAcao = QtWidgets.QAction(QtGui.QIcon("imagens/exit.png"), "&Sair", self)
        sairAcao.setShortcut("Ctrl+S")
        sairAcao.setStatusTip("Sair.")
        sairAcao.triggered.connect(QtWidgets.qApp.quit)
        arquivoMenu.addAction(sairAcao)

        # Menu Sobre
        sobreMenu = menu.addMenu("&Sobre")

        # Sobre -> Informações
        infoAcao = QtWidgets.QAction(QtGui.QIcon("imagens/info.png"), "&Informações", self)
        infoAcao.setShortcut("Ctrl+I")
        infoAcao.setStatusTip("Informações sobre o programa")
        infoAcao.triggered.connect(self.sobrePrograma)
        sobreMenu.addAction(infoAcao)

    def sobrePrograma(self):
        """
        Cria janela pop-up com informações sobre o programa.

        Returns
        -------
        None.

        """
        infoMessage = QtWidgets.QMessageBox()
        infoMessage.setWindowTitle("Sobre")
        infoMessage.setText("Aplicação escrita em Python<br/><br/>\
                      Autor: Rogério Ribeiro Macêdo<br/>\
                      Instituição: Instituto de Física e Química. Universidade Federal de Itajubá<br/>\
                      Ano: 2022 a 2023<br/> \
                      Última modificação: 27 de Setembro de 2023")
        infoMessage.setIcon(1)
        infoMessage.exec_()

    def centralizar(self):
        """
        Centraliza janela principal.

        Returns
        -------
        None.

        """
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def msg_cabecalho():
    """
    Mensagem de cabeçalho.

    Returns
    -------
    None.

    """
    print()
    print("-".center(80, "-"))
    print(f'{"|":<1} {"UNIFEI - Universidade Federal de Itajubá":^76} '
          f'{"|":>1}')
    print(f'{"|":<1} {"LaQC - Laboratório de Química Computacional":^76} '
          f'{"|":>1}')
    print("-".center(80, "-"))
    print(f'{"|":<1} {" ":^76} {"|":>1}')
    print(f'{"|":<1} {"obs 1: digite [sair] para encerrar o programa ":<76} '
          f'{"|":>1}')
    print(f'{"|":<1} {" ":^76} {"|":>1}')
    print(f'{"|":<1} {"obs 2: não informar valor considera que o parâmetro não será modificado.":<76} '
          f'{"|":>1}')
    print(f'{"|":<1} {" ":^76} {"|":>1}')
    print("-".center(80, "-"))
    print(f'{"|":<1} {"Modificação em lote dos arquivo de input do Gaussian":^76} '
          f'{"|":>1}')
    print("-".center(80, "-"))
    print()


def tchau():
    """
    Saindo e dizendo Tchau!.

    Returns
    -------
    None.

    """
    print("")
    print("-".center(80, "-"))
    print(f'{"|":<1} {"UNIFEI - Universidade Federal de Itajubá":^76} '
          f'{"|":>1}')
    print(f'{"|":<1} {"LaQC - Laboratório de Química Computacional":^76} '
          f'{"|":>1}')
    print(f'{"|":<1} {" ":^76} {"|":>1}')
    print(f'{"|":<1} {"Tchau!!!!":^76} '
          f'{"|":>1}')
    print(f'{"|":<1} {" ":^76} {"|":>1}')
    print("-".center(80, "-"))
    print("")
    sys.exit()


def usar_arq_conf():
    """
    Questiona o usuário se irá usar, ou não, arquivo de configuração para realizar alterações.

    Returns
    -------
    Boolean
        True, usará arquivo de configuração.
        False, não usará arquivo, portanto, o script irá questionar o usuário.

    """
    val = input("Usar arquivo de configuração? [N]".ljust(TAM_TEXTO, ".") + ": ").strip()
    if val.upper() == "SAIR":
        tchau()
    else:
        if val == "":
            val = "N"
        else:
            if val not in ["S", "s", "N", "n"]:
                print(f" + Valor ({val}), inválido . Saindo!")
                sys.exit()

    return (val in ["S", "s"])


def existe(arquivo, tipo="arquivo"):
    """
    Verifica se o arquivo/diretorio passado como parâmetro existe.

    Parameters
    ----------
    arquivo : texto
        Nome do arquivo/diretorio a ser verificado.
    tipo : texto
        Indicador se será validado um diretório ou um arquivo.

    Returns
    -------
    Bool
        True, se o arquivo/diretorio existe; False, se o arquivo/diretorio não existe.

    """
    path = Path(arquivo)
    if tipo == "arquivo":
        resultado = (path.exists() and path.is_file())
    else:
        resultado = path.exists()

    return resultado


def ler_arq_conf(arquivo_conf=""):
    """
    Leitura do arquivo de configuração.

    Returns
    -------
    configuracoes : dict
        Dicionário contendo os valores que serão modificados.

    """
    configuracoes = {}
    if arquivo_conf == "":
        arquivo_conf = input("Local/nome do arquivo de configuração".ljust(TAM_TEXTO, ".")
                             + ": ").strip()
    if arquivo_conf != "":
        if arquivo_conf.upper() == "SAIR":
            tchau()
        else:
            if existe(arquivo_conf):
                with open(arquivo_conf, "r") as f_arquivo_conf:
                    for line in f_arquivo_conf:
                        # Se o primeiro caracter é ';' quer dizer que é um comentário
                        if (line[0] != ";") and (len(line.strip()) > 0):
                            variavel, valor = line.split(sep=":=")
                            configuracoes[variavel.strip()] = valor.strip()

                    # fechando arquivo
                    f_arquivo_conf.close()
            else:
                print(f" + Arquivo ({arquivo_conf}) não encontrado!. Saindo!")
                sys.exit()
    else:
        print(" + Local/nome não informado. Saindo!")
        sys.exit()

    return configuracoes


def main():
    """
    Procedimento principal para linha de comando.

    Returns
    -------
    None.

    """
    # Exibe o cabeçalho da aplicação
    msg_cabecalho()

    # Dicionário que conterá as alterações a serem realizadas
    dict_alteracoes = {}

    if usar_arq_conf():
        dict_alteracoes = ler_arq_conf()
        print(dict_alteracoes)


def main_window():
    """
    Procedimento principal para ambiente visual.

    Returns
    -------
    None.

    """
    # Create the Qt Application
    application = QtWidgets.QApplication(sys.argv)

    # Create and show the principal window
    mainWindow = MainWindow()
    mainWindow.show()

    # Run the main Qt loop
    sys.exit(application.exec())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Permite modificações em lote dos arquivos de input do Gaussian.")
    parser.add_argument('-w', '--window', action='store_true', help='Exibe ambiente gráfico.')
    args = parser.parse_args()

    if args.window:
        main_window()
    else:
        main()
