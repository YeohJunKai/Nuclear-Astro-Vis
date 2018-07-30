#library(shiny)
library("plot3D")
library(reticulate)
csv <- import("csv")

source_python("Producing Frames New.py")

file <- formatfile("nucleo.txt")





source_python('add.py')
add(5, 10)