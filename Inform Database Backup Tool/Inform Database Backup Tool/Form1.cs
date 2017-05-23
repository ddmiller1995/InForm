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
            ProjectRootService.ComputeProjectRoot();

            if (saveFileDialog.ShowDialog() == DialogResult.OK || saveFileDialog.FileName != "")
            {
                Cursor.Current = Cursors.WaitCursor;
                // determine where the project is stored in the file system
                string projectRoot = ProjectRootService.ComputeProjectRoot();

                string command = "python manage.py dumpdata";
                // execute the command to retrieve the database dump
                string json = CommandService.Execute(projectRoot, command);
                // save the database dump to the user specified file
                bool fileSaved = SaveFileService.SaveFile(saveFileDialog.FileName, json);

                StringBuilder message = new StringBuilder();
                if (fileSaved)
                {
                    message.Append("Succesfully backed up database to ");
                }
                else
                {
                    message.Append("Failed to backup database to ");
                }
                message.Append(saveFileDialog.FileName);
                Cursor.Current = Cursors.Default;

                string caption = "InForm Database Backup";
                MessageBoxButtons buttons = MessageBoxButtons.OK;
                DialogResult dialogResult = MessageBox.Show(message.ToString(), caption, buttons);

                if (dialogResult == DialogResult.Yes) { this.Close(); }
            }
        }

        private void restoreButton_Click(object sender, EventArgs e)
        {
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                Cursor.Current = Cursors.WaitCursor;
                // determine where the project is stored in the file system
                string projectSrc = ProjectRootService.ComputeProjectSrc();

                string filename = openFileDialog.FileName;
                string command = "python manage.py loaddata " + filename;
                // execute the command to retrieve the database dump
                string json = CommandService.Execute(projectSrc, command);
                Cursor.Current = Cursors.Default;

                string message = "Succesfully restored database from backup file: " + openFileDialog.FileName;

                string caption = "InForm Database Restore";
                MessageBoxButtons buttons = MessageBoxButtons.OK;
                DialogResult dialogResult = MessageBox.Show(message.ToString(), caption, buttons);

                if (dialogResult == DialogResult.Yes) { this.Close(); }
            }
        }

        private void restartButton_Click_Click(object sender, EventArgs e)
        {
            Cursor.Current = Cursors.WaitCursor;
            string projectRoot = ProjectRootService.ComputeProjectRoot();
            string command = "docker-compose restart";
            string result = CommandService.Execute(projectRoot, command);
            Cursor.Current = Cursors.Default;

        }
    }
}
