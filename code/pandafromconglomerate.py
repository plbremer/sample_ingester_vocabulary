import pandas as pd
import json


class PandaFromConglomerate:

    def __init__(self,input_address,output_address):
        self.input_address=input_address
        self.output_address=output_address

    def convert_file(self):

        with open(self.input_address, 'r') as fp:
            conglomerate_json=json.load(fp)        
        
        output_panda_dict={
            'valid_string':[],
            'node_id':[],
            'main_string':[],
            'ontology':[]
        }

        for valid_string in conglomerate_json.keys():
            for mapped_node in conglomerate_json[valid_string]:
                output_panda_dict['valid_string'].append(valid_string)
                output_panda_dict['node_id'].append(mapped_node['node_id'])
                output_panda_dict['main_string'].append(mapped_node['main_string'])
                output_panda_dict['ontology'].append(mapped_node['node_id'].split('_')[0])

        self.output_panda=pd.DataFrame.from_dict(output_panda_dict)

        self.output_panda.to_pickle(self.output_address)



if __name__=="__main__":

    my_PandaFromConglomerate=PandaFromConglomerate(
        'results/conglomerate_vocabulary_jsons/combined_valid_string_as_key.json',
        "results/conglomerate_vocabulary_panda/conglomerate_vocabulary_panda.bin"
    )

    my_PandaFromConglomerate.convert_file()

