from matplotlib import pyplot as plt
import pandas as pd

def get_data(t, i):
    lst = []
    loc = 0

    while True:
        loc = t.find(i, loc)

        if loc != -1:
            end = t.find('\n', loc)
            lst.append(float(t[loc:end].strip().split(':')[1].strip()))
            loc = end
        else:
            break

    return lst

if __name__ == '__main__':
    with open('game.log') as f:
        t = f.read()
        
        Delicacies1 = get_data(t, 'Paris Delicacies Price')
        Delicacies2 = get_data(t, 'Moscow Delicacies Price')
        Delicacies3 = get_data(t, 'Cairo Delicacies Price')
        Delicacies4 = get_data(t, 'Gao Delicacies Price')
        Delicacies5 = get_data(t, 'Mogadishu Delicacies Price')
        Delicacies6 = get_data(t, 'Delhi Delicacies Price')
        Delicacies7 = get_data(t, 'Malacca Delicacies Price')
        Delicacies8 = get_data(t, 'Nanking Delicacies Price')
        Delicacies9 = get_data(t, 'Mexico Delicacies Price')
        Delicacies10 = get_data(t, 'Cusco Delicacies Price')
        itr = range(1, len(Delicacies1) + 1)

        plt.plot(itr, Delicacies1, label="Paris")
        plt.plot(itr, Delicacies2, label="Moscow")
        plt.plot(itr, Delicacies3, label="Cairo")
        plt.plot(itr, Delicacies4, label="Gao")
        plt.plot(itr, Delicacies5, label="Mogadishu")
        plt.plot(itr, Delicacies6, label="Delhi")
        plt.plot(itr, Delicacies7, label="Malacca")
        plt.plot(itr, Delicacies8, label="Nanking")
        plt.plot(itr, Delicacies9, label="Mexico")
        plt.plot(itr, Delicacies10, label="Cusco")

        plt.legend(loc=2, ncol=2)

        plt.show()
