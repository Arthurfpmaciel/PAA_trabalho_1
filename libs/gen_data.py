import os
from bidimensional import generate_data, save_data

# parâmetros dos bins e itens
bin_sizes = [10, 20]
n_itens_list = [100, 200, 400, 800, 1600, 3200, 6400, 12800]
item_sizes_range = {
    "pequenos": [1, 3],
    "medios": [1, 7],
    "grandes": [1, 10]
}

# contadores para cada combinação bin x faixa
counters = {
    10: {"pequenos": 0, "medios": 0, "grandes": 0},
    20: {"pequenos": 0, "medios": 0, "grandes": 0}
}

for bin_size in bin_sizes:
    for faixa, size_range in item_sizes_range.items():
        folder = f"./data/bin{bin_size}/{faixa}"
        
        for n in n_itens_list:
            # gera os dados
            bp, itens = generate_data(bin_size, bin_size,
                                      size_range[0], size_range[1], n)
            
            # incrementa o contador
            counters[bin_size][faixa] += 1
            count = counters[bin_size][faixa]
            
            # define o nome do arquivo
            filename = f"{folder}/teste_bin{bin_size}_{faixa}_{count}.txt"
            
            # salva o arquivo
            save_data(bp, itens, filename)
            
            # imprime para conferência
            print(f"Gerado {filename} com {len(itens)} itens ({size_range[0]}-{size_range[1]})")
