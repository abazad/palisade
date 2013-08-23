Create Or Replace Package Sq_Lost_Pwd Is

  -- Author  : BOVA
  -- Created : 22.08.2013 15:27:22
  -- Purpose : Recovery lost passwords
  Procedure Send_Notif(Lost_Pwd In Sq_Lost_Password%Rowtype);
  Procedure Recovery;
  Procedure Create_Job;
  Procedure Start_Job;

End Sq_Lost_Pwd;
/
Create Or Replace Package Body Sq_Lost_Pwd Is

  Procedure Send_Notif(Lost_Pwd In Sq_Lost_Password%Rowtype) As
    v_Msg Varchar2(2000);
    Crlf  Varchar2(2) := Chr(13) || Chr(10);
  Begin
    v_Msg := 'From:' || Mail.c_Smtp_User || Crlf ||
             'Subject: proxy.fido.uz->Reset password' || Crlf || 'To:' ||
             Lost_Pwd.Email || Crlf ||
             'This is mail for Squid password recovery. ' || Crlf ||
             'Follow this link please.' || Crlf || 'http://' ||
             Palisade.c_Http_Host || '/user/edit_password?secret_key=' ||
             Lost_Pwd.Secret_Key || '&email=' || Lost_Pwd.Email;
    Mail.Send(Lost_Pwd.Email, v_Msg);
  
  End Send_Notif;

  Procedure Change_State(Lost_Pwd In Sq_Lost_Password%Rowtype,
                         i_State  In Varchar2) Is
  Begin
    Update Sq_Lost_Password
       Set State = i_State
     Where Email = Lost_Pwd.Email;
    Commit;
  End Change_State;

  Procedure Recovery Is
  Begin
    For Lost_Pwd In (Select * From Sq_Lost_Password Where State = 'NEW') Loop
      Send_Notif(Lost_Pwd);
      Change_State(Lost_Pwd, 'SENT');
    End Loop;
  End Recovery;

  Procedure Create_Job Is
  Begin
    Dbms_Scheduler.Create_Job(Job_Name        => 'RECOVERY_PASSWORD_JOB',
                              Job_Type        => 'STORED_PROCEDURE',
                              Job_Action      => 'sq_lost_pwd.recovery',
                              Repeat_Interval => 'sysdate+1/1440');
    Commit;
  
  End Create_Job;

  Procedure Start_Job Is
    Job_Already_Exist_Error Exception;
    Pragma Exception_Init(Job_Already_Exist_Error, -27477);
  Begin
    Create_Job;
    Dbms_Scheduler.Enable(Name => 'RECOVERY_PASSWORD_JOB');
    Commit;
  Exception
    When Job_Already_Exist_Error Then
      Null;
  End Start_Job;

End Sq_Lost_Pwd;
/
