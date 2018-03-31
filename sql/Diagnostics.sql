
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

------------------------------ Diagnostic Queries ------------------------------

-------------------- Activity --------------------

-- Look at all activity
SELECT * FROM pg_stat_activity;

-- Find only running, foreground tasks
SELECT * FROM pg_stat_activity
WHERE NOT (state = 'idle' OR pid = pg_backend_pid());

-------------------- Locks --------------------

-- Check on the locks
SELECT relation::regclass, * FROM pg_locks;

-- Find blocked locks
SELECT relation::regclass, * FROM pg_locks
WHERE NOT GRANTED;

-- Convenience query for seeing what queries are blocking what other queries and how
SELECT
	COALESCE(blocking_lock.relation::regclass::text, blocking_lock.locktype) as locked_item,
	NOW() - blocked_activity.query_start AS wait_duration,
	blocked_activity.pid AS blocked_pid,
	blocked_activity.query as blocked_query,
	blocked_lock.mode as blocked_mode,
	blocking_activity.pid AS blocking_pid,
	blocking_activity.query as blocking_query,
	blocking_lock.mode as blocking_mode
FROM pg_catalog.pg_locks blocked_lock
JOIN pg_stat_activity blocked_activity ON blocked_lock.pid = blocked_activity.pid
JOIN pg_catalog.pg_locks blocking_lock ON
	(blocking_lock.transactionid = blocked_lock.transactionid OR
		(blocking_lock.locktype = blocked_lock.locktype AND blocking_lock.relation = blocked_lock.relation)
	) AND blocked_lock.pid != blocking_lock.pid
JOIN pg_stat_activity blocking_activity ON
	blocking_lock.pid = blocking_activity.pid
	AND blocking_activity.datid = blocked_activity.datid
WHERE
	NOT blocked_lock.granted
	AND blocking_activity.datname = current_database()
ORDER BY wait_duration DESC;
