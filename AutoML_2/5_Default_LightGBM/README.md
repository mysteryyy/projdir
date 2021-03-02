# Summary of 5_Default_LightGBM

[<< Go back](../README.md)


## LightGBM
- **n_jobs**: -1
- **objective**: binary
- **metric**: binary_logloss
- **num_leaves**: 63
- **learning_rate**: 0.05
- **feature_fraction**: 0.9
- **bagging_fraction**: 0.9
- **min_data_in_leaf**: 10
- **explain_level**: 0

## Validation
 - **validation_type**: kfold
 - **shuffle**: True
 - **stratify**: True
 - **k_folds**: 5

## Optimized metric
logloss

## Training time

3.7 seconds

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.549907 | nan         |
| auc       | 0.699093 | nan         |
| f1        | 0.542318 |   0.263493  |
| accuracy  | 0.699971 |   0.601321  |
| precision | 0.53271  |   0.601321  |
| recall    | 1        |   0.0324133 |
| mcc       | 0.295231 |   0.135277  |


## Confusion matrix (at threshold=0.601321)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                    2374 |                      50 |
| Labeled as positive |                     992 |                      57 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
