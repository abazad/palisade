Select Sum(Bytes), Url_Hostname
  From Sq_Access_Log_Data d
 Where d.Access_Time >= Trunc(Sysdate)
   And User_Name = 'alohon'
 Group By Url_Hostname
 Order By 1 Desc
