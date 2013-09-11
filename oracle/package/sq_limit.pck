Create Or Replace Package Sq_Limit Is

  -- Author  : VLADANDR
  -- Created : 09.04.2009 17:37:03
  -- Purpose : for squid proxy server
  Procedure Lock_User(i_User_Name In Sq_User.Login%Type);
  Procedure Traffic_Limit_Checker;
  Procedure Unlock_Users;
  Procedure Start_Job;
  Procedure Create_Job;
  Procedure Stop_Job;
End Sq_Limit;
/
Create Or Replace Package Body Sq_Limit Is
  --Lock specifiyed user       
  Procedure Lock_User(i_User_Name In Sq_User.Login%Type) Is
  Begin
    Update Sq_User c Set c.Status = 'B' Where c.Login = i_User_Name;
    Commit;
  
  End;

  --===============================
  -- Процедура проверки превышения
  -- расхода трафика через прокси 
  -- сервер SQUID
  --===============================
  Procedure Traffic_Limit_Checker Is
    -- Local Variables HERE               
    v_Per_User_Traff  Varchar2(2000);
    Cur               Integer;
    v_Authuser        Varchar2(100);
    v_Traffic_Limit   Integer;
    v_Traffic_Expense Integer;
    Cur_Exe           Integer;
  Begin
  
    v_Per_User_Traff := '
              Select t.User_Name, Round(Sum(t.Bytes) / (1024 * 1024))
        From Sq_Access_Log_Data t
       Where t.Access_Time >= Trunc(Sysdate)       
         And t.User_Name In (Select u.Login From SQ_User u)
         and t.sq_req_status not in (' || '''' ||
                        'TCP_DENIED' || '''' || ')         
       Group By t.User_Name';
  
    Cur := Dbms_Sql.Open_Cursor;
    Dbms_Sql.Parse(Cur, v_Per_User_Traff, Dbms_Sql.Native);
    Dbms_Sql.Define_Column(Cur, 1, v_Authuser, 200);
    Dbms_Sql.Define_Column(Cur, 2, v_Traffic_Expense);
    Cur_Exe := Dbms_Sql.Execute(Cur);
  
    Loop
      If Dbms_Sql.Fetch_Rows(Cur) > 0 Then
        Dbms_Sql.Column_Value(Cur, 1, v_Authuser);
        Dbms_Sql.Column_Value(Cur, 2, v_Traffic_Expense);
      
        Begin
          -- Which traffic limit allow to Current User
          Select c.Traffic_Limit
            Into v_Traffic_Limit
            From Sq_User c
           Where Upper(c.Login) = Upper(v_Authuser);
        Exception
        
          When No_Data_Found Then
            Null;
        End;
        --execute immediate v_Query;              
      
        If v_Traffic_Expense > v_Traffic_Limit Then
          -- Limit Exceeded , Block Squid User
          Lock_User(v_Authuser);
        
        Else
          Dbms_Output.Put_Line('Limit not exceed');
        End If;
      
      Else
        -- No more rows to analyze
        Exit;
      End If;
    End Loop;
    Commit;
  Exception
    When Others Then
      Null;
  End;

  --===============================
  -- Запуск JOB-ов 
  --===============================

  Procedure Start_Job Is
    Job_Already_Exist_Error Exception;
    Pragma Exception_Init(Job_Already_Exist_Error, -27477);
  Begin
    Create_Job;
    -- Run limit checker
    Dbms_Scheduler.Enable(Name => 'traffic_limit_checker_job');
    -- Squid User Unlocker
    Dbms_Scheduler.Enable(Name => 'squid_Unlock_Job');
    Commit;
  Exception
    When Job_Already_Exist_Error Then
      Null;
    
  End Start_Job;

  --===============================
  -- Процедура создания Job-ов
  --===============================

  Procedure Create_Job Is
  
  Begin
    -- Create job for squid users unlock                  
    Dbms_Scheduler.Create_Job(Job_Name      => 'squid_Unlock_Job',
                              Schedule_Name => 'atNight',
                              Job_Type      => 'STORED_PROCEDURE',
                              Job_Action    => 'SQ_limit.Unlock_Users',
                              Enabled       => True);
  
    Commit;
  
    Dbms_Scheduler.Create_Job(Job_Name        => 'traffic_limit_checker_job',
                              Job_Type        => 'STORED_PROCEDURE',
                              Job_Action      => 'SQ_Limit.traffic_limit_checker',
                              Repeat_Interval => 'sysdate+1/144',
                              Enabled         => True);
    Dbms_Scheduler.Set_Attribute(Name      => 'traffic_limit_checker_job',
                                 Attribute => 'RESTARTABLE',
                                 Value     => True);
    Dbms_Scheduler.Set_Attribute(Name      => 'traffic_limit_checker_job',
                                 Attribute => 'max_failures',
                                 Value     => 1000);
    Commit;
  
  End Create_Job;

  --===============================
  -- Остановка JOB-ов 
  --===============================      

  Procedure Stop_Job Is
  Begin
    Dbms_Scheduler.Disable(Name => 'traffic_limit_checker_job');
    -- Disable  squid_Unlock_Job job
    Dbms_Scheduler.Disable(Name => 'squid_Unlock_Job');
    Commit;
  
  End Stop_Job;

  --===============================
  -- Процедура РАЗблокировки пользователя
  -- прокси сервера SQUID
  --===============================
  Procedure Unlock_Users Is
  Begin
    For Row In (Select c.Login From Sq_User c Where c.Status In ('B')) Loop
      Update Sq_User c Set c.Status = 'A' Where c.Login = Row.Login;
      Commit;
    End Loop;
  
  End;

End Sq_Limit;
/
