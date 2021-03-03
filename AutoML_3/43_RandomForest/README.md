# Summary of 43_RandomForest

[<< Go back](../README.md)


## Random Forest
- **n_jobs**: -1
- **criterion**: gini
- **max_features**: 0.7
- **min_samples_split**: 50
- **max_depth**: 3
- **explain_level**: 0

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.9
 - **shuffle**: True
 - **stratify**: True

## Optimized metric
logloss

## Training time

7.1 seconds

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.53912  | nan         |
| auc       | 0.685793 | nan         |
| f1        | 0.561497 |   0.263206  |
| accuracy  | 0.695402 |   0.457567  |
| precision | 0.482759 |   0.457567  |
| recall    | 1        |   0.0203493 |
| mcc       | 0.356229 |   0.263206  |


## Confusion matrix (at threshold=0.457567)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                     228 |                      15 |
| Labeled as positive |                      91 |                      14 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
