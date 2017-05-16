using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Inform_Database_Backup_Tool
{
    public class SaveFileService
    {
        public static bool SaveFile(string filename, string body)
        {
            using (StreamWriter writer = new StreamWriter(filename))
            {
                writer.Write(body);
            }
            return true;
        }
    }
}
