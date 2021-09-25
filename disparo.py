import colores

class Disparo:
    def __init__(self, win, shoting, x, y):
        self.x = x
        self.y = y
        self.w = 5
        self.h = 15
        self.shoting = shoting
        self.win = win
        self.col = colores.col

    def show(self, avionx, aviony):
        if self.shoting:
            self.shoting = False
            if self.y <= 0:
                self.x = avionx
                self.y = aviony
        if self.y > -self.h:
            self.y -= 6
        self.win.fill(self.col[13], rect=[self.x, self.y, self.w, self.h])
