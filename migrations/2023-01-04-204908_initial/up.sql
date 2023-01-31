CREATE TABLE users (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    email VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL,
    email_verified BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX users_idx ON users (
    name, email
);