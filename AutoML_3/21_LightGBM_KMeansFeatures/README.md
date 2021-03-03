# Summary of 21_LightGBM_KMeansFeatures

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

1.2 seconds

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.528114 | nan         |
| auc       | 0.730355 | nan         |
| f1        | 0.572414 |   0.328821  |
| accuracy  | 0.715517 |   0.479355  |
| precision | 0.564103 |   0.506427  |
| recall    | 1        |   0.0249901 |
| mcc       | 0.349435 |   0.271026  |


## Confusion matrix (at threshold=0.479355)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                     217 |                      26 |
| Labeled as positive |                      73 |                      32 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
