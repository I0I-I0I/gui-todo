create table if not exists todos (
	id integer primary key autoincrement,
	ordering int not null,
	state text not null,
	title text not null,
	date timestamp default current_timestamp not null
)
