SELECT *
FROM 
    (SELECT 
        st.id AS id,
        st.question AS question, 
        (st.box0 LIKE nerd.box0 AND st.box0 LIKE 'x')
            OR (st.box1 LIKE nerd.box1 AND st.box1 LIKE 'x')
            OR (st.box2 LIKE nerd.box2 AND st.box2 LIKE 'x')
            OR (st.box3 LIKE nerd.box3 AND st.box3 LIKE 'x')
        AS correct
    FROM results AS st
    INNER JOIN results AS nerd
    ON nerd.id = 0 AND nerd.question = st.question
    ) AS st
