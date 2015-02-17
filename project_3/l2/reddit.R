reddit <- read.csv('reddit.csv')

install.packages('ggplot2', dependencies = T) 
library(ggplot2)

str(reddit)

qplot(data=reddit, x = country)

