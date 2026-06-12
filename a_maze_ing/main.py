import pdb;

class Cell():
    _h:int
    _w:int
    _x:int
    _y:int
    _visited: bool


    def __init__(self, x:int, y:int, h: int, w: int) :
        self._h = h
        self._w = w
        self._x = x
        self._y = y

    def get_char(self, h: int, w: int) -> str:
        if(h == 0 or h == self._h - 1):
            if(w == self._w - 1):
                return ("+\n")
            else:
                return("+ ")
        if (h > 0  and h < self._h): 
            if(w == 0):
                return ("+ ")
            elif (w == self._w - 1):
                return ("+\n")
            else:
                return "  "
        if (h == self._h - 1): 
            if(w == 0):
                return ("+")
            if (w == self._w - 1):
                return ("+")
    
    def display_cell(self) -> None:
        for _h in range(0, self._h):
            for _w in range(0, self._w):
                print(self.get_char(_h, _w), end="")

    def set_visited_status(self, status:bool) -> None:
        self._visited = status

class Maze(Cell):
    _m_h: int
    _m_w: int
    _c_h: int 
    _c_w: int
    _cells: list[Cell]

    def __init__(self, m_h: int, m_w: int, c_h: int, c_w: int) -> None:
        self._m_h = m_h
        self._m_w = m_w
        self._c_h = c_h
        self._c_w = c_w
        self._cells = []

    def display_maze(self) -> None:
        for c in self._cells:
            c.display_cell()    

    def map_initialisation(self) -> None:
        for x in range(self._m_h):
            for y in range(self._m_w):
                cell = Cell(x, y, self._c_h, self._c_w)
                self._cells.append(cell)
        assert(len(self._cells) > 0)
    

def main():
    maze = Maze(10,10,4,4)
    maze.map_initialisation()
    maze.display_maze()


if __name__ == "__main__":
    main()
