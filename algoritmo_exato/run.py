# import sys
# import random
# from libs.algorithm import exact_search_with_external
# from libs.utils import show_bins, load_data
# import time
# if len(sys.argv) < 2:
#     print("Uso: python ./libs/teste.py <caminho para o arquivo de teste>")

# start = time.time()
# file = sys.argv[1]
# random.seed(1)
# # carregar elementos
# bin_w, bin_h, itens = load_data(file)
# # preprocessamento
# itens.sort(key=lambda it: it.area(), reverse=True)

# bins_res, z_res = exact_search_with_external(itens, bin_w=10, bin_h=10, time_limit=10)
# print("z_res:", z_res)
# print("tempo:",round(time.time()-start,5))
# show_bins(bins_res)


import random
from libs.algorithm import exact_search_with_external
from libs.utils import show_bins, load_data, generate_random_itens
import time

random.seed(1)
# carregar elementos
itens = generate_random_itens(60)
# preprocessamento
itens.sort(key=lambda it: it.area(), reverse=True)

start = time.time()
bins_res, z_res = exact_search_with_external(itens, bin_w=10, bin_h=10, time_limit=None)
print("z_res:", z_res)
print("tempo:",round(time.time()-start,5))
show_bins(bins_res)