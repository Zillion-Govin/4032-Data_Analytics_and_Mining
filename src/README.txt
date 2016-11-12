+===================================================+
|		GROUP ID : 37								|
|		GROUP MEMBERS :								|
|		- Kelvin Chandra							|
|		- Muhammad Faris							|
|		- Stefan Artaputra Indriawan				|
|		- Stefan Setyadi Tjeng						|
|		- Zillion Govin	(Group Leader)				|
+===================================================+

+===================================================+
|		PROGRAMMING LANGUAGE & LIBRARIES			|
|		- Python 2.7								|
|		- Numpy										|
|		- Pandas									|
|		- SciPy										|
+===================================================+

+===================================================+
|					INSTRUCTIONS					|
+===================================================+

+=======================+
|	Dataset Splitting	|
+=======================+
Dataset Randomization:
	- Open transform.ktr in Pentaho Data Integration
	- Change the file location of original data if needed
	- Run transformation and ratigs_randomized.dat will be generated
Dataset Splitter:
	- Run script "splitter.py"
	- Two files "ratings_test.dat" and "ratings_training.dat" will be generated

+===========================+
|	Dataset Preprocessing	|
+===========================+
Dataset Converion to Matrix Form:
	- Run script "matrix.py"
	- Result will be saved in "dataset_matrix" folder

+===============================================+
|		Similarity Computation Without 0		|
+===============================================+
	- Open "similarity.py"
	- Run "cosine_similarity()", "correlation_similarity()", and "adjusted_cosine_similarity()" function
	- 3 types of Similarity Matrix will be generated in the folder "similarity_matrix"

+===========================+
|	Prediction Computation	|
+===========================+
