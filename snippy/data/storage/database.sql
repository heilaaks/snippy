-- database.sql
--
-- Snippy - command, solution, reference and code snippet manager.
-- Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU Affero General Public License as published
-- by the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU Affero General Public License for more details.
--
-- You should have received a copy of the GNU Affero General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.
--
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
