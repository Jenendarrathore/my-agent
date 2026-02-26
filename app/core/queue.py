from arq.connections import ArqRedis

# Placeholders for separate queue pools
# These are populated by the setup system during app lifespan
base_pool: ArqRedis | None = None
email_pool: ArqRedis | None = None
