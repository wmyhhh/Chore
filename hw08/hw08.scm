(define (square-exp term) `(* ,term ,term))

`(+ ,(square-exp 'a) ,(square-exp 'b))