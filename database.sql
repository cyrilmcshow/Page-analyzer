DROP TABLE IF EXISTS urls CASCADE;
CREATE TABLE urls(
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255),
    created_at date
    );

DROP TABLE IF EXISTS urls CASCADE;
create table url_checks(
	id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	url_id bigint references urls(id),
	status_code int,
	h1 varchar(255),
	title varchar(255),
	description varchar(255),
	created_at date
);