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

            // determine where the project is stored in the file system
            string projectRoot = ProjectRootService.ComputeProjectRoot();

            string command = "python manage.py dumpdata";
            // execute the command to retrieve the database dump
            string json = CommandService.Execute(projectRoot, command);
            // save the database dump to the user specified file
            bool result = SaveFileService.SaveFile("", "");

            //if (saveFileDialog1.ShowDialog() == DialogResult.OK || saveFileDialog1.FileName != "")
            //{
   
            //}
        }

        private void restoreButton_Click(object sender, EventArgs e)
        {
            if (openFileDialog1.ShowDialog() == DialogResult.OK)
            {
                string fileName = openFileDialog1.FileName;
                var dialog = openFileDialog1;
            }
        }
    }
}
