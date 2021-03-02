# Summary of 13_Xgboost

[<< Go back](../README.md)


## Extreme Gradient Boosting (Xgboost)
- **n_jobs**: -1
- **objective**: binary:logistic
- **eval_metric**: logloss
- **eta**: 0.1
- **max_depth**: 8
- **min_child_weight**: 1
- **subsample**: 1.0
- **colsample_bytree**: 1.0
- **explain_level**: 0

## Validation
 - **validation_type**: kfold
 - **shuffle**: True
 - **stratify**: True
 - **k_folds**: 10

## Optimized metric
logloss

## Training time

16.8 seconds

## Metric details
|           |    score |    threshold |
|:----------|---------:|-------------:|
| logloss   | 0.552422 | nan          |
| auc       | 0.69776  | nan          |
| f1        | 0.545561 |   0.220155   |
| accuracy  | 0.700259 |   0.64927    |
| precision | 0.535714 |   0.64927    |
| recall    | 1        |   0.00537839 |
| mcc       | 0.292213 |   0.172254   |


## Confusion matrix (at threshold=0.64927)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                    2372 |                      52 |
| Labeled as positive |                     989 |                      60 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
