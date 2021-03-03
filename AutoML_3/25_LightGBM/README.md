# Summary of 25_LightGBM

[<< Go back](../README.md)


## LightGBM
- **n_jobs**: -1
- **objective**: binary
- **metric**: binary_logloss
- **num_leaves**: 63
- **learning_rate**: 0.2
- **feature_fraction**: 0.5
- **bagging_fraction**: 1.0
- **min_data_in_leaf**: 30
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
| logloss   | 0.550222 | nan         |
| auc       | 0.704292 | nan         |
| f1        | 0.554572 |   0.192962  |
| accuracy  | 0.715517 |   0.631659  |
| precision | 0.625    |   0.631659  |
| recall    | 1        |   0.0148506 |
| mcc       | 0.312085 |   0.192962  |


## Confusion matrix (at threshold=0.631659)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                     234 |                       9 |
| Labeled as positive |                      90 |                      15 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
