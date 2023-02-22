from nltk.util import trigrams
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import json
import os
import time
import pickle
import pandas as pd

class SearchModelCreator:

    def __init__(self,panda_containing_training_set_address,output_directory_address,header_subset_definitions_address):
        self.conglomerate_panda=pd.read_pickle(panda_containing_training_set_address)
        #self.training_set=temp['valid_strings'].values
        self.output_directory_address=output_directory_address
        with open(header_subset_definitions_address, 'r') as f:
            self.header_definition_json=json.load(f) 
        self.tfidf_matrix_dict=dict()


    def create_tfidf_matrix_per_header_defined(self):
        for temp_header in self.header_definition_json.keys(): 
            #collect all subset_definitions
            temp_subset_definitions=self.header_definition_json[temp_header]

            temp_panda_subset_list=list()
            for temp_subset_definition in temp_subset_definitions:
                temp_panda_subset_list.append(
                    self.conglomerate_panda.loc[
                        self.conglomerate_panda.node_id.str.contains(temp_subset_definition)
                    ]
                )
            temp_conglomerate_panda_subset=pd.concat(temp_panda_subset_list,axis='index',ignore_index=True)
            temp_model_vocabulary=temp_conglomerate_panda_subset['valid_string']
        
            temp_TfidfVectorizer=TfidfVectorizer(
                analyzer=trigrams,
                #max_df=1,
                #min_df=0.001
            )
            self.tfidf_matrix_dict[temp_header]=temp_TfidfVectorizer.fit_transform(temp_model_vocabulary)
            with open(self.output_directory_address+'tfidfVectorizer'+'_'+temp_header+'.bin','wb') as fp:
                pickle.dump(temp_TfidfVectorizer,fp)


    def create_NearestNeighbors_model_per_header_defined(self):
        for temp_header in self.header_definition_json.keys():
        
            temp_NN_model=NearestNeighbors(
                n_neighbors=50,
                n_jobs=5,
                metric='cosine'
            )
            temp_NN_model.fit(self.tfidf_matrix_dict[temp_header])
            with open(self.output_directory_address+'NearestNeighbors'+'_'+temp_header+'.bin','wb') as fp:
                pickle.dump(temp_NN_model,fp)

if __name__ == "__main__":
    my_SearchModelCreator=SearchModelCreator(
        'results/conglomerate_vocabulary_panda/conglomerate_vocabulary_panda.bin',
        'results/models/',
        'resources/parameter_files/subset_per_heading.json'
    )
    my_SearchModelCreator.create_tfidf_matrix_per_header_defined()
    my_SearchModelCreator.create_NearestNeighbors_model_per_header_defined()
