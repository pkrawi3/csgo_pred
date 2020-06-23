###########
# Modules #
###########

library(rsample)
library(caret)
library(MASS)
library(SDMTools)
library(tidyverse)
library(e1071)
library(kableExtra)
library(gbm)
library(ROSE)

#############
# Data Prep #
#############

data = read_csv(file = "csgo_data.csv")
data = data[-c(1)]

# Data Splitting to Test/Train
data_tst_trn = initial_split(data, prop=0.5)
data_trn = training(data_tst_trn)
data_tst = testing(data_tst_trn)

############
# Modeling #
############

ranndom_forest_model = caret::train(
                                    home_win ~ . - home_score - away_score,
                                    data = data_trn,
                                    method = "rf",
                                    trControl = trainControl(method="cv", number=5)
                                    )

##############
# Validation #
##############
conf = caret::confusionMatrix(
                              data = data_tst$home_win,
                              reference = predict(ranndom_forest_model, data_tst)
                              )

  
  
  
  
