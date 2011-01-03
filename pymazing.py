from PIL import Image, ImageDraw
from collections import defaultdict
import logging

WHITE=255

m = Image.open("mazes/Maze3.gif")
m = m.convert("RGB")

current_path = []

visited = {}
original = m.load()
cells = m.convert("1").load()


draw = ImageDraw.Draw(m)

end = (720, 487)
start = (20, 530)
path_matrix = { start : ((-1, -1), 0) }

max_x, max_y = m.size
print max_x,max_y

def find_neighbors(x, y):
  neighbors = []

  for i in xrange(-1,2):
    for j in xrange(-1,2):
      dest_x, dest_y = x+i, y+j
      if dest_x >= max_x or dest_y >= max_y or dest_x < 0 or dest_y < 0:
        continue

      possible_distance = path_matrix[(x,y)][1] + 1
      if (dest_x, dest_y) in path_matrix:
        current_distance = path_matrix[(dest_x, dest_y)][1]
        if current_distance > possible_distance:
          path_matrix[(dest_x, dest_y)] = (x, y), possible_distance
      else:
        path_matrix[(dest_x, dest_y)] = (x, y), possible_distance

      if cells[dest_x, dest_y] == WHITE and not (dest_x, dest_y) in visited:
        neighbors.append((dest_x, dest_y))

  return neighbors

def visit_cell((x,y)):
  if (x, y) in visited:
    return []

  original[(x,y)] = 200

  visited[(x,y)] = True
  neighbors = find_neighbors(x,y)
  return neighbors

queue = [start]
while queue:
  cell = queue.pop(0)
  if cell == end:
    print "Found End"
    back_cell = cell
    while back_cell != start:
      back_cell, distance = path_matrix[back_cell]
      print back_cell
      x,y=  back_cell
      x1,y1 = x-2, y-2
      x2,y2 = x+2, y+2
      original[x,y] = 25
      draw.ellipse([x1,y1,x2,y2], fill="#0f0")
    break
  queue.extend(visit_cell(cell))

m.save("solved.png")

