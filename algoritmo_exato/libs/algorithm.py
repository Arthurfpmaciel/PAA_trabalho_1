import time
from libs.utils import gerar_posicoes_candidatas, inner_enumeration, lower_bound_items_area
from libs.entities import Item, Bin

# heurística FFD 2d para obter z*
def first_fit_decreasing_2d(itens, bin_w=10, bin_h=10):
    items_copy = [it.copy() for it in itens]
    items_copy.sort(key=lambda it: it.area(), reverse=True)
    bins=[]
    for it in items_copy:
        placed=False
        for b in bins:
            for (x,y) in gerar_posicoes_candidatas(b, it):
                if b.pack(it, x, y):
                    placed=True
                    break
            if placed: break
        if not placed:
            bnew = Bin(bin_w, bin_h)
            bnew.pack(it,0,0)
            bins.append(bnew)
    return bins, len(bins)

# implementa a árvore de busca externa, usando busca por profundidade para poda
def branch_external(itens, bin_w, bin_h, inner_cache, best_z, time_limit=None):
    start = time.time()
    n = len(itens)
    best_assignment = None
    best_positions = None
    _, z_star = first_fit_decreasing_2d([it.copy() for it in itens], bin_w, bin_h)
    current_best_z = min(best_z if best_z is not None else float('inf'), z_star)
    bins_assigned = []
    # busca por profundidade (DFS) recursiva
    def dfs(k):
        nonlocal current_best_z, best_assignment, best_positions
        if time_limit and (time.time() - start) > time_limit:
            return
        if len(bins_assigned) >= current_best_z:
            return
        if k == n:
            merged_positions = {}
            for blk in bins_assigned:
                ok,pos = inner_enumeration(blk, itens, bin_w, bin_h, inner_cache)
                if not ok:
                    return
                merged_positions.update(pos)
            current_best_z = len(bins_assigned)
            best_assignment = [list(b) for b in bins_assigned]
            best_positions = dict(merged_positions)
            return
        for b_idx in range(len(bins_assigned)):
            bins_assigned[b_idx].append(k)
            lb = lower_bound_items_area(bins_assigned[b_idx], itens, bin_w, bin_h)
            if lb <= 1:
                key = frozenset(bins_assigned[b_idx])
                if key in inner_cache:
                    feasible = inner_cache[key][0]
                else:
                    feasible, _ = inner_enumeration(bins_assigned[b_idx], itens, bin_w, bin_h, inner_cache)
                if feasible:
                    dfs(k+1)
            bins_assigned[b_idx].pop()
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

def branch_external_v2(itens, bin_w, bin_h, inner_cache, best_z, time_limit=None):
    start = time.time()
    n = len(itens)
    best_assignment = None
    best_positions = None
    _, z_star = first_fit_decreasing_2d([it.copy() for it in itens], bin_w, bin_h)
    current_best_z = min(best_z if best_z is not None else float('inf'), z_star)
    bins_assigned = []
    # busca por profundidade (DFS) recursiva
    def dfs_v2(k):
        nonlocal current_best_z, best_assignment, best_positions
        if time_limit and (time.time() - start) > time_limit:
            return True
        if len(bins_assigned) >= current_best_z:
            return False
        if k == n:
            merged_positions = {}
            for blk in bins_assigned:
                ok,pos = inner_enumeration(blk, itens, bin_w, bin_h, inner_cache)
                if not ok:
                    return False
                merged_positions.update(pos)
            current_best_z = len(bins_assigned)
            best_assignment = [list(b) for b in bins_assigned]
            best_positions = dict(merged_positions)
            return False
        for b_idx in range(len(bins_assigned)):
            bins_assigned[b_idx].append(k)
            lb = lower_bound_items_area(bins_assigned[b_idx], itens, bin_w, bin_h)
            if lb <= 1:
                key = frozenset(bins_assigned[b_idx])
                if key in inner_cache:
                    feasible = inner_cache[key][0]
                else:
                    feasible, _ = inner_enumeration(bins_assigned[b_idx], itens, bin_w, bin_h, inner_cache)
                if feasible:
                    stop = dfs_v2(k+1)
                    if stop:
                        return True
            bins_assigned[b_idx].pop()
            if time_limit and (time.time() - start) > time_limit:
                return True
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
                    stop = dfs_v2(k+1)
                    if stop:
                        return True
            bins_assigned.pop()
        return False
    dfs_v2(0)
    return best_assignment, current_best_z, best_positions

# wrapper que usa branch_external e reconstrói Bins com posições
def exact_search_with_external(itens, bin_w=10, bin_h=10, time_limit=None):
    inner_cache = {}
    assignment, z_opt, pos_map = branch_external_v2(itens, bin_w, bin_h, inner_cache, best_z=None, time_limit=time_limit)
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

# interface simplificada para o algoritmo exato
def algoritmo_exato(itens, bin_w=10, bin_h=10, time_limit=10):
    bins_res, z_res = exact_search_with_external(itens, bin_w=bin_w, bin_h=bin_h, time_limit=time_limit)
    return bins_res, z_res
