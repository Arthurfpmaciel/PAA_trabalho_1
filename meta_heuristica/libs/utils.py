from libs.sa import Item, Bin
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# gera todas as posições possíveis onde um novo item pode ser colocado dentro da bain
def gerar_posicoes_candidatas(bin_sim:Bin, item:Item):
    pos = [(0,0)]
    for i in bin_sim.itens:
        pos.append((i.x + i.w, i.y))
        pos.append((i.x, i.y + i.h))
    seen = set()
    out=[]
    for (x,y) in pos:
        if (x,y) in seen:
            continue
        seen.add((x,y))
        if x + item.w <= bin_sim.w and y + item.h <= bin_sim.h:
            out.append((x,y))
    return out

# calcula o limite inferior do numero de bins
# baseado na área total de todos os itens juntos
def lower_bound_items_area(indices, itens, bin_w, bin_h):
    total = sum(itens[i].area() for i in indices)
    return (total + bin_w*bin_h - 1) // (bin_w*bin_h)

# enumeração exata
# tenta empacotar um subconjunto de itens em uma única bin com memorização dos resultados ja calculados
def inner_enumeration(indices, itens, bin_w, bin_h, cache):
    key = frozenset(indices)
    if key in cache:
        return cache[key]
    local = [itens[i].copy() for i in indices]
    local.sort(key=lambda it: it.area(), reverse=True)
    sim = Bin(bin_w, bin_h)
    positions = {}
    def backtrack(pos):
        if pos == len(local):
            for it in sim.itens:
                positions[it.id] = (it.x, it.y)
            return True
        item = local[pos]
        cand = gerar_posicoes_candidatas(sim, item)
        cand.sort(key=lambda p: (p[0], p[1]))
        for (x,y) in cand:
            if sim.pack(item, x, y):
                if backtrack(pos+1):
                    return True
                sim.itens.pop()
                item.x = None
                item.y = None
        return False

    feasible = backtrack(0)
    cache[key] = (feasible, positions if feasible else None)
    return cache[key]

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