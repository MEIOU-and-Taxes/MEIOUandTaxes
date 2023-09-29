import os
os.chdir(os.path.dirname(__file__))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button
from functools import partial
import glob
from typing import cast

fig, ax = plt.subplots(num="MEIOU and Taxes - Sim graphs", figsize = (16, 9))
ax.show = lambda: None #type:ignore

def menu(msg=None):
    ax.clear()
    ax.set_title('Menu')
    ax.text(0.5, 0.5, horizontalalignment='center', verticalalignment='center', s="""\

Welcome to the M&T sim graphing tool!

Select the graph you want to see below.

""".strip())
    if msg:
        ax.text(0.5, 0.5, msg)
    plt.draw()
menu()

# Reading data

def get_data(_, i: str):
    lst = []
    loc = 0

    while True:
        loc = data.find(i, loc)

        if loc != -1:
            end = data.find('\n', loc)
            lst.append(float(data[loc:end].strip().split(':')[1].strip()))
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
    with open('game.log', 'r') as f:
        text += f.read()
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
            page.append(line.split(';'))
    if page:
        pages.append(page)
    del page
hpad = 0.0125
vpad = 0.0125
vsize = 0.05

max_rows = max((len(page) for page in pages))
plt.subplots_adjust(left=0.05, right=0.95, bottom=0.04 + max_rows * vsize, top=0.925)

# Plotting evil deeds

def plot_new(_, graph, title):
    ax.clear()
    graph(data, ax)
    ax.set_title(title)
    ax.legend(loc=2, ncol=2)
    plt.draw()

done = set()
for pi, page in enumerate(pages):
    height_page = (max_rows * vsize - vpad * (max_rows + 1)) / len(page)
    for ri, row in enumerate(page):
        width_row = (1 - hpad * (len(row) + 1)) / len(row)
        for si, slot in enumerate(row):
            if not slot:
                continue
            if slot not in graphs:
                raise ValueError(f'Wtf is this??? "{slot}"\nCould not find "graph{slot.replace(" ", "_")}"')
            if slot in done:
                raise ValueError(f'Duplicate entry: "{slot}"')
            pos = plt.axes((
                si * width_row + hpad * (si + 1),
                (len(page) - ri - 1) * (height_page + vpad) + vpad,
                width_row,
                height_page
            ))
            pos.set_visible(False)
            btn = Button(pos, slot)
            btn.on_clicked(partial(plot_new, title=graphs[slot][0], graph=graphs[slot][1]))
            pages[pi][ri][si] = (btn, pos) #type:ignore
            done.add(slot)

done = set(graphs) - done
if done:
    print('WARNING\nMissing: "','", "'.join(done),'"',sep='')

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
next_button = Button(plt.axes((0.825, 0.9375, 0.15, 0.05)), "Next")
next_button.on_clicked(page_next)

def page_prev(_):
    global cur_page
    load_page(cur_page - 1 if cur_page > 1 else len(pages))
prev_button = Button(plt.axes((0.65, 0.9375, 0.15, 0.05)), "Prev")
prev_button.on_clicked(page_prev)

def reload_log(_):
    global logs, data
    logs, data = read_all_logs()
    menu()
reload_button = Button(plt.axes((0.025, 0.9375, 0.2, 0.05)), "Refresh data")
reload_button.on_clicked(reload_log)

def backup_log(_):
    last_log_num = int(logs[-1][5:-4])
    try:
        os.rename('game.log', f'game_{last_log_num + 1}.log')
    except FileNotFoundError:
        pass
    menu()
backup_button = Button(plt.axes((0.25, 0.9375, 0.1, 0.05)), "Backup game.log")
backup_button.on_clicked(backup_log)

plt.show()
