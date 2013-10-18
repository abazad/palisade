Create Or Replace Package Sq_Reports Is

  -- Author  : BOVA
  -- Created : 14.10.2013 11:38:22
  -- Purpose : Generate reports for Squid access history

  Function Report_1_Tab(i_Login In Sq_User.Login%Type) Return Xmltype;
  Procedure Report_1;
  Procedure Run_Report(i_Report_Name In Varchar2);

End Sq_Reports;
/
Create Or Replace Package Body Sq_Reports Is

  Function Report_1_Tab(i_Login In Sq_User.Login%Type) Return Xmltype Is
    v_Res Xmltype;
  Begin
    Select Xmlelement("Employee",
                      Xmlattributes(i_Login As User_Name),
                      Xmlagg(Xmlelement("ROW",
                                        Xmlforest(Url_Hostname, Bytes))))
      Into v_Res
      From (Select t.User_Name, t.Url_Hostname, Sum(t.Bytes) Bytes
              From Sq_Access_Log_Data t
             Where t.Access_Time >= Trunc(Sysdate, 'MM')
               And t.User_Name = i_Login
               And t.Sq_Req_Status Not In ('TCP_DENIED')
             Group By t.User_Name, t.Url_Hostname
             Order By 3 Desc)
     Where Rownum < 10;
  
    Return v_Res;
  End Report_1_Tab;

  Procedure Report_1 Is
    v_Xmldata   Xmltype;
    v_Xsl       Clob;
    v_Html      Xmltype;
    v_Report_Id Sq_Report_Data.Id%Type;
  Begin
    -- Prepare Report processing
    Select Sq_Report_Data_Seq.Nextval Into v_Report_Id From Dual;
  
    Insert Into Sq_Report_Data
    Values
      (v_Report_Id, Sysdate, 'report_1', 'RUNNING', Null);
    Commit;
    -- Make Report
    For r In (Select Login From Sq_User Order By Login) Loop
      Select Xmlconcat(v_Xmldata, Report_1_Tab(r.Login))
        Into v_Xmldata
        From Dual;
    End Loop;
    --load XSL Template 
    Select Data
      Into v_Xsl
      From Sq_Report_Xsl
     Where Report_Name = 'report_1';
    -- Transform XML to HTML
    v_Html := v_Xmldata.Transform(Xmltype(v_Xsl));
    -- Finish report processing
    Update Sq_Report_Data
       Set State = 'FINISHED', Data = v_Html.Getclobval()
     Where Id = v_Report_Id;
  
  End Report_1;

  Procedure Run_Report(i_Report_Name In Varchar2) Is
  Begin
    Dbms_Scheduler.Create_Job(Job_Name   => i_Report_Name,
                              Job_Type   => 'STORED_PROCEDURE',
                              Job_Action => 'sq_reports.' || i_Report_Name);
    Dbms_Scheduler.Enable(Name => i_Report_Name);
  End Run_Report;
End Sq_Reports;
/
