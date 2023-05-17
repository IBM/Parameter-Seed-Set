#!/bin/bash

cd results
domains=("pipesworld-tankage-nosplit" "genome-edit-distance-split" "genome-edit-distance-positional" "genome-edit-distance" "organic-synthesis-MIT" "organic-synthesis-alkene" "organic-synthesis-original" "genome-edit-distance")
ROOT_PATH="~/htg-domains/"

for domain in  ${domains[*]};
do
    mkdir $domain
    cd $domain
    f="${ROOT_PATH}/${domain}/"
    echo $f
    python ./runner.py --domain-file "${f}/domain.pddl" --problem-dir $f > output.log
    cd ..
done
