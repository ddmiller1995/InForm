﻿namespace Inform_Database_Backup_Tool
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.backupButton = new System.Windows.Forms.Button();
            this.restoreButton = new System.Windows.Forms.Button();
            this.openFileDialog = new System.Windows.Forms.OpenFileDialog();
            this.saveFileDialog = new System.Windows.Forms.SaveFileDialog();
            this.restartButton_Click = new System.Windows.Forms.Button();
            this.tableLayoutPanel1.SuspendLayout();
            this.SuspendLayout();
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.ColumnCount = 2;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel1.Controls.Add(this.backupButton, 0, 1);
            this.tableLayoutPanel1.Controls.Add(this.restoreButton, 0, 2);
            this.tableLayoutPanel1.Controls.Add(this.restartButton_Click, 0, 0);
            this.tableLayoutPanel1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tableLayoutPanel1.Location = new System.Drawing.Point(0, 0);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 3;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 50F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 25F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Percent, 25F));
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(1918, 1365);
            this.tableLayoutPanel1.TabIndex = 0;
            // 
            // backupButton
            // 
            this.tableLayoutPanel1.SetColumnSpan(this.backupButton, 2);
            this.backupButton.Dock = System.Windows.Forms.DockStyle.Fill;
            this.backupButton.Location = new System.Drawing.Point(100, 782);
            this.backupButton.Margin = new System.Windows.Forms.Padding(100);
            this.backupButton.Name = "backupButton";
            this.backupButton.Size = new System.Drawing.Size(1718, 141);
            this.backupButton.TabIndex = 0;
            this.backupButton.Text = "Download backup file";
            this.backupButton.UseVisualStyleBackColor = true;
            this.backupButton.Click += new System.EventHandler(this.backupButton_Click);
            // 
            // restoreButton
            // 
            this.tableLayoutPanel1.SetColumnSpan(this.restoreButton, 2);
            this.restoreButton.Dock = System.Windows.Forms.DockStyle.Fill;
            this.restoreButton.Location = new System.Drawing.Point(100, 1123);
            this.restoreButton.Margin = new System.Windows.Forms.Padding(100);
            this.restoreButton.Name = "restoreButton";
            this.restoreButton.Size = new System.Drawing.Size(1718, 142);
            this.restoreButton.TabIndex = 1;
            this.restoreButton.Text = "Restore from a backup file";
            this.restoreButton.UseVisualStyleBackColor = true;
            this.restoreButton.Click += new System.EventHandler(this.restoreButton_Click);
            // 
            // openFileDialog
            // 
            this.openFileDialog.DereferenceLinks = false;
            this.openFileDialog.FileName = "openFileDialog1";
            this.openFileDialog.Filter = "JSON Files (*.json)|*.json|All files (*.*)|*.*";
            // 
            // saveFileDialog
            // 
            this.saveFileDialog.DereferenceLinks = false;
            this.saveFileDialog.Filter = "JSON Files (*.json)|*.json|All files (*.*)|*.*";
            this.saveFileDialog.Title = "Save a database backup";
            // 
            // restartButton_Click
            // 
            this.tableLayoutPanel1.SetColumnSpan(this.restartButton_Click, 2);
            this.restartButton_Click.Dock = System.Windows.Forms.DockStyle.Fill;
            this.restartButton_Click.Location = new System.Drawing.Point(200, 200);
            this.restartButton_Click.Margin = new System.Windows.Forms.Padding(200);
            this.restartButton_Click.Name = "restartButton_Click";
            this.restartButton_Click.Size = new System.Drawing.Size(1518, 282);
            this.restartButton_Click.TabIndex = 2;
            this.restartButton_Click.Text = "Restart";
            this.restartButton_Click.UseVisualStyleBackColor = true;
            this.restartButton_Click.Click += new System.EventHandler(this.restartButton_Click_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(12F, 25F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1918, 1365);
            this.Controls.Add(this.tableLayoutPanel1);
            this.Name = "Form1";
            this.Text = "InForm Database Backup Tool";
            this.tableLayoutPanel1.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private System.Windows.Forms.Button backupButton;
        private System.Windows.Forms.Button restoreButton;
        private System.Windows.Forms.OpenFileDialog openFileDialog;
        private System.Windows.Forms.SaveFileDialog saveFileDialog;
        private System.Windows.Forms.Button restartButton_Click;
    }
}

