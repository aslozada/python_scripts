# Limpando configurações anteriores
reset

# Configurações gerais
set terminal png enhanced font 'arial, 10' size 800,600
set output 'average_spectrum.png'
set key off
set encoding utf8

# Margens do gráfico
set lmargin 12
set rmargin 5
set tmargin 6
set bmargin 5.5

# Configurações do Título
set title "Espectro UV/Vis (Média Aritmética)" font "Arial, 25"

# Configurações do Eixo X
set xlabel "{/Symbol l} / nm" font "Arial, 14" offset 0, -1
set xtics font "Arial, 10"

# Configurações do Eixo y
set ylabel "Absorbância" font "Arial, 14"
set ytics font "Arial, 10" 

# Gerando gráfico
plot 'average_spectrum.dat' with lines linewidth 2
set terminal win