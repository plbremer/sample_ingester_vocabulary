import json
import networkx as nx
from collections.abc import Iterable
import sys


class NodeIDDictParser:

    def __init__(self,file_path,attributes,main_attribute):
        self.input_nx=nx.read_gpickle(file_path)
        self.attributes_to_record=attributes
        self.main_attribute=main_attribute


    def reduce_ncbi_taxonomy(self):
        '''
        the logic for this came from exploring the ncbi taxonomy a little in 
        "propose_ncbi_removals.ipynb"
        the eventual conclusion was that the safest thing to do was to remove
        those subgraphs where the parent node contained the string "unclassified" or "environmental"
        as in "environmental samples"
        these seemed to contain the largest dumps, and reduced the total number of nodes from 2344973
        to 942320
        there are still many "overly specific" nodes, imo, but we dont have the manpower to deeply explore
        hundreds of thousands of nodes
        '''

        unclassified_or_environmental_nodes=set()
        for temp_node in self.input_nx.nodes:
            if ('unclassified' in self.input_nx.nodes[temp_node]['scientific_name']) or ('environmental' in self.input_nx.nodes[temp_node]['scientific_name']):
                unclassified_or_environmental_nodes.add(temp_node)
            
        unclassified_or_environmental_nodes_and_children=set()
        unclassified_or_environmental_nodes_and_children.update(
            unclassified_or_environmental_nodes
        )
    
        for temp_node in unclassified_or_environmental_nodes:
            
            unclassified_or_environmental_nodes_and_children.update(
                nx.descendants(self.input_nx,temp_node)
            )

        self.input_nx.remove_nodes_from(
            unclassified_or_environmental_nodes_and_children
        )

    def reduce_mesh_taxonomy(self):
        '''
        '''
        pass

    def reduce_unit_taxonomy(self):
        '''
        not so much a reduction as a cleaning
        the synonym attributes are very poorly arranged
        '''

        for temp_node in self.input_nx.nodes:
            if 'synonym' in self.input_nx.nodes[temp_node]:
                new_synonym_list=list()
                for temp_syn in self.input_nx.nodes[temp_node]['synonym']:
                    if '\"' in temp_syn:
                        new_synonym_list.append(
                            temp_syn.split('\"')[1]
                        )
                    else:
                        new_synonym_list.append(temp_syn)

                self.input_nx.nodes[temp_node]['synonym']=new_synonym_list

        

    #def define_attributes_to_maintain(self,attributes):

    # def flatten(self,xs):
    #     '''
    #     given a list of elements (can contain arbitrarily nested lists)
    #     creates a generator? of flattned elements
    #     warning: strings will become lists of char
    #     '''
    #     for x in xs:
    #         if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
    #             yield from self.flatten(x)
    #         else:
    #             yield x

    # def create_one_values_to_node_id_dict(self,temp_node):
    #     '''
    #     This takes a single node and returns a dict
    #     where the keys (probably many) are the nested values of the node
    #     and the value for each key is the node ID
    #     '''
    #     one_node_id_dict=dict()
    #     #we make scientific name the endpoint so that it works like the mesh hierarchies
    #     #scientific_name=self.input_nx.nodes[temp_node][temp_attribute]
    #     for temp_attribute in self.attributes_that_differentiate_node_id:
    #         #print(temp_attribute)
    #         if temp_attribute not in self.input_nx.nodes[temp_node].keys():
    #             continue
    #         elif isinstance(self.input_nx.nodes[temp_node][temp_attribute],str):
    #             #print(total_ncbi_networkx.nodes[temp_node][temp_attribute])
    #             one_node_id_dict[self.input_nx.nodes[temp_node][temp_attribute]]=[temp_node]
    #         else:
    #             #print(set(flatten(total_ncbi_networkx.nodes[temp_node][temp_attribute])))
    #             temp_dict={
    #                 element:[temp_node] for element in set(self.flatten(self.input_nx.nodes[temp_node][temp_attribute]))
    #             }
    #             one_node_id_dict.update(temp_dict)
    #     return one_node_id_dict

    # def create_all_attribute_to_node_id_dict(self):
    #     '''
    #     takes an entire networkx and features that help to differentiate nodes
    #     returns a dict of {attribute:[node_ids]} (i think)
    #     '''
    #     self.total_feature_node_id_dict=dict()
    #     for i,temp_node in enumerate(self.input_nx.nodes):
    #         small_dict_to_add=self.create_one_values_to_node_id_dict(temp_node)
    #         for temp_key in small_dict_to_add.keys():
    #             try:
    #                 self.total_feature_node_id_dict[temp_key]=self.total_feature_node_id_dict[temp_key]+small_dict_to_add[temp_key]
    #             except KeyError:
    #                 self.total_feature_node_id_dict[temp_key]=small_dict_to_add[temp_key]
    #         # what we had before. this basically erased all but the last entry for any particular node, so like, "Liver Neoplasms" had only one entry
    #         # self.total_feature_node_id_dict.update(
    #         #     #self.create_one_values_to_node_id_dict(temp_node)
    #         # )

    #def create_all_attribute_to_node_id_dict(self,tree_type,formal_word):
    def create_all_attribute_to_node_id_dict(self):
        '''
        we basically assume that there isnt some crazy nested situaion with respect ot the freature nodes
        the above commented code was an attempt to overengineer some foolpreoof solution for a case that didnt exist
        for each node in the tree
        
        the output is in the form of 
        {
            'node id':[strings that map to node id]
        }
        '''
        #self.total_feature_node_id_dict=dict()

        self.node_id_to_strings_dict=dict()
        for temp_node in self.input_nx.nodes:
            
            self.node_id_to_strings_dict[temp_node]=dict()
            #self.node_id_to_strings_dict[temp_node]=[]

            self.node_id_to_strings_dict[temp_node]['valid_strings']=set()

            #self.total_feature_node_id_dict[series['NCBI GeneID']]['valid_strings']


            for temp_attribute in self.attributes_to_record:
                
                #if there is no attribute for this node id
                if temp_attribute not in self.input_nx.nodes[temp_node].keys():
                    continue
                
                if isinstance(self.input_nx.nodes[temp_node][temp_attribute],list)==True:
                    for element in self.input_nx.nodes[temp_node][temp_attribute]:
                        if isinstance(element,list)==True:
                            #print('found a nested list')
                            raise Exception('found a nested list')
                        self.node_id_to_strings_dict[temp_node]['valid_strings'].add(element)
                else:
                    self.node_id_to_strings_dict[temp_node]['valid_strings'].add(
                        self.input_nx.nodes[temp_node][temp_attribute]
                    )

            #set not json serializable
            self.node_id_to_strings_dict[temp_node]['valid_strings']=list(self.node_id_to_strings_dict[temp_node]['valid_strings'])
            self.node_id_to_strings_dict[temp_node]['main_string']=self.input_nx.nodes[temp_node][self.main_attribute]

                

if __name__ == "__main__":

    ontology=sys.argv[1]
    drop_nodes=sys.argv[2]
    
    if ontology=='ncbi':
        my_NodeIDDictParser=NodeIDDictParser(
            'results/individual_nxs/ncbi_nx.bin',
            {'common_name','genbank_common_name','scientific_name'},
            'scientific_name'
        )
        if drop_nodes=='True':
            my_NodeIDDictParser.reduce_ncbi_taxonomy()
        my_NodeIDDictParser.create_all_attribute_to_node_id_dict()
        with open('results/individual_vocabulary_jsons/ncbi.json', 'w') as fp:
            json.dump(my_NodeIDDictParser.node_id_to_strings_dict, fp,indent=4)        

    elif ontology=='mesh':
        my_NodeIDDictParser=NodeIDDictParser(
            'results/individual_nxs/mesh_nx.bin',
            {'mesh_label','common_name'},
            'mesh_label'
        )
        # if drop_nodes==True:
        #     my_NodeIDDictParser.reduce_ncbi_taxonomy()
        my_NodeIDDictParser.create_all_attribute_to_node_id_dict()
        with open('results/individual_vocabulary_jsons/mesh.json', 'w') as fp:
            json.dump(my_NodeIDDictParser.node_id_to_strings_dict, fp,indent=4)       

    elif ontology=='unit':
        my_NodeIDDictParser=NodeIDDictParser(
            'results/individual_nxs/unit_nx.bin',
            {'name','synonym'},
            'name'
        )


        if drop_nodes=='True':
            my_NodeIDDictParser.reduce_unit_taxonomy()
        my_NodeIDDictParser.create_all_attribute_to_node_id_dict()
        with open('results/individual_vocabulary_jsons/unit.json', 'w') as fp:
            json.dump(my_NodeIDDictParser.node_id_to_strings_dict, fp,indent=4)    
