from tkinter import *
from random import randrange

def grille():
    #ont génère un damié sur le canvas
    for x in range(20,440,20):
        Can.create_line(x,20,x,421, fill = 'darkkhaki')
        Can.create_line(20,x,421,x, fill = 'darkkhaki')

def gene_mine(nbmine):
    #génére aléatoirement un objet mine
    #sur le damié
    global mines
    if nbmine>400:
        return
    for i in range(nbmine):
        x = randrange(20,420,20)
        y = randrange(20,420,20)
        if (x,y) in mines:
            gene_mine(1)
            continue
        mines[(x,y)] = Can.create_rectangle(x,y,x+20,y+20, outline = 'black',
                                            fill = '',tag  = "mine")

def gene_casevide():
    #on génère toute les cases n'étant poas des mines pour mieux les gérer
    global mines
    #on essaie tout les coordonné possible
    for x in range(20,420,20):
        for y in range(20,420,20):
            #onn vérifie de na pas utilise ceux d'une mine
            if (x,y) in mines:
                continue
            #on utilise un tuple plus simple à gérer
            mine = tuple(mines)
            #on test a toutes le distance
            for dist in range(1,20):
                for xmine,ymine in mine:
                    #quand la case et dans la limite ,on a ça distance
                    if xmine-20*dist-1<x<xmine+20*dist+1 \
                    and ymine-20*dist-1<y<ymine+20*dist+1:
                        #on ajoute alors la case dans
                        #le dictionaire avec un tuple(id,dist)
                        casesvides[(x,y)] = (
                            Can.create_rectangle(x, y,x+20, y+20, outline = '',
                                                 tags= 'casevide'), dist)
                        break
                if xmine-20*dist-1<x<xmine+20*dist+1 \
                    and ymine-20*dist-1<y<ymine+20*dist+1:
                    break

def afficher(x,y):
    #prend les coordonné d'une case vide sinon ne fait rien
    global drapeaux, casesvides, couleur
    if (x,y) in mines:
        return
    #elle affiche cette case vide de sorte a ce que l'on voit ça dist
    #on supprime les cases drapeaux de la liste des drapeaux
    if 'drapeaux' in Can.gettags(casesvides[x,y][0]):
        drapeaux = list(set(drapeaux))
        drapeaux.remove((x,y))
    #on verifie qu'il ne sois pas déjà affiché
    if 'affiché' in Can.gettags(casesvides[x,y][0]):
                                return
    Can.itemconfig(casesvides[x,y][0],
                   fill = '#'+str(couleur[casesvides[x,y][1]])+'00',
                   outline = 'black', tags = ('casevide','affiché'))
    Can.create_text(x+10, y+10, text = str(casesvides[x,y][1]),
                    font = ('Time', 10), fill = 'white')

def cliquegauche(event):
    #on gère l'évènement clique gauche sur un case du damié
    global nbcoup, mines, casesvides, WIN
    #au cas ou on aurait perdu , pour éviter de modifié l'écran
    global casesvides, drapeaux, couleur, LOSE
    if LOSE:
        return
    #on récupère les coordonné où on a cliqué et ajusté pour la grille
    x = 20*(event.x//20)
    y = 20*(event.y//20)
    #on s'assure que le clique n'est pas hors du canvas
    if 20>x or 20>y or x>=420 or y>=420:
        return
    #on vérifie si le clique est sur une mine
    if (x,y) in mines:
        #et on lance le game over
        gameover()
    else:
        #on vérifie que se n'est pas une case vide déjà affichée
        if 'affiché' in Can.gettags(casesvides[(x,y)][0]):
            return
        #sinon on compte le nombre de coup
        nbcoup += 1
        Sv22.set("nombre de coups :"+str(nbcoup))
        #et on affiche la case
        afficher(x,y)
        #et indique ses coordonné sur la grille
        text21.config(text = "Vous avez cliquez en\n("+str(x)+","+str(y)+")")

def cliquedroit(event):
    #on gère l'évènement cliquedroit sur le damié
    global mines, drapeaux, casesvides
    x = (event.x//20)*20
    y = (event.y//20)*20
    #on s'assure que le clique n'est pas hors du canvas
    if 20>x or 20>y or x>=420 or y>=420:
        return
    #on teste si c'est une mine ou une case vide et agit en concéquence
    if (x,y) in mines:
        Can.itemconfig(mines[(x,y)], fill = "green", outline = "black")
    else:
        #on vérifie que se n'est pas une case vide déjà affichée
        if 'affiché' in Can.gettags(casesvides[(x,y)][0]):
            return
        Can.itemconfig(casesvides[(x,y)][0], fill = 'green', outline = 'black',
                       tags = ('casevide','drapeaux'))
    drapeaux.append((x,y))
    if set(drapeaux) == set(mines):
        text21.config(text = "Bravo vous avez trouvé les mine, \n YOU WIN")
        for x,y in casesvides:
            afficher(x,y)

def gameover():
    global LOSE
    #gère un game over, et affiche le nécéssaire
    text21.config(text = 'Vous avez cliqué sur une mine,\n GAME OVER')
    Can.itemconfigure("mine", fill = 'red', outline = "red4")
    LOSE = True

#défitnition de la fenêtre
fen = Tk()
fen['bg'] = 'bisque'
fen.title('Démineur')

#définition des frames
Fr1 = Frame(fen, bg = 'bisque')
Fr2 = Frame(fen, bg = 'bisque')

Fr1.pack(side = LEFT, padx = 10, pady = 10)
Fr2.pack(side = RIGHT, padx = 10)

#définition des sous frames
Sfr21 = Frame(Fr2, bg = 'darkgoldenrod')
Sfr22 = Frame(Fr2, bg = 'blue3')
Sfr23 = Frame(Fr2)

Sfr21.pack()
Sfr22.pack()
Sfr23.pack()

#définition du canevas
Can = Canvas(Fr1, width = 440, height = 440, bg = 'khaki')
Can.pack()

#définition variable
nbcoup = 0
Sv22 = StringVar()
Sv22.set("nombre de coup :"+str(nbcoup))
drapeaux = []
mines = {}
casesvides = {}
couleur = {0:'f',1:'e',2:'d',3:'c',4:'b',5:'a',6:'9',7:'8',
           8:7,9:6,10:5,11:4,12:3,13:2,14:1,
           15:0,16:0,17:0,18:0,19:0}
LOSE = False

#défition des Labels
text22 = Label(Sfr21, textvariable = Sv22,
               bg = 'cyan', relief = RAISED
      )
text21 = Label(Sfr21, text = 'Cliquez sur la grille \npour commencer',
      fg = 'goldenrod', bg = 'darkgoldenrod', relief = RAISED, width =30
      )
text21.pack(padx = 50, pady = 50)
text22.pack(padx = 50, pady = 50)
#définition des bouttons

#programme
grille()
gene_mine(10)
gene_casevide()
Can.bind("<Button-1>",cliquegauche)
Can.bind("<Button-3>",cliquedroit)
fen.mainloop()
