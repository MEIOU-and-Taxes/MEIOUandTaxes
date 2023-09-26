from matplotlib import pyplot as plt
import pandas as pd

def get_data(t, i):
    lst = []
    loc = 0

    while True:
        loc = t.find(i, loc)

        if loc != -1:
            end = t.find('\n', loc)
            lst.append(float(t[loc:end].strip().split(':')[1].strip().split("£")[-1]))
            loc = end
        else:
            break

    return lst

if __name__ == '__main__':
    with open('game.log') as f:
        t = f.read()
        
        Class = get_data(t, 'Class Pop Total')

        itr = range(1, len(Class) + 1)

        plt.plot(itr, Class, label="Total")
        

        plt.title("Total Pop Worldwide")
        plt.ylim(bottom=3500)
        plt.legend(loc=2, ncol=2)

        plt.show()
