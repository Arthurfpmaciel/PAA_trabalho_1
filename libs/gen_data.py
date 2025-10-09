from bidimensional import generate_data, save_data

bin_w = 10
bin_h = 10
n_itens = [10,20,50,100,200]
item_sizes_range = [[1,10],[1,7],[1,3]]
count = 0
for i in n_itens:
    for j in item_sizes_range:
        bp, itens = generate_data(bin_w, bin_h,j[0],j[1],i)
        count+=1
        save_data(bp,itens,f"./data/teste_{count}.txt")