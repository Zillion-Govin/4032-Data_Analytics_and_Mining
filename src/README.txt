+=================================================================================+
|                       CZ4032 - DATA ANALYTICS AND MINING                        |
|                             MOVIE RECOMMENDER                                   |
+=================================================================================+

+=================================================================================+
|                             GROUP ID : 37                                       |
|                             MEMBERS                                             |
|                             - Kelvin Chandra                                    |
|                             - Muhammad Faris                                    |
|                             - Stefan Artaputra Indriawan                        |
|                             - Stefan Setyadi Tjeng                              |
|                             - Zillion Govin (Group Leader)                      |
+=================================================================================+

+=================================================================================+
|                             PROGRAMMING LANGUAGE & LIBRARIES                    |
|                             - Python 2.7                                        |
|                             - Numpy                                             |
|                             - Pandas                                            |
|                             - SciPy                                             |
+=================================================================================+

+=================================================================================+
|                             INSTRUCTIONS                                        |
+=================================================================================+

>> DATA SPLITTING
	Dataset Randomization:
		- Open "transform.ktr" in Pentaho Data Integration
		- Change the file location of original data if needed
		- Run transformation and "ratings_randomized.dat" will be generated

	Dataset Splitter:
		- Run script "splitter.py"
		- Two files "ratings_test.dat" and "ratings_training.dat" will be generated

>> DATA PREPROCESSING
	Dataset Converion to Matrix Form:
		- Run script "matrix.py"
		- Result will be saved in "dataset_matrix" folder

>> SIMILARITY COMPUTATION WITHOUT 0
	- Open "similarity.py"
	- Run "cosine_similarity()", "correlation_similarity()", and "adjusted_cosine_similarity()" function
	- 3 types of Similarity Matrix will be generated in the folder "similarity_matrix"

>> PREDICTION
	1) Open "prediction/predict.py"

	2) Choose Weighted Sum:
		- Normal Weighted Sum:
			- uncomment the code under ## NORMAL WEIGHTED SUM
			- comment the code under ## IMPROVED WEIGHTED SUM

		- Improved Weighted Sum: 
			- uncomment the code under ## IMPROVED WEIGHTED SUM
			- comment the code under ## NORMAL WEIGHTED SUM

	3) Choose Similarity Algorithm
		- With 0
			- uncomment one of the line under ## SIMILARITY MATRIX WITH 0
			- depending on the desired algorithm (cosine, correlation, or adjusted cosine)

		- Without 0
			- uncomment one of the line under ## SIMILARITY MATRIX WITHOUT 0
			- depending on the desired algorithm (cosine, correlation, or adjusted cosine)
			- uncomment the code ## LOAD SIMILARITY MATRIX WITHOUT 0

	4) Predict top k
		- uncomment one of the code under ## PREDICTION MSE
		- depending on the similariy algorithm chosen