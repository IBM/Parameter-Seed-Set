#!/bin/bash

 domains=("childsnack-contents" "blocksworld-large-simple" "logistics-large-simple" "visitall-multidimensional" "rovers-large-simple")
ROOT_PATH="~/htg-domains/"
cd results

for domain in  ${domains[*]};
do
    mkdir ${domain}
    cd ${domain}
    FOLDER_PATH="${ROOT_PATH}/${domain}/*"
    echo ${FOLDER_PATH}
    for f in $FOLDER_PATH;
    do 
	subdomain="$(basename $f)"
        echo $subdomain
        mkdir $subdomain
        cd $subdomain
        python ./runner.py --domain-file "${f}/domain.pddl" --problem-dir $f > output.log
        cd ..
    done
    cd ..
done
cd ..
