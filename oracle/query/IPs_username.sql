Select distinct d.client_src_ip
  From Sq_Access_Log_Data d
 Where d.Access_Time >= Trunc(Sysdate)
   And User_Name = 'maxpal'
