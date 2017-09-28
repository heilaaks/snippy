-- database.sql

-- Schema for Snippy application.

-- Snippets are short command examples.
create table if not exists contents (
    data        text not null unique,
    brief       text default '',
    groups      text default '',
    tags        text default '',
    links       text default '',
    category    text default 'snippets',
    filename    text default '',
    utc         datetime default current_timestamp,
    digest      blob(64),
    metadata    text default '',
    id          integer primary key
);
