-- database.sql

-- Schema for Snippy application.

-- Content is either command, solution, referece or code examples.
create table if not exists contents (
    data        text not null unique,
    brief       text default '',
    groups      text default '',
    tags        text default '',
    links       text default '',
    category    text default 'snippet',
    name        text default '',
    filename    text default '',
    versions    text default '',
    uuid        text not null unique,
    created     datetime default current_timestamp,
    updated     datetime default current_timestamp,
    digest      blob(64),
    metadata    text default '',
    id          integer primary key
);
