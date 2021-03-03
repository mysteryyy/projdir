# Summary of 8_Default_NeuralNetwork

[<< Go back](../README.md)


## Neural Network
- **n_jobs**: -1
- **dense_1_size**: 32
- **dense_2_size**: 16
- **learning_rate**: 0.05
- **explain_level**: 0

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.9
 - **shuffle**: True
 - **stratify**: True

## Optimized metric
logloss

## Training time

1.0 seconds

## Metric details
|           |    score |     threshold |
|:----------|---------:|--------------:|
| logloss   | 0.585997 | nan           |
| auc       | 0.628807 | nan           |
| f1        | 0.510145 |   0.310536    |
| accuracy  | 0.706897 |   0.503374    |
| precision | 0.588235 |   0.503374    |
| recall    | 1        |   8.38956e-19 |
| mcc       | 0.210914 |   0.310536    |


## Confusion matrix (at threshold=0.503374)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                     236 |                       7 |
| Labeled as positive |                      95 |                      10 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
