Begin
  Dbms_Network_Acl_Admin.Create_Acl(Acl         => 'acl_fido_smtp_srv.xml',
                                    Description => 'Access to smtp mail server',
                                    Principal   => 'PALISADE',
                                    Is_Grant    => True,
                                    Privilege   => 'connect',
                                    Start_Date  => Systimestamp,
                                    End_Date    => Null);

  Commit;
  Dbms_Network_Acl_Admin.Assign_Acl(Acl        => 'acl_fido_smtp_srv.xml',
                                    Host       => 'smtp.fido.uz',
                                    Lower_Port => 25,
                                    Upper_Port => Null);
  Commit;
End;
/
