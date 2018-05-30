require(tidyverse)
require(readr)


fid   =  readLines("..//Data/fullOutput")
# Positions of Isotopic Abundances
idx <- grep(" ISOTOPIC ABUNDANCES",fid)

df <- data.frame(fid)
id1 <- idx[1]+1
id2 <- idx[1]+24
df1 <- df[id1:id2,1]

as.numeric(str_extract_all(df1, "[0-9]+")[[1]])


match <- "([A-Z][ \t\n\r\f\v])"

grep(match, df1,value=T)
unlist(df1)


cat(" ISOTOPIC ABUNDANCES", file = fid)