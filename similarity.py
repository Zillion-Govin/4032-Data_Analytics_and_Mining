import io
import os

import numpy as np
import pandas as pd

from scipy.spatial.distance import cdist

ENCODING = 'ASCII'

# source matrix file name
source = 'matrix.csv'

# transposed dataframe matrix (user x movie)
source_df = pd.read_csv(source, delimiter=',', header = 0, index_col = 0, encoding = ENCODING).transpose()

def cosine_similarity(source_df):
	print("----------------------------RUNNING COSINE SIMILARITY----------------------------\n")
	header = list(source_df.columns)

	item_vector = source_df[header].values.transpose()

	similarity_matrix = np.around( (1 - cdist(item_vector, item_vector, 'cosine')), 2)

	similarity_df = pd.DataFrame(
			data = similarity_matrix,
			index = header,
			columns = header
		)

	# write to file
	similarity_df.to_csv('similarity_cosine.csv', encoding = ENCODING)
	print("\n----------------------------DONE!----------------------------")

def correlation_similarity(source_df):
	print("----------------------------RUNNING CORRELATION SIMILARITY----------------------------\n")
	header = list(source_df.columns)

	item_vector = source_df[header].values.transpose()

	similarity_matrix = np.around( (1 - cdist(item_vector, item_vector, 'correlation')), 2)

	similarity_df = pd.DataFrame(
			data = similarity_matrix,
			index = header,
			columns = header
		)

	# write to file
	similarity_df.to_csv('similarity_correlation.csv', encoding = ENCODING)
	print("\n----------------------------DONE!----------------------------")

# MAIN
# uncomment to run
cosine_similarity(source_df)
# correlation_similarity(source_df)