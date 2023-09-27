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

import os
def read_and_concatenate_old_logs(directory='.'):
    concatenated_text = ''
    for file_name in sorted(os.listdir(directory)):
        if file_name.startswith('game_') and file_name.endswith('.log') and file_name != 'game.log':
            with open(file_name, 'r') as f:
                concatenated_text += f.read()
    return concatenated_text

if __name__ == '__main__':
    with open('game.log') as f:
        t = read_and_concatenate_old_logs()
        t += f.read()
        
        PeasantI = get_data(t, 'Peasant Income Property')
        PeasantS = get_data(t, 'Peasant Spend Property')
        NomadI = get_data(t, 'Nomad Income Property')
        NomadS = get_data(t, 'Nomad Spend Property')
        ResidentI = get_data(t, 'Resident Income Property')
        ResidentS = get_data(t, 'Resident Spend Property')
        NobleI = get_data(t, 'Noble Income Property')
        NobleS = get_data(t, 'Noble Spend Property')
        BurgherI = get_data(t, 'Burgher Income Property')
        BurgherS = get_data(t, 'Burgher Spend Property')
        ClergyI = get_data(t, 'Clergy Income Property')
        ClergyS = get_data(t, 'Clergy Spend Property')
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
