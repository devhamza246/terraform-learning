import asyncpg


# Database connection pool
async def get_database_pool():
    return await asyncpg.create_pool(
        user="postgres", password="1234", database="terraform", host="localhost"
    )


# Create record
async def create_record(pool, data):
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO table_name (column1, column2) VALUES ($1, $2)",
            data["column1"],
            data["column2"],
        )


# Read record
async def read_record(pool, record_id):
    async with pool.acquire() as connection:
        result = await connection.fetchrow(
            "SELECT * FROM table_name WHERE id = $1", record_id
        )
        return dict(result)


# Update record
async def update_record(pool, record_id, data):
    async with pool.acquire() as connection:
        await connection.execute(
            "UPDATE table_name SET column1 = $1, column2 = $2 WHERE id = $3",
            data["column1"],
            data["column2"],
            record_id,
        )


# Delete record
async def delete_record(pool, record_id):
    async with pool.acquire() as connection:
        await connection.execute("DELETE FROM table_name WHERE id = $1", record_id)
