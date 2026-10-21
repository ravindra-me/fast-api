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