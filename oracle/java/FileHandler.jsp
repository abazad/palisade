create or replace and compile java source named "FileHandler" as
import java.lang.*;
import java.util.*;
import java.io.*;
import java.sql.Timestamp;

public class FileHandler
{
  private static int SUCCESS = 1;
  private static  int FAILURE = 0;

  public static int delete (String path) {
    File myFile = new File (path);
    if (myFile.delete()) return SUCCESS; else return FAILURE;
  }

}
/
