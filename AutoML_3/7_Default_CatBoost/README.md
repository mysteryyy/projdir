# Summary of 7_Default_CatBoost

[<< Go back](../README.md)


## CatBoost
- **n_jobs**: -1
- **learning_rate**: 0.1
- **depth**: 6
- **rsm**: 1
- **loss_function**: Logloss
- **explain_level**: 0

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.9
 - **shuffle**: True
 - **stratify**: True

## Optimized metric
logloss

## Training time

2.1 seconds

## Metric details
|           |    score |    threshold |
|:----------|---------:|-------------:|
| logloss   | 0.54243  | nan          |
| auc       | 0.686812 | nan          |
| f1        | 0.554913 |   0.236966   |
| accuracy  | 0.715517 |   0.482985   |
| precision | 0.565217 |   0.482985   |
| recall    | 1        |   0.00174257 |
| mcc       | 0.318487 |   0.214493   |


## Confusion matrix (at threshold=0.482985)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                     223 |                      20 |
| Labeled as positive |                      79 |                      26 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
