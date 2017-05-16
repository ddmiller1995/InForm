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
                bool fileSaved = SaveFileService.SaveFile(saveFileDialog1.FileName, json);

                StringBuilder message = new StringBuilder();
                if (fileSaved)
                {
                    message.Append("Succesfully backed up database to ");
                } else
                {
                    message.Append("Failed to backup database to ");
                }
                message.Append(saveFileDialog1.FileName);

                string caption = "InForm Database Backup";
                MessageBoxButtons buttons = MessageBoxButtons.OK;
                DialogResult dialogResult = MessageBox.Show(message.ToString(), caption, buttons);

                if (dialogResult == DialogResult.Yes) { this.Close(); }
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

                string message = "Succesfully restored database from backup file: " + openFileDialog1.FileName;

                string caption = "InForm Database Restore";
                MessageBoxButtons buttons = MessageBoxButtons.OK;
                DialogResult dialogResult = MessageBox.Show(message.ToString(), caption, buttons);

                if (dialogResult == DialogResult.Yes) { this.Close(); }
            }
        }
    }
}
