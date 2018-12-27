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
                  , uuid        UUID NOT NULL UNIQUE
                  , created     TIMESTAMP WITH TIME ZONE
                  , updated     TIMESTAMP WITH TIME ZONE
                  , digest      CHAR(64)
          )
;
