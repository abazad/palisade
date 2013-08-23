Create Or Replace Package Mail Is
  c_Smtp_User Constant Varchar2(255) := 'vladimir@fido.uz';
  c_Smtp_Pass Constant Varchar2(255) := 'htytccfyc';

  -- Author  : BOVA
  -- Created : 22.08.2013 14:47:37
  -- Purpose : Notification via email

  Procedure Send(i_Smtp_Rcpt In Varchar2, i_Msg In Varchar2);
End Mail;
/
Create Or Replace Package Body Mail As

  Procedure Send(i_Smtp_Rcpt In Varchar2, i_Msg In Varchar2) Is
    v_Conn Utl_Smtp.Connection;
  Begin
    v_Conn := Utl_Smtp.Open_Connection('smtp.fido.uz', 25);
    Utl_Smtp.Ehlo(v_Conn, 'smtp.fido.uz');
    Utl_Smtp.Command(v_Conn, 'AUTH LOGIN');
    Utl_Smtp.Command(v_Conn,
                     Utl_Encode.Text_Encode(c_Smtp_User,
                                            'WE8ISO8859P1',
                                            Utl_Encode.Base64));
    Utl_Smtp.Command(v_Conn,
                     Utl_Encode.Text_Encode(c_Smtp_Pass,
                                            'WE8ISO8859P1',
                                            Utl_Encode.Base64));
  
    Utl_Smtp.Mail(v_Conn, c_Smtp_User);
    Utl_Smtp.Rcpt(v_Conn, i_Smtp_Rcpt);    
    Utl_Smtp.Data(v_Conn, i_Msg);
    Utl_Smtp.Quit(v_Conn);
  End Send;

End Mail;
/
