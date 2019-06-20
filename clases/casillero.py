class Casillero():
    def __init__(self, posx, posy, letra, color='white', seleccionado=False):
        self.posx = posx
        self.posy = posy
        self.letra = letra
        self.color = color
        self.seleccionado = seleccionado
    
    
    #Métodos 
    def __str__(self):
        return (self.letra + ' (' + str(self.posx) + ', ' + str(self.posy) + ')')

    def get_posx(self):
        return (self.posx)
        
    def set_posx(self, posx):
        self.posx = posx
    
    def get_posy(self):
        return (self.posy)
        
    def set_posy(self, posy):
        self.posy = posy
    
    def get_letra(self):
        return (self.letra)
        
    def set_letra(self, letra):
        self.letra = letra
    
    def get_color(self):
        return (self.color)
        
    def set_color(self, color):
        self.color = color
    
    def click(self, color):
        self.seleccionado = not self.seleccionado
        
        if (self.seleccionado):
            self.color = color
        else:
            self.color = 'white'

    def esta_seleccionado(self):
        return self.seleccionado
