import os
import copy
from libs.sa import simulated_annealing
from libs.utils import load_data
import pandas as pd

def validation(group):
    file_name = f"./data/meta_val_{group}.csv"
    df = pd.DataFrame(columns=["file","item_group","bin_size","n_itens","n_bins","time_sec","total_void_area"])
    print("\nExecutando todos os testes automáticos...\n")
    bin_file = ["bin10","bin20"]
    group_file = [group]
    for i in bin_file:
        for j in group_file:
            files = os.listdir(f"./data/{i}/{j}")
            for f in files:
                print(f)
                bin_w, bin_h, itens = load_data(f"./data/{i}/{j}/{f}")
                itens_copy = copy.deepcopy(itens)
                result = simulated_annealing(itens_copy, bin_w, bin_h,'mr',L_factor=5, alpha=0.9 ,max_iters=100)
                bins_res = result['best_bp']
                line = [f, j, bin_w, len(itens_copy), len(bins_res.bins), result['time'], bins_res.void_areas()]
                print(line)
                df.loc[len(df)] = line
    df.to_csv(file_name,index=False)
    print(f"\nArquivo CSV salvo em: {os.path.abspath(file_name)}\n")

groups = ["pequenos","medios","grandes"]
idx = 2 # altere o índice para fazer testes dos outros grupos
validation(groups[idx])