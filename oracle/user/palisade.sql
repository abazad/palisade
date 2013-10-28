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

-- for working with external files
execute dbms_java.grant_permission('PALISADE', 'SYS:java.io.FilePermission', '/u02/export/palisade', 'read' );
execute dbms_java.grant_permission('PALISADE', 'java.io.FilePermission', '<<ALL FILES>>', 'read ,write, execute, delete');

-- Object Grants
grant execute on dbms_scheduler to palisade;
grant create job to palisade;

grant DEBUG CONNECT SESSION to palisade;