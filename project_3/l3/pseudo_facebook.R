pf <- read.csv('pseudo_facebook.tsv', sep="\t")

library("ggplot2")

ggplot(data = pf, aes(x = dob_day)) + 
  geom_histogram() + 
  scale_x_discrete(breaks = 1:31) + 
  facet_wrap(~dob_month)

head(pf)

ggplot(aes(x = friend_count), data=pf) + geom_histogram()

qplot(x = friend_count, data=pf, xlim=c(0, 1000), binwidth=25)

qplot(x = friend_count, data = pf, binwidth = 25) + 
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50)) + facet_wrap(~ gender)

ggplot(aes(x = friend_count), data = subset(pf, !is.na(gender))) +
  geom_histogram() + 
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50)) +
  facet_wrap(~gender)


table(pf$gender)
by(pf$friend_count, pf$gender, summary)


ggplot(aes(x = tenure/365), data = pf) + 
  geom_histogram(binwidth = 1, color = 'black', fill = '#099DD9')

ggplot(aes(x = tenure/365), data = pf) + 
  geom_histogram(binwidth = .25, color = 'black', fill = '#F79420')


ggplot(aes(x = tenure / 365), data = pf) + 
  geom_histogram(color = 'black', fill = '#F79420') + 
  scale_x_continuous(breaks = seq(1, 7, 1), limits = c(0, 7)) + 
  xlab('Number of years using Facebook') + 
  ylab('Number of users in sample')

ggplot(aes(x=age), data=pf) + geom_histogram(color = 'black', fill = '#F79420') +
  scale_x_continuous(breaks = seq(1, 120, 1), limits = c(11, 31))

ggplot(aes(x = age), data = pf) + 
  geom_histogram(binwidth = 1, fill = '#5760AB') + 
  scale_x_discrete(breaks = seq(0, 113, 5))