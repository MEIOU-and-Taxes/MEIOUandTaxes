from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

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

#def calculate_correlations(prices, wealth_vars):
#    all_vars = prices + wealth_vars
#    
#    # Ensure all variables are of the same length by truncating to the shortest length
#    min_length = min(len(var) for var in all_vars)
#    print(f"Minimum length of data arrays: {min_length}")
#    
#    # Ensure we have enough data points
#    if min_length <= 1:
#        raise ValueError("Insufficient data points to calculate correlations. Data arrays are too short.")
#    
#    aligned_vars = [np.array(var[:min_length]) for var in all_vars]
#    
#    # Check for NaN values or zero variation in any of the variables
#    for idx, var in enumerate(aligned_vars):
#        if len(var) == 0:
#            print(f"Variable {idx} ({labels[idx]}) is empty.")
#        if np.std(var) == 0:
#            print(f"Variable {idx} ({labels[idx]}) has zero variation.")
#    
#    # Stack the variables vertically to ensure they are aligned correctly for correlation calculation
#    stacked_vars = np.vstack(aligned_vars)
#    correlation_matrix = np.corrcoef(stacked_vars)
#    return correlation_matrix

def calculate_correlations(prices, wealth_vars):
    correlation_matrix = np.corrcoef(prices + wealth_vars)
    return correlation_matrix

if __name__ == '__main__':
    with open('game.log') as f:
        t = read_and_concatenate_old_logs()
        t += f.read()
        
        food = get_data(t, 'Global Food Price')
        salt = get_data(t, 'Global Salt Price')
        fiber = get_data(t, 'Global Fiber Price')
        fuel = get_data(t, 'Global Fuel Price')
        raw = get_data(t, 'Global Raw Material Price')
        timber = get_data(t, 'Global Timber Price')
        exotic = get_data(t, 'Global Exotics Price')
        consumer = get_data(t, 'Global Consumer Product Price')
        military = get_data(t, 'Global Military Product Price')
        naval = get_data(t, 'Global Naval Product Price')
        industrial = get_data(t, 'Global Industrial Product Price')
        luxury = get_data(t, 'Global Luxury Product Price')
        knowledge = get_data(t, 'Global Knowledge Price')
        wealth = get_data(t, 'Prod Leak Test')
        wealth2 = get_data(t, 'Tax Leak Test')
        wealth3 = get_data(t, 'Expected Wealth Change')
        wealth4 = get_data(t, 'Expected Income Spend')
        wealth5 = get_data(t, 'Infra Leak Test ')
        wealth6 = get_data(t, 'Tariff_Income')
        itr = range(1, len(food) + 1)

        print(wealth5)
        

        # Combining price lists and wealth variables
        price_vars = [food, salt, fiber, fuel, raw, timber, exotic, consumer, military, naval, industrial, luxury, knowledge]
        wealth_vars = [wealth, wealth2, wealth3, wealth4, wealth5, wealth6]
        labels = ['Food', 'Salt', 'Fiber', 'Fuel', 'Raw', 'Timber', 'Exotics', 'Consumer', 
                'Military', 'Naval', 'Industrial', 'Luxury', 'Knowledge', 
                'Prod Leak', 'Tax Leak', 'Expected Wealth', 'Expected Income', 'Infra Leak', 'Tariff Income']

        correlation_matrix = calculate_correlations(price_vars, wealth_vars)

        # Convert correlation matrix to DataFrame for better readability
        df_corr = pd.DataFrame(correlation_matrix, index=labels, columns=labels)

        # Display the correlation matrix
        print(df_corr)

        # Optionally, you can plot the correlation matrix as a heatmap
        plt.figure(figsize=(10, 8))
        plt.imshow(df_corr, cmap='coolwarm', interpolation='none')
        plt.colorbar()
        plt.xticks(range(len(labels)), labels, rotation=90)
        plt.yticks(range(len(labels)), labels)
        plt.title('Correlation Matrix')
        plt.show()