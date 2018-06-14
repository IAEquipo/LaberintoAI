class BeingView(View):

    def __init__(self, m, n):
        View.__init__(self, m, n)
        self.map = [[ [-1,0,0,0,0] for j in range(m)] for i in range(n)]

    def paint_map(self, screen):

        x = 0
        y = 0

        for line in self.map:
            for value in line:
                if flag == 0:
                    value = value[0]
                if value == '0':
                    pygame.draw.rect(screen, GRAY, (x, y, PIXEL, PIXEL), 0)
                elif value == '1':
                    pygame.draw.rect(screen, ORANGE_L, (x, y, PIXEL, PIXEL), 0)
                elif value == '2':
                    pygame.draw.rect(screen, BLUE, (x, y, PIXEL, PIXEL), 0)
                elif value == '3':
                    pygame.draw.rect(screen, YELLOW, (x, y, PIXEL, PIXEL), 0)
                elif value == '4':
                    pygame.draw.rect(screen, GREEN, (x, y, PIXEL, PIXEL), 0)
                elif value == -1:
                    pygame.draw.rect(screen, BLACK, (x, y, PIXEL, PIXEL), 0)
                else:
                    pygame.draw.rect(screen, DEFAULT, (x, y, PIXEL, PIXEL), 0)
                x += PIXEL
            y += PIXEL
            x = 0
