import random
import time
import copy
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from libs.sa import *
from validation import validation

def menu_principal():
    while True:
        print("\n======================================")
        print(" EXECUTAR TESTE META-HEURÍSTICA: SIMULATED ANNEALING (SA)")
        print("======================================\n")
        print("1 - Teste personalizado")
        print("2 - Executar conjunto de experimento 1")
        print("3 - Executar conjunto de experimento 2")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            teste_sa_personalizado()
        elif opcao == "2":
            print("\nDigite o time limit em segundos (ENTER para usar 300): ", end="")
            entrada = input().strip()

            if entrada == "":
                time_limit = 300
            else:
                try:
                    time_limit = int(entrada)
                except ValueError:
                    print("Entrada inválida! Usando time limit padrão = 300.")
                    time_limit = 300
        elif opcao == "3":
            groups = ["pequenos", "medios", "grandes"]

            print("Selecione a classe de itens:")
            print("0 - pequenos")
            print("1 - medios")
            print("2 - grandes")

            entrada = input("Digite a opção: ").strip()
            if not entrada.isdigit():
                print("Opção inválida! Digite apenas 0, 1 ou 2.")
                return
            entrada = int(entrada)
            if entrada < 0 or entrada > 2:
                print("Opção inválida! Escolha apenas 0, 1 ou 2.")
                return

            validation(groups[entrada])
        elif opcao == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida! Tente novamente.")

def teste_sa_personalizado():
    print("\n=== Testar Simulated Annealing (BP2D) ===")

    try:
        qtd = int(input("Quantidade de itens: "))
    except ValueError:
        print("Entrada inválida!")
        return

    if qtd < 1:
        print("\nERRO: A quantidade mínima de itens é 1.")
        return

    inp = input("Tamanho máximo do item (padrão 10): ").strip()
    try:
        tamanho_itens = int(inp) if inp else 10
    except ValueError:
        print("Entrada inválida!")
        return

    if tamanho_itens < 1:
        print("\nERRO: O tamanho do item deve ser pelo menos 1.")
        return

    inp = input("Tamanho da largura/altura do bin (padrão 10): ").strip()
    try:
        bin_w = bin_h = int(inp) if inp else 10
    except ValueError:
        print("Entrada inválida!")
        return

    if bin_w < 5 or bin_h < 5:
        print("\nERRO: O tamanho mínimo do bin é 5.")
        return

    if tamanho_itens > bin_w or tamanho_itens > bin_h:
        print("\nERRO: O tamanho máximo do item deve ser menor ou igual ao tamanho do bin!")
        return

    print("\n--- Parâmetros do Simulated Annealing ---")

    inp = input("Temperatura inicial T0 (padrão 1000): ").strip()
    try:
        T0 = float(inp) if inp else 1000.0
    except ValueError:
        print("Valor inválido.")
        return

    inp = input("Fator de resfriamento alpha (padrão 0.95): ").strip()
    try:
        alpha = float(inp) if inp else 0.95
    except ValueError:
        print("Valor inválido.")
        return

    inp = input("Fator L (iterações por temperatura) [padrão 10]: ").strip()
    try:
        L_factor = int(inp) if inp else 10
    except ValueError:
        print("Valor inválido.")
        return

    inp = input("Temperatura mínima T_min (padrão 1e-3): ").strip()
    try:
        T_min = float(inp) if inp else 1e-3
    except ValueError:
        print("Valor inválido.")
        return

    inp = input("Número máximo de iterações (padrão 200): ").strip()
    try:
        max_iters = int(inp) if inp else 200
    except ValueError:
        print("Valor inválido.")
        return

    inp = input("Heurística de encaixe (mr, bl, bf) [padrão = mr]: ").strip().lower()
    method = inp if inp else "mr"

    itens = generate_random_itens(qtd, 1, tamanho_itens)

    print("\nExecutando Simulated Annealing...")
    start = time.time()
    resultado = simulated_annealing(
        itens,
        bin_w=bin_w,
        bin_h=bin_h,
        method=method,
        T0=T0,
        alpha=alpha,
        L_factor=L_factor,
        T_min=T_min,
        max_iters=max_iters
    )
    end = time.time()

    print("\n=== Resultado Simulated Annealing ===")
    print(f"Tempo total: {end - start:.4f} s")
    print(f"Bins Usados: {len(resultado['best_bp'].bins)}")

    bins = resultado["best_bp"]
    show_bins(bins)

if __name__ == "__main__":
    menu_principal()


# apresentação: executar os testes:
    # 10 itens de tamanho até 10
    # 20 itens de tamanho ate 7
    # 50 itens de tamanho até 3