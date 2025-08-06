(define (subsets s)
    (if (null? s) nil
        
        (let ( (rest (subsets(cdr s))) )
        (append rest
               (map (lambda (t) (cons (car s) t)) rest)
               
               (list(list(car s))))
        
        )
    )
)

(define (even s)
    (filter (lambda (s) (even? (apply + s)) ) subsets(s) )
)