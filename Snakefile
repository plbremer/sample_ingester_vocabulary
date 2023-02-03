rule parse_genes_human:
    output:
        "results/individual_vocabulary_jsons/genes_human.json"
    #lot of broken stuff with mamba. will try to simply keep one environment and run in that
    # conda:
    #     "../binbase_sample_ingester.yml"
    shell:
        "python3 ./code/genetsvparser.py"

rule parse_ncbi:
    output:
        "results/individual_nxs/ncbi_nx.bin"
    shell:
        "python3 ./code/nxparser_ncbi.py"

rule parse_mesh:
    output:
        "results/individual_nxs/mesh_nx.bin"
    shell:
        "python3 ./code/nxparser_mesh.py"

                
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
#         "python3 ./code/fill_in_additional_columns.py {min_fold_change} {named_or_all}"
