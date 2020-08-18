# ML Algorithms from Scratch

## 1. Linear Regression
Dataset: [Kaggle - USA Housing Prices](https://www.kaggle.com/farhankarim1/usa-house-prices).     
Goal: Predict the housing prices using linear regression. Try only using numpy and compare with sklearn.    
Model Equation: 

In linear regression we assume dependant variable y has a linear relationship with independant variables x. Therefore should be in the form: 
` y = wX + b `.    

The best `w` value is chosen by minimising the squared errors &Sigma;(y<sub>i</sub> - wx<sub>i</sub>)<sup>2</sup>   

### Closed Form Matrix Solution
This optimisation problem can be solved either using the least squares method or using normal equations.    
For this problem we will use the closed form solution, however if W is quite sparse, an iterative method may be more appropriate. 

W = (X<sup>T</sup>X)<sup>-1</sup>X<sup>T</sup>Y


## 2. K-Nearest Neighbours (KNN)


## 3. K-Means


