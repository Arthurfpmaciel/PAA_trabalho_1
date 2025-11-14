Bin Packing Bidimensional (BP2D) - Algoritmos Exatos e Heurísticas
==================================================================

Este repositório contém o trabalho da disciplina Projeto e Análise de Algoritmos,
no qual foram desenvolvidos:

- Um algoritmo exato
- Duas heurísticas principais: Bottom-Left e MaxRects

para resolver o problema do Bin Packing Bidimensional (BP2D).

------------------------------------------------------------------
Instruções de Execução
------------------------------------------------------------------

1. (Opcional) Criar ambiente virtual
   ```sh
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```
2. Instalar dependências
   ```sh
   pip install -r requirements.txt
   ```
3. Entrar no diretório do algoritmo desejado

   - Algoritmo Exato:
     ```sh
     cd algoritmo_exato
     ```
   - Heurísticas:
     ```sh
     cd heuristicas
     ```
4. Executar
    
   - Algoritmo Exato:
     ```sh
     python main.py
     ```
   - Heurísticas:
     ```sh
     python libs/main.py
     ```
