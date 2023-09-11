SELECT st.id AS "Student", SUM(st.correct) AS "Correct", CAST(SUM(st.correct) AS REAL) / COUNT(st.correct) AS "Average"
FROM
	/*
	Returns a table with columns (id, question, correct)
	where correct is a 0 or 1 depending on whether the question was answered correctly
	*/
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
GROUP BY st.id

