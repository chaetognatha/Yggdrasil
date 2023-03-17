#!/usr/bin/env nextflow
// Enable DSL2 functionality
nextflow.enable.dsl = 2

// params
params.proj_root = "$HOME/TEST"
params.Project_IDs = "wrong1,wrong2,wrong3"
params.raw = "$HOME/TEST/"

workflow {
    // get project IDs
    proj_ids = Channel.from(params.Project_IDs.split(','))
    // make project directories and symlink raw data
    SETUP(proj_ids) | CHECK
    PASS_FILE | READ_FILE
    TEMPLATE_TEST(SETUP.out)
    PUBLISH(SETUP.out)
}

process SETUP {
    input:
    val proj_id
    output:
    path proj_id
    script:
    """
    mkdir -p ${proj_id}
    """
}

process CHECK {
    input:
    path proj_id
    output:
    path "${proj_id}/raw"
    script:
    """
    touch ${proj_id}/raw
    """
}

process TEMPLATE_TEST {
    input:
    path proj_id
    output:
    path "${proj_id}/test.txt"
    script:
    template "test.py"
}

process PUBLISH {
    publishDir "${params.proj_root}", mode: 'move'
    input:
    path proj_id
    output:
    path proj_id
    script:
    """
    echo "publishing ${proj_id}"
    """
}

process PASS_FILE {
    output: 
    path "*"
    script:
    """
    #!/usr/bin/env python3
    for i in range(10):
        with open(f'{i}.txt', 'w') as f:
            f.write("test")
    """
}

process READ_FILE {
    input:
    path x
    output:
    path "*.txt"
    shell:
    """
    echo !x > !x.txt
    """
}