(define (domain connected-nodestypes)
  (:requirements :strips)
  
  (:predicates
    (at ?loc)
    (connected ?from ?to)
  )
  
  (:action move
    :parameters (?from ?to)
    :precondition (and (at ?from) (connected ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )
)