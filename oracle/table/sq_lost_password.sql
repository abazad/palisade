CREATE TABLE "SQ_LOST_PASSWORD" (
        id INTEGER NOT NULL,
        created_on DATE,
        email VARCHAR2(250 CHAR),
        state VARCHAR2(50 CHAR),
        secret_key VARCHAR2(32 CHAR),
        PRIMARY KEY (id)
)