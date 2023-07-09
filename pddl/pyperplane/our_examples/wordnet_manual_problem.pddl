(define (problem connected-nodes-kinds-problem)
  (:domain connected-nodes-kinds-domain)
  
  (:objects
    fish boat water vehicle animal
  )
  
  (:init
    (at fish)
    (connected-related-to fish water)
    (connected-related-to water boat)
    (connected-is-a fish animal)
    (connected-is-a boat vehicle)
  )
  
  (:goal
    (at vehicle)
  )
)