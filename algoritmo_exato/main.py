import os
import time
import copy
from libs.algorithm import exact_search_with_external
from libs.utils import show_bins, load_data, total_filled_area, total_void_area, generate_random_itens
from validation2 import *
from validation1 import *
import pandas as pd


def menu_principal():
    while True:
        print("\n======================================")
        print(" Executar testes algoritmo exato")
        print("======================================\n")
        print("1 - Teste personalizado")
        print("2 - Executar conjunto de experimento 1")
        print("3 - Executar conjunto de experimento 2")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            testepersonalizado()
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
            validation2(time_limit)
        elif opcao == "3":
            print("\nDigite o time limit em segundos (ENTER para usar 60): ", end="")
            entrada = input().strip()

            if entrada == "":
                time_limit = 60
            else:
                try:
                    time_limit = int(entrada)
                except ValueError:
                    print("Entrada inválida! Usando time limit padrão = 60.")
                    time_limit = 60
            validation()
        elif opcao == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida! Tente novamente.")


def testepersonalizado():
    print("\n=== Testar Personalizado ===")

    # --- quantidade de itens ---
    try:
        qtd = int(input("Quantidade de itens: "))
    except ValueError:
        print("Entrada inválida!")
        return

    if qtd < 1:
        print("\nERRO: A quantidade mínima de itens é 1.")
        return

    # --- tamanho máximo dos itens ---
    inp = input("Tamanho máximo do item (padrão 10): ").strip()
    try:
        tamanho_itens = int(inp) if inp else 10
    except ValueError:
        print("Entrada inválida!")
        return

    if tamanho_itens < 1:
        print("\nERRO: O tamanho do item deve ser pelo menos 1.")
        return

    # --- tamanho do bin ---
    inp = input("Tamanho da largura/altura do bin (padrão 10): ").strip()
    try:
        bin_w = bin_h = int(inp) if inp else 10
    except ValueError:
        print("Entrada inválida!")
        return

    if bin_w < 5 or bin_h < 5:
        print("\nERRO: O tamanho mínimo do bin é 5.")
        return

    # --- validação: item precisa caber no bin ---
    if tamanho_itens > bin_w or tamanho_itens > bin_h:
        print("\nERRO: O tamanho máximo do item deve ser menor ou igual ao tamanho do bin!")
        return

    # Geração dos itens
    itens = generate_random_itens(qtd, 1, tamanho_itens)

    print("\nExecutando algoritmo exato...")
    start = time.time()
    resultado = exact_search_with_external(itens, bin_w, bin_h)
    end = time.time()

    print(f"\nTempo: {end - start:.4f} s")

    if isinstance(resultado, dict) and "bins" in resultado:
        bins = resultado["bins"]
    else:
        bins = resultado[0]

    show_bins(bins)

if __name__ == "__main__":
    menu_principal()