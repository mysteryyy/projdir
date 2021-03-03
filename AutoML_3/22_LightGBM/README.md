# Summary of 22_LightGBM

[<< Go back](../README.md)


## LightGBM
- **n_jobs**: -1
- **objective**: binary
- **metric**: binary_logloss
- **num_leaves**: 63
- **learning_rate**: 0.2
- **feature_fraction**: 0.5
- **bagging_fraction**: 1.0
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

0.8 seconds

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.562445 | nan         |
| auc       | 0.694297 | nan         |
| f1        | 0.546547 |   0.205494  |
| accuracy  | 0.706897 |   0.65309   |
| precision | 0.551724 |   0.65309   |
| recall    | 1        |   0.0124954 |
| mcc       | 0.29249  |   0.205494  |


## Confusion matrix (at threshold=0.65309)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                     230 |                      13 |
| Labeled as positive |                      89 |                      16 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
