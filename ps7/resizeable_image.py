import imagematrix

class ResizeableImage(imagematrix.ImageMatrix):
    def best_seam(self):
        table = {}
        for j in range(self.height):
            for i in range(self.width):
                if j == 0:
                    table[(i,j)] = [self.energy(i,j), [(i,j)]]
                else:
                    options = []
                    options.append(table[(i,j-1)])
                    if i > 0:
                        options.append(table[(i-1,j-1)])
                    if i < self.width - 1:
                        options.append(table[(i+1,j-1)])

                    best = 'inf'
                    this_energy = self.energy(i,j)
                    for option in options:
                        if option[0] < best:
                            best = option[0]
                            table[(i,j)] = [ this_energy + option[0], option[1] + [(i,j)]]
        ans = table[(0,self.height - 1)]
        for i in range(self.width):
            option = table[(i, self.height - 1)]
            if option[0] < ans[0]:
                ans = option
        return ans[1]

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
