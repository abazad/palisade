-- Create table
create table SQ_ACCESS_LOG_DATA_2
(
  id                  INTEGER not null,
  access_time         DATE,
  response_time       INTEGER,
  client_src_ip       VARCHAR2(15 CHAR),
  sq_req_status       VARCHAR2(64 CHAR),
  http_status_code    VARCHAR2(4 CHAR),
  bytes               INTEGER,
  req_method          VARCHAR2(10 CHAR),
  user_name           VARCHAR2(32 CHAR),
  sq_hierarchy_status VARCHAR2(32 CHAR),
  server_fqdn         VARCHAR2(255 CHAR),
  mime_type           VARCHAR2(32 CHAR),
  mime_type_desc      VARCHAR2(32 CHAR),
  url                 VARCHAR2(4000 CHAR),
  url_hostname        VARCHAR2(255 CHAR)
)
partition by range (access_time)
(
partition p_2013_8 values less than (to_date('2013-09-01', 'YYYY-MM-DD')) tablespace SQ_DATA,
partition p_2013_9 values less than (to_date('2013-10-01', 'YYYY-MM-DD')) tablespace SQ_DATA,
partition p_2013_10 values less than (to_date('2013-11-01', 'YYYY-MM-DD')) tablespace SQ_DATA,
partition p_2013_11 values less than (to_date('2013-12-01', 'YYYY-MM-DD')) tablespace SQ_DATA,
partition p_2013_12 values less than (to_date('2014-01-01', 'YYYY-MM-DD')) tablespace SQ_DATA,
partition p_2014_1 values less than (to_date('2014-02-01', 'YYYY-MM-DD')) tablespace SQ_DATA,
partition p_2014_2 values less than (to_date('2014-03-01', 'YYYY-MM-DD')) tablespace SQ_DATA,
partition p_2014_3 values less than (to_date('2014-04-01', 'YYYY-MM-DD')) tablespace SQ_DATA,
partition p_2014_4 values less than (to_date('2014-05-01', 'YYYY-MM-DD')) tablespace SQ_DATA
);

-- Create/Recreate indexes
create index SQ_ACCESS_LOG_DATA_I1 on SQ_ACCESS_LOG_DATA (USER_NAME)
  tablespace SQ_INDX
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    minextents 1
    maxextents unlimited
  );
create index SQ_ACCESS_LOG_DATA_I2 on SQ_ACCESS_LOG_DATA (USER_NAME, ACCESS_TIME)
  tablespace SQ_INDX
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    minextents 1
    maxextents unlimited
  );
-- Create/Recreate primary, unique and foreign key constraints
alter table SQ_ACCESS_LOG_DATA
  add primary key (ID)
  using index
  tablespace SQ_DATA
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    minextents 1
    maxextents unlimited
  );
