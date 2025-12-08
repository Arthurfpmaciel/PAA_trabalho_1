from libs.entities import Item, Bin
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# gerar itens aleatórios
def generate_random_itens(n, min_value = 1, max_value=7):
    l = [i for i in range(min_value, max_value+1)]
    itens = [Item(random.choice(l), random.choice(l)) for i in range(n)]
    return itens

def load_data(file):
    itens = []
    with open(file,'r') as f:
        for idx, line in enumerate(f):
            w,h = map(int, line.strip().split())
            if idx==0:
                bin_w = w
                bin_h = h
            else:
                itens.append(Item(w,h))
    return bin_w, bin_h, itens

# plotagem de cada bin com os itens empacotados
def show_bins(bins):
        all_items = sum(len(b.itens) for b in bins)
        colors = plt.get_cmap('tab20', all_items)
        color_index = 0
        for i, bin in enumerate(bins):
            fig, ax = plt.subplots()
            ax.set_title(f"Bin {i+1}")
            ax.set_xlim(0, bin.w)
            ax.set_ylim(0, bin.h)
            ax.set_aspect('equal')
            for i in bin.itens:
                color = colors(color_index % all_items)
                rect = patches.Rectangle((i.x, i.y), i.w, i.h, linewidth=1, edgecolor='black', facecolor=color)
                ax.add_patch(rect)
                ax.text(i.x + i.w/2, i.y + i.h/2, f"{i.w}x{i.h}", ha='center', va='center')
                color_index+=1
        plt.show()

def total_filled_area(bins):
    return sum([b.filled_area() for b in bins])

def total_void_area(bins):
    return sum([b.void_area() for b in bins])