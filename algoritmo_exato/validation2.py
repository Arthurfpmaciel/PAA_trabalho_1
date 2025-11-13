import os
import time
import copy
from libs.algorithm import exact_search_with_external
from libs.utils import show_bins, load_data, total_filled_area, total_void_area, generate_random_itens
import pandas as pd

import sys
sys.setrecursionlimit(3000)
file_name = "./data/exato_val2.csv"
df = pd.DataFrame(columns=["classe","n","tempo","n_bins_otima","n_bins_melhor"])

print("\nExecutando todos os testes automáticos...\n")


classes = [1,2,3]
ns = [20,40,60,80,100]
# ns = [10,20,30,40,50,60,70,80]
def teste_exato(classe, n, time_limit=10):
    if classe ==1:
        bin_w = bin_h = 10
        max_v = 10
    if classe ==2:
        bin_w = bin_h = 30
        max_v = 10
    if classe ==3:
        bin_w = bin_h = 100
        max_v = 35
    itens = generate_random_itens(n,1, max_v)
    start = time.time()
    bins_res, z_res = exact_search_with_external(itens, bin_w, bin_h,time_limit)
    end = round(time.time() - start,6)
    # end = end if end <= time_limit else None
    n_bins = len(bins_res) if end < time_limit else None
    return [classe, n, end, n_bins, len(bins_res)]


time_limit = 300
for classe in classes:
    print(f"-Classe {classe}")
    for n in ns:
        print(f"\tNúmero de instâncias: {n}")
        result = teste_exato(classe,n,time_limit) 
        print(f"\t\tResultado{result}")
        df.loc[len(df)] = result

df.to_csv(file_name,index=False)