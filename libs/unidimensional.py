import random
from decimal import Decimal
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm
import numpy as np

class Item:
    def __init__(self, size):
        self.size = size
    def __repr__(self):
        return f"|Item: {self.size}|"
    
class Bin:
    def __init__(self, max_size = 1):
        self.max_size = max_size
        self.itens = []
        self.size = 0
    def pack(self,item:Item):
        if item.size +self.size <= self.max_size:
            self.itens.append(item)
            self.size += item.size
            return True
        return False
    def unpack(self):
        if len(self.itens)>0:
            item = self.itens[-1]
            del self.itens[-1] 
            self.size -= item.size
            return item
        return None
    def __repr__(self):
        return f"Caixa ({self.size}/{self.max_size}): {"".join([repr(i) for i in self.itens])}"
    

def generate_random_itens(n):
    l = [Decimal('0.1') * i for i in range(1, 7)]
    itens = [Item(random.choice(l)) for i in range(n)]
    return itens


class BinPacking:
    def __init__(self, max_size=1):
        self.bin_max_size = max_size
        self.bins = [Bin(max_size)]
    def new_bin(self):
        self.bins.append(Bin(self.bin_max_size))
    
    def new_bin_and_pack(self, item):
        self.new_bin()
        return self.bins[-1].pack(item)


    # NF (Next Fit): a primeira caixa é a caixa atual, tenta colocar o ítem, se não couber a proxima caixa se torna a caixa atual
    # FF (First Fit): tenta colocar o ítem na primeira caixa que ele couber
    # BF (Best Fit): coloca o item na primeira caixa que sobrar menos tamanho
    def packing(self, itens, mode = "FF"):
        if mode =="NF":
            curr = 0
            for i in range(len(itens)):
                packed = False
                while not packed:
                    packed = self.bins[curr].pack(itens[i])
                    if not packed:
                        curr +=1
                        packed = self.new_bin_and_pack(itens[i])
                    
        elif mode == "FF":
            for i in itens:
                for j in range(len(self.bins)):
                    if self.bins[j].pack(i):
                        break
                    elif j == len(self.bins)-1:
                        self.new_bin_and_pack(i)
                        break

        elif mode == "BF":
            for i in itens:
                gaps = [self.bins[j].max_size - self.bins[j].size for j in range(len(self.bins))]
                diffs = [j-i.size for j in gaps]
                valid_bins = [j for j in range(len(self.bins)) if diffs[j]>=0]
                diffs = [d for d in diffs if d>=0]
                if len(diffs)==0:
                    self.new_bin_and_pack(i)
                else:
                    idx = valid_bins[diffs.index(min(diffs))]
                    self.bins[idx].pack(i)
        return self.bins        
    def __repr__(self):
        s = ""
        for i in range(len(self.bins)):
            s += f"{i} "+ repr(self.bins[i])+"\n"
        return s
    
    def show_bins(self):
        for i, b in enumerate(self.bins):
            fig, ax = plt.subplots()
            ax.set_title(f"Bin {i+1}")
            ax.set_xlim(0,1)
            ax.set_ylim(0,1)
            ax.set_aspect('equal')
            for j,item in enumerate(b.itens):
                rect = patches.Rectangle((0,j), 1, float(item.size), linewidth=1, edgecolor='black', facecolor='lightblue')
                ax.add_patch(rect)
                ax.text(1 + 1/2, float(item.size) + 1/2, f"{float(item.size)}", ha='center', va='center')
            plt.show()

    def show_bins_v2(self):
        fig, ax = plt.subplots(figsize=(6, len(self.bins)*0.8))
        all_items = sum(len(b.itens) for b in self.bins)
        # colors = cm.get_cmap('tab20', all_items)
        colors = plt.get_cmap('tab20', all_items)
        color_index = 0

        for i, bin in enumerate(self.bins):
            x_offset = 0  # início da barra
            y_pos = len(self.bins) - i - 1  # posição vertical (de cima para baixo)
            for item in bin.itens:
                size = float(item.size)
                color = colors(color_index % all_items)
                rect = patches.Rectangle((x_offset, y_pos), size, 0.8, 
                                        linewidth=1, edgecolor='black', facecolor=color)
                ax.add_patch(rect)
                ax.text(x_offset + size/2, y_pos + 0.4, f"{size:.2f}", ha='center', va='center')
                x_offset += size
                color_index+=1
            # borda do bin
            ax.add_patch(patches.Rectangle((0, y_pos), 1, 0.8, 
                                        linewidth=2, edgecolor='black', facecolor='none'))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, len(self.bins))
        ax.set_xlabel("Capacidade do Bin")
        ax.set_yticks([len(self.bins) - i - 0.6 for i in range(len(self.bins))])
        ax.set_yticklabels([f"Bin {i+1}" for i in range(len(self.bins))])
        plt.tight_layout()
        plt.show()

itens = generate_random_itens(20)
print("FF")
bp = BinPacking()
bp.packing(itens,"FF")
print(bp)
print("NF")
bp = BinPacking()
bp.packing(itens,"NF")
print(bp)
print("BF")
bp = BinPacking()
bp.packing(itens,"BF")
print(bp)
bp.show_bins_v2()