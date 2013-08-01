PROMPT Specify PATH to DATA directory:;
DEFINE DATA_PATH = &DATA_PATH;

create tablespace SQ_DATA
  datafile '&DATA_PATH/sq_data01.dbf' 
  size 16M 
  autoextend on 
  Next 32M
  maxsize Unlimited
  Segment Space Management Auto;

PROMPT Specify PATH to INDEX directory:;
DEFINE INDEX_PATH = &INDEX_PATH;

create tablespace SQ_INDX
  datafile '&INDEX_PATH/sq_indx01.dbf' 
  size 16M 
  autoextend on 
  Next 32M
  maxsize Unlimited
  Segment Space Management Auto;
