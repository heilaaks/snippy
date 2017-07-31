-- database.sql

-- Schema for Snippy application.

-- Snippets are short command examples.
create table if not exists snippet (
    id          integer primary key,
    snippet     text not null unique,
    tags        text default '',
    comment     text default '',
    link        text default '',
    metadata    text default ''
);

-- Resolutions are longer troubleshooting notes.
create table if not exists resolve (
    id          integer primary key,
    resolve     text not null unique,
    tags        text default '',
    comment     text default '',
    link        text default '',
    metadata    text default ''
);
