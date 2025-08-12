(define (fact n) 
    (if (zero? n) 1 
    (* n (fact (- n 1))))
)

(fact 5)

(define original fact)

(define fact (lambda (n)
            (print (list 'fact n))
            (original n)))

(fact 5)

(define fact original)

(fact 5)

(define-macro (trace expr)      ;(trace (fact 5))
(define operator (car expr))        ;fact
`(begin
(define original ,operator)
(define ,operator (lambda (n)
            (print (list (quote ,operator) n))
            (original n)))
(define result ,expr)
(define ,operator original)
result))

(trace (fact 5))

(fact 5)
