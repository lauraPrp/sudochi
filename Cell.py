class Cell:
    def __init__(self, x_coord, y_coord, value,colour,is_selected):
        self.colour = colour
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.value = value
        self.is_selected = is_selected



    def highlight(self):
        self.colour="255,255,0"
