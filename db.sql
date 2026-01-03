create table if not exists users(
	id serial primary key,
	username text unique not null, 
	full_name text,
	email text unique,
	created_at timestamp default current_timestamp
);

create table if not exists books(
	id serial primary key,
	owner_id int not null references users(id) on delete cascade,
	title text not null,
	author text,
	condition text,
	description text,
	created_at timestamp default current_timestamp
);

create table if not exists listings(
	id serial primary key,
	book_id int not null references books(id) on delete cascade,
	status text not null default 'available',
	created_at timestamp default current_timestamp
);

create table if not exists swap_requests(
	id serial primary key,
	listing_id int not null references listings(id) on delete cascade,
	requester_id int not null references users(id) on delete cascade,
	message text,
	status text not null default 'pending',
	created_at timestamp default current_timestamp
);

create table if not exists study_groups(
	id serial primary key,
	owner_id int not null references users(id) on delete cascade,
	title text not null,
	topic text,
	event_time timestamp,
	capacity int default 10,
	created_at timestamp default current_timestamp
);

create table if not exists study_group_members(
	id serial primary key,
	group_id int not null references study_groups(id) on delete cascade,
	user_id int not null references users(id) on delete cascade,
	joined_at timestamp default current_timestamp
);

create table if not exists notifications(
	id serial primary key,
	user_id int not null references users(id) on delete cascade,
	message text
);

create table if not exists Accounts(
	user_id int primary key references users(id) on delete cascade,
	username text not null,
	password text not null unique
);
insert into Accounts(user_id,username,password)
values (1,'alice','$2b$12$DEdAJA.0GnwYSeBGABqUlea/WPu7GUpiJIJ97uZy2J7JitcIXECPa'),
		(2,'bob','$2b$12$vaHomAA06SeZWPVKOqGvk.hQbstzly.h86Mxz78mWL.g/FL0efbty'),
		(12,'admin','$2b$12$1St7tavFW3omL5MEZdmx.ejGYYAe.R3xovyEkDdDKEEFVEaZFrH/W');

--Sample data ( em bảo chat tạo)
-- Users
INSERT INTO users (username, full_name, email) VALUES
('alice', 'Alice Nguyen', 'alice@example.com'),
('bob', 'Bob Tran', 'bob@example.com'),
('carol', 'Carol Le', 'carol@example.com');



-- Books
INSERT INTO books (owner_id, title, author, condition, description) VALUES
(1, 'Python Crash Course', 'Eric Matthes', 'new', 'Beginner-friendly Python book'),
(2, 'Deep Learning with Python', 'Francois Chollet', 'good', 'Keras-based deep learning'),
(3, 'Clean Code', 'Robert C. Martin', 'fair', 'Best practices for software engineering');


-- Listings
INSERT INTO listings (book_id, status) VALUES
(1, 'available'),
(2, 'available'),
(3, 'available');


-- Swap Requests
INSERT INTO swap_requests (listing_id, requester_id, message, status) VALUES
(1, 2, 'Hi Alice, I want to swap this book.', 'pending'),
(2, 3, 'Can I get this book?', 'pending');


-- Study Groups
INSERT INTO study_groups (owner_id, title, topic, event_time, capacity) VALUES
(1, 'Python Study Group', 'Python Basics', '2025-12-20 18:00:00', 5),
(2, 'Deep Learning Circle', 'Neural Networks', '2025-12-22 17:00:00', 3);


-- Study Group Members
INSERT INTO study_group_members (group_id, user_id) VALUES
(1, 1),
(1, 2),
(2, 2),
(2, 3);

CREATE INDEX idx_books_owner_id ON books(owner_id);
CREATE INDEX idx_listings_status ON listings(status);
CREATE INDEX idx_swap_requests_listings_id ON swap_requests(listing_id);
CREATE INDEX idx_swap_requests_requester_id ON swap_requests(requester_id);

