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

            if (saveFileDialog.ShowDialog() == DialogResult.OK || saveFileDialog.FileName != "")
            {
                Cursor.Current = Cursors.WaitCursor;
                // determine where the project is stored in the file system
                string projectRoot = ProjectRootService.ComputeProjectSrc();

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
                DialogResult confirmationResult = MessageBox.Show("Are you sure want to restore the database? \nAll data will be overwritten by the data in the json file you are using to restore.", "Confirmation", MessageBoxButtons.OKCancel);
                if (confirmationResult == DialogResult.OK)
                {
                    Cursor.Current = Cursors.WaitCursor;
                    // determine where the project is stored in the file system
                    string projectSrc = ProjectRootService.ComputeProjectSrc();

                    string filename = openFileDialog.FileName;
                    string command = "python manage.py loaddata \"" + filename + "\"";
                    // execute the command to retrieve the database dump
                    string result = CommandService.Execute(projectSrc, command);
                    Cursor.Current = Cursors.Default;

                    string message = "Restored database from backup file: " + openFileDialog.FileName;
                    message += "\n" + result;

                    string caption = "InForm Database Restore";
                    MessageBoxButtons buttons = MessageBoxButtons.OK;
                    DialogResult dialogResult = MessageBox.Show(message.ToString(), caption, buttons);

                    if (dialogResult == DialogResult.Yes) { this.Close(); }
                }

            }
        }

        private void restartButton_Click_Click(object sender, EventArgs e)
        {


            MessageBoxButtons buttons = MessageBoxButtons.OKCancel;
            DialogResult dialogResult = MessageBox.Show("Are you sure you want to restart the web server? Everyone will temporarily be unable to access it.", "InForm restart", buttons);
            if (dialogResult == DialogResult.OK)
            {
                var x = 1;
                Cursor.Current = Cursors.WaitCursor;
                string projectRoot = ProjectRootService.ComputeProjectRoot();
                string command = "docker-compose restart";
                string result = CommandService.Execute(projectRoot, command);
                Cursor.Current = Cursors.Default;

                MessageBox.Show("Succesfully restarted InForm", "Success", MessageBoxButtons.OK);
            }


        }
    }
}
