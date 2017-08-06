-- database.sql

-- Schema for Snippy application.

-- Snippets are short command examples.
create table if not exists snippets (
    id          integer primary key,
    snippet     text not null unique,
    brief       text default '',
    tags        text default '',
    link        text default '',
    metadata    text default ''
);

-- Resolutions are longer troubleshooting notes.
create table if not exists resolves (
    id          integer primary key,
    resolve     text not null unique,
    brief       text default '',
    tags        text default '',
    link        text default '',
    metadata    text default ''
);
