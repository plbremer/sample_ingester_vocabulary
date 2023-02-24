import pandas as pd
import json
from pprint import pprint

class SexListParser():

    def __init__(self,input_file_path,output_file_path):
        self.input_file_path=input_file_path
        self.output_file_path=output_file_path

    def create_attribute_to_node_id(self):
        '''
        in the case of sexes, because we couldnt find a nice ontology we are just making our own list
        the node id, valid string, and main string will all be the same
        '''

        input_panda=pd.read_csv(self.input_file_path,sep='\t',header=None)
        print(input_panda)
        # input_panda.drop_duplicates(inplace=True)
        # input_panda.drop_duplicates(
        #     subset=['DrugName'],
        #     inplace=True
        # )
        # input_panda.reset_index(drop=True,inplace=True)


        self.total_feature_node_id_dict=dict()
        for index, series in input_panda.iterrows():
            
            
            self.total_feature_node_id_dict[series[0]]=dict()
            
            self.total_feature_node_id_dict[series[0]]['valid_strings']=[series[0]]
            self.total_feature_node_id_dict[series[0]]['main_string']=series[0]
            

        #     self.total_feature_node_id_dict[index]['valid_strings']=[
        #         series['DrugName'],
        #         series['ActiveIngredient']
        #     ]

        #     # self.total_feature_node_id_dict[series['Description']]={
        #     #     'node_ids':[series['NCBI GeneID']],
        #     #     'formal_word':[series['Description']]
        #     # }
        #pprint(self.total_feature_node_id_dict)
        with open(self.output_file_path, 'w') as fp:
            json.dump(self.total_feature_node_id_dict, fp,indent=4) 


if __name__=="__main__":
    # my_FDADrugTSVParser=FDADrugTSVParser('/home/rictuar/coding_projects/fiehn_work/binbase_sample_ingester/resources/ncbi_genes_human.tsv')
    # my_FDADrugTSVParser.create_attribute_to_node_id_from_panda()
    # with open('../intermediate_results/attribute_node_id_pairs/genes_human.json', 'w') as fp:
    #     json.dump(my_FDADrugTSVParser.total_feature_node_id_dict, fp,indent=4)   

    my_SexListParser=SexListParser(
        'resources/sexes_parker_created.txt',
        'results/individual_vocabulary_jsons/sex.json'
    )
    my_SexListParser.create_attribute_to_node_id()
