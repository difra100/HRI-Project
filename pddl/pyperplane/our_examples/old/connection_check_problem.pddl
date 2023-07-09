(define (problem connected-nodes-problem)
  (:domain connected-nodes)
  
  (:objects
    fish water boat vehicle 
  )
  
  (:init
    (at start)
    (connected start node1)
    (connected start node3)
    (connected node1 node2)
    (connected node2 end)
  )
  
  (:goal
    (at end)
  )
)
