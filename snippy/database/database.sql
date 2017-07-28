-- database.sql

-- Schema for snippy application.

-- Snippets are short text based command or code examples.
create table if not exists snippet (
    id          integer primary key,
    snippet     text not null unique,
    metadata    text default '',
    tags        text default '',
    comment     text default ''
);

-- Logs are troubleshooting reference notes.
create table if not exists log (
    id          integer primary key,
    log         text not null unique,
    metadata    text default '',
    tags        text default '',
    comment     text
);
