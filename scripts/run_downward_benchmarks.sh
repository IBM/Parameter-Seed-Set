#!/bin/bash

cd results
DOMAINS=( 'thoughtful' 'barman' 'visitall')

for dir in "${DOMAINS[@]}";
do
    mkdir $dir-grounding
    cd $dir-grounding
    python ./runner.py --domain-file ~/downward-benchmarks/$dir.pddl --problem-dir ~/downward-benchmarks/$dir-sat14-strips --use-grounding > $dir.out
    cd ..
done


DOMAINS=('blocks' 'depot' 'driverlog' 'freecell' 'gripper' 'mystery' 'satellite' 'tpp' 'zenotravel')

for dir in "${DOMAINS[@]}";
do
    mkdir $dir-grounding
    cd $dir-grounding
    python ./runner.py --domain-file ~/downward-benchmarks/$dir.pddl --problem-dir ~/downward-benchmarks/$dir --use-grounding > $dir.out
    cd ..
done

DOMAINS=('logistics00' 'logistics98' 'pipesworld-notankage' 'pipesworld-tankage' 'pipesworld-tankage-nosplit')
for dir in "${DOMAINS[@]}";
do
    mkdir $dir-grounding
    cd $dir-grounding
    python ./runner.py --domain-file ~/downward-benchmarks/$dir/domain.pddl --problem-dir ~/downward-benchmarks/$dir --use-grounding > $dir.out
    cd ..
done

cd ..

