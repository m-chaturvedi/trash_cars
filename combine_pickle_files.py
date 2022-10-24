__author__ = 'chaturvedi'

import pickle

file_1 = 'log_pickle_1.log'
file_2 = 'log_pickle_2.log'
file_comb = 'log_pickle_tmp.log'

if __name__ == '__main__':
    with open(file_1) as f1:
        other_cars, user_cars = pickle.load(f1)

    with open(file_2) as f2:
        other_cars_2, user_cars_2 = pickle.load(f2)

    other_cars += other_cars_2
    user_cars += user_cars_2

    with open(file_comb, 'w+') as f:
        pickle.dump([other_cars, user_cars], f)
