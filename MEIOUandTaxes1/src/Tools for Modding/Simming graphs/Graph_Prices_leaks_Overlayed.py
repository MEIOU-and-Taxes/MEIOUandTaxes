from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import mplcursors


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

def toggle_visibility(event, line_map):
    """Toggle the visibility of a line when the legend is clicked."""
    legend_item = event.artist
    label = legend_item.get_label()  # Get the label of the legend item
    if label in line_map:
        orig_line = line_map[label]
        visible = not orig_line.get_visible()
        orig_line.set_visible(visible)
        # Adjust legend item transparency based on line visibility
        legend_item.set_alpha(1.0 if visible else 0.2)
        event.canvas.draw()

if __name__ == '__main__':
    # Ensure the script is running from the directory where the game.log file is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)
    
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

        # Create subplots: 2 rows and 1 column
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

        # Plot Prices on the first subplot
        lines1 = []
        lines1.append(ax1.plot(itr, food, label="Food")[0])
        lines1.append(ax1.plot(itr, salt, label="Salt")[0])
        lines1.append(ax1.plot(itr, fiber, label="Fiber")[0])
        lines1.append(ax1.plot(itr, fuel, label="Fuel")[0])
        lines1.append(ax1.plot(itr, raw, label="Raw")[0])
        lines1.append(ax1.plot(itr, timber, label="Timber")[0])
        lines1.append(ax1.plot(itr, exotic, label="Exotics")[0])
        lines1.append(ax1.plot(itr, consumer, label="Consumer")[0])
        lines1.append(ax1.plot(itr, military, label="Military")[0])
        lines1.append(ax1.plot(itr, naval, label="Naval")[0])
        lines1.append(ax1.plot(itr, industrial, label="Industrial")[0])
        lines1.append(ax1.plot(itr, luxury, label="Luxury")[0])
        lines1.append(ax1.plot(itr, knowledge, label="Knowledge")[0])
        ax1.set_ylabel("Price Value")
        ax1.grid(True)

        # Plot Wealth/Leak Variables on the second subplot
        lines2 = []
        lines2.append(ax2.plot(itr, wealth, label="Prod Leak", linestyle='--')[0])
        lines2.append(ax2.plot(itr, wealth2, label="Tax Leak", linestyle='--')[0])
        lines2.append(ax2.plot(itr, wealth3, label="Expected Wealth", linestyle='--')[0])
        lines2.append(ax2.plot(itr, wealth4, label="Expected Income", linestyle='--')[0])
        lines2.append(ax2.plot(itr, wealth5, label="Infra Leak", linestyle='--')[0])
        lines2.append(ax2.plot(itr, wealth6, label="Tariff Income", linestyle='--')[0])
        ax2.set_ylabel("Wealth/Leak Value")
        ax2.set_xlabel("Iteration")
        ax2.grid(True)

        # Create legends for both subplots
        legend1 = ax1.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=2)
        legend2 = ax2.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=2)

        # Map each legend label to the corresponding plot line
        line_map1 = {line.get_label(): line for line in lines1}
        line_map2 = {line.get_label(): line for line in lines2}

        def on_pick(event, line_map):
            """Handle pick events for both text and lines."""
            legend_item = event.artist
            if isinstance(legend_item, plt.Line2D):  # Legend line
                toggle_visibility(event, line_map)
            elif isinstance(legend_item, plt.Text):  # Legend text
                label = legend_item.get_text()
                if label in line_map:
                    orig_line = line_map[label]
                    visible = not orig_line.get_visible()
                    orig_line.set_visible(visible)
                    # Adjust legend item transparency based on line visibility
                    legend_item.set_alpha(1.0 if visible else 0.2)
                    event.canvas.draw()

        # Connect the legends to the toggle function
        fig.canvas.mpl_connect('pick_event', lambda event: on_pick(event, line_map1))
        fig.canvas.mpl_connect('pick_event', lambda event: on_pick(event, line_map2))

        # Make legend items clickable (both lines and text)
        for legend_item in legend1.get_lines() + legend1.get_texts():
            legend_item.set_picker(True)  # Enable picking for the legend items

        for legend_item in legend2.get_lines() + legend2.get_texts():
            legend_item.set_picker(True)

        plt.suptitle("Global Prices and Wealth Variables Over Time")
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()