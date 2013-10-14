Select Sq_Req_Status, Count(Sq_Req_Status)
  From Sq_Access_Log_Data
 Where Access_Time >= Trunc(Sysdate)
 Group By Sq_Req_Status
 Order By 2 Desc
