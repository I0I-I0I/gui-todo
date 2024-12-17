create table if not exists todos (
	id integer primary key autoincrement,
	idx int not null,
	title text not null,
	date timestamp default current_timestamp not null
)
