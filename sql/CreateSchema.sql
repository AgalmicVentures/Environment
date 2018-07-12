
-- Copyright (c) 2015-2018 Agalmic Ventures LLC (www.agalmicventures.com)
--
-- Permission is hereby granted, free of charge, to any person obtaining a copy
-- of this software and associated documentation files (the "Software"), to
-- deal in the Software without restriction, including without limitation the
-- rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
-- sell copies of the Software, and to permit persons to whom the Software is
-- furnished to do so, subject to the following conditions:
--
-- The above copyright notice and this permission notice shall be included in
-- all copies or substantial portions of the Software.
--
-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
-- IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
-- FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
-- AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
-- LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
-- OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
-- THE SOFTWARE.

------------------------------ Create Schema ------------------------------

-- This script is responsible for setting up the schema of the TODO database.

-------------------- Tables --------------------

CREATE SEQUENCE ExceptionIdSequence;
CREATE SEQUENCE RunIdSequence;

CREATE TABLE Run(
	id INT PRIMARY KEY DEFAULT nextval('RunIdSequence'),

	command TEXT,
	gitVersion TEXT NOT NULL,
	workingDirectory TEXT,
	processId INT NOT NULL,
	uid INT NOT NULL,
	username TEXT,
	language TEXT,
	startTime TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE Exception(
	id INT PRIMARY KEY DEFAULT nextval('ExceptionIdSequence'),
	runId INT NOT NULL REFERENCES Run,
	threadId BIGINT NOT NULL,

	exceptionType TEXT NOT NULL,
	message TEXT NOT NULL,
	backtrace TEXT NOT NULL,
	time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-------------------- Privileges --------------------

GRANT SELECT ON ALL TABLES IN SCHEMA public
    TO TODO_db_reader;

GRANT INSERT, SELECT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER ON ALL TABLES IN SCHEMA public
    TO TODO_db_writer;

GRANT SELECT ON ALL SEQUENCES IN SCHEMA public
    TO TODO_db_reader;

GRANT SELECT, UPDATE, USAGE ON ALL SEQUENCES IN SCHEMA public
    TO TODO_db_writer;

