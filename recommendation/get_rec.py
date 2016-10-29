import os
import json

rec_file = os.path.join('..', 'stefan', 'top10.txt')
movie_file = os.path.join('..', 'dataset_raw', 'movies.dat')

def write_json(movie, lookup):
	obj = {}

	for k,v in movie.iteritems():
		obj[lookup[k]] = []

		for i in v:
			j = i.split('=')[0]
			obj[lookup[k]].append(lookup[j])

	with open('recommendation.js', 'a') as target:
		target.write('var data = ')
		json_str = json.dumps(obj, ensure_ascii = False, indent = 2)
		target.write(json_str)


movie = {}

lookup = {}

with open(rec_file, 'r') as source:
	for line in source:
		movie_rec = line.split(':')

		movie[movie_rec[0]] = movie_rec[1].strip('\n').split(',')

with open(movie_file, 'r') as source:
	for line in source:
		temp = line.split('::')

		lookup[temp[0]] = temp[1]

write_json(movie, lookup)