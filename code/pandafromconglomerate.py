import pandas as pd
import json
import sqlalchemy

class PandaFromConglomerate:

    def __init__(self,input_address,output_address,db_address):
        self.input_address=input_address
        self.output_address=output_address
        self.db_address=db_address

    def convert_file(self):

        with open(self.input_address, 'r') as fp:
            conglomerate_json=json.load(fp)        
        
        output_panda_dict={
            'valid_string':[],
            'node_id':[],
            'main_string':[],
            'ontology':[],
        }

        for valid_string in conglomerate_json.keys():
            for mapped_node in conglomerate_json[valid_string]:
                output_panda_dict['valid_string'].append(valid_string)
                output_panda_dict['node_id'].append(mapped_node['node_id'])
                output_panda_dict['main_string'].append(mapped_node['main_string'])
                output_panda_dict['ontology'].append(mapped_node['node_id'].split('_')[0])
                

        self.output_panda=pd.DataFrame.from_dict(output_panda_dict)

        self.output_panda['valid_string']=self.output_panda['valid_string'].str.lower()

        self.output_panda['use_count']=0

        #for motivation, see the experimental jupyter notebook 'see_valid_string_to_main_string_redundancy'
        non_species_panda=self.output_panda.loc[self.output_panda.ontology != 'ncbi']
        species_panda=self.output_panda.loc[self.output_panda.ontology == 'ncbi']
        species_panda=species_panda.drop_duplicates(subset=('valid_string','main_string'))
        self.output_panda=pd.concat([species_panda,non_species_panda],ignore_index=True)



    def preload_use_counts(self,bindiscover_terms_used_address):
    

        use_count_panda=pd.read_csv(bindiscover_terms_used_address,sep='\t')

        names_to_increase_use_count=use_count_panda.stack().str.lower().unique()

        self.output_panda['main_lower']=self.output_panda.main_string.str.lower()

        self.output_panda['use_count']=self.output_panda['use_count'].mask(
            cond=(
                self.output_panda['main_lower'].isin(names_to_increase_use_count) 
            ),
            other=1
        )

        self.output_panda.drop(
            'main_lower',
            axis='columns',
            inplace=True
        )

        # self.output_panda.to_pickle(self.output_address)


    def create_connection(self):
        ## sqlite://<nohostname>/<path>
        engine=sqlalchemy.create_engine(f"sqlite:///{self.db_address}")
        # print('got here')
        self.connection=engine.connect()


    def build_vocab_table_string(self):
        # metadata_category_string=(' TEXT, '.join(self.metadata_categories))+' TEXT'
        self.vocab_table_string='''
        CREATE TABLE vocab_table(
        main_string TEXT,
        valid_string TEXT,
        node_id TEXT, 
        ontology TEXT,
        use_count INTEGER
        )
        '''

    def create_vocab_table(self):
        self.connection.execute(
            self.vocab_table_string
        )

    def upload_conglomerate_to_db(self):
        self.output_panda.to_sql(
            'vocab_table',
            self.connection,
            if_exists='replace',
            index=False
        )

    def create_index_vocab(self):

        '''
        '''


        query=f'''
        create index vocab_main_and_valid_string
        on vocab_table (main_string, valid_string)
        '''

        temp_cursor=self.connection.execute(
            query
        )

        query=f'''
        create index vocab_valid_string
        on vocab_table (valid_string)
        '''

        temp_cursor=self.connection.execute(
            query
        )

        query=f'''
        create index vocab_ontology
        on vocab_table (ontology)
        '''

        temp_cursor=self.connection.execute(
            query
        )


        return



if __name__=="__main__":

    my_PandaFromConglomerate=PandaFromConglomerate(
        'results/conglomerate_vocabulary_jsons/combined_valid_string_as_key.json',
        "results/conglomerate_vocabulary_panda/conglomerate_vocabulary_panda.bin",
        'results/database/sample_ingester_database.db'
    )

    my_PandaFromConglomerate.convert_file()
    my_PandaFromConglomerate.preload_use_counts('resources/bindiscover_metadata_for_use_counts.tsv')

    my_PandaFromConglomerate.create_connection()
    my_PandaFromConglomerate.build_vocab_table_string()
    my_PandaFromConglomerate.create_vocab_table()
    my_PandaFromConglomerate.upload_conglomerate_to_db()
    my_PandaFromConglomerate.create_index_vocab()