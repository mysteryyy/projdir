# Summary of 3_DecisionTree_KMeansFeatures

[<< Go back](../README.md)


## Decision Tree
- **n_jobs**: -1
- **criterion**: gini
- **max_depth**: 4
- **explain_level**: 0

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.9
 - **shuffle**: True
 - **stratify**: True

## Optimized metric
logloss

## Training time

1.4 seconds

## Metric details
|           |    score |    threshold |
|:----------|---------:|-------------:|
| logloss   | 0.531618 | nan          |
| auc       | 0.683598 | nan          |
| f1        | 0.539846 |   0.170121   |
| accuracy  | 0.70977  |   0.517431   |
| precision | 1        |   0.517431   |
| recall    | 1        |   0.00497238 |
| mcc       | 0.312049 |   0.170121   |


## Confusion matrix (at threshold=0.517431)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                     243 |                       0 |
| Labeled as positive |                     101 |                       4 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
