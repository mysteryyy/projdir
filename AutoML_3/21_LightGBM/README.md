# Summary of 21_LightGBM

[<< Go back](../README.md)


## LightGBM
- **n_jobs**: -1
- **objective**: binary
- **metric**: binary_logloss
- **num_leaves**: 15
- **learning_rate**: 0.1
- **feature_fraction**: 0.8
- **bagging_fraction**: 0.8
- **min_data_in_leaf**: 10
- **explain_level**: 0

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.9
 - **shuffle**: True
 - **stratify**: True

## Optimized metric
logloss

## Training time

0.7 seconds

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.531905 | nan         |
| auc       | 0.713698 | nan         |
| f1        | 0.581395 |   0.264376  |
| accuracy  | 0.701149 |   0.511388  |
| precision | 0.511628 |   0.511388  |
| recall    | 1        |   0.0170124 |
| mcc       | 0.376431 |   0.264376  |


## Confusion matrix (at threshold=0.511388)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                     222 |                      21 |
| Labeled as positive |                      83 |                      22 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
