import json
header_vocabulary_json_address="resources/parameter_files/subset_per_heading.json"
with open(header_vocabulary_json_address,'r') as f:
    header_vocabulary_json=json.load(f)
gui_headers=header_vocabulary_json.keys()

shrink_ncbi_nx='True'


# rule copy_datasets_to_frontend:
#     input:
#         # "results/training_set/valid_string_list_dataframe.bin",
#         expand("results/models/tfidfVectorizer_{headers}.bin",headers=gui_headers),
#         expand("results/models/NearestNeighbors_{headers}.bin",headers=gui_headers),
#         expand("results/models/unique_valid_strings_{headers}.bin",headers=gui_headers),
#         expand("results/models/conglomerate_vocabulary_panda_{headers}.bin",headers=gui_headers),
#         "resources/parameter_files/subset_per_heading.json",
#         "resources/parameter_files/ngram_limits_per_heading.json",
#     output:
#         expand("../frontend/additional_files/tfidfVectorizer_{headers}.bin",headers=gui_headers),
#         expand("../frontend/additional_files/NearestNeighbors_{headers}.bin",headers=gui_headers),
#         expand("../frontend/additional_files/unique_valid_strings_{headers}.bin",headers=gui_headers),
#         expand("../frontend/additional_files/conglomerate_vocabulary_panda_{headers}.bin",headers=gui_headers),
#         "../frontend/additional_files/subset_per_heading.json",
#         "../frontend/additional_files/ngram_limits_per_heading.json",
#     shell:
#         '''
#         cp results/models/* ../frontend/additional_files/ 
#         cp resources/parameter_files/subset_per_heading.json ../frontend/additional_files/ 
#         cp resources/parameter_files/ngram_limits_per_heading.json ../frontend/additional_files/ 
#         '''
        
#         #cp results/conglomerate_vocabulary_panda/conglomerate_vocabulary_panda.bin ../frontend/additional_files/ 




rule make_curation_models:
    input:
        # "results/training_set/valid_string_list_dataframe.bin"
        "results/conglomerate_vocabulary_panda/conglomerate_vocabulary_panda.bin"
    output:
        # "results/models/tfidfVectorizer.bin",
        # "results/models/NearestNeighbors.bin",
        expand("results/models/tfidfVectorizer_{headers}.bin",headers=gui_headers),
        expand("results/models/NearestNeighbors_{headers}.bin",headers=gui_headers),
        expand("results/models/unique_valid_strings_{headers}.bin",headers=gui_headers),
        expand("results/models/conglomerate_vocabulary_panda_{headers}.bin",headers=gui_headers)
    shell:
        "python3 code/searchmodelcreator.py"






rule make_panda_from_conglomerate_file:
    input:
        "results/conglomerate_vocabulary_jsons/combined_valid_string_as_key.json"
    output:
        "results/conglomerate_vocabulary_panda/conglomerate_vocabulary_panda.bin"
    shell:
        "python3 code/pandafromconglomerate.py"  




rule parse_sexes:
    output:
        "results/individual_vocabulary_jsons/sex.json",
    #lot of broken stuff with mamba. will try to simply keep one environment and run in that
    # conda:
    #     "../binbase_sample_ingester.yml"
    shell:
        "python3 code/sexlistparser.py"



rule parse_genes:
    output:
        "results/individual_vocabulary_jsons/genesHuman.json",
    #    "results/individual_vocabulary_jsons/genesMusMusculus.json"
    #lot of broken stuff with mamba. will try to simply keep one environment and run in that
    # conda:
    #     "../binbase_sample_ingester.yml"
    shell:
        "python3 code/genetsvparser.py"

rule parse_drugs:
    output:
        "results/individual_vocabulary_jsons/drugs.json"
    #lot of broken stuff with mamba. will try to simply keep one environment and run in that
    # conda:
    #     "../binbase_sample_ingester.yml"
    shell:
        "python3 code/fdadrugtsvparser.py"

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
        "results/individual_vocabulary_jsons/genesHuman.json",
        "results/individual_vocabulary_jsons/unit.json",
        "results/individual_vocabulary_jsons/drugs.json",
        #"results/individual_vocabulary_jsons/genesMusMusculus.json",
        "results/individual_vocabulary_jsons/sex.json"
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









# # this rule is no longer relevant and we moved to dataframe rather than json
# rule make_vocabulary_list:
#     input:
#         "results/conglomerate_vocabulary_jsons/combined_valid_string_as_key.json"
#     output:
#         "results/training_set/valid_string_list_dataframe.bin"
#     shell:
#         "python3 code/vocabularyextracter.py"  

























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
