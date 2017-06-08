using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading.Tasks;

namespace BackupApi
{
    public class ProjectRootService
    {
        public static string ComputeProjectRoot()
        {
            string[] drives = Environment.GetLogicalDrives();
            foreach (string dr in drives)
            {
                if (dr != @"C:\")
                {
                    continue;
                }
                DriveInfo di = new DriveInfo(dr);
                if (!di.IsReady)
                {
                    continue;
                }
                DirectoryInfo driveRootDir = di.RootDirectory;



                DirectoryInfo projectRoot = GetChildDirOrNull(driveRootDir, "InForm");
                if (projectRoot == null)
                {
                    return null;
                }
                return projectRoot.FullName;
            }
            return null;
        }

        public static string ComputeProjectSrc()
        {
            string[] drives = Environment.GetLogicalDrives();
            foreach (string dr in drives)
            {
                if (dr != @"C:\")
                {
                    continue;
                }
                DriveInfo di = new DriveInfo(dr);
                if (!di.IsReady)
                {
                    continue;
                }
                DirectoryInfo driveRootDir = di.RootDirectory;



                DirectoryInfo projectRoot = GetChildDirOrNull(driveRootDir, "InForm");
                if (projectRoot == null)
                {
                    return null;
                }

                DirectoryInfo projectSrc = GetChildDirOrNull(projectRoot, "src");
                if (projectSrc == null)
                {
                    return null;
                }
                return projectSrc.FullName;
            }
            return null;
        }

        private static DirectoryInfo GetChildDirOrNull(DirectoryInfo parentDir, string dirName)
        {
            DirectoryInfo[] subDirs = parentDir.GetDirectories();
            DirectoryInfo targetDir = null;
            foreach (DirectoryInfo dirInfo in subDirs)
            {
                if (dirInfo.Name == dirName)
                {
                    targetDir = dirInfo;
                }
            }
            return targetDir;
        }

    }
}
