import pandas as pd
import json
import sqlalchemy


class DatabaseCreator:


    def __init__(self,db_address,subset_json_address,no_vocab_header_address):
        self.db_address=db_address
        self.subset_json_address=subset_json_address
        self.no_vocab_header_address=no_vocab_header_address
        
    def make_header_list(self):
        with open(self.subset_json_address, 'r') as fp:
            subset_per_heading_json=json.load(fp)
        no_vocab_header_panda=pd.read_csv(self.no_vocab_header_address)
        self.metadata_categories=set(subset_per_heading_json.keys()).union(
            set(
                no_vocab_header_panda['headers_without_vocabs'].tolist()
            )
        )
        
    def create_connection(self):
        ## sqlite://<nohostname>/<path>
        engine=sqlalchemy.create_engine(f"sqlite:///{self.db_address}")
        print('got here')
        self.connection=engine.connect()
    
    def build_study_table_string(self):
        metadata_category_string=(' TEXT, '.join(self.metadata_categories))+' TEXT'
        self.study_table_string='''
        CREATE TABLE study_table(
        author_id TEXT,
        study_id TEXT,
        sample_id TEXT, 
        metadata_parallel_id TEXT,
        '''+metadata_category_string+' )'
        
    def create_study_table(self):
        self.connection.execute(
            self.study_table_string
        )
        
if __name__=="__main__":
    my_DatabaseCreator=DatabaseCreator(
        'results/database/sample_ingester_database.db',
        'resources/parameter_files/subset_per_heading.json',
        'resources/parameter_files/headers_without_vocabs.tsv',  
        
    )
    my_DatabaseCreator.make_header_list()
    # print(my_DatabaseCreator.metadata_categories)
    # print(my_DatabaseCreator.build_study_table_string())
    my_DatabaseCreator.create_connection()
    my_DatabaseCreator.build_study_table_string()
    my_DatabaseCreator.create_study_table()