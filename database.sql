drop table if exists url_checks CASCADE ;
drop table if exists urls CASCADE ;

create table urls(
id serial primary key,
name varchar(255) unique,
created_at DATE DEFAULT CURRENT_TIMESTAMP
);

create table url_checks(
    id serial primary key,
    url_id integer references urls (id) on delete cascade on update cascade,
    status_code integer,
    h1 varchar(255),
    title varchar(255),
    description varchar(255),
    created_at DATE DEFAULT CURRENT_TIMESTAMP
)