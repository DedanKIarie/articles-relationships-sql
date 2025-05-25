CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS magazines (
    id  INTERGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY ,
    title TEXT NOT NULL, 
    author_id INTERGER,
    magazine_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(id)
    FOREIGN KEY (magazine_id) REFERENCES magazines(id)
);