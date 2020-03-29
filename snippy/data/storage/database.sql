-- database.sql
--
-- SPDX-License-Identifier: AGPL-3.0-or-later
-- 
-- snippy - software development and maintenance notes manager.
-- Copyright 2017-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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
                  , category    text DEFAULT 'snippet'
                  , data        text NOT NULL UNIQUE
                  , brief       text DEFAULT ''
                  , description text DEFAULT ''
                  , name        text DEFAULT ''
                  , groups      text DEFAULT ''
                  , tags        text DEFAULT ''
                  , links       text DEFAULT ''
                  , source      text DEFAULT ''
                  , versions    text DEFAULT ''
                  , languages   text DEFAULT ''
                  , filename    text DEFAULT ''
                  , created     TIMESTAMP WITH TIME ZONE
                  , updated     TIMESTAMP WITH TIME ZONE
                  , uuid        UUID NOT NULL UNIQUE
                  , digest      CHAR(64)
          )
;
