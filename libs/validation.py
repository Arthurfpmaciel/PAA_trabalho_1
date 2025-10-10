import bidimensional as bpp
import pandas as pd

df = pd.DataFrame(columns=["n_itens","bin_h_and_w","itens_group","time","n_bins",
                           "total_filled_area","total_void_area","total_void_area_ignore_last","algorithm"])


print("Teste do algoritmo Botton Left")
algorithm = "botton_left"
bin_w_and_h = [10,20]
n_itens = [i*100 for i in range(1,11)]
item_sizes_range = {"group_1":[1,10],"group_2":[1,7],"group_3":[1,3]}
count = 1
for i in n_itens:
    for j in list(item_sizes_range.keys()):
        for k in bin_w_and_h:
            file = f"./data/teste_{count}.txt"
            bp, itens = bpp.load_data(file)
            timer = bp.bottom_left(itens)
            df.loc[len(df)] = [i, k, j, timer, len(bp.bins),bp.filled_areas(), bp.void_areas(), bp.void_areas(True), algorithm]
            count+=1


print("Teste do algoritmo Max Rects")
algorithm = "max_rects"
count = 1
for i in n_itens:
    for j in list(item_sizes_range.keys()):
        for k in bin_w_and_h:
            file = f"./data/teste_{count}.txt"
            bp, itens = bpp.load_data(file)
            timer = bp.max_rects(itens)
            df.loc[len(df)] = [i, j, k, timer, len(bp.bins), bp.filled_areas(), bp.void_areas(), bp.void_areas(True), algorithm]
            count+=1

df.to_csv("./data/df_val.csv", index=False)