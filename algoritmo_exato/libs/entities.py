# classe de itens para o algoritmo exato
class Item:
    _next_id = 0
    def __init__(self, w, h, id=None):
        self.w = w
        self.h = h
        self.x = None
        self.y = None
        if id is None:
            self.id = Item._next_id
            Item._next_id += 1
        else:
            self.id = id
    # configurar coordenadas
    def set_position(self,x,y):
        self.x = x
        self.y = y
    # calcular área
    def area(self):
        return self.w * self.h
    # copiar item
    def copy(self):
        return Item(self.w, self.h, id=self.id)
    # representação em string
    def __repr__(self):
        return f"I{self.id}({self.w}x{self.h})"

# classe de caixas para o algorimto exato
class Bin:
    def __init__(self, w=10, h=10):
        self.w = w; self.h = h
        self.itens = []
        
    # verifica se um item cabe na bin na posição x y
    def fits(self, item, x, y):
        if x + item.w > self.w or y + item.h > self.h:
            return False
        for i in self.itens:
            if not (x + item.w <= i.x or x >= i.x + i.w or y + item.h <= i.y or y >= i.y + i.h):
                return False
        return True
    # armazenar item na posição x y
    def pack(self,item,x,y):
        if self.fits(item,x,y):
            item.set_position(x,y)
            self.itens.append(item)
            return True
        return False
    
    # calcula a área com itens
    def filled_area(self):
        return sum(i.area() for i in self.itens)
    
    # calcula a área vazia
    def void_area(self):
        return self.w*self.h - self.filled_area()

    # representação em string
    def __repr__(self):
        return f"Bin({len(self.itens)} items, filled={self.filled_area()}/{self.w*self.h})"