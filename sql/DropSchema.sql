
-- Copyright (c) 2015-2023 Agalmic Ventures LLC (www.agalmicventures.com)
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

------------------------------ Drop Schema ------------------------------

-------------------- Procedures --------------------

DO
$$
DECLARE
	dropSql TEXT;
BEGIN
	SELECT string_agg(format(
			'DROP %s %s;',
			CASE
				WHEN proisagg THEN 'AGGREGATE'
				ELSE 'FUNCTION'
			END,
			oid::regprocedure),
		E'\n')
	FROM pg_proc
	WHERE pronamespace = 'public'::regnamespace
		AND prolang IN (SELECT oid FROM pg_language WHERE lanname IN ('sql', 'plpgsql'))
	INTO dropSql;

	IF dropSql IS NOT NULL THEN
		EXECUTE dropSql;
	END IF;
END
$$ LANGUAGE plpgsql;

-------------------- Tables --------------------

DROP TABLE IF EXISTS LogMessage;
DROP TABLE IF EXISTS Exception;
DROP TABLE IF EXISTS Run;
DROP TABLE IF EXISTS SchemaMigration;

-------------------- Sequences --------------------

DROP SEQUENCE IF EXISTS LogMessageIdSequence;
DROP SEQUENCE IF EXISTS ExceptionIdSequence;
DROP SEQUENCE IF EXISTS RunIdSequence;
DROP SEQUENCE IF EXISTS SchemaMigrationIdSequence;
