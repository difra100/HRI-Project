(define (domain connected-nodes)
  (:requirements :strips)
  
  (:predicates
    (at ?loc)
    (connected-related-to ?from ?to)
    (connected-is-a ?from ?to)
  )
  
  (:action move-related-to
    :parameters (?from ?to)
    :precondition (and (at ?from) (connected-related-to ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )

  (:action move-is-a
    :parameters (?from ?to)
    :precondition (and (at ?from) (connected-is-a ?from ?to))
    :effect (and (not (at ?from)) (at ?to))
  )


)