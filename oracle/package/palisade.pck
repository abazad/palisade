create or replace package palisade is

  -- Author  : BOVA
  -- Created : 22.08.2013 16:12:35
  -- Purpose : 
  
  c_http_host constant varchar2(2000) := '10.50.50.20:5000';

end palisade;
/
create or replace package body palisade is

  -- Private type declarations
  type <TypeName> is <Datatype>;
  
  -- Private constant declarations
  <ConstantName> constant <Datatype> := <Value>;

  -- Private variable declarations
  <VariableName> <Datatype>;

  -- Function and procedure implementations
  function <FunctionName>(<Parameter> <Datatype>) return <Datatype> is
    <LocalVariable> <Datatype>;
  begin
    <Statement>;
    return(<Result>);
  end;

begin
  -- Initialization
  <Statement>;
end palisade;
/
