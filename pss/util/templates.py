PROBLEM_TEMPLATE="(define (problem {aname})\n \
        (:domain {aname}-domain)\n \
        (:init (= (total-cost) 0))\n \
        (:goal\n \
            (and {goal} )\n \
        )\n \
        (:metric minimize (total-cost))\n \
    )\n"

DOMAIN_TEMPLATE ="(define (domain {aname}-domain)\n \
    (:constants \n \t{objects}\n \t) \n \
    (:predicates \n \t(mark ?o) \n \t) \n \
    (:functions \n \t(total-cost) - number \n \t)\n{operators}\n )\n"

SEED_TEMPLATE = "     (:action seed{parameter} \n \
       \t:parameters () \n \
       \t;{comment}\n \
       \t:precondition (not (mark {parameter})) \n \
       \t:effect (and (mark {parameter})\n \t\t(increase (total-cost) {cost})) \n \t)\n"

GET_TEMPLATE = "     (:action get{index} \n \
        \t:parameters ()\n \
        \t; {comment}\n \
        \t:precondition (and {requires} \n \
        \t \t \t ( not (mark {achieve})))\n \
        \t:effect (and (mark {achieve})\n \
        \t \t \t(increase (total-cost) 0))\n \t)\n"
