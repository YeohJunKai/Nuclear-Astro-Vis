library(shiny)
library("plot3D")
library(reticulate)
csv <- import("csv")

source_python("Producing Frames New.py")

file <- formatfile("nucleo.txt")


times <- read.csv("Times.csv")
times<-as.matrix(times)
steps<-length(times)

specs <- read.csv("Specs.csv")


ui <- fluidPage(  headerPanel("3D Histogram"),
  sidebarLayout(
                  sidebarPanel(
                   sliderInput(inputId = "phi",      label = "ColAttitude Viewing Angle (Phi)",      value = 20, min = 0, max = 180),sliderInput(inputId = "theta",      label = "Azimuthal Viewing Angle (Theta)",      value = 90, min = 0, max = 360),    
                   sliderInput(inputId = "neuno",      label = "Neutron Number Range",      value = c(0,specs[1]),step=1, min = 0, max = specs[1])
                   ,sliderInput(inputId = "prono",      label = "Proton Number Range",      value = c(0,specs[2]), step=1,min = 0, max = specs[2]),
                   sliderInput(inputId = "time",      label = "Time",      value = 1, min = 1, max = steps, step=1,animate=TRUE),
                   sliderInput("ani", "Looping Animation:",
                               min = 1, max = steps,
                               value = 1, step = 1,
                               animate =
                                 animationOptions(interval = 800, loop = TRUE)),
                   checkboxGroupInput("checkGroup", label = h3("Z Axis Scale"), 
                                      choices = list("Normal" = 1, "Logarithmic" = 2),
                                      selected = 1),
                   fileInput("file", label = h3("File Input(With .txt extension)")))
                   
                   ,mainPanel(plotOutput("hist"))))


server <- function(input, output) {
  mydata <- reactive({as.matrix(read.csv(paste("Frame ",input$time,".csv",sep="")))})
  seldata<-reactive({mydata()[c(((input$neuno[1])+1):((input$neuno[2])+1)),c(((input$prono[1])+1):((input$prono[2])+1))]})
  phival<-reactive({input$phi})
  thetaval<-reactive({input$theta})
  rowno<-reactive({c(input$neuno[1]:input$neuno[2])})
  colno<-reactive({c(input$prono[1]:input$prono[2])})
  output$hist <-  renderPlot({ 
                              par(mar=c(0.1,0.50,0.80,0.50))
                                        hist3D(x=rowno(),y=colno(),z = seldata(), bty = "g", phi = phival(),
                                         border = "black", shade = 0.2, theta = thetaval(),
                                         space = 0.3, ticktype = "detailed", d = 2,zlim=c(0,max(seldata())),r=1,xlab="Neutron Number",ylab="Proton Number",zlab="Abundance Ratio") }) 
  
  } 
shinyApp(ui = ui, server = server)

