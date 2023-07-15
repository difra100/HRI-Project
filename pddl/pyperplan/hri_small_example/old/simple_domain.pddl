(define (domain simple-domain)
  (:requirements :strips)
  
  (:predicates
    (at ?loc)
  )
  
  (:action goto
    :parameters (?from ?to)
    :precondition (at ?from)
    :effect (and (not (at ?from)) (at ?to))
  )
)