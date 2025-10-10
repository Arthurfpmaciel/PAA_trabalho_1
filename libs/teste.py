import sys
import bidimensional as bpp

if len(sys.argv) < 2:
    print("Uso: python ./libs/teste.py <caminho para o arquivo de teste>")

file = sys.argv[1]

bp, itens = bpp.load_data(file)

bp.max_rects(itens)
bp.show_bins()
