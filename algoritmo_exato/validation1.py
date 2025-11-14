import os
import time
import copy
from libs.algorithm import exact_search_with_external
from libs.utils import show_bins, load_data, total_filled_area, total_void_area
import pandas as pd

import sys
sys.setrecursionlimit(3000)
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
            bins_res, z_res = exact_search_with_external(itens_copy, bin_w, bin_h,time_limit=60)
            end = round(time.time() - start,6)
            result = [f, bin_w, len(itens), j, len(bins_res), end, total_filled_area(bins_res), total_void_area(bins_res), z_res]
            print(result)
            df.loc[len(df)] = [f, bin_w, len(itens), j, len(bins_res), end, total_filled_area(bins_res), total_void_area(bins_res), z_res]
df.to_csv(file_name,index=False)




\begin{table}[htbp]
\centering
\label{tab:alg_exato_2_conjunto_1}
\begin{tabular}{|c|c|c|c|c|}
\hline
\textbf{Bin} & \textbf{Itens} & \textbf{n_bins} & \textbf{Tempo (s)} & \textbf{Area_livre} \\
\hline
10x10 & 100 & 34 & 60.001622 & 257 \\
10x10 & 200 & 65 & 60.006058 & 399 \\
10x10 & 400 & 122 & 60.023705 & 235 \\
10x10 & 800 & 235 & 60.001413 & 126 \\
10x10 & 1600 & 480 & 60.349494 & 441 \\
\hline
\end{tabular}
\caption{Algoritmo Exato aplicados a itens grandes do segundo conjunto}
\end{table}

classe,n,tempo,n_bins_otima,n_bins_melhor
1 & 20 & 0.001 & 10 & 10\\
1 & 40 & 0.216933 & 9 & 9\\
1 & 60 & 117.784805 & 20 & 20\\
1 & 80 & 0.032347 & 26 & 26\\
1 & 100 & 300.004245 & — & 34\\
2 & 20 & 0.001004 & 1 & 1\\
2 & 40 & 0.164741 & 2 & 2\\
2 & 60 & 2.670404 & 2 & 2\\
2 & 80 & 509.783291 & — & 3\\
2 & 100 & 308.093332 & — & 4\\
3 & 20 & 0.001002 & 1 & 1\\
3 & 40 & 0.103155 & 2 & 2\\
3 & 60 & 1593.198721 & — & 3\\
3 & 80 & 313.706239 & — & 3\\
3 & 100 & 324.570184 & — & 3\\

\hline
1 & 20 & 4.546087 & 7 & 7 \\
1 & 40 & 60.000322 & — & 13 \\
1 & 60 & 60.000605 & — & 21 \\
1 & 80 & 60.001013 & — & 28 \\
1 & 100 & 60.00161 & — & 32 \\
2 & 20 & 0.002631 & 1 & 1 \\
2 & 40 & 1.13961 & 2 & 2 \\
2 & 60 & 61.630287 & — & 3 \\
2 & 80 & 149.78633 & — & 4 \\
2 & 100 & 169.868335 & — & 4 \\
3 & 20 & 0.000287 & 1 & 1 \\
3 & 40 & 266.920615 & — & 2 \\
3 & 60 & 9.870552 & 2 & 2 \\
3 & 80 & 62.851872 & — & 4 \\
3 & 100 & 60.851042 & — & 5 \\
\hline