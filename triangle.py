import pygame.gfxdraw
from shapely.geometry import Point, Polygon

class Triangle:
    def __init__(self, cords, color, num):
        self.cords = cords
        self.first_point = cords[0]
        self.middle_point = cords[1]
        self.last_point = cords[2]
        self.poly_obj = Polygon(cords)
        self.color = color
        self.num = num

    def draw(self, surface):
        pygame.gfxdraw.aapolygon(surface, self.cords, self.color)
        pygame.gfxdraw.filled_polygon(surface, self.cords, self.color)

    def collide_with_mouse(self, mouse_x, mouse_y):
        mouse_point = Point(mouse_x, mouse_y)
        return self.poly_obj.contains(mouse_point)

    def get_num(self):
        return self.num