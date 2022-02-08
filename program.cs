using System;
using System.Collections.Generic;
using Microsoft.Win32;
namespace ConsoleApp1
{
    class Program
    {
        private static void Main(string[] args)
        {
            string hwid = GetHWID(); //Code is not 100% mine from here downwards, used a public repo to find the code to where the registry value was stored
            Console.Write(hwid);
        }
        private static string GetHWID()
        {
            string location = @"SOFTWARE\Microsoft\Cryptography";
            string name = "MachineGuid";
            using (RegistryKey localMachineX64View = RegistryKey.OpenBaseKey(RegistryHive.LocalMachine, RegistryView.Registry64))
            {
                using (RegistryKey rk = localMachineX64View.OpenSubKey(location))
                {
                    if (rk == null)
                    {
                        throw new KeyNotFoundException(string.Format(location));
                    }
                    object HWID = rk.GetValue(name);
                    if (HWID == null)
                    {
                        throw new IndexOutOfRangeException(string.Format(name));
                    }
                    return HWID.ToString();
                }
            }
        }
    }
}
