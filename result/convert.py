# CONVERT SIMILARITY RESULT TO MOVIE TITLE

import os
import json

# sim_file = os.path.join('..', 'stefan', 'top10-basic.txt')
# sim_file = os.path.join('..', 'stefan', 'top10-correlation_without_0.txt')
sim_file = os.path.join('..', 'stefan', 'top10-cosine_without_0.txt')

# target_file = 'top10-basic.js'
# target_file = 'top10-correlation_without_0.js'
target_file = 'top10-cosine_without_0.js'

movie_file = os.path.join('..', 'dataset_raw', 'movies_image.dat')

def write_json(movie, lookup):
	obj = {}

	for k,v in movie.iteritems():
		obj[lookup[k][0]] = []

		for i in v:
			j = i.split('=')[0]
			obj[lookup[k][0]].append([lookup[j][0], lookup[j][1]])

	with open(target_file, 'w') as target:
		target.write('var data = ')
		json_str = json.dumps(obj, ensure_ascii = False, indent = 2)
		target.write(json_str)


movie = {}

lookup = {}

with open(sim_file, 'r') as source:
	for line in source:
		similar_movies = line.split(':')

		movie[similar_movies[0]] = similar_movies[1].strip('\n').split(',')

with open(movie_file, 'r') as source:
	for line in source:
		temp = line.strip('\n').split('::')

		lookup[temp[0]] = [temp[1], temp[3]]

write_json(movie, lookup)