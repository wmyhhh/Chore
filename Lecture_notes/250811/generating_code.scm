; quote '
; quasi quote ` can be unquoted by ,

scm> '(+ 2 ,(- 5 3))
(+ 2 (unquote (- 5 3)))

scm> `(+ 2 ,(- 5 3))
(+ 2 2)


; tremendously useful for generating codes
(begin
(define (sum x total)
    (if (< x 10) 
        (sum (+ x 2) (+ total (* x x)))
    total))
 (sum 2 0)
)

(begin
(define (sum x total)
    (if (< (* x x) 50) 
        (sum (+ x 1) (+ total x))
    total))
 (sum 1 0)
)

(define (sum-while   initial-x   condition         add-to-total   update-x)
;       (sum-while   1           '(< (* x x) 50)   'x             '(+ x 1))
`(begin
(define (f x total)
    (if ,condition
        (f ,update-x (+ total ,add-to-total))
    total))
 (f ,initial-x 0))
)

scm> (sum-while   1           '(< (* x x) 50)   'x             '(+ x 1))
(begin (define (f x total) (if (< (* x x) 50) (f (+ x 1) (+ total x)) total)) (f 1 0))

scm> (eval (sum-while   1           '(< (* x x) 50)   'x             '(+ x 1)))
28
