(define (ascending? s) 
    (if (or (null? s) (null? (cdr s)))
        #t
    (if (> (car s) (car (cdr s)))
        #f
        (ascending? (cdr s)))
    )
)

; GPT 
;(define (ascending? s)
;  (or (null? (cdr s))
;      (and (<= (car s) (cadr s))
;           (ascending? (cdr s)))))

(define (my-filter pred s) 
    (if (null? s)
        '()
        (if (pred(car s))
            (cons (car s) (my-filter pred (cdr s)))
            (my-filter pred (cdr s)))
    )
)

(define (interleave lst1 lst2) 
    (cond 
    ((null? lst1)    lst2)
    ((null? lst2)    lst1)
    (else   ((cons (car lst1)) (cons (car lst2)) (interleave (cdr lst1) (cdr lst2)))
    )
    )
)

(define (interleave lst1 lst2) 
  (cond 
    ((null? lst1) lst2)
    ((null? lst2) lst1)
    (else (cons (car lst1)
                (cons (car lst2)
                      (interleave (cdr lst1) (cdr lst2))))))
)


(define (no-repeats s) 
    (if (null? s)
        '()
        (let (
            (filtered (filter (lambda (y) (not (= (car s) y))) (cdr s))))
        (cons (car s) (no-repeats filtered))
        )
    )
)

