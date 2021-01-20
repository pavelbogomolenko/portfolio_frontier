import math

import numpy as np
from scipy.optimize import minimize


#           AMZN     MSFT     GOOGL    IBM      CSCO
# AMZN   0.007106 0.003409 0.003438 0.002831 0.002611
# MSFT   0.003409 0.003604 0.002411 0.001941 0.001770
# GOOGL  0.003438 0.002411 0.004139 0.002006 0.001479
# IBM    0.002831 0.001941 0.002006 0.004500 0.002768
# CSCO   0.002611 0.001770 0.001479 0.002768 0.004715
# P_VAR_COVAR_MATRIX = np.array([
#     [0.007106 * 12, 0.003409 * 12, 0.003438 * 12, 0.002831 * 12, 0.002611 * 12],
#     [0.003409 * 12, 0.003604 * 12, 0.002411 * 12, 0.001941 * 12, 0.001770 * 12],
#     [0.003438 * 12, 0.002411 * 12, 0.004139 * 12, 0.002006 * 12, 0.001479 * 12],
#     [0.002831 * 12, 0.001941 * 12, 0.002006 * 12, 0.004500 * 12, 0.002768 * 12],
#     [0.002611 * 12, 0.001770 * 12, 0.001479 * 12, 0.002768 * 12, 0.004715 * 12]
# ])

#         AMZN     EBAY     AAPL     ABC      AMD      GOOGL    ABBV     CDNS     EA       CSCO     XRAY     FANG     GS       WMT      BA       MSFT     BAC      T
# AMZN   0.095430 0.030869 0.034753 0.021974 0.071344 0.047671 0.029347 0.026039 0.037453 0.033734 0.018466 0.044795 0.022280 0.004046 0.038174 0.031853 0.031056 0.003491
# EBAY   0.030869 0.133063 0.042347 0.025037 0.085212 0.020039 0.020036 0.033588 0.034715 0.035841 0.011854 0.073288 0.043893 -0.001470 0.049440 0.023383 0.040348 0.014279
# AAPL   0.034753 0.042347 0.255265 0.022071 0.037522 0.010620 0.011527 0.033776 0.041307 0.042687 0.013394 0.029121 0.027873 0.009145 0.036096 0.019617 0.028120 0.009752
# ABC    0.021974 0.025037 0.022071 0.055801 0.029349 0.007821 0.015758 0.007260 0.012870 0.018888 0.013800 0.013299 0.017603 0.007439 0.031930 0.004830 0.019994 0.010754
# AMD    0.071344 0.085212 0.037522 0.029349 0.307376 0.034503 0.032254 0.038207 0.044484 0.055128 0.013852 0.071355 0.051524 0.002784 0.060647 0.036473 0.067310 0.025006
# GOOGL  0.047671 0.020039 0.010620 0.007821 0.034503 0.086523 0.017202 0.022420 0.028139 0.015056 0.024425 0.037874 0.023121 -0.001519 0.027716 0.025340 0.036106 0.003665
# ABBV   0.029347 0.020036 0.011527 0.015758 0.032254 0.017202 0.078829 0.000441 0.011239 0.023983 0.023595 0.036686 0.021030 0.001201 0.038777 0.018234 0.033936 0.014946
# CDNS   0.026039 0.033588 0.033776 0.007260 0.038207 0.022420 0.000441 0.058347 0.035244 0.029124 0.023089 0.042686 0.028343 0.010854 0.020978 0.017893 0.029682 0.002255
# EA     0.037453 0.034715 0.041307 0.012870 0.044484 0.028139 0.011239 0.035244 0.108908 0.031840 0.014955 0.066240 0.017113 -0.006132 0.036857 0.012825 0.020726 0.002993
# CSCO   0.033734 0.035841 0.042687 0.018888 0.055128 0.015056 0.023983 0.029124 0.031840 0.057514 0.018470 0.050932 0.031260 0.009079 0.042173 0.017625 0.033520 0.013488
# XRAY   0.018466 0.011854 0.013394 0.013800 0.013852 0.024425 0.023595 0.023089 0.014955 0.018470 0.058464 0.044721 0.024831 0.008850 0.028022 0.012694 0.028720 0.018479
# FANG   0.044795 0.073288 0.029121 0.013299 0.071355 0.037874 0.036686 0.042686 0.066240 0.050932 0.044721 0.283630 0.083537 0.006126 0.096653 0.026787 0.083540 0.039399
# GS     0.022280 0.043893 0.027873 0.017603 0.051524 0.023121 0.021030 0.028343 0.017113 0.031260 0.024831 0.083537 0.073881 0.005507 0.058065 0.020425 0.069424 0.016480
# WMT    0.004046 -0.001470 0.009145 0.007439 0.002784 -0.001519 0.001201 0.010854 -0.006132 0.009079 0.008850 0.006126 0.005507 0.030345 0.007338 0.002871 0.005709 0.007719
# BA     0.038174 0.049440 0.036096 0.031930 0.060647 0.027716 0.038777 0.020978 0.036857 0.042173 0.028022 0.096653 0.058065 0.007338 0.155276 0.025867 0.060201 0.026413
# MSFT   0.031853 0.023383 0.019617 0.004830 0.036473 0.025340 0.018234 0.017893 0.012825 0.017625 0.012694 0.026787 0.020425 0.002871 0.025867 0.041149 0.027017 0.006761
# BAC    0.031056 0.040348 0.028120 0.019994 0.067310 0.036106 0.033936 0.029682 0.020726 0.033520 0.028720 0.083540 0.069424 0.005709 0.060201 0.027017 0.091910 0.013116
# T      0.003491 0.014279 0.009752 0.010754 0.025006 0.003665 0.014946 0.002255 0.002993 0.013488 0.018479 0.039399 0.016480 0.007719 0.026413 0.006761 0.013116 0.033503

P_VAR_COVAR_MATRIX = np.array([
    [0.095430, 0.030869, 0.034753, 0.021974, 0.071344, 0.047671, 0.029347, 0.026039, 0.037453, 0.033734, 0.018466, 0.044795, 0.022280, 0.004046, 0.038174, 0.031853, 0.031056, 0.003491],
    [0.030869, 0.133063, 0.042347, 0.025037, 0.085212, 0.020039, 0.020036, 0.033588, 0.034715, 0.035841, 0.011854, 0.073288, 0.043893, -0.001470, 0.049440, 0.023383, 0.040348, 0.014279],
    [0.034753, 0.042347, 0.255265, 0.022071, 0.037522, 0.010620, 0.011527, 0.033776, 0.041307, 0.042687, 0.013394, 0.029121, 0.027873, 0.009145, 0.036096, 0.019617, 0.028120, 0.009752],
    [0.021974, 0.025037, 0.022071, 0.055801, 0.029349, 0.007821, 0.015758, 0.007260, 0.012870, 0.018888, 0.013800, 0.013299, 0.017603, 0.007439, 0.031930, 0.004830, 0.019994, 0.010754],
    [0.071344, 0.085212, 0.037522, 0.029349, 0.307376, 0.034503, 0.032254, 0.038207, 0.044484, 0.055128, 0.013852, 0.071355, 0.051524, 0.002784, 0.060647, 0.036473, 0.067310, 0.025006],
    [0.047671, 0.020039, 0.010620, 0.007821, 0.034503, 0.086523, 0.017202, 0.022420, 0.028139, 0.015056, 0.024425, 0.037874, 0.023121, -0.001519, 0.027716, 0.025340, 0.036106, 0.003665],
    [0.029347, 0.020036, 0.011527, 0.015758, 0.032254, 0.017202, 0.078829, 0.000441, 0.011239, 0.023983, 0.023595, 0.036686, 0.021030, 0.001201, 0.038777, 0.018234, 0.033936, 0.014946],
    [0.026039, 0.033588, 0.033776, 0.007260, 0.038207, 0.022420, 0.000441, 0.058347, 0.035244, 0.029124, 0.023089, 0.042686, 0.028343, 0.010854, 0.020978, 0.017893, 0.029682, 0.002255],
    [0.037453, 0.034715, 0.041307, 0.012870, 0.044484, 0.028139, 0.011239, 0.035244, 0.108908, 0.031840, 0.014955, 0.066240, 0.017113, -0.006132, 0.036857, 0.012825, 0.020726, 0.002993],
    [0.033734, 0.035841, 0.042687, 0.018888, 0.055128, 0.015056, 0.023983, 0.029124, 0.031840, 0.057514, 0.018470, 0.050932, 0.031260, 0.009079, 0.042173, 0.017625, 0.033520, 0.013488],
    [0.018466, 0.011854, 0.013394, 0.013800, 0.013852, 0.024425, 0.023595, 0.023089, 0.014955, 0.018470, 0.058464, 0.044721, 0.024831, 0.008850, 0.028022, 0.012694, 0.028720, 0.018479],
    [0.044795, 0.073288, 0.029121, 0.013299, 0.071355, 0.037874, 0.036686, 0.042686, 0.066240, 0.050932, 0.044721, 0.283630, 0.083537, 0.006126, 0.096653, 0.026787, 0.083540, 0.039399],
    [0.022280, 0.043893, 0.027873, 0.017603, 0.051524, 0.023121, 0.021030, 0.028343, 0.017113, 0.031260, 0.024831, 0.083537, 0.073881, 0.005507, 0.058065, 0.020425, 0.069424, 0.016480],
    [0.004046, -0.001470, 0.009145, 0.007439, 0.002784, -0.001519, 0.001201, 0.010854, -0.006132, 0.009079, 0.008850, 0.006126, 0.005507, 0.030345, 0.007338, 0.002871, 0.005709, 0.007719],
    [0.038174, 0.049440, 0.036096, 0.031930, 0.060647, 0.027716, 0.038777, 0.020978, 0.036857, 0.042173, 0.028022, 0.096653, 0.058065, 0.007338, 0.155276, 0.025867, 0.060201, 0.026413],
    [0.031853, 0.023383, 0.019617, 0.004830, 0.036473, 0.025340, 0.018234, 0.017893, 0.012825, 0.017625, 0.012694, 0.026787, 0.020425, 0.002871, 0.025867, 0.041149, 0.027017, 0.006761],
    [0.031056, 0.040348, 0.028120, 0.019994, 0.067310, 0.036106, 0.033936, 0.029682, 0.020726, 0.033520, 0.028720, 0.083540, 0.069424, 0.005709, 0.060201, 0.027017, 0.091910, 0.013116],
    [0.003491, 0.014279, 0.009752, 0.010754, 0.025006, 0.003665, 0.014946, 0.002255, 0.002993, 0.013488, 0.018479, 0.039399, 0.016480, 0.007719, 0.026413, 0.006761, 0.013116, 0.033503]
])


def portfolio_sd_func(weights):
    weights_row = np.array([weights])
    weights_col = np.array(weights).reshape(len(weights), 1)

    return math.sqrt(weights_row.dot(P_VAR_COVAR_MATRIX).dot(weights_col))


def minimze_sd_func():
    row, col = P_VAR_COVAR_MATRIX.shape
    initial_guess = [1 / row] * row
    bounds = ((0, None),) * row
    constraints = ({'type': 'eq', 'fun': lambda w: sum(w) - 1},)

    return minimize(portfolio_sd_func, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)


if __name__ == '__main__':
    print(minimze_sd_func())