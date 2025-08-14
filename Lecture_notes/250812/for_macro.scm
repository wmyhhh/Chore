(define (map fn vals)
    (if (null? vals)
        ()
    (cons (fn (car vals)) (map fn (cdr vals))))
)

scm> (define (map fn vals) (if (null? vals) () (cons (fn (car vals)) (map fn (cdr vals)))))
map
scm> (map (lambda (x) (* x x)) '(1 2 3 4))
(1 4 9 16)

(define-macro (for sym vals expr)
    (list 'map (list 'lambda (list sym) expr) vals)
)