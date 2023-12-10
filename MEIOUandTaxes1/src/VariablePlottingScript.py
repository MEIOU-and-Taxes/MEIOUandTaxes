import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# This script transforms the VariablesPerIDP File into a proper array (data) which stores all variables
# The variables are sorted by the province ID, note here, python starts at 0 as index, therefore
# there will be an empty value at the index 0.

# Make sure you run this file from a console to see errors related from python if you change smth
# This can take a while to run. Its just a massive workload to go through

# TODO: Add Axis descriptions
# TODO: Add code for plotting for certain IDP ranges, for example from 1000 - 2000

dataFile = open("VariablesPerIDP.py", 'r')

dataLines = dataFile.readlines()

data = {}

for tmpLine in dataLines:
    split1 = tmpLine.split('=')
    if len(split1) == 2:
        value = float(split1[1])

        split2 = split1[0].split('[')
        variable = split2[0]

        idp = int(split2[1][:-1])

        #print(variable, idp, value)

        if variable not in data:
            data[variable] = []

        while len(data[variable]) <= idp:
            data[variable].append(0.0)
        
        data[variable][idp] = value
        


# After converting everything into the array its now saved as Data with the variable and the idp

# Follow the keys.txt file in the MEIOUandTaxes1 folder to know which variable represents what. 
# For plotting a single variable one can use this simple code:

#plt.plot(data['abr'], 'bo') # abr for pixelsize
#plt.show()


Cont = np.array(data['aae'])
ContIDP = np.nonzero((Cont == 41) | (Cont == 58))

print(ContIDP) 

# For more complex calculations we need to convert the data into a numpy array
# numpy takes over stuff like multiplications or divisions

tmpNp = np.array(data['abt'])
tmpNp2 = np.array(data['alp'])

# However in case of division, the potential zero's or Nones can lead to problems within the variables.
# Therefore it might be necessary to set variables close 0 or 0 to a fixed value:

# In case you want to know which variables are going to be adjusted by the piece of code
# This will print the relevant indices, therefore province IDs.

#indices = np.nonzero(tmpNp2 <0.5)
#print(indices)

#tmpNp[tmpNp < 1 ] = 100
#tmpNp2[tmpNp2 < 1] = 1 # Sets everything below 1 to a 1.

# Numpy can follow simple mathematical formulas, like this one for a division.
TestContIDP = np.reshape(ContIDP, -1)

DivTest = tmpNp[TestContIDP] - tmpNp2[TestContIDP]
#print(DivTest)

# In case you want to know which values are above a certain value or below, just activate this bit
#indices = np.nonzero(DivTest > 20)
#print(indices)

print(TestContIDP)

#plt.plot(TestContIDP, tmpNp[TestContIDP], 'go') 
#plt.plot(TestContIDP, tmpNp2[TestContIDP], 'bs')
#plt.plot(TestContIDP, DivTest, 'yx')

plt.plot(tmpNp[TestContIDP], 'go') 
plt.plot(tmpNp2[TestContIDP], 'bs')
plt.plot(DivTest, 'yx')


#plt.set_xticklabels(TestContIDP)
#plt.xticks(TestContIDP)
#plt.xscale('log')

plt.show()