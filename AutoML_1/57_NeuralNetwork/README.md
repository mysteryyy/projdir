# Summary of 57_NeuralNetwork

[<< Go back](../README.md)


## Neural Network
- **n_jobs**: -1
- **dense_1_size**: 32
- **dense_2_size**: 4
- **learning_rate**: 0.05
- **explain_level**: 0

## Validation
 - **validation_type**: kfold
 - **shuffle**: True
 - **stratify**: True
 - **k_folds**: 10

## Optimized metric
logloss

## Training time

6.9 seconds

## Metric details
|           |    score |      threshold |
|:----------|---------:|---------------:|
| logloss   | 0.610507 | nan            |
| auc       | 0.565653 | nan            |
| f1        | 0.472309 |   0.231254     |
| accuracy  | 0.694212 |   0.454721     |
| precision | 0.408451 |   0.454721     |
| recall    | 1        |   2.91606e-113 |
| mcc       | 0.105306 |   0.295933     |


## Confusion matrix (at threshold=0.454721)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                    2382 |                      42 |
| Labeled as positive |                    1020 |                      29 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
