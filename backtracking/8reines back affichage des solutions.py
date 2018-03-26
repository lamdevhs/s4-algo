# -*- coding: utf-8 -*-

#fonctions d'affichage avec TKinter  ##########################################
from Tkinter import*
from copy import*
import time


ecriture=("comic sans ms",16)


def afficher_valeur_case(p,sol,canevas):
    pas=50
    #ecriture de la nouvelle valeur
    if sol[p]==-1:
        canevas.create_text(25+pas*p, 25,text=-1,font="comic 18",fill="brown")
    else:
        canevas.create_text(25+pas*p, 25,text=sol[p],font="comic 18",fill="black")
   
    
def afficher_sol(sol,canevas):
    time.sleep(0.01)
    canevas.delete(ALL)
    #remplissage 
    for i in range(len(sol)):
        afficher_valeur_case(i,sol,canevas)
    fenetre.update()            


#fonctions de résolution bk #######################################################
 # sol est la solution étendue en (p,N) .
 # La dame en ligne p est elle bien placée?
def ajout_possible(p, sol):
     ok=True
     lig=0
     while lig < p and ok:
         if (sol[lig] == sol[p] or            # conflit sur une colonne
             sol[lig] + lig == sol[p] + p or  # conflit sur une diagonale
             sol[lig] - lig == sol[p] - p):   # autre diagonale
                 ok=False
         else:
             lig+=1 
     return ok



 # E: N :largeur de l'échiquier
 #    p : numéro de la ligne traitée 
 # S: affichage des solutions.  
def placer_dame1(p, N,sol):
     if p == N:
         global cpt_sol
         cpt_sol+=1
         print (sol)
     else:
              # Essaie de placer une dame sur chaque colonne à la ligne n.
              for col in range(N):
                  sol[p]=col
                  afficher_sol(sol,canevas)
                  if ajout_possible(p, sol):
                          placer_dame1(p+1,N,sol)
                  sol[p]=-1 #ici pas obligatoire mais permet de suivre visuellement
              afficher_sol(sol,canevas)

def reines1(N):
    global cpt_sol
    cpt_sol=0
    sol=[-1]*N
    placer_dame1(0, N,sol)
    print(cpt_sol)
    
#version avec append et pop

 # E: N :largeur de l'échiquier
 #    p : numéro de la ligne traitée 
 # S: affichage des solutions.  
def placer_dame2(p, N,sol):
     if p == N:
         global cpt_sol
         cpt_sol+=1
         print (sol)
     else:
              # Essaie de placer une dame sur chaque colonne à la ligne n.
              for col in range(N):
                  sol.append(col)
                  afficher_sol(sol,canevas)                  
                  if ajout_possible(p, sol):
                          placer_dame2(p+1,N,sol)
                  sol.pop() #aucun candidat solution on revient en arrière
                  #afficher_sol(sol,canevas)                 

def reines2(N):
    global cpt_sol
    cpt_sol=0
    sol=[]
    placer_dame2(0, N,sol)
    print(cpt_sol)

#################################################################################"

fenetre=Tk()  
cadre=Frame(fenetre,borderwidth=4)

texte1=Label(fenetre,text="8 reines",fg="green",font=ecriture)
texte1.pack(side="top")

canevas=Canvas(fenetre,height=50,width=400,bg="white")  #création
canevas.pack()   #affichage

#reines1(8)
reines2(8)

fenetre.mainloop()
    