import math
from itertools import combinations
import mpmath
import matplotlib.pyplot as plt


def my_foo(val):
    return (math.tanh(val)+1)/2 >= 0.5


def proizv_my_foo(val):
    return (mpmath.sech(val)**2)/2



def step_foo(val):
    return val>=0


def proizvod_step(val):
    return 1


def net_culc(W, X):
    net = 0
    for i in range(1, 5):
        net += W[i]*X[i]+W[0]
    return net



def generate_bool_foo(n: int):
    return [1]+list(map(int, list(bin(n)[2:].zfill(4))))


def learning(W, active_foo, proizvod_foo, name):
    n = 0.3
    err_prev = math.inf

    print(name)
    e=[]
    for j in range(50):
        err = 0
        for i in range(16):
            X = generate_bool_foo(i)
            # print(X)
            net= net_culc(W, X)
            out = active_foo(net)
            dt = proizvod_foo(net)
            sigma = IDEALVALUE[i]-out
            for k in range(5):
                W[k] += n*sigma*dt*X[k]
            err+=abs(sigma)
        print(f'{j} epoch: W={W}, Err={err}')
        if err_prev == 0 and err == 0:
            break
        e.append(err)
        err_prev = err
    print(f'Конечные веса: {W}')
    return e


def learn_part(n=4, epohs=200):
    bool_vals = [generate_bool_foo(i) for i in range(2**n)]
    # s = [(y, x) for y, x in zip(IDEALVALUE, bool_vals)]
    val = [i for i in range(16)]
    for i in range(2, 16):
        combin = combinations(val, i)
        for items in combin:
            W = [0]*5
            err_prev = math.inf
            for j in range(epohs):
                err = 0
                for item in items:
                    X = bool_vals[item]
                    net= net_culc(W, X)
                    out = my_foo(net)
                    dt = proizv_my_foo(net)
                    # print(sigma)
                    sigma = IDEALVALUE[item]-out
                    for k in range(5):
                        W[k] += 0.3*sigma*dt*X[k]
                    err+=abs(sigma)
                if err_prev == 0 and err == 0:
                    err1 = 0
                    for m in range(16):
                        net=net_culc(W, bool_vals[m])
                        out = int(my_foo(net))
                        sigma = IDEALVALUE[m]-out
                        err1 += abs(sigma)
                    if err1 == 0:
                        return items
                err_prev=err
                
def print_min_part():
    items = learn_part()
    print(items)
    W =[0]*5
    err_prev = math.inf
    e=[]
    for i in range(200):
        err = 0
        for item in items:
            X = generate_bool_foo(item)
            # print(X)
            net= net_culc(W, X)
            out = my_foo(net)
            dt = proizv_my_foo(net)
            sigma = IDEALVALUE[item]-out
            for k in range(5):
                W[k] += 0.3*sigma*dt*X[k]
            err+=abs(sigma)
        print(f'{i} epoch: W={W}, Err={err}')
        e.append(err)
        if err_prev == 0 and err == 0:
            break
        err_prev = err
    print(f'Конечные веса W={W}')
    return e, len(items)
        


def show_e(e, name='Функция E(k)', x='k', y = 'E'):
    fig, ax = plt.subplots()
    ax.plot([i for i in range(len(e))], e)
    plt.title(name)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid(True)
    plt.show()


W = [0]*5
IDEALVALUE = list(map(int, list(str(1111100011111111))))

if __name__ == "__main__":
    e = learning(W, step_foo, proizvod_step, 'Функция активации -- step:')
    W = [0]*5
    show_e(e, name=f'Зависимость E от k для step функции на всех значениях ')
    e = learning(W, my_foo, proizv_my_foo, 'Функция активации, заданная в 3 варианте.')
    show_e(e, name=f'Зависимость E от k для функции 3его варианта на всех значениях')
    print('Определение минимального набора на котором можно обучить сеть')
    e, l = print_min_part()
    show_e(e, name=f'Зависимость E от k при {l} значениях')