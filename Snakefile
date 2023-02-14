shrink_ncbi_nx='True'

rule parse_genes_human:
    output:
        "results/individual_vocabulary_jsons/genes_human.json"
    #lot of broken stuff with mamba. will try to simply keep one environment and run in that
    # conda:
    #     "../binbase_sample_ingester.yml"
    shell:
        "python3 code/genetsvparser.py"

rule parse_ncbi:
    output:
        "results/individual_nxs/ncbi_nx.bin"
    shell:
        "python3 code/nxparser_ncbi.py"

rule parse_mesh:
    output:
        "results/individual_nxs/mesh_nx.bin"
    shell:
        "python3 code/nxparser_mesh.py"

rule parse_units:
    output:
        'results/individual_nxs/unit_nx.bin'
    shell:
        'python3 code/nxparser_units.py'

rule ncbi_to_json:
    input:
        "results/individual_nxs/ncbi_nx.bin"
    output:
        "results/individual_vocabulary_jsons/ncbi.json"
    shell:
        "python3 code/NodeIDDictParser.py ncbi True" 

rule mesh_to_json:
    input:
        "results/individual_nxs/mesh_nx.bin"
    output:
        "results/individual_vocabulary_jsons/mesh.json"
    shell:
        "python3 code/NodeIDDictParser.py mesh currently_irrelevant"

rule unit_to_json:
    input:
        "results/individual_nxs/unit_nx.bin"
    output:
        "results/individual_vocabulary_jsons/unit.json"
    shell:
        "python3 code/NodeIDDictParser.py unit True"

rule make_conglomerate_json:
    input:
        "results/individual_vocabulary_jsons/mesh.json",
        "results/individual_vocabulary_jsons/ncbi.json",
        "results/individual_vocabulary_jsons/genes_human.json"
    output:
        "results/conglomerate_vocabulary_jsons/combined_ontologies.json"
    shell:
        "python3 code/conglomeratejsonmaker.py"  

rule make_conglomerate_json_valid_string_as_key:
    input:
        "results/conglomerate_vocabulary_jsons/combined_ontologies.json"
    output:
        "results/conglomerate_vocabulary_jsons/combined_valid_string_as_key.json"
    shell:
        "python3 code/conglomeratejsonvalidstringaskey.py"  

rule make_vocabulary_list:
    input:
        "results/conglomerate_vocabulary_jsons/combined_valid_string_as_key.json"
    output:
        "results/training_set/valid_string_list_dataframe.bin"
    shell:
        "python3 code/vocabularyextracter.py"  

rule make_curation_models:
    input:
        "results/training_set/valid_string_list_dataframe.bin"
    output:
        "results/models/tfidfVectorizer.bin",
        "results/models/NearestNeighbors.bin",
    shell:
        "python3 code/searchmodelcreator.py"   

rule copy_datasets_to_frontend:
    input:
        "results/conglomerate_vocabulary_jsons/combined_valid_string_as_key.json",
        "results/training_set/valid_string_list_dataframe.bin",
        "results/models/tfidfVectorizer.bin",
        "results/models/NearestNeighbors.bin",
    output:
        "../frontend/additional_files/combined_valid_string_as_key.json",
        "../frontend/additional_files/valid_string_list_dataframe.bin",
        "../frontend/additional_files/tfidfVectorizer.bin",
        "../frontend/additional_files/NearestNeighbors.bin",    
    shell:
        '''
        cp results/conglomerate_vocabulary_jsons/combined_valid_string_as_key.json ../frontend/additional_files/ 
        cp results/training_set/valid_string_list_dataframe.bin ../frontend/additional_files/ 
        cp results/models/tfidfVectorizer.bin ../frontend/additional_files/ 
        cp results/models/NearestNeighbors.bin ../frontend/additional_files/
        '''


# rule step_0_c_complete_pipeline_input:
#     input:
#         "../results/{min_fold_change}/step_0_b_shape_aws_pull_to_pipeline_input/dummy.txt"
#     output:
#         "../results/{min_fold_change}/step_0_c_complete_pipeline_input/dummy.txt"
#     conda:
#         "./envs/binvestigate_3_8_fresh_2.yml"
#     #params:
#     #    count_cutoff="{min_fold_change}"
#     #script:
#     #    "/home/rictuar/coding_projects/fiehn_work/gc_bin_base/code/create_organ_networkx.py"
#     shell:
#         "python3 code/fill_in_additional_columns.py {min_fold_change} {named_or_all}"
