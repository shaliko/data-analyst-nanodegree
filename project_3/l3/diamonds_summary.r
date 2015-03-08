library(ggplot2)
data(diamonds)

ggplot(diamonds, aes(x=price)) + geom_histogram()


summary(diamonds$price)

nrow(diamonds[diamonds$price < 500,])
nrow(diamonds[diamonds$price < 250,])
nrow(diamonds[diamonds$price >= 15000,])

ggplot(aes(x=price), data = diamonds) + geom_histogram(binwidth = 250)+
  scale_x_continuous(breaks = seq(0,5000,250), limit = c(0,5000))

#For diamonds that cost less than $2,000, the most common price of a diamond is around $700 (binwidth = 1)

ggplot(aes(x=price), data = diamonds) + geom_histogram(binwidth = 250)+
  scale_x_continuous(breaks = seq(0,5000,250), limit = c(0,5000)) + facet_wrap(~cut, ncol=2)


by(diamonds$price,diamonds$cut,summary)
by(diamonds$price,diamonds$cut,max)


qplot(x = price, data = diamonds) + facet_wrap(~cut)

qplot(x = price, data = diamonds) + facet_wrap(~cut, scales = "free_y")

ggplot(aes(x=price/carat), data = na.omit(diamonds)) + geom_histogram()+
  facet_wrap(~cut, scales  = "free_y") + scale_x_log10()


ggplot(aes(x = color, y = price/carat), data = na.omit(diamonds)) + geom_boxplot()


summary(subset(diamonds,color=='D')$price)
summary(subset(diamonds,color=='J')$price)
IQR(subset(diamonds, color == 'D')$price)
by(diamonds$price, diamonds$color, IQR)
