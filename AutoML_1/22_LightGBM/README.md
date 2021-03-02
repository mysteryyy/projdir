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
 - **validation_type**: kfold
 - **shuffle**: True
 - **stratify**: True
 - **k_folds**: 10

## Optimized metric
logloss

## Training time

4.2 seconds

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.558649 | nan         |
| auc       | 0.688414 | nan         |
| f1        | 0.544944 |   0.182757  |
| accuracy  | 0.699395 |   0.653894  |
| precision | 0.533333 |   0.653894  |
| recall    | 1        |   0.0046885 |
| mcc       | 0.296657 |   0.181672  |


## Confusion matrix (at threshold=0.653894)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                    2389 |                      35 |
| Labeled as positive |                    1009 |                      40 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
