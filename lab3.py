import numpy as np
import matplotlib.pyplot as plt


def x_calc(X):
    return [np.exp(x-1) for x in X]

def vidr_hoff(x, q, n):
    return n*q*x

def net(X, W):
    return sum([w*x for x, w in zip(X,W)])

def mse(x_defined, x_calculated):
    return sum([(x_d-x_c)**2 for x_d, x_c in  zip(x_defined, x_calculated)])**0.5


def method_sliding_window(N, n, X, m, p):
    W = [0]*p
    X_pred = [0]*20
    for k in range(m):
        # print('li')
        for i in range(p, N):
            X_pred[i] = sum([w*x for w, x in zip(W, X[i-p:i])])
            diff = X[i]-X_pred[i]
            # print(diff)
            for j in range(p):
                W[j]+=vidr_hoff(X[i-p+j], n, diff)

    return X_pred, W

def predict_x_define_e(N, n, X_right, m, p):
    X_pred, W = method_sliding_window(N, n, X_right, m, p)
    X_pred.extend(np.zeros(N))
    for i in range(N, 2*N):
        X_pred[i] = sum([w*x for w, x in zip(W, X_right[i-p:i])])
        e = (mse(X_right[N:], X_pred[N:]))

    return e, X_pred


def drow_foo_to_compare(X_d, T_d, X_p, center, ishod, y, x, name):
    fig, ax = plt.subplots()
    ax.plot(T_d, X_d)
    ax.plot(T_d, X_p, 'o')
    plt.title(name)
    plt.xlabel(x)
    plt.ylabel(y)
    if not ishod:
        plt.axvline(x=center, linestyle='--')
    plt.grid(True)
    plt.show()


def drow_e(e, param, x, y, name):
    fig, ax = plt.subplots()
    ax.plot(param, e)
    ax.plot(param, e, 'o')
    plt.title(name)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":


    a = -2
    b = 2
    N = 20
    n = 0.3
    p = 4


    t = list(np.linspace(a, 2*b-a, 2*N))
    X=x_calc(t)# значение функции на [a,b]


    # Исходная функция
    drow_foo_to_compare(X[:20], t[:20], X[:20], b, True, 'x', 't', 'X(t)')


    _, X_p = predict_x_define_e(N, n, X, 1, p)
    # сравнение исходной функции и предсказанной при n=0.3, p=4 и одной эпохе обучения
    drow_foo_to_compare(X, t, X_p, b, False, 'x', 't', 'X(t)')


    err = []
    # вычисление ошибки для разных размеров окн
    for i in range(1, 17): # для большего размера не вычисляет
        e, X_p = predict_x_define_e(N, n, X, 8000, i)
        err.append(e)
    drow_e(err, [i for i in range(1, 17)], 'p', 'E', 'E(p) при m =8000 n = 0.3')
    err.clear()


    # вычисление ошибки для разого кол-ва обучающих эпох
    for i in range(1, 20, 1):
        e, X_p = predict_x_define_e(N, n, X, i, 4)
        err.append(e)
    drow_e(err, [i for i in range(1, 20, 1)], 'm', 'E', 'E(m) при p = 4, n = 0.3')