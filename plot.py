import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from steiner import steiner_main
import random

class SteinerTreePlotter:
    def __init__(self, entry_x, entry_y, canvas) -> None:
        self.vertices = {}
        self.entry_x = entry_x
        self.entry_y = entry_y
        self.canvas = canvas

    def plot_vertex(self):
        x = float(self.entry_x.get())
        y = float(self.entry_y.get())
        if (x, y) not in list(self.vertices.values()): 
            self.vertices[len(self.vertices)] = (x, y)
        plt.scatter(x, y, color='blue')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Vertex Plot')
        self.canvas.draw()

    def plot_vertices(self):
        for vertex in list(self.vertices.values()):
            x, y = vertex
            if (x, y) not in list(self.vertices.values()): 
                self.vertices[len(self.vertices)] = (x, y)
            plt.scatter(x, y, color='blue')
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.title('Vertex Plot')
        self.canvas.draw()

    def clear_plot(self):
        self.vertices = {}
        plt.clf()
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Vertex Plot')
        self.canvas.draw()

    def steiner_tree(self): 
        plt.clf()
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Vertex Plot')
        self.canvas.draw()
        self.plot_vertices()   
        if len(self.vertices) < 3: return
        orig_len = len(self.vertices)
        g = steiner_main(self.vertices)
        for edge in g.mst_edges:
            v1, v2 = edge
            x1, y1 = self.vertices[v1]
            x2, y2 = self.vertices[v2]
            plt.plot([x1, x2], [y1, y2], linestyle='-', color='red')
        self.canvas.draw()
        self.vertices = dict(list(self.vertices.items())[:orig_len])
    
    def setup(self, number): 
        plt.clf()
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Vertex Plot')
        self.canvas.draw()
        if number == 1:
            self.vertices = {
                0: (0,0), 
                1: (4,0), 
                2: (2,3)
                }
        elif number == 2:
            self.vertices = {
                0: (0,0), 
                1: (0,1), 
                2: (1.3,1), 
                3: (1.3,0)
            }
        elif number == 3:
            self.vertices = {}
            for i in range(10):
                for j in range(10): 
                    self.vertices[len(self.vertices)] = (i**2,j**2)
        elif number == 4:
            self.vertices = {}
            for _ in range(100): 
                self.vertices[len(self.vertices)] = (random.uniform(0, 20.0), random.uniform(0, 20.0))
        self.plot_vertices()            

def on_close(root):
    root.destroy()

def on_figure_close(event, root):
    root.quit()

def main():
    root = tk.Tk()
    root.title("Vertex Plotter")

    label_x = ttk.Label(root, text="X-coordinate:")
    label_x.grid(row=0, column=0, padx=5, pady=5, sticky="E")

    entry_x = ttk.Entry(root)
    entry_x.grid(row=0, column=1, padx=5, pady=5)

    label_y = ttk.Label(root, text="Y-coordinate:")
    label_y.grid(row=1, column=0, padx=5, pady=5, sticky="E")

    entry_y = ttk.Entry(root)
    entry_y.grid(row=1, column=1, padx=5, pady=5)

    fig, ax = plt.subplots()
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Vertex Plot')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=3, column=0, columnspan=2)

    plotter = SteinerTreePlotter(entry_x, entry_y, canvas)

    plot_button = ttk.Button(root, text="Plot Vertex", command=plotter.plot_vertex)
    plot_button.grid(row=2, column=0, padx=5, pady=10)

    steiner_tree_button = ttk.Button(root, text="Find steiner tree", command=plotter.steiner_tree)
    steiner_tree_button.grid(row=2, column=1, padx=5, pady=10)

    clear_button = ttk.Button(root, text="Clear Plot", command=plotter.clear_plot)
    clear_button.grid(row=2, column=2, padx=5, pady=10)
    
    setup1_button = ttk.Button(root, text="3 vertices", command= lambda: plotter.setup(1))
    setup1_button.grid(row=3, column=2, padx=5, pady=10)

    setup2_button = ttk.Button(root, text="4 vertices", command= lambda: plotter.setup(2))
    setup2_button.grid(row=4, column=0, padx=5, pady=10)

    setup3_button = ttk.Button(root, text="Grid", command= lambda: plotter.setup(3))
    setup3_button.grid(row=4, column=1, padx=5, pady=10)

    setup4_button = ttk.Button(root, text="Random setup", command= lambda: plotter.setup(4))
    setup4_button.grid(row=4, column=2, padx=5, pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))

    fig.canvas.mpl_connect('close_event', lambda event: on_figure_close(event, root))

    root.mainloop()

if __name__ == "__main__":
    main()
