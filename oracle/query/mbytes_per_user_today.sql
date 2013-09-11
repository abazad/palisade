Select d.User_Name, Round(Sum(d.Bytes) / (1024 * 1024))
  From Sq_Access_Log_Data d
 Where d.Access_Time >= Trunc(Sysdate)
   And d.Sq_Req_Status Not In ('TCP_DENIED')
 Group By d.User_Name
 Order By 2 Desc
