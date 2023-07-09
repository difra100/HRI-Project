(define (domain connected-nodes-kinds-domain)
  (:requirements :strips)
  
  (:predicates
    (at ?loc)
    (connected-related ?from ?to)
    (connected-hyponym ?from ?to)
    (connected-hypernym ?from ?to)
    (connected-meronym ?from ?to)
    (connected-holonym ?from ?to)
    (connected-antonym ?from ?to)
    (connected-attribute ?from ?to)
    (connected-entailment ?from ?to)
    (connected-cause ?from ?to)



  )
  
  (:action move-related
    :parameters (?from ?to)
    :precondition (and (at ?from) (connected-related ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )

  (:action move-hyponym
    :parameters (?from ?to)
    :precondition (and (at ?from) (connected-hyponym ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )

  (:action move-hypernym
    :parameters (?from ?to)
    :precondition (and (at ?from) (connected-hypernym ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )
  (:action move-meronym
    :parameters (?from ?to)
    :precondition (and (at ?from) (connected-meronym ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )
  (:action move-holonym
    :parameters (?from ?to)
    :precondition (and (at ?from) (connected-holonym ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )
  (:action move-antonym
    :parameters (?from ?to)
    :precondition (and (at ?from) (connected-antonym ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )

  (:action move-attribute
    :parameters (?from ?to)
    :precondition (and (at ?from) (connected-attribute ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )
   (:action move-entailment
    :parameters (?from ?to)
    :precondition (and (at ?from) (connected-entailment ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )
   (:action move-cause
    :parameters (?from ?to)
    :precondition (and (at ?from) (connected-cause ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )
  
  

)