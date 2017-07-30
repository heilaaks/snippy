-- database.sql

-- Schema for Snippy application.

-- Snips are short command examples.
create table if not exists snip (
    id          integer primary key,
    snip        text not null unique,
    metadata    text default '',
    tags        text default '',
    comment     text default '',
    link        text default ''
);

-- Resolutions are longer troubleshooting notes.
create table if not exists resolve (
    id          integer primary key,
    resolve     text not null unique,
    metadata    text default '',
    tags        text default '',
    comment     text default '',
    link        text default ''
);
