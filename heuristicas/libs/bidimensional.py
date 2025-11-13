import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

# elemento bidimensional com dimensões e coordenadas
class Item:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.x = None
        self.y = None
    # configura as coordenadas do item
    def set_position(self,x,y):
        self.x = x
        self.y = y
    def area(self):
        return self.w * self.h

# gera n itens em um intervalo de inteiros
def generate_random_itens(n, min_value = 1, max_value=7):
    l = [i for i in range(min_value, max_value+1)]
    itens = [Item(random.choice(l), random.choice(l)) for i in range(n)]
    return itens

# caixa que armazena itens bidimensionais
class Bin:
    def __init__(self, w=10, h=10):
        self.h = h
        self.w = w
        self.itens = []
    # verifica se um item pode ser colocado em uma coordenada da bin
    # considera as dimensões da bin e os outros itens empacotados
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
    
    # empacota um item na coordenada x y
    def pack(self,item:Item, x,y):
        if self.fits(item,x,y):
            item.set_position(x,y)
            self.itens.append(item)
            return True
        return False
    
    def filled_area(self):
        return sum([i.area() for i in self.itens])
    
    def void_area(self):
        void_area = self.w * self.h - self.filled_area()
        return void_area

# extensão da classe Bin para o algoritmo max rects
class MaxRectsBin(Bin):
    def __init__(self, w=10, h=10):
        super().__init__(w,h)
        self.free_rects = [(0, 0, w, h)]

    # inserção em uma bin por meio do algoritmo max rects
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

    # divide um retangulo livre que recebeu um item em até 2 outros retangulos livres
    def split_free_rect(self, free_rect, item):
        fx, fy, fw, fh = free_rect
        self.free_rects.remove(free_rect)
        if item.w < fw:
            self.free_rects.append((fx + item.w, fy, fw - item.w, item.h))
        if item.h < fh:
            self.free_rects.append((fx, fy + item.h, fw, fh - item.h))
        self.cleanup()

    # remove retangulos que contem outros retangulos
    def cleanup(self):
        cleaned = []
        for r in self.free_rects:
            if not any(self.contains(o, r) for o in self.free_rects if o != r):
                cleaned.append(r)
        self.free_rects = cleaned

    # verifica se um retangulo a contem em seu interior um retangulo b
    @staticmethod
    def contains(a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return bx >= ax and by >= ay and bx + bw <= ax + aw and by + bh <= ay + ah

# classe que gerencia as bins e os algoritmos de bin packing
class BinPacking:
    def __init__(self,w=10,h=10):
        self.bin_w = w
        self.bin_h = h
        self.bins = []
    # cria uma nova bin que atende ao tipo de algoritmo de bin packing
    def new_bin(self, type = "bl"):
        if type == "bl":
            self.bins.append(Bin(self.bin_w,self.bin_h))
        if type == "mr":
            self.bins.append(MaxRectsBin(self.bin_w,self.bin_h))
    
    # algoritmo de bin packing bottom left:
    # busca colocar um novo item mais ao fundo e a mais a esquerda possível
    def bottom_left(self,itens):
        start = time.time()
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
        return time.time()-start
    
    # algoritmo de bin packin maximal rectangles
    # armazena os retangulos vazios na bin e quando recebe um novo item busca coloca-lo no retangulo vazio em que ele melhor se encaixa
    def max_rects(self,itens):
        start = time.time()
        for item in itens:
            packed = False
            for b in self.bins:
                pos = b.insert(item)
                if pos:
                    packed = True
                    break
            if not packed:
                self.new_bin(type="mr")
                self.bins[-1].insert(item)
        return time.time()-start

    # visualização gráfica das bins
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

    def void_areas(self, ignore_last = False):
        void_areas = sum([b.void_area() for b in self.bins])
        if ignore_last:
            void_areas -= self.bins[-1].void_area()
        return void_areas
    
    def filled_areas(self):
        return sum([b.filled_area() for b in self.bins])

def generate_data(bin_w, bin_h, min_item_size, max_item_size, n_itens):
    itens = generate_random_itens(n_itens, min_item_size, max_item_size)
    bp = BinPacking(bin_w,bin_h)
    return bp, itens

def save_data(bp:BinPacking, itens, file):
    with open(file, 'w') as f:
        f.write(f"{bp.bin_w} {bp.bin_h}\n")
        for i in itens:
            f.write(f"{i.w} {i.h}\n")

def load_data(file):
    itens = []
    bp = None
    with open(file,'r') as f:
        for idx, line in enumerate(f):
            w,h = map(int, line.strip().split())
            if idx==0:
                bp = BinPacking(w,h)
            else:
                itens.append(Item(w,h))
    return bp, itens



# itens = generate_random_itens(50)
# bp  = BinPacking()
# bp.bottom_left(itens)
# bp.show_bins()

# bp, itens = load_data("./data/teste_12.txt")

# # bp  = BinPacking()
# bp.bottom_left(itens)
# bp.show_bins()