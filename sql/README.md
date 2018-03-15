
## SQL (`sql/`)
This folder contains stubs for setting up a new database environment in
PostgreSQL.

*All scripts require modification at all points where `TODO` is present.*

### `CreateRoles.sql`
Creates group roles for admins, writers, and readers. Then creates users in
those groups.

*This must be run first, one time, so that permissions may be granted after
the schema is created.*

### `CreateSchema.sql`
Creates a simple example schema for tracking when a bit of software runs and
throws exceptions.

### `DropSchema.sql`
Drops everything created by `CreateSchema.sql` in the correct order.
