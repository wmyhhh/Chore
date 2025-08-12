; return (+ (* a a) (* b b))

(define (square-exp term) `(* ,term ,term))

`(+ ,(square-exp 'a) ,(square-exp 'b))