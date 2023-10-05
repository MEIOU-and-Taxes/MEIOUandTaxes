try:
    import os
    os.chdir(os.path.dirname(__file__))

    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.widgets import Button
    from functools import partial
    import glob

    fig, ax = plt.subplots(num="MEIOU and Taxes - Sim graphs", figsize = (16, 9))
    ax.show = lambda: None #type:ignore

    def menu(msg=None):
        ax.clear()
        ax.set_title('Menu')
        ax.text(0.5, 0.5, horizontalalignment='center', verticalalignment='center', s="""\

Welcome to the M&T sim graphing tool!

Select the graph you want to see below.
Use the buttons at the top right to change
graph option pages.
Refresh to read game.log again.
    """.strip())
        if msg:
            ax.text(0.5, 0.5, msg)
        plt.draw()
    menu()

    colors = {
        'r': ('tab:red', 'lightcoral'),
        'g': ('limegreen', 'palegreen'),
        'c': ('turquoise', 'paleturquoise'),
        'y': ('yellow', 'lightgoldenrodyellow'),
        'b': ('deepskyblue', 'lightskyblue'),
        'l': ('silver', 'gainsboro'),
        'd': ('grey', 'lightgrey'),
        'p': ('mediumorchid', 'violet'),
        'o': ('sandybrown', 'navajowhite'),
        'i': ('whitesmoke', 'slategray'),
    }

    # Reading data

    def get_data(_, i):
        lst = []
        loc = 0

        while True:
            loc = data.find(i, loc)

            if loc != -1:
                end = data.find('\n', loc)
                lst.append(float(data[loc:end].strip().split(':')[1].strip().split("£")[-1]))
                loc = end
            else:
                break

        return np.array(lst)

    # Highly cursed
    import all_graphs
    all_graphs.get_data = get_data
    graphs = {func.__name__.removeprefix('graph').replace('_', ' '): (func.__doc__, func) for name in dir(all_graphs) if (func := getattr(all_graphs, name)) and name.lower().startswith('graph')}

    # Read file(s)

    def read_all_logs():
        text = ''
        files = glob.glob("game_*.log")
        files.sort(key=lambda x: int(x[5:-4]))
        for fn in files:
            with open(fn, 'r') as f:
                text += f.read()
        logs = len(files)
        try:
            with open('game.log', 'r') as f:
                text += f.read()
                logs += 1
        except FileNotFoundError:
            print("WARNING: Could not find game.log")
        print(f'Read {logs} log file{"" if logs == 1 else "s"}')
        return files, text

    logs, data = read_all_logs()

    # Positioning of buttons and the like

    pages = []
    with open('graph_pages.csv', 'r') as f:
        page = []
        for line in f:
            line = line[:-1]
            if not line:
                continue
            if line.startswith(':'):
                if page:
                    pages.append(page)
                    page = []
            else:
                page.append([x.rstrip() for x in line.split(';')])
        if page:
            pages.append(page)
        del page
    hpad = 0.0125
    vpad = 0.0125
    vsizemin = 0.04

    max_rows = max((len(page) for page in pages))
    max_height = max_rows * vsizemin + (max_rows + 1) * vpad
    if max_height + 0.04 > 0.45:
        raise ValueError('Too many rows/vsizemin too large!')
    plt.subplots_adjust(left=0.05, right=0.95, bottom=max_height + 0.04, top=0.925)

    # Plotting evil deeds

    def plot_new(_, graph, title):
        ax.clear()
        try:
            graph(data, ax)
            ax.legend(loc=2, ncol=2)
        except Exception as e:
            ax.text(0.5, 0.5, f'Error:\n{e}', horizontalalignment='center', verticalalignment='center')
        ax.set_title(title)
        plt.draw()

    done = set()
    color = None
    for pi, page in enumerate(pages):
        height_page = (max_height - vpad * (len(page)+1)) / len(page)
        for ri, row in enumerate(page):
            width_row = (1 - hpad * (len(row) + 1)) / len(row)
            vpos = (len(page) - ri - 1) * (height_page + vpad) + vpad
            for si, slot in enumerate(row):
                if not slot:
                    continue
                if slot[-2] == ':':
                    color = slot[-1]
                    slot = slot[:-2]
                if slot not in graphs:
                    raise ValueError(f'Unknown entry: "{slot}"\nCould not find function "graph{slot.replace(" ", "_")}"')
                if slot in done:
                    raise ValueError(f'Duplicate entry: "{slot}"\nSecond occurrence in page {pi+1}')
                pos = plt.axes((
                    si * width_row + hpad * (si + 1),
                    vpos,
                    width_row,
                    height_page
                ))
                pos.set_visible(False)
                if color:
                    try:
                        btn = Button(pos, slot, None, *colors[color])
                    except KeyError:
                        print(f'WARNING: Unknown color {color} used for {slot}')
                        btn = Button(pos, slot, None, *colors['l'])
                    color = None
                else:
                    btn = Button(pos, slot, None, *colors['l'])
                btn.on_clicked(partial(plot_new, title=graphs[slot][0], graph=graphs[slot][1]))
                pages[pi][ri][si] = (btn, pos) #type:ignore
                done.add(slot)
    del hpad, vpad, vsizemin, max_rows, max_height, color

    done = set(graphs) - done
    if done:
        print('WARNING\nMissing: "','", "'.join(done),'"',sep='')
    del done

    # Other buttons

    cur_page = 1
    def load_page(i):
        global cur_page
        for row in pages[cur_page-1]:
            for slot in row:
                if slot:
                    slot[1].set_visible(False) #type:ignore
        cur_page = i
        for row in pages[cur_page-1]:
            for slot in row:
                if slot:
                    slot[1].set_visible(True)
        plt.draw()
    load_page(1)

    def page_next(_):
        global cur_page
        load_page(cur_page + 1 if cur_page < len(pages) else 1)
    next_button = Button(plt.axes((0.825, 0.9375, 0.15, 0.05)), "Next", None, *reversed(colors['c']))
    next_button.on_clicked(page_next)

    def page_prev(_):
        global cur_page
        load_page(cur_page - 1 if cur_page > 1 else len(pages))
    prev_button = Button(plt.axes((0.65, 0.9375, 0.15, 0.05)), "Prev", None, *reversed(colors['c']))
    prev_button.on_clicked(page_prev)

    def reload_log(_):
        global logs, data
        logs, data = read_all_logs()
        menu()
    reload_button = Button(plt.axes((0.025, 0.9375, 0.2, 0.05)), "Refresh data", None, *reversed(colors['g']))
    reload_button.on_clicked(reload_log)

    def backup_log(_):
        last_log_num = int(logs[-1][5:-4])
        try:
            os.rename('game.log', f'game_{last_log_num + 1}.log')
        except FileNotFoundError:
            pass
        menu()
    backup_button = Button(plt.axes((0.25, 0.9375, 0.1, 0.05)), "Backup game.log", None, *reversed(colors['r']))
    backup_button.on_clicked(backup_log)

    plt.show()

except Exception as e:
    print(e)
    input('\nPress enter to close...')
