from bidimensional import generate_data, save_data

bin_w = 10
bin_h = 10
count = 0

bin_w_and_h = [10,20]
n_itens = [i*100 for i in range(1,11)]
item_sizes_range = [[1,10],[1,7],[1,3]]

for i in n_itens:
    for j in item_sizes_range:
        for k in bin_w_and_h:
            bp, itens = generate_data(k, k,j[0],j[1],i)
            count+=1
            save_data(bp,itens,f"./data/teste_{count}.txt")