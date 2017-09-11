-- database.sql

-- Schema for Snippy application.

-- Snippets are short command examples.
create table if not exists snippets (
    content     text not null unique,
    brief       text default '',
    groups      text default '',
    tags        text default '',
    links       text default '',
    digest      blob(64),
    metadata    text default '',
    id          integer primary key
);

-- Solutions are longer troubleshooting notes.
create table if not exists solutions (
    content     text not null unique,
    brief       text default '',
    groups      text default '',
    tags        text default '',
    links       text default '',
    digest      blob(64),
    metadata    text default '',
    id          integer primary key
);
