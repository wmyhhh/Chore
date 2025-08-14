CREATE TABLE nouns AS
    SELECT 'dog' as phrase UNION
    SELECT 'cat'           UNION
    SELECT 'frog'          UNION
    SELECT 'bird';

CREATE TABLE ands AS
    SELECT first.phrase || ' and ' || second.phrase AS conca_phrase
    FROM nouns AS first, nouns AS second
    WHERE first.phrase <> second.phrase;

CREATE TABLE chases AS
    SELECT subject.conca_phrase || '  chase  ' || object.conca_phrase
    FROM ands AS subject, ands AS object
    WHERE subject.conca_phrase <> object.conca_phrase;