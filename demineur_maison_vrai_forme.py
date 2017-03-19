from tkinter import *
from random import randrange


class Grille:
    """grille prend deux argument:
           - dimg = dimension de la grille en carré par coté
           - dimc = dimension d'un carré en pixel """
    def __init__(self, dimg, dimc):
        self.dimg = dimg
        self.dimc = dimc
        self.dimgpix = dimg*dimc
        self.cases = set({})

    def afficher_grille(self, fen, bg = 'white', fg = 'black', border = 10):
        """créé le canvas avec les lignes correspondant à la grille,
           -bg est la couleur de l'arrière plan
           -fg est la couleur des lignes
           -border est le décalage entre la grille et le bord du canvas"""
        self.can = Canvas(fen, width = self.dimgpix+border*2,
                         height = self.dimgpix+border*2, bg = bg)
        self.can.pack(padx = 10, pady = 10)

        if self.cases:
            for case in self.cases:
                x = case.coord_get()[0]
                y = case.coord_get()[1]
                self.can.create_rectangle(x*self.dimc+border, y*self.dimc+border,
                                        (x+1)*self.dimc+border,
                                        (y+1)*self.dimc+border, outline = fg)
            

    def addcase(self, case):
        self.cases.add(case)

    def mine_get(self):
        return [case.coord_get() for case in self.cases
                    if case.genre_get() == 'mine']
    
    def cases_get(self):
        return [case.coord_get() for case in self.cases]
    
class Case:
    """ objet case:
         -x et y sont les coordonné
         -genre : mine, vide
         -tag : drapeaux, chiffre, blank"""
    def __init__(self, x, y, genre):
        self.coord = (x,y)
        self.genre = genre

    def tag(self, tag):
        self.tag = tag

    def genre_get(self):
        return self.genre

    def tag_get(self):
        if self.tag:
            return self.tag
        else:
            return None

    def coord_get(self):
        return self.coord

        
def initialisation():
    """Créé la fenêtre et son contenue:
    sous fenêtre, label, canvas ..."""
    fen = Tk()
    fen.title('Démineuré')
    #fen.geometry('400x400')

    Sf1 = Frame(fen, width = 200, height = 200, bg = 'red')
    Sf2 = Frame(fen, width = 200, height = 200, bg = 'blue')
    Sf1.grid()
    Sf2.grid()
    Grl = Grille(20, 20)
    
    Sf1.grid_propagate(0)
    gene_cases(Grl,5,Sf2, 20)
    return fen

def gene_cases(grille, nbmines, fen, largeur):
    for i in range(nbmines):
        x = randrange(0,largeur)
        y = randrange(0,largeur)
        if (x, y) in grille.mine_get():
            nbmines += 1
            continue
        else:
            grille.addcase(Case(x, y, 'mine'))
        
    for x in range(largeur):
        for y in range(largeur):
            if (x, y) in grille.mine_get():
                continue
            else:
                grille.addcase(Case(x, y, 'vide'))
    grille.afficher_grille(fen, border = 20, bg = 'lightgrey')

  
if __name__ == "__main__":
    initialisation().mainloop()
