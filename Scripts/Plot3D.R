# Plot 3D

library("plot3D")

Ab1 <- read.csv("Frame 1.csv",header = F) 
Ab1 <- t(Ab1)

plot(Ab1)

data.matrix(Ab1)

x= Ab1[,1]
y = Ab1[,2]
z = as.matrix(Ab1[,3])



hist3D(x,y,z)

plot(data.matrix(Ab1))

expand.grid(z~x+y)


DF <- data.frame(a=1:3, b=letters[10:12],
                 c=seq(as.Date("2004-01-01"), by = "week", len = 3),
                 stringsAsFactors = TRUE)