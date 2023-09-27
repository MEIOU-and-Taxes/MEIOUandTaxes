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
        
        #Direct = get_data(t, 'BUTax Direct')
        #Indirect = get_data(t, 'BUTax Indirect')
        #Revenue = get_data(t, 'BUTax Revenue')
        #Total = get_data(t, 'BUTax Total')
        Fees = get_data(t, 'BUTax Fees')
        Rents = get_data(t, 'BUTax Rents')
        Obligations = get_data(t, 'BUTax Obligations')
        Poll = get_data(t, 'BUTax Poll')
        Land = get_data(t, 'BUTax Land')
        PropertyBU = get_data(t, 'BUTax PropertyBU')
        Chattel = get_data(t, 'BUTax Chattel')
        Inheritance = get_data(t, 'BUTax Inheritance')
        TollBU = get_data(t, 'BUTax TollBU')
        SaltBU = get_data(t, 'BUTax SaltBU')
        SubstancesBU = get_data(t, 'BUTax SubstancesBU')
        TimberBU = get_data(t, 'BUTax TimberBU')
        AlcoholBU = get_data(t, 'BUTax AlcoholBU')
        ForestBU = get_data(t, 'BUTax ForestBU')
        #Corruption = get_data(t, 'BUTax Corruption')
        #Farming = get_data(t, 'BUTax Farming')
        Special = get_data(t, 'BUTax Special')
        Commerce = get_data(t, 'BUTax Commerce')
        BUProperty = get_data(t, 'BUTax BUProperty')
        itr = range(1, len(Poll) + 1)

        #plt.plot(itr, Direct, label="Direct", linestyle='--')
        #plt.plot(itr, Indirect, label="Indirect", linestyle='--')
        #plt.plot(itr, Revenue, label="Revenue", linestyle='--')
        #plt.plot(itr, Farming, label="Rev Farming", linestyle='--')
        #plt.plot(itr, Corruption, label="Corruption", linestyle='--')
        #plt.plot(itr, Total, label="Total")
        plt.plot(itr, Obligations, label="Elite Obligations", linestyle='--')
        #plt.plot(itr, BUProperty, label="Property Income", linestyle='--')
        plt.plot(itr, Fees, label="Generic Fees", linestyle='--')
        plt.plot(itr, Rents, label="Feudal Rents", linestyle='--')
        plt.plot(itr, ForestBU, label="Forest Rents", linestyle='--')
        plt.plot(itr, Poll, label="Poll Tax", linestyle='--')
        plt.plot(itr, Land, label="Land Tax", linestyle='--')
        plt.plot(itr, PropertyBU, label="Property Tax", linestyle='--')
        plt.plot(itr, Chattel, label="Chattel Tax")
        plt.plot(itr, Inheritance, label="Inheritance Tax")
        plt.plot(itr, TollBU, label="Tolls")
        plt.plot(itr, SaltBU, label="Salt Excise")
        plt.plot(itr, SubstancesBU, label="Substances Excise")
        plt.plot(itr, TimberBU, label="Timber Excise")
        plt.plot(itr, AlcoholBU, label="Alcohol Excise")
        plt.plot(itr, Special, label="Special Taxes")
        plt.plot(itr, Commerce, label="Commerce Fees")

        plt.legend(loc=2, ncol=2)

        plt.show()
