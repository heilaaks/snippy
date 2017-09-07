-- database.sql

-- Schema for Snippy application.

-- Snippets are short command examples.
create table if not exists snippets (
    id          integer primary key,
    snippet     text not null unique,
    brief       text default '',
    groups      text default '',
    tags        text default '',
    links       text default '',
    metadata    text default '',
    digest      blob(64)
);

-- Solutions are longer troubleshooting notes.
create table if not exists solutions (
    id          integer primary key,
    solution    text not null unique,
    brief       text default '',
    groups      text default '',
    tags        text default '',
    links       text default '',
    metadata    text default '',
    digest      blob(64)
);
