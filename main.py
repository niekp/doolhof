from maze import maze
from solver import solver
import time

m = maze('21x21.png')
m.parse()

# Zoek de oplossing
s = solver(m)
s.solve(0.02);

# Animeer de oplossing
s.reset();
s.solve(0);

solution = []

for pos in s.getPath():
	solution.append(pos)

	m.output(solution);
	time.sleep(0.03)
