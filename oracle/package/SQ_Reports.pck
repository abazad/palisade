Create Or Replace Package Sq_Reports Is

  -- Author  : BOVA
  -- Created : 14.10.2013 11:38:22
  -- Purpose : Generate reports for Squid access history

  Procedure Report_1;

End Sq_Reports;
/
Create Or Replace Package Body Sq_Reports Is

  Procedure Report_1 Is
    v_Data Sq_Report_Data.Data%Type;
  Begin
    v_Data := '<!DOCTYPE html><html>' || '<table>';
    For r In (Select *
                From (Select t.User_Name, t.Url_Hostname, Sum(t.Bytes)
                        From Sq_Access_Log_Data t
                       Where t.Access_Time >= Trunc(Sysdate, 'MM')
                         And t.User_Name = 'bogdan'
                         And t.Sq_Req_Status Not In ('TCP_DENIED')
                       Group By t.User_Name, t.Url_Hostname
                       Order By 3 Desc)
               Where Rownum <= 10) Loop
      v_Data := v_Data || '<tr><td>' || r.Url_Hostname || '</td></tr>';
    End Loop;
    Insert Into Sq_Report_Data
    Values
      (Sq_Report_Data_Seq.Nextval, Sysdate, 'rep1', v_Data);
    Commit;
  
  End Report_1;
End Sq_Reports;
/
