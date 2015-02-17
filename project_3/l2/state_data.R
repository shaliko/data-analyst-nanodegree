stateInfo <- read.csv('stateData.csv')

subset(stateInfo, highSchoolGrad > 50)


stateInfo[stateInfo$highSchoolGrad > 50, ]
