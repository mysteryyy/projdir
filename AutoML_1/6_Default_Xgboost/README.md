# Summary of 6_Default_Xgboost

[<< Go back](../README.md)


## Extreme Gradient Boosting (Xgboost)
- **n_jobs**: -1
- **objective**: binary:logistic
- **eval_metric**: logloss
- **eta**: 0.075
- **max_depth**: 6
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

12.5 seconds

## Metric details
|           |    score |    threshold |
|:----------|---------:|-------------:|
| logloss   | 0.545796 | nan          |
| auc       | 0.698738 | nan          |
| f1        | 0.543392 |   0.223467   |
| accuracy  | 0.694212 |   0.469619   |
| precision | 0.490255 |   0.469619   |
| recall    | 1        |   0.00188027 |
| mcc       | 0.300083 |   0.124824   |


## Confusion matrix (at threshold=0.469619)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                    2084 |                     340 |
| Labeled as positive |                     722 |                     327 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
