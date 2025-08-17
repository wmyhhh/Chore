(define-macro (switch expr cases)
(cons
    `cond
    (map (lambda (case) (cons `(equal? ,expr ,(car case)) (cdr case)))
        casess))
)

(define (switch expr cases)
    (cons
        `cond
        (map (lambda (case) (cons `(equal? ,expr ,(car case)) (cdr case)))
        cases)
    )
)

(switch '(+ 1 1) '((1 (print 'a))
                      (2 (print 'b))
                      (3 (print 'c))))

(define (switch expr cases)
    `(let ((val ,expr))
	  ,(cons
	    'cond
	    (map (lambda (case) (cons
	           `(equal? val ,(car case))
		       (cdr case)))
		     cases))))