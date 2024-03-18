DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
	id SERIAL,
	key varchar(200) DEFAULT NULL,
	secret_key varchar(200) DEFAULT NULL,
	target_url varchar(200) DEFAULT NULL,
	is_active boolean DEFAULT NULL, 
	clicks Integer DEFAULT NULL,
	PRIMARY KEY (id)	
);