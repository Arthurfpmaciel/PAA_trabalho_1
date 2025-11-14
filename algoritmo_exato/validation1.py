import os
import time
import copy
from libs.algorithm import exact_search_with_external
from libs.utils import show_bins, load_data, total_filled_area, total_void_area
import pandas as pd

import sys
sys.setrecursionlimit(3000)

def validation(time_limit):

    file_name = "./data/exato_val.csv"
    df = pd.DataFrame(columns=["file","bin_size","n_itens","item_group","n_bins","time_sec","total_filled_area","total_void_area","z_value"])

    print("\nExecutando todos os testes automáticos...\n")
    bin_file = ["bin10","bin20"]
    group_file = ["pequenos","medios","grandes"]

    for i in bin_file:
        for j in group_file:
            files = os.listdir(f"./data/{i}/{j}")
            for f in files:
                print(f)
                bin_w, bin_h, itens = load_data(f"./data/{i}/{j}/{f}")
                itens_copy = copy.deepcopy(itens)
                start = time.time()
                bins_res, z_res = exact_search_with_external(itens_copy, bin_w, bin_h,time_limit)
                end = round(time.time() - start,6)
                result = [f, bin_w, len(itens), j, len(bins_res), end, total_filled_area(bins_res), total_void_area(bins_res), z_res]
                print(result)
                df.loc[len(df)] = [f, bin_w, len(itens), j, len(bins_res), end, total_filled_area(bins_res), total_void_area(bins_res), z_res]
    df.to_csv(file_name,index=False)

    print(f"\nArquivo CSV salvo em: {os.path.abspath(file_name)}\n")
