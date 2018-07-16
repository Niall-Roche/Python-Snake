green = (0,155,0)

class Block(object):
    """docstring for Block."""
    xPos = 0
    yPos = 0
    colour = green
    size = 0
    img=None
    def __init__(self, xPos, yPos, colour, size, img):
        self.xPos = xPos
        self.yPos = yPos
        self.colour = colour
        self.size = size
        self.img = img

    def get_center(self):
        return (self.xPos + (self.size/2), self.yPos + (self.size/2))

    def top_left(self):
        return (self.xPos, self.yPos)

    def top_right(self):
        return (self.xPos + self.size, self.yPos)

    def bottom_left(self):
        return (self.xPos, self.yPos + self.size)

    def top_left(self):
        return (self.xPos + self.size, self.yPos + self.size)
