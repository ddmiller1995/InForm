using BackupApi;
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


        private void backupButton_Click(object sender, EventArgs e)
        {
            if (saveFileDialog1.ShowDialog() == DialogResult.OK || saveFileDialog1.FileName != "")
            {
                // determine where the project is stored in the file system
                string projectRoot = ProjectRootService.ComputeProjectRoot();

                string command = "python manage.py dumpdata";
                // execute the command to retrieve the database dump
                string json = CommandService.Execute(projectRoot, command);
                // save the database dump to the user specified file
                bool result = SaveFileService.SaveFile(saveFileDialog1.FileName, json);
            }
        }

        private void restoreButton_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                // determine where the project is stored in the file system
                string projectRoot = ProjectRootService.ComputeProjectRoot();

                string filename = openFileDialog1.FileName;
                string command = "python manage.py loaddata " + filename;
                // execute the command to retrieve the database dump
                string json = CommandService.Execute(projectRoot, command);
            }
        }
    }
}
