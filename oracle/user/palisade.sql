-- Create the user
create user palisade
  identified by Q1w3tre321
  default tablespace SQ_DATA
  temporary tablespace TEMP
  profile DEFAULT;
-- Grant/Revoke role privileges
grant resource to palisade;
grant connect to palisade;


-- Modify the user
alter user PALISADE
  quota unlimited on sq_data
  quota unlimited on sq_indx;