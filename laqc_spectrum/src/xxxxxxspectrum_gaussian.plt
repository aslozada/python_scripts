# Limpando configurações anteriores
reset

# Configurações gerais
set terminal png enhanced font 'arial, 10' size 800,600
set output 'spectrum_gaussian.png'
set key off
set encoding utf8


# Margens do gráfico
set lmargin 12
set rmargin 5
set tmargin 6
set bmargin 5.5

# Configurações do Título
set title "Espectro UV/Vis" font "Arial, 25"

# Configurações do Eixo X
set xlabel "{/Symbol l} / nm" font "Arial, 14" offset 0, -1
set xtics font "Arial, 10"

# Configurações do Eixo y
set ylabel "Absorbância / Unidades arbitrárias" font "Arial, 14"
set ytics font "Arial, 10" 

# Cores das linhas
#set style line 1  lc rgb 'red'     lw 1.5
##set style line 2  lc rgb 'orange'  lw 1.5
#set style line 3  lc rgb 'blue'    lw 1.5
##set style line 4  lc rgb 'black'   lw 1.5
#set style line 5  lc rgb 'yellow'  lw 1.5

set style line  1 lt 1 lc rgb '#000004' # black
set style line  2 lt 1 lc rgb '#1c1044' # dark blue
set style line  3 lt 1 lc rgb '#4f127b' # dark purple
set style line  4 lt 1 lc rgb '#812581' # purple
set style line  5 lt 1 lc rgb '#b5367a' # magenta
set style line  6 lt 1 lc rgb '#e55964' # light red
set style line  7 lt 1 lc rgb '#fb8761' # orange


# Gerando gráfico
stats "spectrum_gaussian.dat"
maximum_number_of_curves = int(STATS_blocks)-1
every_nth_curve = 1   
set style line 1 lc rgb '#0060ad' lw 6
set style line 2 lt 2 lw 2 pt 3 ps 0.5
plot for [i=0 : maximum_number_of_curves : every_nth_curve] "spectrum_gaussian.dat" every:::i::i w l linewidth 2 linecolor i

#plot 'spectrum_gaussian.dat' with lines ls 2 # linewidth 2 ls 2
set terminal win