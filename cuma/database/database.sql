-- database.sql

-- Schema for cuma application.

-- Snippets are command or code snippets.
create table if not exists snippet (
    id          integer primary key,
    snippet     text not null unique,
    metadata    text default '',
    tags        text default '',
    comment     text default ''
);

-- Logs are troubleshooting reference notes.
create table if not exists troubleshooting (
    id          integer primary key,
    log         text not null unique,
    metadata    text default '',
    tags        text default '',
    comment     text
);
