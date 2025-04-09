from matplotlib import pyplot as plt
import os

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

def read_and_concatenate_old_logs(directory='.'):
    concatenated_text = ''
    for file_name in sorted(os.listdir(directory)):
        if file_name.startswith('game_') and file_name.endswith('.log') and file_name != 'game.log':
            with open(file_name, 'r') as f:
                concatenated_text += f.read()
    return concatenated_text

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
        
        wealth = get_data(t, 'Total Wealth')
        wealth2 = get_data(t, 'Infra Wealth')
        itr = range(1, len(wealth) + 1)
        
        # Get data from WealthChange
        TradeValue = get_data(t, 'WealthChange Trade Value')
        Gold = get_data(t, 'WealthChange Gold')
        Property = get_data(t, 'WealthChange Property')
        Wages = get_data(t, 'WealthChange Wages')
        Infra = get_data(t, 'WealthChange Infra')
        Manpower = get_data(t, 'WealthChange Manpower')
        StateInc = get_data(t, 'WealthChange StateInc')
        ExtraTax = get_data(t, 'WealthChange ExtraTax')

        # Create subplots: 2 rows and 1 column
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

        # Plot Wealth on the first subplot
        lines1 = []
        lines1.append(ax1.plot(itr, wealth, label="Wealth")[0])
        lines1.append(ax1.plot(itr, wealth2, label="Infra Wealth")[0])
        ax1.set_ylabel("Wealth Value")
        ax1.grid(True)

        # Plot WealthChange on the second subplot
        lines2 = []
        lines2.append(ax2.plot(itr, TradeValue, label="Trade Value", linestyle='-')[0])
        lines2.append(ax2.plot(itr, Gold, label="Gold", linestyle='-')[0])
        lines2.append(ax2.plot(itr, Property, label="Property", linestyle='-')[0])
        lines2.append(ax2.plot(itr, Wages, label="Wages", linestyle='-')[0])
        lines2.append(ax2.plot(itr, Infra, label="Infra", linestyle='-')[0])
        lines2.append(ax2.plot(itr, Manpower, label="Manpower", linestyle='-')[0])
        lines2.append(ax2.plot(itr, StateInc, label="State Income", linestyle='-')[0])
        lines2.append(ax2.plot(itr, ExtraTax, label="Special Taxes", linestyle='-')[0])
        ax2.set_ylabel("Wealth Change Components")
        ax2.set_xlabel("Iteration")
        ax2.grid(True)

        # Create legends for both subplots
        legend1 = ax1.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), ncol=1, borderaxespad=1, fontsize='medium', frameon=True)
        legend2 = ax2.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), ncol=1, borderaxespad=1, fontsize='medium', frameon=True)

        # Adjust the subplot parameters to make room for the legend on the right
        plt.subplots_adjust(right=0.9)

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

        plt.suptitle("Total Wealth and Wealth Change Components Over Time")
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()
