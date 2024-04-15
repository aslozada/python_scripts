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

datafile = 'spectrum_gaussian.dat'
stats datafile
unset key
plot for [IDX=0:STATS_blocks-1] \
    datafile \
    index IDX \
    using 1:2 \
    with lines \
	lw 1 \

