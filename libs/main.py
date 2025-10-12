import copy
from bidimensional import BinPacking, generate_random_itens, load_data

def run_and_display_results(bin_w, bin_h, itens, test_name):
    """
    Executa ambas as heurísticas para um conjunto de itens e exibe os resultados.
    """
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

def main():
    """
    Função principal que exibe o menu e gerencia a entrada do usuário.
    """
    while True:
        print("\n" + "="*50)
        print("    INTERFACE DE TESTES PARA BIN PACKING 2D")
        print("="*50)
        print("\nEscolha um dos testes abaixo:\n")
        print("1. Teste Pequeno (20 itens) - Ideal para visualização rápida.")
        print("2. Teste Médio (100 itens) - Um cenário balanceado.")
        print("3. Teste Grande (500 itens) - Para comparar desempenho em escala.")
        print("4. Teste Desafiador (50 itens grandes) - Itens com tamanho próximo ao da caixa.")
        print("5. Teste com Itens Variados (200 itens) - Mistura de itens muito pequenos e grandes.")
        print("6. Carregar de Arquivo (data/teste.txt) - Use um conjunto de dados predefinido.")
        print("9. Teste Personalizado - Você define todos os parâmetros.")
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
            test_name = "Teste Desafiador (Itens Grandes)"
            itens = generate_random_itens(n=50, min_value=4, max_value=8)
            run_and_display_results(bin_w, bin_h, itens, test_name)

        elif choice == '5':
            test_name = "Teste com Itens Variados"
            itens_pequenos = generate_random_itens(n=100, min_value=1, max_value=3)
            itens_grandes = generate_random_itens(n=100, min_value=4, max_value=7)
            itens = itens_pequenos + itens_grandes
            run_and_display_results(bin_w, bin_h, itens, test_name)
        
        elif choice == '6':
            test_name = "Carregar de Arquivo"
            file_path = ".data/teste.txt"  # Altere este caminho se necessário
            try:
                bp_template, itens = load_data(file_path)
                run_and_display_results(bp_template.bin_w, bp_template.bin_h, itens, test_name)
            except FileNotFoundError:
                print(f"\n[ERRO] Arquivo não encontrado em: '{file_path}'")
                print("Por favor, crie o arquivo ou escolha outra opção.")
            except Exception as e:
                print(f"\n[ERRO] Ocorreu um problema ao ler o arquivo: {e}")

        elif choice == '9':
            test_name = "Teste Personalizado"
            try:
                p_bin_w = int(input("Largura da caixa (padrão 10): ") or "10")
                p_bin_h = int(input("Altura da caixa (padrão 10): ") or "10")
                p_n_itens = int(input("Número de itens: "))
                p_min_val = int(input("Tamanho mínimo do item: "))
                p_max_val = int(input("Tamanho máximo do item: "))

                if p_min_val > p_max_val:
                    print("\n[ERRO] O tamanho mínimo não pode ser maior que o máximo.")
                    continue
                if p_max_val > p_bin_w or p_max_val > p_bin_h:
                    print("\n[AVISO] O tamanho máximo do item é maior que a dimensão da caixa.")

                itens = generate_random_itens(p_n_itens, p_min_val, p_max_val)
                run_and_display_results(p_bin_w, p_bin_h, itens, test_name)

            except ValueError:
                print("\n[ERRO] Por favor, insira apenas números inteiros.")
            except Exception as e:
                print(f"\n[ERRO] Ocorreu um erro inesperado: {e}")
        
        elif choice == '0':
            print("\nSaindo do programa. Até mais!")
            break
            
        else:
            print("\n[ERRO] Opção inválida. Por favor, tente novamente.")
        
        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()