Create Or Replace Package Sq_Load Is

  -- Author  : BOVA
  -- Created : 01.12.2010 11:36:57
  -- Purpose : export, import data 

  -- Public type declarations

  -- Public function and procedure declarations
  Procedure Get_Dir_List(p_Directory Varchar2);
  Function Delete_File(p_Path Varchar2) Return Number;
  Procedure Load_Ext_Data;
  Procedure Run;
  Procedure Delete_Processed_Files;
  Function Get_Dir_Path(Ora_Dir_Name Varchar2) Return Varchar2;
  Procedure Job_Start;
  Procedure Job_Stop;

End Sq_Load;
/
/* 
file_status description
   0 - new file
   1 - in process file
   2 - processed file
   3 - deleted file
*/

Create Or Replace Package Body Sq_Load Is
  g_Dir_Name        Varchar2(255) := 'PALISADE';
  g_New_File        Number(1) := 0;
  g_Processing_File Number(1) := 1;
  g_Processed_File  Number(1) := 2;
  g_Deleted_File    Number(1) := 3;

  -- Function and procedure implementations

  /* Function for puting file names to table */
  Procedure Get_Dir_List(p_Directory Varchar2) As
    Language Java Name 'sqDirList.getList( java.lang.String )';
  Function Delete_File(p_Path In Varchar2) Return Number As
    Language Java Name 'FileHandler.delete (java.lang.String) return java.lang.int';

  /* Function return full path of directory using directory name */
  Function Get_Dir_Path(Ora_Dir_Name Varchar2) Return Varchar2 Is
    Ora_Dir_Path Varchar2(255);
  Begin
    Select d.Directory_Path
      Into Ora_Dir_Path
      From All_Directories d
     Where d.Directory_Name = Ora_Dir_Name;
    Return Ora_Dir_Path;
  End Get_Dir_Path;

  /* Procedure for loading data from external table*/
  Procedure Load_Ext_Data Is
    -- exception when can't open external table    
    /* bind 
    ORA-29913: error in executing ODCIEXTTABLEOPEN callout
    with e_err_open_ext_tbl*/
    e_Err_Open_Ext_Tbl Exception;
    Pragma Exception_Init(e_Err_Open_Ext_Tbl, -29913);
    Cursor Cur_Log_Data_Ext Is
      Select * From Sq_Access_Log_Data_Ext;
  
  Begin
    --TODO: EXIT if no data imported
    For r In Cur_Log_Data_Ext Loop
      Insert Into Sq_Access_Log_Data
        (Id,
         Access_Time,
         Response_Time,
         Client_Src_Ip,
         Sq_Req_Status,
         Http_Status_Code,
         Bytes,
         Req_Method,
         User_Name,
         Sq_Hierarchy_Status,
         Server_Fqdn,
         Mime_Type,
         Mime_Type_Desc,
         Url,
         Url_Hostname)
      Values
        (Sq_Access_Log_Data_Sq.Nextval,
         r.Access_Time,
         r.Response_Time,
         r.Client_Src_Ip,
         r.Sq_Req_Status,
         r.Http_Status_Code,
         r.Bytes,
         r.Req_Method,
         r.User_Name,
         r.Sq_Hierarchy_Status,
         r.Server_Fqdn,
         r.Mime_Type,
         r.Mime_Type_Desc,
         r.Url,
         r.Url_Hostname);
      --      Select * From Sq_Access_Log_Data_Ext;
    End Loop;
  
    -- Change file status to Processed_file
    Update Sq_Access_Log_Files t
       Set t.File_Status = g_Processed_File
     Where t.File_Status = g_Processing_File;
    -- Data inserted, file_status changed - need commit 
    Commit;
    -- Data loaded into db, then delete files from filesystem
    Delete_Processed_Files;
  Exception
    When e_Err_Open_Ext_Tbl Then
      Null;
    
  End Load_Ext_Data;

  /* Procedure for deleting processed files*/
  Procedure Delete_Processed_Files Is
    v_Dir_Path   Varchar2(255);
    v_File_Path  Varchar2(255);
    v_Del_Status Number;
  Begin
    v_Dir_Path := Get_Dir_Path(g_Dir_Name);
    For f In (Select File_Id, Name
                From Sq_Access_Log_Files t
               Where Upper(t.Name) Like 'SQ_%.TXT'
                 And t.File_Status = g_Processed_File) Loop
      v_File_Path  := v_Dir_Path || '/' || f.Name;
      v_Del_Status := Delete_File(v_File_Path);
      If v_Del_Status = 1 Then
        -- When file deleted Update file status here
        Update Sq_Access_Log_Files t
           Set t.File_Status = g_Deleted_File
         Where t.File_Id = f.File_Id;
      End If;
    End Loop;
    Commit;
  End Delete_Processed_Files;

  /*Procedure for altering external table properties*/
  Procedure Alt_Ext_Tbl_Loc Is
    --Pragma Autonomous_Transaction;
    v_Step_Cnt       Number(9) := 0;
    v_File_Cnt_Limit Number(3) := 50;
    v_File_List      Varchar2(8000) := '';
    v_Sql            Varchar2(8000);
  Begin
    /* 
    Concatenate  external files which status are NEW_FILE or PROCESSING_FILE
    into one string using limit for file count here
    */
    For r In (Select File_Id, Name
                From Sq_Access_Log_Files t
               Where Upper(t.Name) Like 'SQ_%.TXT'
                 And t.File_Status In (g_New_File, g_Processing_File)
                 And Rownum < v_File_Cnt_Limit) Loop
      If v_Step_Cnt = 0 Then
        v_File_List := v_File_List || '' || '''' || r.Name || '''';
      Else
        v_File_List := v_File_List || ', ' || '''' || r.Name || '''';
      End If;
      v_Step_Cnt := v_Step_Cnt + 1;
      -- Change file status to Processing_file
      Update Sq_Access_Log_Files t
         Set t.File_Status = g_Processing_File
       Where t.File_Id = r.File_Id;
    
    End Loop;
  
    -- If we have files to load, then change LOCATION propertie of external table
    If v_File_List Is Not Null Then
      v_Sql := 'alter table sq_access_log_data_ext location (' ||
               v_File_List || ')';
      Execute Immediate v_Sql;
      -- Important commit
      --Commit;
    End If;
  
  Exception
    When No_Data_Found Then
      Null;
    
  End Alt_Ext_Tbl_Loc;

  /* Execute all actions together here*/
  Procedure Run Is
  Begin
    Get_Dir_List(Get_Dir_Path(g_Dir_Name));
    Alt_Ext_Tbl_Loc;
    Load_Ext_Data;
    Execute Immediate 'TRUNCATE Table SQ_DIR_LIST_TEMP';
    Commit;
  End Run;

  /* Start job here*/
  Procedure Job_Start Is
    Vjob Number;
  Begin
    -- Squid Log Importer
    Dbms_Job.Submit(Vjob, 'sq_Load.Run;', Sysdate, 'sysdate+1/720');
    Commit;
  
  End Job_Start;

  /* Stop job here*/
  Procedure Job_Stop Is
  Begin
    -- Remove Squid_Log_Importer, Traffic_Limit_Checker jobs
    For i In (Select Job
                From User_Jobs t
               Where Upper(t.What) Like 'SQ_LOAD.%') Loop
      Dbms_Job.Remove(Job => i.Job);
    End Loop;
    Commit;
  
  End Job_Stop;

End Sq_Load;
/
