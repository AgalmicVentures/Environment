
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
	COALESCE(blockingLock.relation::regclass::text, blockingLock.locktype) AS lockedItem,
	NOW() - blockedActivity.query_start AS waitDuration,
	blockedActivity.pid AS blockedPid,
	blockedActivity.query AS blockedQuery,
	blockedLock.mode AS blockedMode,
	blockingActivity.pid AS blockingPid,
	blockingActivity.query AS blockingQuery,
	blockingLock.mode AS blockingMode
FROM pg_catalog.pg_locks blockedLock
JOIN pg_stat_activity blockedActivity ON blockedLock.pid = blockedActivity.pid
JOIN pg_catalog.pg_locks blockingLock ON
	(blockingLock.transactionid = blockedLock.transactionid OR
		(blockingLock.locktype = blockedLock.locktype AND blockingLock.relation = blockedLock.relation)
	) AND blockedLock.pid != blockingLock.pid
JOIN pg_stat_activity blockingActivity ON
	blockingLock.pid = blockingActivity.pid
	AND blockingActivity.datid = blockedActivity.datid
WHERE
	NOT blockedLock.granted
	AND blockingActivity.datname = current_database()
ORDER BY waitDuration DESC;

-------------------- Space --------------------

SELECT *,
	pg_size_pretty(totalBytes) AS totalSize,
	pg_size_pretty(indexBytes) AS indexSize,
	pg_size_pretty(toastBytes) AS toastSize,
	pg_size_pretty(tableBytes) AS tableSize
FROM (
	SELECT *,
		totalBytes - indexBytes - COALESCE(toastBytes, 0) AS tableBytes
	FROM (
		SELECT c.oid,
			nspname AS tableSchema,
			relname AS tableName,
			c.reltuples AS rowEstimate,
			pg_total_relation_size(c.oid) AS totalBytes,
			pg_indexes_size(c.oid) AS indexBytes,
			pg_total_relation_size(reltoastrelid) AS toastBytes
		FROM pg_class c
		LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
		WHERE relkind = 'r'
	) x
	ORDER BY totalBytes DESC
) y;
