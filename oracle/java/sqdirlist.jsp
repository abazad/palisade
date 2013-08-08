create or replace and compile java source named sqdirlist as
import java.io.*;
import java.sql.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class sqDirList
{
  public static void getList(String directory)
                     throws SQLException
  {
      File path = new File( directory );
      String[] list = path.list();
      String element;
      Pattern p = Pattern.compile("SQ_*");
      Matcher matcher = p.matcher("");
        
      
      for (int i = 0; i< list.length; i++)
      {
          element = list[i];
          matcher.reset(element);
          if (matcher.lookingAt())
             try {
               #sql {INSERT INTO SQ_ACCESS_LOG_FILES (FILE_ID, NAME, FILE_STATUS)
                      VALUES (Sq_Access_Log_Files_Sq.Nextval, :element, 0) 
                     };
             } 
             catch (oracle.jdbc.driver.OracleSQLException e) {
                 continue;
               }  
      }
  }
}
/
