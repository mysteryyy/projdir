# Summary of 71_LightGBM

[<< Go back](../README.md)


## LightGBM
- **n_jobs**: -1
- **objective**: binary
- **metric**: binary_logloss
- **num_leaves**: 15
- **learning_rate**: 0.2
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

1.2 seconds

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.537647 | nan         |
| auc       | 0.708779 | nan         |
| f1        | 0.556213 |   0.259662  |
| accuracy  | 0.718391 |   0.558847  |
| precision | 0.652174 |   0.558847  |
| recall    | 1        |   0.0225137 |
| mcc       | 0.320285 |   0.181327  |


## Confusion matrix (at threshold=0.558847)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                     235 |                       8 |
| Labeled as positive |                      90 |                      15 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
