import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from lmfit import Model

def function(x, A1, A2, x0, p):
    return np.nan_to_num((A1 - A2) / (1 + (x / x0)**p) + A2)

def create_model(function, y_data):
    model = Model(function)
    params = model.make_params(A1=max(y_data), A2=min(y_data), x0=len(y_data)/2, p=1)
    params['p'].set(min=0)
    return model, params

def fit_model(model, params, x_data, y_data):
    return model.fit(y_data, params, x=x_data)

def plot_result(result):
    result.plot_fit()
    plt.title('Model Fitting Result')
    plt.xlabel('X data')
    plt.ylabel('Y data')
    plt.grid(True)
    plt.show()

y_data = np.array([30.24703633, 44.01453155, 44.06832377, 42.6652645, 42.6749522, 42.50873168,
    42.56685787, 42.02536648, 42.76456342, 42.87571702, 42.7292543, 42.98495857,
    42.76532823, 42.36775016, 41.57131931, 42.45787126, 42.21363926, 41.0387508,
    41.49356278, 41.32402804, 41.33919694, 40.9848311, 41.22919057, 41.02829828,
    41.99604844, 43.93550032, 46.88183556, 52.27966858, 59.70248566, 69.59005736,
    80.4972594, 92.69585723, 102.1555131, 112.7701721, 121.5899299, 130.204334,
    137.0532823, 143.1460803, 148.6493308, 153.0806883, 157.1366475])
x_data = np.arange(len(y_data))

model, params = create_model(function, y_data)
result = fit_model(model, params, x_data, y_data)

print(result.fit_report())
plot_result(result)
