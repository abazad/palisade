Create Or Replace Package Sq_Lost_Pwd Is

  -- Author  : BOVA
  -- Created : 22.08.2013 15:27:22
  -- Purpose : Recovery lost passwords
  Procedure Send_Notif(Lost_Pwd In Sq_Lost_Password%Rowtype);
  Procedure Recovery;

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
    For Lost_Pwd In (Select * From Sq_Lost_Password where state='NEW') Loop
      Send_Notif(Lost_Pwd);
      Change_State(Lost_Pwd, 'SENT');
    End Loop;
  End Recovery;

End Sq_Lost_Pwd;
/
