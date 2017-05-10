using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Inform_Database_Backup_Tool
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        static System.Collections.Specialized.StringCollection log = new System.Collections.Specialized.StringCollection();

        static void WalkDirectoryTree(DirectoryInfo root)
        {
            FileInfo[] files = null;
            DirectoryInfo[] subDirs = null;

            // First, process all the files directly under this folder
            try
            {
                files = root.GetFiles("*.py");
            }
            // This is thrown if even one of the files requires permissions greater
            // than the application provides.
            catch (UnauthorizedAccessException e)
            {
                // This code just writes out the message and continues to recurse.
                // You may decide to do something different here. For example, you
                // can try to elevate your privileges and access the file again.
                log.Add(e.Message);
            }

            catch (DirectoryNotFoundException e)
            {
                Console.WriteLine(e.Message);
            }

            if (files != null)
            {
                foreach (FileInfo fi in files)
                {
                    // In this example, we only access the existing FileInfo object. If we
                    // want to open, delete or modify the file, then
                    // a try-catch block is required here to handle the case
                    // where the file has been deleted since the call to TraverseTree().
                    Console.WriteLine(fi.FullName);
                }

                // Now find all the subdirectories under this directory.
                subDirs = root.GetDirectories();

                foreach (DirectoryInfo dirInfo in subDirs)
                {
                    if (dirInfo.Name == "InForm")
                    {
                        Console.WriteLine("aye");
                    }
                    // Resursive call for each subdirectory.
                    WalkDirectoryTree(dirInfo);
                }
            }
        }

        private void backupButton_Click(object sender, EventArgs e)
        {


            if (saveFileDialog1.ShowDialog() == DialogResult.OK || saveFileDialog1.FileName != "")
            {
                var x = saveFileDialog1.FileName;
                // find and set project root
                string[] drives = Environment.GetLogicalDrives();

                foreach (string dr in drives)
                {
                    DriveInfo di = new DriveInfo(dr);

                    // Here we skip the drive if it is not ready to be read. This
                    // is not necessarily the appropriate action in all scenarios.
                    if (!di.IsReady)
                    {
                        Console.WriteLine("The drive {0} could not be read", di.Name);
                        continue;
                    }
                    System.IO.DirectoryInfo rootDir = di.RootDirectory;
                    WalkDirectoryTree(rootDir);
                }

                // cd into project_root\src
                // execute "python manage.py dumpdata > 
            }
        }

        private void restoreButton_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                string fileName = openFileDialog1.FileName;
            }
        }
    }
}
