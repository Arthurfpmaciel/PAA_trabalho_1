import bidimensional as bpp
import os
import time
import copy

def format_row(columns):
    """Formata as colunas para espaçamento fixo."""
    return (
        f"{str(columns[0]):<10}"   # bin_size
        f"{str(columns[1]):<10}"   # n_itens
        f"{str(columns[2]):<12}"   # item_group
        f"{str(columns[3]):<15}"   # algorithm
        f"{str(columns[4]):<10}"   # n_bins
        f"{str(columns[5]):<12}"   # time_sec
        f"{str(columns[6]):<18}"   # total_filled_area
        f"{str(columns[7]):<18}"   # total_void_area
        f"{str(columns[8]):<18}"   # total_void_area_ignore_last
    )


def executar_todos_os_testes(
    bins_folder="./data",
    algorithms=("bottom_left", "max_rects"),
    output_file="./data/resultados_execucao.txt"
):
    """
    Executa todos os testes encontrados na pasta 'data',
    para todas as heurísticas e combinações de arquivos.
    """
    with open(output_file, "w") as f:
        for algo in algorithms:
            f.write(f"\n{'='*30}\n")
            f.write(f"RESULTADOS DO ALGORITMO: {algo.upper()}\n")
            f.write(f"{'='*30}\n\n")

            # Cabeçalho da tabela
            f.write(format_row([
                "bin_size", "n_itens", "item_group", "algorithm",
                "n_bins", "time_sec", "total_filled_area",
                "total_void_area", "total_void_area_ignore_last"
            ]) + "\n")
            f.write("-" * 110 + "\n")

            for bin_size_folder in os.listdir(bins_folder):
                bin_size_path = os.path.join(bins_folder, bin_size_folder)
                if not os.path.isdir(bin_size_path):
                    continue

                try:
                    bin_size = int(bin_size_folder.replace("bin", ""))
                except:
                    continue

                for item_group_folder in os.listdir(bin_size_path):
                    group_path = os.path.join(bin_size_path, item_group_folder)
                    if not os.path.isdir(group_path):
                        continue

                    for file_name in os.listdir(group_path):
                        if not file_name.endswith(".txt"):
                            continue
                        file_path = os.path.join(group_path, file_name)

                        # Carrega os dados
                        bp, itens = bpp.load_data(file_path)

                        bp_copy = copy.deepcopy(bp)
                        itens_copy = copy.deepcopy(itens)

                        start = time.time()
                        if algo == "bottom_left":
                            bp_copy.bottom_left(itens_copy)
                        else:
                            bp_copy.max_rects(itens_copy)
                        elapsed = time.time() - start

                        # Escreve resultado
                        f.write(format_row([
                            bin_size,
                            len(itens),
                            item_group_folder,
                            algo,
                            len(bp_copy.bins),
                            f"{elapsed:.6f}",
                            bp_copy.filled_areas(),
                            bp_copy.void_areas(),
                            bp_copy.void_areas(ignore_last=True)
                        ]) + "\n")

            f.write("\n\n")

    print(f"\nResultados organizados e salvos em {output_file}\n")
