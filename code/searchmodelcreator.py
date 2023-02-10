from nltk.util import trigrams
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import json
import os
import time
import pickle
import pandas as pd

class SearchModelCreator:

    def __init__(self,training_set_address,output_directory_address):
        temp=pd.read_pickle(training_set_address)
        self.training_set=temp['valid_strings'].values
        self.output_directory_address=output_directory_address

    def create_tfidf_matrix(self):
        self.TfidfVectorizer=TfidfVectorizer(
            analyzer=trigrams,
            #max_df=1,
            #min_df=0.001
        )
        self.tfidf_matrix=self.TfidfVectorizer.fit_transform(self.training_set)
        with open(self.output_directory_address+'tfidfVectorizer.bin','wb') as fp:
            pickle.dump(self.TfidfVectorizer,fp)


    def create_NearestNeighbors_model(self):
        self.NN_model=NearestNeighbors(
            n_neighbors=50,
            n_jobs=5,
            metric='cosine'
        )
        self.NN_model.fit(self.tfidf_matrix)
        with open(self.output_directory_address+'NearestNeighbors.bin','wb') as fp:
            pickle.dump(self.NN_model,fp)

if __name__ == "__main__":
    my_SearchModelCreator=SearchModelCreator(
        'results/training_set/valid_string_list_dataframe.bin',
        'results/models/'
    )
    my_SearchModelCreator.create_tfidf_matrix()
    my_SearchModelCreator.create_NearestNeighbors_model()
