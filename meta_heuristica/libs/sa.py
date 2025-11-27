import random
import time
import copy
import math
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
    def area(self):
        return self.w * self.h
    def copy(self):
        new = Item(self.w, self.h)
        # posição não copiada para evitar confusão em reempacotamento
        return new

def generate_random_itens(n, min_value = 1, max_value=7):
    l = [i for i in range(min_value, max_value+1)]
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
            px = i.x; py = i.y; pw = i.w; ph = i.h
            if not (x + item.w <= px or x >= px + pw or y + item.h <= py or y >= py + ph):
                return False
        return True
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
        if free_rect in self.free_rects:
            self.free_rects.remove(free_rect)
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

class BinPacking:
    def __init__(self,w=10,h=10):
        self.bin_w = w
        self.bin_h = h
        self.bins = []
    def new_bin(self, type = "bl"):
        if type == "bl":
            self.bins.append(Bin(self.bin_w,self.bin_h))
        if type == "mr":
            self.bins.append(MaxRectsBin(self.bin_w,self.bin_h))
    def bottom_left(self,itens):
        for b in self.bins:
            b.itens = []
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
    def max_rects(self,itens):
        for b in self.bins:
            b.itens = []
            if isinstance(b, MaxRectsBin):
                b.free_rects = [(0,0,b.w,b.h)]
        start = time.time()
        for item in itens:
            packed = False
            for b in self.bins:
                if isinstance(b, MaxRectsBin):
                    pos = b.insert(item)
                else:
                    pos = None
                if pos:
                    packed = True
                    break
            if not packed:
                self.new_bin(type="mr")
                self.bins[-1].insert(item)
        return time.time()-start
    def void_areas(self, ignore_last = False):
        void_areas = sum([b.void_area() for b in self.bins])
        if ignore_last and len(self.bins)>0:
            void_areas -= self.bins[-1].void_area()
        return void_areas
    def filled_areas(self):
        return sum([b.filled_area() for b in self.bins])
    
def show_bins(self):
    all_items = sum(len(b.itens) for b in self.bins)
    colors = plt.get_cmap('tab20', max(1, all_items))
    color_index = 0
    for idx, bin in enumerate(self.bins):
        fig, ax = plt.subplots()
        ax.set_title(f"Bin {idx+1}")
        ax.set_xlim(0, bin.w)
        ax.set_ylim(0, bin.h)
        ax.set_aspect('equal')
        for it in bin.itens:
            color = colors(color_index % max(1, all_items))
            rect = patches.Rectangle((it.x, it.y), it.w, it.h, linewidth=1, edgecolor='black', facecolor=color)
            ax.add_patch(rect)
            ax.text(it.x + it.w/2, it.y + it.h/2, f"{it.w}x{it.h}", ha='center', va='center')
            color_index+=1
    plt.show()

def generate_data(bin_w, bin_h, min_item_size, max_item_size, n_itens):
    itens = generate_random_itens(n_itens, min_item_size, max_item_size)
    bp = BinPacking(bin_w,bin_h)
    return bp, itens

def pack_permutation(perm, bin_w, bin_h, method='mr'):
    items_copy = [Item(it.w, it.h) for it in perm]
    bp = BinPacking(bin_w, bin_h)
    if method == 'mr':
        bp.bins = []
        bp.max_rects(items_copy)
    else:
        bp.bins = []
        bp.bottom_left(items_copy)
    return bp

def cost_of_packing(bp: BinPacking, bigM=10**6, ignore_last=True):
    n_bins = len(bp.bins)
    void = bp.void_areas(ignore_last=ignore_last)
    return n_bins * bigM + void

def op_2opt(perm):
    n = len(perm)
    if n < 4:
        return perm[:]
    i, j = sorted(random.sample(range(n), 2))
    p = perm[:]
    p[i:j+1] = list(reversed(p[i:j+1]))
    return p

# block swap
def op_block_swap(perm, max_block=4):
    n = len(perm)
    if n < 4:
        return perm[:]
    i = random.randrange(0, n-1)
    j = random.randrange(i+1, n)
    max_size1 = min(max_block, n - i - 1)
    max_size2 = min(max_block, n - j)
    if max_size1 < 1:
        size1 = 1
    else:
        size1 = random.randint(1, max_size1)
    if max_size2 < 1:
        size2 = 1
    else:
        size2 = random.randint(1, max_size2)
    if j < i + size1:
        j = i + size1
        if j >= n:
            p = perm[:]
            a, b = random.sample(range(n), 2)
            p[a], p[b] = p[b], p[a]
            return p

    p = perm[:]
    block1 = p[i:i+size1]
    block2 = p[j:j+size2]
    new = p[:i] + block2 + p[i+size1:j] + block1 + p[j+size2:]
    return new

# block insertion
def op_block_insertion(perm, max_block=4):
    n = len(perm)
    if n < 4:
        return perm[:]
    i, j = sorted(random.sample(range(n), 2))
    max_block_size = min(max_block, n - i)
    block_size = random.randint(1, max_block_size)
    block = perm[i:i+block_size]
    remainder = perm[:i] + perm[i+block_size:]
    if j > i:
        j = j - block_size
        if j < 0:
            j = 0
        if j > len(remainder):
            j = len(remainder)
    else:
        if j < 0:
            j = 0
    new = remainder[:j] + block + remainder[j:]
    return new

# rotate
def op_rotate(perm):
    p = perm[:]
    if len(p) > 0:
        idx = random.randrange(len(p))
        it = p[idx]
        new_item = type(it)(it.h, it.w)
        p[idx] = new_item
    return p

# swap
def op_swap(perm):
    n = len(perm)
    if n < 2:
        return perm[:]
    p = perm[:]
    i, j = random.sample(range(n), 2)
    p[i], p[j] = p[j], p[i]
    return p

# insertion
def op_insertion(perm):
    n = len(perm)
    if n < 2:
        return perm[:]
    p = perm[:]
    i, j = random.sample(range(n), 2)
    item = p.pop(i)
    p.insert(j, item)
    return p

# operador unificado
def random_neighbor(perm):
    operations = [op_2opt, op_block_swap, op_block_insertion, op_rotate, op_swap, op_insertion]
    weights = [1, 1, 1, 3, 2, 2]
    op = random.choices(operations, weights=weights, k=1)[0]
    return op(perm)

def simulated_annealing(items, bin_w=10, bin_h=10, method='mr',
                        T0=1000.0, alpha=0.95, L_factor=10, T_min=1e-3, max_iters=200):
    start_time = time.time()
    perm0 = sorted(items, key=lambda it: it.area(), reverse=True)
    curr_perm = perm0[:]
    bp_curr = pack_permutation(curr_perm, bin_w, bin_h, method=method)
    curr_cost = cost_of_packing(bp_curr)
    best_perm = curr_perm[:]
    best_cost = curr_cost
    best_bp = bp_curr
    n = len(items)
    L = min(max(1, L_factor * n),2000)
    T = T0
    iters = 0
    history = []
    while T > T_min and iters < max_iters:
        for _ in range(L):
            cand_perm = random_neighbor(curr_perm)
            cand_bp = pack_permutation(cand_perm, bin_w, bin_h, method=method)
            cand_cost = cost_of_packing(cand_bp)
            delta = cand_cost - curr_cost
            if delta <= 0 or random.random() < math.exp(-delta / T):
                curr_perm = cand_perm
                curr_cost = cand_cost
                bp_curr = cand_bp
                if curr_cost < best_cost:
                    best_cost = curr_cost
                    best_perm = curr_perm[:]
                    best_bp = bp_curr
            history.append((time.time() - start_time, curr_cost, best_cost))
        T *= alpha
        iters += 1
    total_time = time.time() - start_time
    return {
        'best_bp': best_bp,
        'best_perm': best_perm,
        'best_cost': best_cost,
        'time': total_time,
        'history': history
    }

# random.seed(1)

# # gerar instancia
# bp, itens = generate_data(bin_w=10, bin_h=10, min_item_size=1, max_item_size=6, n_itens=800)

# bp1 = BinPacking(bp.bin_w, bp.bin_h)
# time1 = bp1.bottom_left(itens)
# print("tempo MR:", time1)
# print("Número de bins:", len(bp1.bins))
# print("area preenchida:", bp1.filled_areas())
# print("void areas (ignore last):", bp1.void_areas(ignore_last=True))

# # rodar SA
# result = simulated_annealing(itens,
#                              bin_w=bp.bin_w,
#                              bin_h=bp.bin_h,
#                              method='mr',
#                              T0=1000.0,
#                              alpha=0.95,
#                              L_factor=2,
#                              T_min=1e-3,
#                              max_iters=100)

# print("Tempo:", result['time'])
# print("Número de bins (melhor):", len(result['best_bp'].bins))
# print("Void areas (ignore last):", result['best_bp'].void_areas(ignore_last=True))
# print("Area preenchida:", result['best_bp'].filled_areas())


