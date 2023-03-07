from typing import List
from sqlalchemy.sql.expression import text

from app.Configuration.Helpers.tools import get_enviromental_variable


def get_snowflake_id_generator_queries() -> List[text]:

    # The id of this database shard, must be set differently, for each schema shard you have.
    # Here we use only the public schema for now, otherwise we should consider changing it for each database.
    # Take care, you should not create a new sequence each time otherwise you are going
    return [
        text("CREATE SCHEMA IF NOT EXISTS PUBLIC;"),
        text("CREATE SEQUENCE IF NOT EXISTS PUBLIC.global_snowflake_id_sequence;"),
        text(
            f"""
            CREATE OR REPLACE FUNCTION PUBLIC.generate_snowflake_id(OUT result BIGINT) AS $$
            DECLARE
                epoch bigint := 1314220021721;
                sequence_id bigint;
                milliseconds bigint;
                shard_id int := {get_enviromental_variable('POSTGRES_SHARD_ID')};
            BEGIN
                SELECT nextval('PUBLIC.global_snowflake_id_sequence') % 1024 INTO sequence_id;
                SELECT FLOOR(EXTRACT(EPOCH FROM clock_timestamp()) * 1000) INTO milliseconds;
                result := (milliseconds - epoch) << 23;
                result := result | (shard_id << 10);
                result := result | (sequence_id);
            END;
            $$ LANGUAGE PLPGSQL;"""
        ),
    ]
