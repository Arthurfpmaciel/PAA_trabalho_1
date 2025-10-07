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
    
class MaxRectsBin(Bin):
    def __init__(self, w=10, h=10):
        super().__init__(w,h)
        self.free_rects = [(0, 0, w, h)]

    def insert(self, item:Item):
        best_rect = None
        best_area_fit = float('inf')

        for rect in self.free_rects:
            x, y, rw, rh = rect
            if item.w <= rw and item.h <= rh:
                area_fit = rw * rh - item.w * item.h
                if area_fit < best_area_fit:
                    best_rect = rect
                    best_area_fit = area_fit

        if best_rect is None:
            return None

        x, y, rw, rh = best_rect
        item.set_position(x,y)
        self.itens.append(item)
        self.split_free_rect(best_rect, item)
        return x, y

    def split_free_rect(self, free_rect, item):
        fx, fy, fw, fh = free_rect
        self.free_rects.remove(free_rect)
        # dividir em pedaços livres (direita e abaixo)
        if item.w < fw:
            self.free_rects.append((fx + item.w, fy, fw - item.w, item.h))
        if item.h < fh:
            self.free_rects.append((fx, fy + item.h, fw, fh - item.h))
        self.cleanup()

    def cleanup(self):
        cleaned = []
        for r in self.free_rects:
            if not any(self.contains(o, r) for o in self.free_rects if o != r):
                cleaned.append(r)
        self.free_rects = cleaned

    @staticmethod
    def contains(a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return bx >= ax and by >= ay and bx + bw <= ax + aw and by + bh <= ay + ah

class BinManager:
    def __init__(self, w = 10, h = 10):
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.bins = [MaxRectsBin(bin_width, bin_height)]

    def add_item(self, item:Item):
        for b in self.bins:
            pos = b.insert(item)
            if pos:
                return b  # item coube em um bin existente

        # não coube → criar um novo bin
        new_bin = MaxRectsBin(self.bin_width, self.bin_height)
        new_bin.insert(item)
        self.bins.append(new_bin)
        return new_bin
    
    def max_rects(self,itens):
        for item in itens:
            for b in self.bins:
                pos = b.insert(item)
                if pos:
                    return b
            new_bin = MaxRectsBin(self.bin_width, self.bin_height)
            new_bin.insert(item)
            self.bins.append(new_bin)

    def show_bins(self):
        for i, b in enumerate(self.bins):
            fig, ax = plt.subplots()
            ax.set_title(f"Bin {i+1}")
            ax.set_xlim(0, b.width)
            ax.set_ylim(0, b.height)
            ax.set_aspect('equal')
            for j, (x, y, w, h) in enumerate(b.placed):
                color = plt.colormaps["tab20"](j % 20)
                ax.add_patch(plt.Rectangle((x, y), w, h, facecolor=color, edgecolor="black"))
                ax.text(x + w/2, y + h/2, f"{w:.1f}x{h:.1f}", ha="center", va="center", fontsize=8)
            plt.show()

class BinPacking:
    def __init__(self):
        self.bins = []

    def new_bin(self, w = 10, h = 10, type = "bl"):
        if type == "bl":
            self.bins.append(Bin(w,h))
        if type == "mr":
            self.bins.append(MaxRectsBin(w,h))
    
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
        
    def max_rects(self,itens):
        for item in itens:
            packed = False
            for b in self.bins:
                pos = b.insert(item)
                if pos:
                    packed = True
                    break
            if not packed:
                self.new_bin(10,10,type="mr")
                self.bins[-1].insert(item)

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


bp  = BinPacking()
bp.max_rects(itens)
bp.show_bins()