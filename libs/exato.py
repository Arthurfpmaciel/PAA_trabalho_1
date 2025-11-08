import time
import random
import copy

# --- Assumimos Item e Bin conforme implementados antes (id, copy, set_position, fits, pack) ---
class Item:
    _next_id = 0
    def __init__(self, w, h, id=None):
        self.w = w
        self.h = h
        self.x = None
        self.y = None
        if id is None:
            self.id = Item._next_id
            Item._next_id += 1
        else:
            self.id = id
    def set_position(self,x,y):
        self.x = x
        self.y = y
    def area(self):
        return self.w * self.h
    def copy(self):
        return Item(self.w, self.h, id=self.id)
    def __repr__(self):
        return f"I{self.id}({self.w}x{self.h})"

class Bin:
    def __init__(self, w=10, h=10):
        self.w = w; self.h = h
        self.itens = []
    def fits(self, item, x, y):
        if x + item.w > self.w or y + item.h > self.h:
            return False
        for i in self.itens:
            if not (x + item.w <= i.x or x >= i.x + i.w or y + item.h <= i.y or y >= i.y + i.h):
                return False
        return True
    def pack(self,item,x,y):
        if self.fits(item,x,y):
            item.set_position(x,y)
            self.itens.append(item)
            return True
        return False
    def filled_area(self): return sum(i.area() for i in self.itens)
    def void_area(self): return self.w*self.h - self.filled_area()
    def __repr__(self): return f"Bin({len(self.itens)} items, filled={self.filled_area()}/{self.w*self.h})"

# --- utilitários (posições candidatas, lower bound e inner_enumeration simples / placeholder) ---
def gerar_posicoes_candidatas(bin_sim:Bin, item:Item):
    pos = [(0,0)]
    for i in bin_sim.itens:
        pos.append((i.x + i.w, i.y))
        pos.append((i.x, i.y + i.h))
    # filtrar e deduplicar
    seen = set(); out=[]
    for (x,y) in pos:
        if (x,y) in seen: continue
        seen.add((x,y))
        if x + item.w <= bin_sim.w and y + item.h <= bin_sim.h:
            out.append((x,y))
    return out

def lower_bound_items_area(indices, itens, bin_w, bin_h):
    total = sum(itens[i].area() for i in indices)
    return (total + bin_w*bin_h - 1) // (bin_w*bin_h)  # ceil(total/area_bin)

# inner_enumeration: backtracking left-most downward (same idea que já discutimos)
def inner_enumeration(indices, itens, bin_w, bin_h, cache):
    key = frozenset(indices)
    if key in cache:
        return cache[key]
    # criar cópias locais
    local = [itens[i].copy() for i in indices]
    # ordenar por área decrescente (ajuda a poda)
    local.sort(key=lambda it: it.area(), reverse=True)
    sim = Bin(bin_w, bin_h)
    positions = {}

    def backtrack(pos):
        if pos == len(local):
            # preencher positions
            for it in sim.itens:
                positions[it.id] = (it.x, it.y)
            return True
        item = local[pos]
        cand = gerar_posicoes_candidatas(sim, item)
        # ordenar left-most downward
        cand.sort(key=lambda p: (p[0], p[1]))
        for (x,y) in cand:
            if sim.pack(item, x, y):
                if backtrack(pos+1):
                    return True
                # desfazer
                sim.itens.pop()
                item.x = None; item.y = None
        return False

    feasible = backtrack(0)
    cache[key] = (feasible, positions if feasible else None)
    return cache[key]

# --- heurística FFD 2D rápida para obter z* ---
def first_fit_decreasing_2d(itens, bin_w=10, bin_h=10):
    items_copy = [it.copy() for it in itens]
    items_copy.sort(key=lambda it: it.area(), reverse=True)
    bins=[]
    for it in items_copy:
        placed=False
        for b in bins:
            for (x,y) in gerar_posicoes_candidatas(b, it):
                if b.pack(it, x, y):
                    placed=True; break
            if placed: break
        if not placed:
            bnew = Bin(bin_w, bin_h)
            bnew.pack(it,0,0)
            bins.append(bnew)
    return bins, len(bins)

# ------------------ AQUI: implementação da ÁRVORE EXTERNA ------------------
def branch_external(itens, bin_w, bin_h, inner_cache, best_z, time_limit=None):
    """
    Implementa a árvore externa (DFS). Retorna (best_assignment, best_z, positions_map)
    - best_assignment: list of lists: cada elemento é lista de índices de 'itens' atribuídos ao bin
    - positions_map: merged map item_id -> (x,y) for the stored best solution
    """
    start = time.time()
    n = len(itens)
    best_assignment = None
    best_positions = None

    # Iniciar com heurística para z*
    _, z_star = first_fit_decreasing_2d([it.copy() for it in itens], bin_w, bin_h)
    # permitimos melhorar esse z_star
    current_best_z = min(best_z if best_z is not None else float('inf'), z_star)

    bins_assigned = []  # cada elemento: lista de índices

    # DFS recursivo
    def dfs(k):
        nonlocal current_best_z, best_assignment, best_positions
        # timeout
        if time_limit and (time.time() - start) > time_limit:
            return
        # poda por número de bins já usados
        if len(bins_assigned) >= current_best_z:
            return
        if k == n:
            # solução completa: validar (cada bin já foi validado durante inserções, mas vamos reconstruir posições)
            # para segurança, rodar inner_enumeration para cada bin e juntar posições
            merged_positions = {}
            for blk in bins_assigned:
                ok,pos = inner_enumeration(blk, itens, bin_w, bin_h, inner_cache)
                if not ok:
                    return
                merged_positions.update(pos)
            # atualiza melhor sol
            current_best_z = len(bins_assigned)
            best_assignment = [list(b) for b in bins_assigned]
            best_positions = dict(merged_positions)
            return

        # pegar item k e tentar em cada bin ativo
        for b_idx in range(len(bins_assigned)):
            bins_assigned[b_idx].append(k)
            # poda por lower bound
            lb = lower_bound_items_area(bins_assigned[b_idx], itens, bin_w, bin_h)
            if lb <= 1:
                # validar (cache inner)
                key = frozenset(bins_assigned[b_idx])
                if key in inner_cache:
                    feasible = inner_cache[key][0]
                else:
                    feasible, _ = inner_enumeration(bins_assigned[b_idx], itens, bin_w, bin_h, inner_cache)
                if feasible:
                    dfs(k+1)
            # desfazer
            bins_assigned[b_idx].pop()
            # timeout check trivial
            if time_limit and (time.time() - start) > time_limit:
                return

        # tentar abrir novo bin se ainda possível melhorar
        if len(bins_assigned) < current_best_z - 1:
            bins_assigned.append([k])
            lb = lower_bound_items_area(bins_assigned[-1], itens, bin_w, bin_h)
            if lb <= 1:
                key = frozenset(bins_assigned[-1])
                if key in inner_cache:
                    feasible = inner_cache[key][0]
                else:
                    feasible, _ = inner_enumeration(bins_assigned[-1], itens, bin_w, bin_h, inner_cache)
                if feasible:
                    dfs(k+1)
            bins_assigned.pop()

    dfs(0)
    return best_assignment, current_best_z, best_positions

# Wrapper que usa branch_external e reconstrói Bins com posições
def exact_search_with_external(itens, bin_w=10, bin_h=10, time_limit=None):
    inner_cache = {}
    # passamos best_z as None to let heuristic set the initial z*
    assignment, z_opt, pos_map = branch_external(itens, bin_w, bin_h, inner_cache, best_z=None, time_limit=time_limit)
    if assignment is None:
        # fallback: retorna solução heurística
        bins_heur, z0 = first_fit_decreasing_2d([it.copy() for it in itens], bin_w, bin_h)
        return bins_heur, z0
    # reconstruir bins com posições
    result_bins=[]
    for blk in assignment:
        b = Bin(bin_w, bin_h)
        ok, positions = inner_enumeration(blk, itens, bin_w, bin_h, inner_cache)
        if not ok:
            raise RuntimeError("Inconsistente: assignment não reconstruível")
        for idx in blk:
            it = itens[idx].copy()
            x,y = positions[it.id]
            it.set_position(x,y)
            b.itens.append(it)
        result_bins.append(b)
    return result_bins, z_opt

# ----------------- Exemplo de uso -----------------
if __name__ == "__main__":
    random.seed(1)
    # gerar itens, pré-processar por área decrescente
    itens = [Item(6,2), Item(3,4), Item(4,4), Item(2,2), Item(5,3), Item(3,3)]
    # Ordenar por área decrescente (pré-processamento)
    itens.sort(key=lambda it: it.area(), reverse=True)
    print("Itens (ordenados):", itens)

    bins_res, z_res = exact_search_with_external(itens, bin_w=10, bin_h=10, time_limit=5)
    print("z_res:", z_res)
    for i,b in enumerate(bins_res):
        print(f" Bin {i+1}: {b}")
        print("  itens:", b.itens)