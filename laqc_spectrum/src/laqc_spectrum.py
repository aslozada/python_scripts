# -*- coding: utf-8 -*-
"""
UNIFEI - Federal University of Itajubá.

LaQC - Computational Chemistry Laboratory

authors:
    Astrubal Lozada (mathematical specification for spectrum calculation)
    Rogério Ribeiro Macêdo (Implementation of mathematical specification and user design)
"""

#
# Importing modules
#
import math
import sys
import platform
from pathlib import Path
import numpy as np
import time

#
# Constants
#
A = 1.30629744736E8
FACT1 = 1.0E7
FACT2 = 1.0E0
SIGMA = 3099.6


def head_msg():
    """
    Header message.

    Returns
    -------
    None.

    """
    print()
    print("-".center(79, "-"))
    print(f'{"|":<1} {"UNIFEI - Federal University of Itajubá":^75} '
          f'{"|":>1}')
    print(f'{"|":<1} {"LaQC - Computational Chemistry Laboratory":^75} '
          f'{"|":>1}')
    print(f'{"|":<1} {" ":^75} {"|":>1}')
    print(f'{"|":<1} {">>> use the command [exit] to terminate the program <<<":^75} '
          f'{"|":>1}')
    print(f'{"|":<1} {" ":^75} {"|":>1}')
    print("-".center(79, "-"))
    print(f'{"|":<1} {"UV-VIS Chart for Excited States Calculations.":^75} '
          f'{"|":>1}')
    print("-".center(79, "-"))
    print()


def get_separator():
    """
    Linux and Windows have different directory separators, so this procedure ensures we get that specific separator.

    Returns
    -------
    separador : string
        Character separator.

    """
    separator = "/"
    operational_system = platform.system()
    if operational_system == 'Linux':
        separator = "/"
    else:
        separator = "\\"

    return separator


def file_exist(file=""):
    """
    Verify if a 'file' exists.

    Parameters
    ----------
    file : txt
        Name of file or directory.

    Returns
    -------
    Bool
        True, exist; False, otherwise.

    """
    file_exist = False
    if len(file) > 0:
        path = Path(file)
        file_exist = path.exists()

    return file_exist


def tchau():
    """
    We are leaving and saying goodbye (tchau, inté!!).

    Returns
    -------
    None.

    """
    print("")
    print("-".center(79, "-"))
    print(f'{"|":<1} {"UNIFEI - Federal University of Itajubá":^75} '
          f'{"|":>1}')
    print(f'{"|":<1} {"LaQC - Computational Chemistry Laboratory":^75} '
          f'{"|":>1}')
    print(f'{"|":<1} {" ":^75} {"|":>1}')
    print(f'{"|":<1} {"Inté!!!!":^75} '
          f'{"|":>1}')
    print(f'{"|":<1} {" ":^75} {"|":>1}')
    print("-".center(79, "-"))
    print("")
    sys.exit()


def questions(type_of_fit, type_of_average, wave_numbers,
              wave_numbers_interval=0.5):
    """
    To specify some parameters.

    Parameters
    ----------
    type_of_fit : str
        Type of adjustment. (gaussian).
    type_of_average : str
        Type of average that will used in the generation of resumen graph.
    wave_numbers : array
        Vector that indicates the wavenumber range that will used in the calculation.
    wave_numbers_interval : str
        The interval between waves.

    Returns
    -------
    tyoe_of_fit, type_of_average, wave_numbers, wave_numbers_interval.

    """
    val = input("Type of adjustment (gaussian or lorentzian) "
                "[gaussian]".ljust(57, ".") + ": ").strip()
    if val != "":
        if val in ['gaussian', 'lorentzian']:
            type_of_fit = val
        else:
            if val == "exit":
                tchau()
            else:
                print(f" + Type of adjustment invalid. ({val}), using ({'gaussian'})")
                type_of_fit = "gaussian"

    val = input("Wavenumbers (100-800) [100-800]".
                ljust(57, ".") + ": ").strip()
    values = [100, 800]
    if val != "":
        if val == "exit":
            tchau()
        else:
            try:
                values = [int(i) for i in val.split("-")]
            except ValueError:
                print(f" + Wave numbers invalid ({val}), using ({'100-800'})")
                values[0] = 100
                values[1] = 800

    val = input("Interval between waves [10.0]".ljust(57, ".") + ": ")
    if val != "":
        if val == "exit":
            tchau()
        else:
            try:
                wave_numbers_interval = float(val)
                wave_numbers = list(np.arange(values[0],
                                              values[1]+1, wave_numbers_interval))
            except ValueError:
                print(f" + Invalid interval ({val}), using ({'10'})")
                wave_numbers_interval = 10

    val = input("Type of average (arithmetic) [arithmetic]".
                ljust(57, ".") + ": ").strip()
    if val != "":
        if val in ['arithmetic']:
            type_of_average = val
        else:
            if val == "exit":
                tchau()
            else:
                print(f" + Invalid type of average ({val}),"
                      "using ({'aritmética'})")
                type_of_average = 'arithmetic'

    # Return
    print(wave_numbers)
    return type_of_fit, type_of_average, wave_numbers, wave_numbers_interval


def get_files(local, file_type=".log"):
    """
    Get all files in the specified directory with a type of extension.

    Returns
    -------
    list_files : array
       Return a list of names with all found files in the specified directory.

    """
    list_files = []

    path = Path(local)

    # List of all files with extension specified in [file_type] parameter.
    list_files = [log_file.name for log_file in path.iterdir()
                  if log_file.is_file() if log_file.suffix == file_type]

    return list_files


def get_files_gaussian(local, file_type=".log"):
    """
    Get all files in the specified directory with a type of extension.

    After finding the file, verify the existence of the expression [Normal termination] in the file log.

    Returns
    -------
    list_files : array
        Return a list of names with all found files in the specified directory.

    """
    list_files = []

    path = Path(local)

    # List of all files with extension specified in [file_type] parameter.
    for log_file in path.iterdir():
        if log_file.is_file() and log_file.suffix == file_type:
            if normal_termination(log_file):
                list_files.append(log_file.name)

    return list_files


def normal_termination(local_log):
    """
    Verify the existence of the expression [Normal termination] in the file log.

    Parameters
    ----------
    local_log : str
        Name of the log file and the path where it is located.

    Returns
    -------
    continuar : bool
        True if the expression [Normal termination] was founded, or false otherwise..

    """
    founded = False
    with open(local_log) as f_file:
        for line in f_file:
            if "Normal termination of Gaussian 09" in line:
                founded = True

    return founded


def extract_data_orca():
    """
    Extract data about excited states in Orca files and create a file name "input.dat".

    Returns
    -------
    None.

    """
    excited_states = []
    list_num_excited_state = []

    try:
        local_files = input("Local of files".ljust(57, ".") + ": ").strip()
        if local_files.strip() != "":
            if local_files[-1] != get_separator():
                local_files = local_files + get_separator()

            if file_exist(local_files):
                list_log = get_files(local_files, '.out')

                for log in list_log:
                    local_log = local_files + log
                    print(f" - Extract excited states from the file: {log}")
                    num_excited_state = 0
                    with open(local_log, 'r', encoding='utf-8') as f_arquivo:
                        section_founded = False

                        for line in f_arquivo:
                            txt_line = line.strip()
                            if txt_line.startswith("ABSORPTION SPECTRUM VIA "
                                                   "TRANSITION ELECTRIC "
                                                   "DIPOLE MOMENTS"):
                                section_founded = True
                            else:
                                if len(txt_line) == 0 and section_founded:
                                    break

                            if section_founded:
                                resto = []
                                for i in txt_line.split(" "):
                                    if i != "":
                                        resto.append(i)

                                try:
                                    int(resto[0])
                                    num_excited_state = num_excited_state + 1
                                    comprimento_onda = resto[2]
                                    forca_oscilador = resto[3]
                                    excited_states.append([comprimento_onda,
                                                           forca_oscilador])
                                except ValueError:
                                    continue
                        list_num_excited_state.append(num_excited_state)
                        f_arquivo.close()

                # Saving data
                f_input = open("input.dat", "w")

                # Total number of structures
                f_input.write(f"{len(list_log):<4d}\n")

                # Total number of excited states founded in which structure.
                val_num_excited_state = " ".join(str(i) for i in
                                                 list_num_excited_state)
                f_input.write(f"{val_num_excited_state}\n")

                # Valores de número de onda e força do oscilador
                for item in excited_states:
                    valor_itens = "  ".join(str(i) for i in item)
                    f_input.write(f"{valor_itens}\n")
                f_input.close()
                print("")
    except OSError as msg_err:
        print(f" + Erro: {msg_err}")


def extract_data_gaussian():
    """
    Extraindo dados de estados excitados no arquivo de saída do Gaussian.

    Returns
    -------
    None.

    """
    excited_states = []
    list_num_excited_state = []

    try:
        local_files = input("Local dos arquivos".ljust(57, ".") + ": ").strip()
        if local_files.strip() != "":
            if local_files[-1] != get_separator():
                local_files = local_files + get_separator()

            if file_exist(local_files):
                list_log = get_files_gaussian(local_files, '.log')

                # Extraindo dados
                print(" - Extraindo dados...")
                for log in list_log:
                    local_log = local_files + log
                    print(f" - Extraindo estado excitado do arquivo: {log}")
                    time.sleep(0.400)
                    num_excited_state = 0
                    with open(local_log, "r") as f_arquivo:
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
                for item in excited_states:
                    f_input.write(f'{"  ".join(str(i) for i in item)}\n')
                f_input.close()
                print("")
            else:
                print(" + Caminho não existe. Saindo!")
                sys.exit()

        else:
            print(" + Caminho não informado. Saindo!")
            sys.exit()
    except OSError as msg_err:
        print(f" + Erro: {msg_err}")


def fit_gaussian(type_of_average, wave_numbers):
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
    dados_spectrum = []

    try:
        f_spectrum_gaussian = open("spectrum_gaussian.dat", "w")

        with open("input.dat", "r") as f_input:
            # m_valor representa a quantidade de estruturas que terão os espectros UV-VIS calculados
            m_valor = int(f_input.readline())
            # n_valor representa a quantidade de estados excitados para cada estrutura
            n_valor = [int(i) for i in f_input.readline().split(" ")]

            maxn = max(n_valor)
            eigenvalue = [[0.0]*maxn for i in np.arange(0, m_valor)]
            strength = [[0.0]*maxn for i in np.arange(0, m_valor)]

            for j in range(0, m_valor):
                for i in range(0, n_valor[j]):
                    read_line = f_input.readline()
                    if (read_line.strip()) != "":
                        values = [float(i) for i in read_line.split("  ")]
                        # Comprimento de onda
                        eigenvalue[j][i] = values[0]
                        # Força do oscilador
                        strength[j][i] = values[1]
        f_input.close()

        for j in range(0, m_valor):
            for nm_valor in wave_numbers:
                spectrum = 0.0
                for i in range(0, n_valor[j]):
                    if type_of_average == 'aritmética':
                        vlr_spectrum = A * (strength[j][i] / (FACT1/SIGMA)) * \
                            math.exp(-(((1.0/nm_valor) - (1.0/eigenvalue[j][i]))/(FACT2/SIGMA))**2)
                        spectrum = spectrum + vlr_spectrum

                # Registra os valores calculados para cada número de onda
                # para depois calcular desvio padrão e erro
                dados_spectrum.append([nm_valor, spectrum])
                f_spectrum_gaussian.write(f"{nm_valor:<4f}   {spectrum:>6.10f}\n")

                if nm_valor in average:
                    average[nm_valor] = average[nm_valor] + spectrum
                else:
                    average[nm_valor] = spectrum

            f_spectrum_gaussian.write("\n")

        f_spectrum_gaussian.close()
        print("")
        print("Aquivo spectrum_gaussian.dat gerado!")

        # Calculating and saving average
        if type_of_average == 'aritmética':
            for key in average.keys():
                average[key] = average[key] / m_valor

        with open("average_spectrum.dat", "w") as f_average:
            for key, value in average.items():
                f_average.write(f"{key:<4f}   {value:>6.10f}\n")
        f_average.close()
        print("Arquivo average_spectrum.dat gerado!")

        # Calculando erro padrão
        np.savetxt("dados_spectrum.txt", dados_spectrum, fmt="%6.10f", delimiter=";")
        medias_spectrum = [[i, average[i]] for i in average]
        np.savetxt("medias.txt", medias_spectrum, fmt="%6.10f", delimiter=";")

        # Calculo do desvio padrão e erro
        calcula_dp_erro(medias_spectrum, dados_spectrum)
    except OSError as msg_err:
        print(f"Erro: {msg_err}")
    except ZeroDivisionError:
        print(f"Divisão por zero: {A} * ({strength[j][i]} / "
              "({fact1}/{sigma})) * math.exp(-(((1.0/{nm})-"
              "(1.0/{eigenvalue[j][i]}))/({fact2}/{sigma}))**2)")


def calcula_dp_erro(medias_spectrum, dados_spectrum):
    """
    Cálculo do desvio padrão e erro padrão.

    Returns
    -------
    None.

    """
    vlr_dp = []
    for i in medias_spectrum:
        num_onda = i[0]
        vlr_spec = i[1]
        qtde = 0
        diferenca = 0
        for j in dados_spectrum:
            if j[0] == num_onda:
                diferenca = diferenca + ((vlr_spec - j[1])**2)
                qtde += 1
        vlr_dp.append([num_onda, diferenca/qtde])


def fit_lorentzian(type_of_average, wave_numbers):
    """
    Ajuste lorentzian.

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

    try:
        f_spectrum_lorentzian = open("spectrum_lorentzian.dat", "w")

        with open("input.dat", "r") as f_input:
            m_valor = int(f_input.readline())
            n_valor = [int(i) for i in f_input.readline().split(" ")]

            maxn = max(n_valor)
            eigenvalue = [[0.0]*maxn for i in range(0, m_valor)]
            strength = [[0.0]*maxn for i in range(0, m_valor)]

            for j in range(0, m_valor):
                for i in range(0, n_valor[j]):
                    read_line = f_input.readline()
                    if (read_line.strip()) != "":
                        values = [float(i) for i in read_line.split("  ")]
                        eigenvalue[j][i] = values[0]
                        strength[j][i] = values[1]
        f_input.close()

        for j in range(0, m_valor):
            for nm_valor in wave_numbers:
                spectrum = 0.0
                for i in range(0, n_valor[j]):
                    if type_of_average == 'aritmética':
                        spectrum = spectrum + A * (strength[j][i] / (FACT1/SIGMA)) * \
                                   (1 / (((nm_valor - eigenvalue[j][i])**2) + 1))

                f_spectrum_lorentzian.write(f"{nm_valor:<4f}   {spectrum:>6.12f}\n")

                if nm_valor in average:
                    average[nm_valor] = average[nm_valor] + spectrum
                else:
                    average[nm_valor] = spectrum

            f_spectrum_lorentzian.write("\n")

        f_spectrum_lorentzian.close()
        print("")
        print("Arquivo spectrum_lorentzian.dat gerado!")

        # Calculating and saving average
        if type_of_average == 'aritmética':
            for key in average.keys():
                average[key] = average[key] / m_valor

        with open("average.dat", "w") as f_average:
            for key, value in average.items():
                f_average.write(f"{key:<4f}   {value:>6.12f}\n")
        f_average.close()
        print("Arquivo average.dat gerado!")
    except OSError as msg_err:
        print(f'Erro ao ajustar como modelo lorentzian: {msg_err}')
    except ValueError as msg_err:
        print(f'Erro ao ajustar como modelo lorentzian: {msg_err}')


def main(type_of_fit, type_of_average, wave_numbers, wave_numbers_interval):
    """
    Função principal.

    Parameters
    ----------
    type_of_fit : TYPE
        tipo de ajuste.
    type_of_average : TYPE
        tipo de media a ser calculada.
    wave_numbers : TYPE
        faixa de números de onda.
    wave_numbers_interval : TYPE
        intervalo para a faixa de número de onda.

    Returns
    -------
    None.

    """
    type_of_fit, type_of_average, wave_numbers, wave_numbers_interval = questions(type_of_fit,
                                                                                  type_of_average, wave_numbers,
                                                                                  wave_numbers_interval)

    if type_of_fit == "gaussian":
        fit_gaussian(type_of_average, wave_numbers)
    elif type_of_fit == "lorentzian":
        fit_lorentzian(type_of_average, wave_numbers)


if __name__ == "__main__":
    type_of_app = "Gaussian"
    type_of_fit = "gaussian"
    type_of_average = 'aritmética'
    wave_numbers_interval = 10
    wave_numbers = list(np.arange(100, 801, wave_numbers_interval))

    head_msg()

    if file_exist("input.dat"):
        main(type_of_fit, type_of_average, wave_numbers, wave_numbers_interval)
    else:
        val = "S"
        val = input("O input.dat não existe. Deseja gerá-lo? "
                    "(S or N) [S]".ljust(57, ".") + ": ")
        if (val == ""):
            val = "S"
        if (val in ['n', 's', 'N', 'S']):
            if (val in ["N", "n"]):
                tchau()
            else:
                val = input("Origem do arquivo de saída (Gaussian ou Orca) "
                            "[Gaussian]".ljust(57, ".") + ": ").strip()
                if val == "exit":
                    tchau()

                if val != "":
                    type_of_app = val

                if type_of_app == "Gaussian":
                    extract_data_gaussian()
                    main(type_of_fit, type_of_average, wave_numbers,
                         wave_numbers_interval)
                else:
                    if type_of_app == "Orca":
                        extract_data_orca()
                        main(type_of_fit, type_of_average, wave_numbers,
                             wave_numbers_interval)
                    else:
                        print(f' + Valor ({val}) inválido!')
        else:
            print(f' + Valor ({val}) inválido!')
