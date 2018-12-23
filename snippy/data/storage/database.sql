-- database.sql
-- Database schema for Snippy application.
CREATE TABLE IF NOT EXISTS contents
          (
                    id          UUID PRIMARY KEY NOT NULL UNIQUE
                  , data        text NOT NULL UNIQUE
                  , brief       text DEFAULT ''
                  , description text DEFAULT ''
                  , groups      text DEFAULT ''
                  , tags        text DEFAULT ''
                  , links       text DEFAULT ''
                  , category    text DEFAULT 'snippet'
                  , name        text DEFAULT ''
                  , filename    text DEFAULT ''
                  , versions    text DEFAULT ''
                  , source      text DEFAULT ''
                  , uuid        text NOT NULL UNIQUE
                  , created     TIMESTAMP
                  , updated     TIMESTAMP
                  , digest      CHAR(64)
          )
;
