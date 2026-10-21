-- # Challenge 6.4 (aapke API ka SQL version)
-- # Ye API request SQL mein likhiye:
-- # GET /tasks?done=false&search=sql&skip=0&limit=2
-- # Results naye pehle (created_at se) aane chahiye.
-- # Isi request ka total nikalne wali query likhiye.
-- # Page 2 ki query likhiye (same filter, limit=2).
-- # Sochiye: jo search text user bhejta hai (jaise sql), wo seedha query mein jud raha hai. Agar koi user search mein '; DELETE FROM tasks; -- bhej de to kya ho sakta hai? Iska naam SQL Injection hai. Sirf apne shabdon mein bataiye kya khatra hai, solution Lesson 7 mein seekhenge.


-- SELECT → FROM → WHERE → ORDER BY → LIMIT → OFFSET
-- offect = (page -1) * perpagitem

select * from tasks where done = false and title ilike '%sql%'  limit 2 OFFSET 2;

create table users(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT now() 
);

create table blogs(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    published BOOLEAN NOT NULL DEFAULT false,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT now() 
);


CREATE INDEX idx_blogs_user_published ON blogs(user_id, published);

