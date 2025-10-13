import os
import copy
from validation import executar_todos_os_testes
from bidimensional import BinPacking, generate_random_itens, load_data

def run_and_display_results(bin_w, bin_h, itens, test_name):
    print("\n" + "="*40)
    print(f"  Resultados para: {test_name}")
    print(f"  Itens a serem empacotados: {len(itens)}")
    print(f"  Dimensões da caixa: {bin_w}x{bin_h}")
    print("="*40 + "\n")

    itens_bl = copy.deepcopy(itens)
    bp_bl = BinPacking(bin_w, bin_h)
    
    print("--- Executando Bottom-Left ---")
    time_bl = bp_bl.bottom_left(itens_bl)
    print(f"Bins usados: {len(bp_bl.bins)}")
    print(f"Área vazia (desconsiderando a última bin): {bp_bl.void_areas(ignore_last=True)}")
    print(f"Tempo de execução: {time_bl:.6f} segundos\n")

    itens_mr = copy.deepcopy(itens)
    bp_mr = BinPacking(bin_w, bin_h)

    print("--- Executando Maximal Rectangles ---")
    time_mr = bp_mr.max_rects(itens_mr)
    print(f"Bins usados: {len(bp_mr.bins)}")
    print(f"Área vazia (desconsiderando a última bin): {bp_mr.void_areas(ignore_last=True)}")
    print(f"Tempo de execução: {time_mr:.6f} segundos\n")

    while True:
        choice = input("Deseja visualizar o resultado gráfico? (s/n): ").lower()
        if choice == 's':
            print("\nExibindo gráficos para Bottom-Left...")
            bp_bl.show_bins()
            print("Exibindo gráficos para Maximal Rectangles...")
            bp_mr.show_bins()
            break
        elif choice == 'n':
            break

def escolher_arquivo():
    """
    Permite escolher um arquivo de teste dentro de data/binXX/grupo/
    """
    base_path = "data"

    print("\nEscolha o tamanho do bin:")
    print("1. bin10")
    print("2. bin20")
    choice_bin = input("Opção: ")
    if choice_bin == '1':
        bin_folder = "bin10"
    elif choice_bin == '2':
        bin_folder = "bin20"
    else:
        print("\n[ERRO] Opção inválida.")
        return None

    print("\nEscolha o grupo de itens:")
    print("1. grandes")
    print("2. medios")
    print("3. pequenos")
    choice_group = input("Opção: ")
    if choice_group == '1':
        group_folder = "grandes"
    elif choice_group == '2':
        group_folder = "medios"
    elif choice_group == '3':
        group_folder = "pequenos"
    else:
        print("\n[ERRO] Opção inválida.")
        return None

    folder_path = os.path.join(base_path, bin_folder, group_folder)

    if not os.path.exists(folder_path):
        print(f"\n[ERRO] Pasta não encontrada: {folder_path}")
        return None

    arquivos = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    if not arquivos:
        print("\n[ERRO] Nenhum arquivo .txt encontrado nessa pasta.")
        return None

    print("\nArquivos disponíveis:")
    for i, arq in enumerate(arquivos, start=1):
        print(f"{i}. {arq}")

    try:
        choice_file = int(input("\nEscolha o número do arquivo: "))
        if 1 <= choice_file <= len(arquivos):
            return os.path.join(folder_path, arquivos[choice_file - 1])
        else:
            print("\n[ERRO] Escolha inválida.")
            return None
    except ValueError:
        print("\n[ERRO] Entrada inválida.")
        return None


def main():
    while True:
        print("\n" + "="*50)
        print("               BIN PACKING 2D")
        print("="*50)
        print("\nEscolha um dos testes abaixo:\n")
        print("1. Teste Pequeno (20 itens)")
        print("2. Teste Médio (100 itens)")
        print("3. Teste Grande (500 itens)")
        print("4. Teste com Itens Variados (200 itens)")
        print("5. Escolher Arquivo de Teste (.txt da pasta data/binXX/grupo)")
        print("6. Executar todos os testes (pode demorar um pouco)")
        print("9. Teste Personalizado")
        print("0. Sair\n")

        choice = input("Digite sua escolha: ")

        bin_w, bin_h = 10, 10
        itens = []
        test_name = ""

        if choice == '1':
            test_name = "Teste Pequeno"
            itens = generate_random_itens(n=20, min_value=1, max_value=4)
            run_and_display_results(bin_w, bin_h, itens, test_name)

        elif choice == '2':
            test_name = "Teste Médio"
            itens = generate_random_itens(n=100, min_value=1, max_value=5)
            run_and_display_results(bin_w, bin_h, itens, test_name)
            
        elif choice == '3':
            test_name = "Teste Grande"
            itens = generate_random_itens(n=500, min_value=1, max_value=6)
            run_and_display_results(bin_w, bin_h, itens, test_name)

        elif choice == '4':
            test_name = "Teste com Itens Variados"
            itens_pequenos = generate_random_itens(n=100, min_value=1, max_value=3)
            itens_grandes = generate_random_itens(n=100, min_value=4, max_value=7)
            itens = itens_pequenos + itens_grandes
            run_and_display_results(bin_w, bin_h, itens, test_name)

        elif choice == '5':
            file_path = escolher_arquivo()
            if file_path:
                print(f"\nArquivo selecionado: {file_path}")
                try:
                    bp_template, itens = load_data(file_path)
                    run_and_display_results(bp_template.bin_w, bp_template.bin_h, itens, f"Arquivo: {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"\n[ERRO] Falha ao carregar arquivo: {e}")
        elif choice == '6':
            print("\nExecutando todos os testes automáticos...\n")
            executar_todos_os_testes()

        elif choice == '9':
            try:
                p_bin_w = int(input("Largura da caixa (padrão 10): ") or "10")
                p_bin_h = int(input("Altura da caixa (padrão 10): ") or "10")
                p_n_itens = int(input("Número de itens: "))
                p_min_val = int(input("Tamanho mínimo do item: "))
                p_max_val = int(input("Tamanho máximo do item: "))

                if p_min_val > p_max_val:
                    print("\n[ERRO] O tamanho mínimo não pode ser maior que o máximo.")
                    continue

                itens = generate_random_itens(p_n_itens, p_min_val, p_max_val)
                run_and_display_results(p_bin_w, p_bin_h, itens, "Teste Personalizado")
            except Exception as e:
                print(f"\n[ERRO] {e}")

        elif choice == '0':
            print("\nSaindo do programa.")
            break

        else:
            print("\n[ERRO] Opção inválida.")

        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()