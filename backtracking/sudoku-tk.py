# -*- coding: utf-8 -*-

import time
from Tkinter import *

# E: . liste représentant la solution explorée en cours
#    . position de la dernière insertion dans la liste
# S: True si l'insertion est acceptable pour la ligne
def checkLine(solution, position):
  line = position // 9
  col = position % 9
  v = solution[position]
  for i in range(col):
    ix = line*9 + i
    x = solution[ix]
    if x == v:
      return False
  return True

# E: . liste représentant la solution explorée en cours
#    . position de la dernière insertion dans la liste
# S: True si l'insertion est acceptable pour la colonne
def checkColumn(solution, position):
  col = position % 9
  line = position // 9
  v = solution[position]
  for i in range(line):
    ix = col + i*9
    x = solution[ix]
    if x == v:
      return False
  return True

# E: . liste représentant la solution explorée en cours
#    . position de la dernière insertion dans la liste
# S: True si l'insertion est acceptable pour la zone carrée
#    qui contient la position
def checkSquare(solution, position):
  line = position // 9
  col = position % 9
  v = solution[position]
  minLine = line - (line % 3)
  minCol = col - (col % 3)
  for i in range(minLine, line):
    for j in range(minCol, minCol + 3):
      ix = i*9 + j
      x = solution[ix]
      if x == v:
        return False
  i = line
  for j in range(minCol, col):
    ix = i*9 + j
    x = solution[ix]
    if x == v:
      return False
  return True

# E: . liste représentant la solution explorée en cours
#    . position de la dernière insertion dans la liste
# S: True si l'insertion est acceptable pour toutes
#    les contraintes à respecter
def checkNewAddition(solution, position):
  return (checkLine(solution, position)
    and checkColumn(solution, position)
    and checkSquare(solution, position))

# E: . canevas sur lequel écrire l'avancement du backtracking
#    . valeur (nombre) à afficher
#    . ligne du sudoku de la valeur
#    . colonne du sudoku de la valeur
# S: affiche un nombre de la solution sur le canevas
def printNumber(canvas, value, line, col):
  value = str(value) if value != 0 else "."
  x = numberMargin + col*numberMargin*2 + squareMargin*(col // 3)
  y = numberMargin + line*numberMargin*2 + squareMargin*(line // 3)
  canvas.create_text(x, y, text = value,
    font = fontForPrinting,
    fill = "black")

# E: . canevas sur lequel écrire l'avancement du backtracking
#    . liste représentant la solution explorée en cours
# S: affiche la solution en cours de construction
def printToCanvas(canvas, solution):
  canvas.delete(ALL)
  for line in range(9):
    for col in range(9):
      value = solution[line*9 + col]
      printNumber(canvas, value, line, col)
  window.update()

# E: . liste représentant la solution explorée en cours
# S: affiche la solution finale valide dans le terminal
def printToConsole(solution):
  print
  print "#"*21
  for line in range(9):
    for col in range(9):
      value = solution[line*9 + col]
      print str(value) if value != 0 else " ",

      if col == 2 or col == 5:
        print "|", # square group separator
    print # newline
    if line == 2 or line == 5:
      print "-"*21
  print "#"*21

# E: . liste représentant la solution explorée en cours
#    . position de la dernière insertion dans la liste
#    . canevas sur lequel écrire l'avancement du backtracking
# S: effectue la résolution par backtracking,
#    appelle les fonctions d'affichages quand nécessaire
def backtracker(solution, position, canvas):
  if 9*9 == position:
    printToConsole(solution)
    for _ in range(2): # blinking effect when solution found
      printToCanvas(canvas, solution)
      time.sleep(speed*5)

      canvas.delete(ALL)
      window.update()
      time.sleep(speed*5)

  else:
    printToCanvas(canvas, solution)
    time.sleep(speed)

    for x in range(1, 9+1):
      solution[position] = x
      if checkNewAddition(solution, position):
        backtracker(solution, position+1, canvas)
      solution[position] = 0

# E: . canevas sur lequel écrire l'avancement du backtracking
# S: prépare le backtracking, appelle le backtracker()
def sudokuSolver(canvas):
  solution = [0]*9*9
  backtracker(solution, 0, canvas)


# ------------------------------------

speed = 0.1
fontForPrinting = ("Arial", 16)
numberMargin = 15 # margin to separate columns / lines
squareMargin = 10 # margin to separate each 3*3 square area
# ^ also used in printNumber()

window = Tk() 
frame = Frame(window, borderwidth = 4)

label = Label(window, text = "Sudoku Solver", fg = "black",
  font = fontForPrinting)
label.pack(side = "top")


dimension = numberMargin*18 + 2*squareMargin

canvas = Canvas(window, height = dimension, width = dimension, bg = "white")
canvas.pack()

sudokuSolver(canvas)

window.mainloop()