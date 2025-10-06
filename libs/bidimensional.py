import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Item:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.x = None
        self.y = None

    def set_position(self,x,y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Item ({self.w}x{self.h}) na coordenada ({self.x},{self.y})"
    
def generate_random_itens(n):
    l = [i for i in range(1, 7)]
    itens = [Item(random.choice(l), random.choice(l)) for i in range(n)]
    return itens

class Bin:
    def __init__(self, w=10, h=10):
        self.h = h
        self.w = w
        self.itens = []

    def fits(self, item, x, y):
        if x + item.w > self.w or y + item.h > self.h:
            return False
        for i in self.itens:
            px = i.x
            py = i.y
            pw = i.w
            ph = i.h
            if not (x + item.w <= px or x >= px + pw or y + item.h <= py or y >= py + ph):
                return False
        return True
    
    def pack(self,item:Item, x,y):
        if self.fits(item,x,y):
            item.set_position(x,y)
            self.itens.append(item)
            return True
        return False
    


class BinPacking:
    def __init__(self):
        self.bins = []

    def new_bin(self, w = 10, h = 10):
        self.bins.append(Bin(w,h))
    
    def bottom_left(self,itens):
        for item in itens:
            placed = False
            for bin in self.bins:
                for y in range(bin.h - item.h + 1):
                    for x in range(bin.w - item.w + 1):
                        if bin.fits(item, x, y):
                            bin.pack(item,x,y)
                            placed = True
                            break
                    if placed:
                        break
                if placed:
                    break
            if not placed:
                self.new_bin()
                self.bins[-1].pack(item,0,0)
        return self.bins
        
    def show_bins(self):
        all_items = sum(len(b.itens) for b in self.bins)
        colors = plt.get_cmap('tab20', all_items)
        color_index = 0
        for i, bin in enumerate(self.bins):
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

itens = generate_random_itens(10)
bp  = BinPacking()
bp.bottom_left(itens)
bp.show_bins()