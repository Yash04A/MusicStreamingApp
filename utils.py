import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import os
from config import app

def uploadData(file, loc, file_name):
    if not os.path.exists(loc):
        os.makedirs(loc)
    new_file_path = os.path.join(loc, file_name)

    if os.path.exists(new_file_path):
        os.remove(new_file_path)

    file.seek(0)
    file.save(new_file_path)

    relative_path = os.path.relpath(new_file_path, start='static').replace(os.path.sep,'/')


    return relative_path

def plot_graph(data,file_name):
    labels, values = zip(*data)

    plt.bar(labels,values)
    plt.xlabel("Song Titles")
    plt.ylabel("Total Streams")
    plt.title('Top 10 Songs based on total streams')

    loc = app.config['DASHBOARD'] 

    if not os.path.exists(loc):
        os.makedirs(loc)
    new_file_path = os.path.join(loc, file_name)

    if os.path.exists(new_file_path):
        os.remove(new_file_path)

    plt.savefig(new_file_path)
    plt.close()

    return new_file_path.replace(os.path.sep,'/')
