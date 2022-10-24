###############################################i#######################################
###################################### run_nn.py ######################################
#!/usr/bin/env python
try:
    import sys
    sys.path.insert(0, './neural_network_chuck/')
    import neuralnetworks1 as nn
    import random
    import math
    import os
    import getopt
    import pygame
    import numpy as np
    import utils
    from car import *
    import pdb
    import webcolors
    import logging
    from car_config import *
    import pickle
    import random
    import matplotlib.pyplot as plt
    # Imports constants/colors from Pygame
    from pygame.locals import *
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

def create_test_train(X, T, N):
    choice_vector = range(N)
    random.shuffle(choice_vector)
    n_train = int(N*NN_TRAIN_FRACTION)
    X_train = X[choice_vector[:n_train], :]
    T_train = T[choice_vector[:n_train]]
    X_test = X[choice_vector[n_train:], :]
    T_test = T[choice_vector[n_train:]]

    return X_train, T_train, X_test, T_test

def plot_graphs(X,T,N, num_dimensions):
    points_in_hidden_layer = 30
    number_of_avg = 20
    percentage_incorrect_arr = []

    for nh in range(1, points_in_hidden_layer + 1):
        nnet1 = nn.NeuralNetworkClassifier(num_dimensions, nh,2)
        avg_percentage_incorrect_arr = []
        for _ in range(number_of_avg):
            X_train, T_train, X_test, T_test = create_test_train(X,T,N)
            nnet1.train(X_train,T_train[:,None], nIterations=1000)
            avg_percentage_incorrect_arr.append\
                (np.mean(np.absolute(np.squeeze(nnet1.use(X_test)) - T_test)))
        percentage_incorrect_arr.append\
            (np.mean(np.array(avg_percentage_incorrect_arr)))


    plt.plot(range(1,points_in_hidden_layer+1), percentage_incorrect_arr)
    plt.xlabel("Number of hidden units")
    plt.ylabel("Fraction Incorrect")
    plt.title("Variation of Incorrect predictions with hidden units")
    plt.savefig("percentage_correct_nh.png")

    with open("percentage_correct_nh.fig", "w") as f:
        pickle.dump(plt.gcf(), f)

    plt.show()

def plot_bt(nnet):
    plt.plot(nnet.getErrorTrace(), lw=2)
    plt.title('Neural Network Error')
    plt.xlabel("Number of iterations")
    plt.ylabel("RMSE")
    plt.savefig("rmse_iter.png")
    # plt.show()


def run_nn():
    with open(PICKLE_FILE) as f:
        other_cars, user_car = pickle.load(f)
    T = []
    user_car_y = []
    other_car_size = []
    for other_car, user_car in zip(other_cars, user_car):
        user_car_y.append(user_car[1])
        T.append(user_car[2])
        other_car_size.append(len(other_car))

    user_car_ys = np.vstack((np.array(user_car_y) - TOP_SCREEN[1][1],
                             TOP_SCREEN[1][1]
                             + BOTTOM_SCREEN[1][1] - np.array(user_car_y))). T

    num_dimensions = max(other_car_size)*2 + 2
    X = np.ones((len(T),num_dimensions - 2))
    X[:, 0::2] = np.ones((len(T),num_dimensions - 2))[:,0::2]*NN_FILLER_VALUE[0]
    X[:, 1::2] = X[:,1::2]*NN_FILLER_VALUE[1]
    N = len(T)
    T = np.array(T)

    i = 0
    for other_car in other_cars:
        dim = 0
        for o_car in other_car:
            X[i][dim] = o_car[0]  # x dim remains the same
            X[i][dim + 1] = o_car[1] - user_car_y[i]
            dim += 2
        i += 1

    X = np.hstack((user_car_ys, X))
    T_non_zero = ((T == NO_MOVE) == False)
    X = X[T_non_zero, :]
    T = T[T_non_zero]
    N = T.shape[0]
    X_train, T_train, X_test, T_test = create_test_train(X,T,N)

    nnet = nn.NeuralNetworkClassifier(num_dimensions, NN_HIDDEN_LAYER,2)
    nnet.train(X_train,T_train[:,None], nIterations=1000)
    Y = np.squeeze(nnet.use(X_test))
    print("RMSE: %s" %np.sqrt(np.mean((Y-T_test)**2)))
    # plot_graphs(X,T,N, num_dimensions)
    # nnet.draw()
    # plt.savefig("nnet.png")
    # plot_bt(nnet)
    return nnet, num_dimensions

if __name__ == '__main__':
    run_nn()



