create users(
    id integer generated always as identity primary key,
    name varchar(50) not null
    email varchar(100) not null
    created_at timestamp not null default now()
)

create tasks(
    id integer generated always as identity primary key
    title varchar(100) not null
    content text
    published boolean not null default False
    user_id integer references users(id) on delete cascade
)

create index idx_tasks_user_ids on tasks(user_id, pus)


select blogs.title, users.name from blogs  join users on blogs.user_id == users.id

select  users.name, STRING_AGG(blogs.title, ', ') AS titles from users left join blogs on blogs.user_id = users.id group by users.name having count(blogs.id);

select users.name from users left join blogs where blogs.id is null


select users.name, count(blogs.id) from users inner join blogs on users.id = blogs.user_id group by users.name;

SELECT users.name, COUNT(blogs.id) AS blog_count
FROM users
LEFT JOIN blogs ON blogs.user_id = users.id
GROUP BY  users.name
ORDER BY users.name;


SELECT users.name, COUNT(blogs.id) AS blog_count
FROM users
LEFT JOIN blogs ON blogs.user_id = users.id where blogs.user_id = users.id and blogs.published = true
GROUP BY  users.name
ORDER BY users.name;


create table events (id int primary key, name text not null, seat_left int not null);
insert into events values(1, 'Concert', 1);