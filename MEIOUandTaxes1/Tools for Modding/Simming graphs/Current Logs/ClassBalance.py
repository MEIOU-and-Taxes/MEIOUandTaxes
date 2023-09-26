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
        
        PeasantI = get_data(t, 'Peasant Income Total')
        PeasantS = get_data(t, 'Peasant Spend Total')
        NomadI = get_data(t, 'Nomad Income Total')
        NomadS = get_data(t, 'Nomad Spend Total')
        ResidentI = get_data(t, 'Resident Income Total')
        ResidentS = get_data(t, 'Resident Spend Total')
        NobleI = get_data(t, 'Noble Income Total')
        NobleS = get_data(t, 'Noble Spend Total')
        BurgherI = get_data(t, 'Burgher Income Total')
        BurgherS = get_data(t, 'Burgher Spend Total')
        ClergyI = get_data(t, 'Clergy Income Total')
        ClergyS = get_data(t, 'Clergy Spend Total')
        itr = range(1, len(PeasantI) + 1)
        PeasantI = [PeasantI[i]-PeasantS[i] for i in range(len(PeasantI))]
        NomadI = [NomadI[i]-NomadS[i] for i in range(len(PeasantI))]
        ResidentI = [ResidentI[i]-ResidentS[i] for i in range(len(PeasantI))]
        NobleI = [NobleI[i]-NobleS[i] for i in range(len(PeasantI))]
        BurgherI = [BurgherI[i]-BurgherS[i] for i in range(len(PeasantI))]
        ClergyI = [ClergyI[i]-ClergyS[i] for i in range(len(PeasantI))]

        plt.plot(itr, PeasantI, label="Peasants")
        plt.plot(itr, NomadI, label="Nomads")
        plt.plot(itr, ResidentI, label="Residents")
        plt.plot(itr, NobleI, label="Nobles")
        plt.plot(itr, BurgherI, label="Burghers")
        plt.plot(itr, ClergyI, label="Clergy")

        plt.legend(loc=2, ncol=2)

        plt.show()
