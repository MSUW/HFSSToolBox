import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Windows.Forms import Application

import sys
sys.path.append(r"C:\Users\msuw1\Desktop\HFSSToolBox")
sys.path.append(r"C:\Program Files\AnsysEM\AnsysEM21.1\Win64")
sys.path.append(r"C:\Program Files\AnsysEM\AnsysEM21.1\Win64\PythonFiles\DesktopPlugin")
sys.path.append(r"C:\Program Files\AnsysEM\AnsysEM21.1\Win64\common\IronPython\Lib")
import ScriptEnv

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oAnsoftApplication.GetAppDesktop()
oDesktop.RestoreWindow()

import MainForm

Application.EnableVisualStyles()
form = MainForm.MainForm(oDesktop,AddErrorMessage,AddWarningMessage,AddInfoMessage)
Application.Run(form)
