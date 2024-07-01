import System.Drawing
import System.Windows.Forms
import os
import time
import clr
clr.AddReference('System.Windows.Forms')
from System.Windows.Forms import Clipboard,TextDataFormat

from System.Drawing import *
from System.Windows.Forms import *

class TempSender():	#虚拟事件触发器类，通过tag模拟特定事件
	Tag = ""
	
class LogHead():
	def __init__(self,color,headtext):
		self.color = color
		self.headtext = headtext

class LogType():
	Log = LogHead( System.Drawing.Color.FromArgb(100, 100, 100) , '[Log]')
	Debug = LogHead( System.Drawing.Color.Black , '[Debug]') 
	Warning = LogHead( System.Drawing.Color.DarkOrange , '[Warning]')
	Error = LogHead( System.Drawing.Color.FromArgb(192, 0, 0) , '[Error]')
	Info = LogHead( System.Drawing.Color.Green , '[Info]')

class MainForm(Form):
	def __init__(self, oDesktop, emsg, wmsg, imsg):
		self.InitializeComponent()
				
		#-----------------------debug---------------------------------
		self.infoNum = 0
		self.debug = True
		self.LogGen('系统初始化完成',LogType.Info)
		#self.LogGen('这是警告！',LogType.Warning)
		#self.LogGen('这是错误！',LogType.Error)
		#self.LogGen('这是调试！',LogType.Debug)
		#self.LogGen('这是Log！',LogType.Log)
		
		#-----------------从设计图转换到实际工作状态---------------------
		self.defaultSize = System.Drawing.Size(382, 550)	#窗口尺寸
		self.ClientSize = self.defaultSize
		
		self._groupBox5.Location = System.Drawing.Point(12, 309)
		self._groupBox5.Size = System.Drawing.Size(358, 110)
		
		self._groupBox6.Location = System.Drawing.Point(12, 309)
		self._groupBox6.Size = System.Drawing.Size(358, 110)
		
		#-------------------------内部变量------------------------------
		self.oDesktop = oDesktop
		self.oProject = [None]*2
		self.oDesign = [None]*2
		self.oEditor = [None]*2
		
		self._projectNameBox = [self._projectNameBox1, self._projectNameBox2]
		self._designNameBox = [self._designNameBox1, self._designNameBox2]
		self._projectCombo = [self._projectCombo1, self._projectCombo2]
		self._designCombo = [self._designCombo1, self._designCombo2]
		self._stateLabel = [self._stateLabel1, self._stateLabel2]
		self._funRadioButton = [self._radioButton1, self._radioButton2, self._radioButton3, self._radioButton4]
		self.funDict = {'reload': 1, 'save': 0, 'sync': 2, 'custom': 3}
		
		self.AddErrorMessage = emsg		#错误信息
		self.AddWarningMessage = wmsg	#警告信息
		self.AddInfoMessage = imsg		#提示信息
		self.State = [False, False]		#准备状态
		self.FileState = False			#文件状态
		self.SOR = "save"				#SR功能指示
		
		self.globalmask = []			#参数mask
		self.masktext = []			#mask提示语
		
		#---------------------参数设置---------------------------------
		f = open("C:/Users/username/Desktop/HFSSToolBox/Toolbox.config",'r')
		lines = f.readlines()
		f.close()
		cdict = self.ConfigFormater(lines)
		
		defautFunction = cdict["defautFunction"]
		defautFunIndex = self.funDict[defautFunction]
		self._funRadioButton[defautFunIndex].Checked = True
		
		miniMode = cdict["miniModelDefalt"]
		self.miniModeFunc = cdict["miniModeFunc"]
		if miniMode == "yes":
			self._miniCheckBox.Checked = True
		
		self.globalmask = cdict["defaulMask"]
		try:
			self.globalmask = dict(eval(self.globalmask)).keys()
			self.globalmask.sort()
			self.GenMaskText()
		except:
			self.LogGen('Mask格式错误，已使用空mask',LogType.Error)
			self.globalmask = []
			self.GenMaskText()
		
		self.defaulPath = cdict["defaulSavePath"]
		#self.defaulPath = "D:/HFSS Prop/"
		
		#self.Location = Point(SystemInformation.WorkingArea.Width - self.Width, SystemInformation.WorkingArea.Height - self.Height)
		self.Location = Point(SystemInformation.WorkingArea.Width - self.Width, 180)
		
		
	def InitializeComponent(self):
		self._components = System.ComponentModel.Container()
		self._getButton1 = System.Windows.Forms.Button()
		self._label1 = System.Windows.Forms.Label()
		self._groupBox1 = System.Windows.Forms.GroupBox()
		self._projectNameBox1 = System.Windows.Forms.TextBox()
		self._designNameBox1 = System.Windows.Forms.TextBox()
		self._swiftButton1 = System.Windows.Forms.Button()
		self._label2 = System.Windows.Forms.Label()
		self._stateLabel1 = System.Windows.Forms.Label()
		self._designCombo1 = System.Windows.Forms.ComboBox()
		self._projectCombo1 = System.Windows.Forms.ComboBox()
		self._groupBox2 = System.Windows.Forms.GroupBox()
		self._stateLabel2 = System.Windows.Forms.Label()
		self._designNameBox2 = System.Windows.Forms.TextBox()
		self._swiftButton2 = System.Windows.Forms.Button()
		self._label4 = System.Windows.Forms.Label()
		self._projectNameBox2 = System.Windows.Forms.TextBox()
		self._getButton2 = System.Windows.Forms.Button()
		self._label5 = System.Windows.Forms.Label()
		self._designCombo2 = System.Windows.Forms.ComboBox()
		self._projectCombo2 = System.Windows.Forms.ComboBox()
		self._groupBox3 = System.Windows.Forms.GroupBox()
		self._radioButton1 = System.Windows.Forms.RadioButton()
		self._radioButton2 = System.Windows.Forms.RadioButton()
		self._groupBox4 = System.Windows.Forms.GroupBox()
		self._openFileDialog1 = System.Windows.Forms.OpenFileDialog()
		self._fileNameBox = System.Windows.Forms.TextBox()
		self._label3 = System.Windows.Forms.Label()
		self._fileSelectButton = System.Windows.Forms.Button()
		self._fileStateLabel = System.Windows.Forms.Label()
		self._saveButton = System.Windows.Forms.Button()
		self._noteBox = System.Windows.Forms.TextBox()
		self._noteLabel = System.Windows.Forms.Label()
		self._saveTipLable = System.Windows.Forms.Label()
		self._timer1 = System.Windows.Forms.Timer(self._components)
		self._groupBox5 = System.Windows.Forms.GroupBox()
		self._radioButton3 = System.Windows.Forms.RadioButton()
		self._syncButton1 = System.Windows.Forms.Button()
		self._syncButton2 = System.Windows.Forms.Button()
		self._clipCheckBox = System.Windows.Forms.CheckBox()
		self._label6 = System.Windows.Forms.Label()
		self._label7 = System.Windows.Forms.Label()
		self._radioButton4 = System.Windows.Forms.RadioButton()
		self._groupBox6 = System.Windows.Forms.GroupBox()
		self._syncLabel2 = System.Windows.Forms.Label()
		self._syncLabel1 = System.Windows.Forms.Label()
		self._hotKey1 = System.Windows.Forms.Button()
		self._miniCheckBox = System.Windows.Forms.CheckBox()
		self._logGroup = System.Windows.Forms.GroupBox()
		self._logBox = System.Windows.Forms.RichTextBox()
		self._compare = System.Windows.Forms.Button()
		self._checkBox1 = System.Windows.Forms.CheckBox()
		self._updateMaskBut = System.Windows.Forms.Button()
		self._maskTip = System.Windows.Forms.ToolTip(self._components)
		self._maskClipBut = System.Windows.Forms.Button()
		self._groupBox1.SuspendLayout()
		self._groupBox2.SuspendLayout()
		self._groupBox3.SuspendLayout()
		self._groupBox4.SuspendLayout()
		self._groupBox5.SuspendLayout()
		self._groupBox6.SuspendLayout()
		self._logGroup.SuspendLayout()
		self.SuspendLayout()
		# 
		# getButton1
		# 
		self._getButton1.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._getButton1.Location = System.Drawing.Point(302, 21)
		self._getButton1.Name = "getButton1"
		self._getButton1.Size = System.Drawing.Size(42, 25)
		self._getButton1.TabIndex = 0
		self._getButton1.Tag = "0"
		self._getButton1.Text = "Get"
		self._getButton1.UseVisualStyleBackColor = True
		self._getButton1.Click += self.GetButtonClick
		# 
		# label1
		# 
		self._label1.Font = System.Drawing.Font("微软雅黑", 10.5, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._label1.Location = System.Drawing.Point(6, 21)
		self._label1.Name = "label1"
		self._label1.Size = System.Drawing.Size(105, 25)
		self._label1.TabIndex = 1
		self._label1.Text = "Project Name"
		self._label1.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# groupBox1
		# 
		self._groupBox1.Controls.Add(self._miniCheckBox)
		self._groupBox1.Controls.Add(self._stateLabel1)
		self._groupBox1.Controls.Add(self._designNameBox1)
		self._groupBox1.Controls.Add(self._swiftButton1)
		self._groupBox1.Controls.Add(self._label2)
		self._groupBox1.Controls.Add(self._projectNameBox1)
		self._groupBox1.Controls.Add(self._getButton1)
		self._groupBox1.Controls.Add(self._label1)
		self._groupBox1.Controls.Add(self._designCombo1)
		self._groupBox1.Controls.Add(self._projectCombo1)
		self._groupBox1.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._groupBox1.Location = System.Drawing.Point(12, 12)
		self._groupBox1.Name = "groupBox1"
		self._groupBox1.Size = System.Drawing.Size(358, 112)
		self._groupBox1.TabIndex = 2
		self._groupBox1.TabStop = False
		self._groupBox1.Text = "操作目标1"
		# 
		# projectNameBox1
		# 
		self._projectNameBox1.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._projectNameBox1.Location = System.Drawing.Point(117, 21)
		self._projectNameBox1.Multiline = True
		self._projectNameBox1.Name = "projectNameBox1"
		self._projectNameBox1.Size = System.Drawing.Size(163, 25)
		self._projectNameBox1.TabIndex = 2
		self._projectNameBox1.Tag = "0"
		self._projectNameBox1.Text = "Null"
		self._projectNameBox1.TextChanged += self.NameKeyIn
		# 
		# designNameBox1
		# 
		self._designNameBox1.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._designNameBox1.Location = System.Drawing.Point(117, 50)
		self._designNameBox1.Multiline = True
		self._designNameBox1.Name = "designNameBox1"
		self._designNameBox1.Size = System.Drawing.Size(163, 25)
		self._designNameBox1.TabIndex = 5
		self._designNameBox1.Tag = "0"
		self._designNameBox1.Text = "Null"
		self._designNameBox1.TextChanged += self.NameKeyIn
		# 
		# swiftButton1
		# 
		self._swiftButton1.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._swiftButton1.Location = System.Drawing.Point(302, 50)
		self._swiftButton1.Name = "swiftButton1"
		self._swiftButton1.Size = System.Drawing.Size(42, 25)
		self._swiftButton1.TabIndex = 3
		self._swiftButton1.Tag = "0"
		self._swiftButton1.Text = "⭕"
		self._swiftButton1.UseVisualStyleBackColor = True
		self._swiftButton1.Click += self.SwiftButtonClick
		# 
		# label2
		# 
		self._label2.Font = System.Drawing.Font("微软雅黑", 10.5, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._label2.Location = System.Drawing.Point(6, 50)
		self._label2.Name = "label2"
		self._label2.Size = System.Drawing.Size(105, 25)
		self._label2.TabIndex = 4
		self._label2.Text = "Design Name"
		self._label2.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# stateLabel1
		# 
		self._stateLabel1.ForeColor = System.Drawing.Color.FromArgb(192, 0, 0)
		self._stateLabel1.Location = System.Drawing.Point(254, 80)
		self._stateLabel1.Name = "stateLabel1"
		self._stateLabel1.Size = System.Drawing.Size(92, 23)
		self._stateLabel1.TabIndex = 6
		self._stateLabel1.Text = "⚫ Not Ready"
		self._stateLabel1.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# designCombo1
		# 
		self._designCombo1.DisplayMember = "1"
		self._designCombo1.FormattingEnabled = True
		self._designCombo1.Location = System.Drawing.Point(117, 50)
		self._designCombo1.Name = "designCombo1"
		self._designCombo1.Size = System.Drawing.Size(179, 25)
		self._designCombo1.TabIndex = 3
		self._designCombo1.Tag = "0"
		self._designCombo1.DropDown += self.DesignSelect
		self._designCombo1.SelectedIndexChanged += self.DesignSelectChange
		# 
		# projectCombo1
		# 
		self._projectCombo1.FormattingEnabled = True
		self._projectCombo1.Location = System.Drawing.Point(117, 21)
		self._projectCombo1.Name = "projectCombo1"
		self._projectCombo1.Size = System.Drawing.Size(179, 25)
		self._projectCombo1.TabIndex = 4
		self._projectCombo1.Tag = "0"
		self._projectCombo1.DropDown += self.ProjectSelect
		self._projectCombo1.SelectedIndexChanged += self.ProjectSelectChange
		# 
		# groupBox2
		# 
		self._groupBox2.Controls.Add(self._stateLabel2)
		self._groupBox2.Controls.Add(self._designNameBox2)
		self._groupBox2.Controls.Add(self._swiftButton2)
		self._groupBox2.Controls.Add(self._label4)
		self._groupBox2.Controls.Add(self._projectNameBox2)
		self._groupBox2.Controls.Add(self._getButton2)
		self._groupBox2.Controls.Add(self._label5)
		self._groupBox2.Controls.Add(self._designCombo2)
		self._groupBox2.Controls.Add(self._projectCombo2)
		self._groupBox2.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._groupBox2.Location = System.Drawing.Point(12, 130)
		self._groupBox2.Name = "groupBox2"
		self._groupBox2.Size = System.Drawing.Size(358, 112)
		self._groupBox2.TabIndex = 7
		self._groupBox2.TabStop = False
		self._groupBox2.Text = "操作目标2"
		# 
		# stateLabel2
		# 
		self._stateLabel2.ForeColor = System.Drawing.Color.FromArgb(192, 0, 0)
		self._stateLabel2.Location = System.Drawing.Point(254, 80)
		self._stateLabel2.Name = "stateLabel2"
		self._stateLabel2.Size = System.Drawing.Size(92, 23)
		self._stateLabel2.TabIndex = 6
		self._stateLabel2.Text = "⚫ Not Ready"
		self._stateLabel2.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# designNameBox2
		# 
		self._designNameBox2.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._designNameBox2.Location = System.Drawing.Point(117, 50)
		self._designNameBox2.Multiline = True
		self._designNameBox2.Name = "designNameBox2"
		self._designNameBox2.Size = System.Drawing.Size(163, 25)
		self._designNameBox2.TabIndex = 5
		self._designNameBox2.Tag = "1"
		self._designNameBox2.Text = "Null"
		self._designNameBox2.TextChanged += self.NameKeyIn
		# 
		# swiftButton2
		# 
		self._swiftButton2.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._swiftButton2.Location = System.Drawing.Point(302, 50)
		self._swiftButton2.Name = "swiftButton2"
		self._swiftButton2.Size = System.Drawing.Size(42, 25)
		self._swiftButton2.TabIndex = 3
		self._swiftButton2.Tag = "1"
		self._swiftButton2.Text = "⭕"
		self._swiftButton2.UseVisualStyleBackColor = True
		self._swiftButton2.Click += self.SwiftButtonClick
		# 
		# label4
		# 
		self._label4.Font = System.Drawing.Font("微软雅黑", 10.5, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._label4.Location = System.Drawing.Point(6, 50)
		self._label4.Name = "label4"
		self._label4.Size = System.Drawing.Size(105, 25)
		self._label4.TabIndex = 4
		self._label4.Text = "Design Name"
		self._label4.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# projectNameBox2
		# 
		self._projectNameBox2.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._projectNameBox2.Location = System.Drawing.Point(117, 21)
		self._projectNameBox2.Multiline = True
		self._projectNameBox2.Name = "projectNameBox2"
		self._projectNameBox2.Size = System.Drawing.Size(163, 25)
		self._projectNameBox2.TabIndex = 2
		self._projectNameBox2.Tag = "1"
		self._projectNameBox2.Text = "Null"
		self._projectNameBox2.TextChanged += self.NameKeyIn
		# 
		# getButton2
		# 
		self._getButton2.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._getButton2.Location = System.Drawing.Point(302, 21)
		self._getButton2.Name = "getButton2"
		self._getButton2.Size = System.Drawing.Size(42, 25)
		self._getButton2.TabIndex = 0
		self._getButton2.Tag = "1"
		self._getButton2.Text = "Get"
		self._getButton2.UseVisualStyleBackColor = True
		self._getButton2.Click += self.GetButtonClick
		# 
		# label5
		# 
		self._label5.Font = System.Drawing.Font("微软雅黑", 10.5, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._label5.Location = System.Drawing.Point(6, 21)
		self._label5.Name = "label5"
		self._label5.Size = System.Drawing.Size(105, 25)
		self._label5.TabIndex = 1
		self._label5.Text = "Project Name"
		self._label5.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# designCombo2
		# 
		self._designCombo2.DisplayMember = "1"
		self._designCombo2.FormattingEnabled = True
		self._designCombo2.Location = System.Drawing.Point(117, 50)
		self._designCombo2.Name = "designCombo2"
		self._designCombo2.Size = System.Drawing.Size(179, 25)
		self._designCombo2.TabIndex = 3
		self._designCombo2.Tag = "1"
		self._designCombo2.DropDown += self.DesignSelect
		self._designCombo2.SelectedIndexChanged += self.DesignSelectChange
		# 
		# projectCombo2
		# 
		self._projectCombo2.FormattingEnabled = True
		self._projectCombo2.Location = System.Drawing.Point(117, 21)
		self._projectCombo2.Name = "projectCombo2"
		self._projectCombo2.Size = System.Drawing.Size(179, 25)
		self._projectCombo2.TabIndex = 4
		self._projectCombo2.Tag = "1"
		self._projectCombo2.DropDown += self.ProjectSelect
		self._projectCombo2.SelectedIndexChanged += self.ProjectSelectChange
		# 
		# groupBox3
		# 
		self._groupBox3.Controls.Add(self._radioButton4)
		self._groupBox3.Controls.Add(self._radioButton3)
		self._groupBox3.Controls.Add(self._radioButton2)
		self._groupBox3.Controls.Add(self._radioButton1)
		self._groupBox3.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._groupBox3.Location = System.Drawing.Point(12, 248)
		self._groupBox3.Name = "groupBox3"
		self._groupBox3.Size = System.Drawing.Size(358, 55)
		self._groupBox3.TabIndex = 8
		self._groupBox3.TabStop = False
		self._groupBox3.Text = "功能选择"
		# 
		# radioButton1
		# 
		self._radioButton1.Checked = True
		self._radioButton1.Location = System.Drawing.Point(13, 22)
		self._radioButton1.Name = "radioButton1"
		self._radioButton1.Size = System.Drawing.Size(104, 24)
		self._radioButton1.TabIndex = 0
		self._radioButton1.TabStop = True
		self._radioButton1.Tag = "save"
		self._radioButton1.Text = "参数保存"
		self._radioButton1.UseVisualStyleBackColor = True
		self._radioButton1.CheckedChanged += self.RadioButtonCheckedChanged
		# 
		# radioButton2
		# 
		self._radioButton2.Location = System.Drawing.Point(95, 22)
		self._radioButton2.Name = "radioButton2"
		self._radioButton2.Size = System.Drawing.Size(104, 24)
		self._radioButton2.TabIndex = 1
		self._radioButton2.Tag = "reload"
		self._radioButton2.Text = "参数读取"
		self._radioButton2.UseVisualStyleBackColor = True
		self._radioButton2.CheckedChanged += self.RadioButtonCheckedChanged
		# 
		# groupBox4
		# 
		self._groupBox4.Controls.Add(self._clipCheckBox)
		self._groupBox4.Controls.Add(self._saveTipLable)
		self._groupBox4.Controls.Add(self._noteLabel)
		self._groupBox4.Controls.Add(self._noteBox)
		self._groupBox4.Controls.Add(self._saveButton)
		self._groupBox4.Controls.Add(self._fileStateLabel)
		self._groupBox4.Controls.Add(self._fileSelectButton)
		self._groupBox4.Controls.Add(self._label3)
		self._groupBox4.Controls.Add(self._fileNameBox)
		self._groupBox4.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._groupBox4.Location = System.Drawing.Point(12, 309)
		self._groupBox4.Name = "groupBox4"
		self._groupBox4.Size = System.Drawing.Size(358, 110)
		self._groupBox4.TabIndex = 9
		self._groupBox4.TabStop = False
		self._groupBox4.Text = "参数保存（目标1）"
		# 
		# openFileDialog1
		# 
		self._openFileDialog1.FileName = "openFileDialog1"
		# 
		# fileNameBox
		# 
		self._fileNameBox.Location = System.Drawing.Point(94, 20)
		self._fileNameBox.Name = "fileNameBox"
		self._fileNameBox.Size = System.Drawing.Size(204, 23)
		self._fileNameBox.TabIndex = 0
		self._fileNameBox.TextChanged += self.FileNameBoxTextChanged
		self._fileNameBox.DoubleClick += self.FileNameBoxDoubleClick
		# 
		# label3
		# 
		self._label3.Font = System.Drawing.Font("微软雅黑", 10.5, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._label3.Location = System.Drawing.Point(8, 20)
		self._label3.Name = "label3"
		self._label3.Size = System.Drawing.Size(80, 23)
		self._label3.TabIndex = 5
		self._label3.Text = "File Name"
		self._label3.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# fileSelectButton
		# 
		self._fileSelectButton.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 0)
		self._fileSelectButton.Location = System.Drawing.Point(304, 20)
		self._fileSelectButton.Name = "fileSelectButton"
		self._fileSelectButton.Size = System.Drawing.Size(42, 23)
		self._fileSelectButton.TabIndex = 7
		self._fileSelectButton.Tag = "1"
		self._fileSelectButton.Text = "···"
		self._fileSelectButton.UseVisualStyleBackColor = True
		self._fileSelectButton.Click += self.FileSelectButtonClick
		# 
		# fileStateLabel
		# 
		self._fileStateLabel.ForeColor = System.Drawing.Color.FromArgb(192, 0, 0)
		self._fileStateLabel.Location = System.Drawing.Point(225, 78)
		self._fileStateLabel.Name = "fileStateLabel"
		self._fileStateLabel.Size = System.Drawing.Size(123, 23)
		self._fileStateLabel.TabIndex = 7
		self._fileStateLabel.Text = "⚫ File not Ready"
		self._fileStateLabel.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# saveButton
		# 
		self._saveButton.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 134)
		self._saveButton.Location = System.Drawing.Point(240, 51)
		self._saveButton.Name = "saveButton"
		self._saveButton.Size = System.Drawing.Size(106, 23)
		self._saveButton.TabIndex = 8
		self._saveButton.Text = "SAVE!"
		self._saveButton.UseVisualStyleBackColor = True
		self._saveButton.Click += self.SaveButtonClick
		# 
		# noteBox
		# 
		self._noteBox.Location = System.Drawing.Point(94, 51)
		self._noteBox.Name = "noteBox"
		self._noteBox.Size = System.Drawing.Size(140, 23)
		self._noteBox.TabIndex = 9
		# 
		# noteLabel
		# 
		self._noteLabel.Font = System.Drawing.Font("微软雅黑", 10.5, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._noteLabel.Location = System.Drawing.Point(8, 51)
		self._noteLabel.Name = "noteLabel"
		self._noteLabel.Size = System.Drawing.Size(80, 23)
		self._noteLabel.TabIndex = 10
		self._noteLabel.Text = "Note"
		self._noteLabel.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# saveTipLable
		# 
		self._saveTipLable.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._saveTipLable.ForeColor = System.Drawing.Color.Green
		self._saveTipLable.Location = System.Drawing.Point(14, 81)
		self._saveTipLable.Name = "saveTipLable"
		self._saveTipLable.Size = System.Drawing.Size(220, 20)
		self._saveTipLable.TabIndex = 11
		self._saveTipLable.TextAlign = System.Drawing.ContentAlignment.MiddleRight
		# 
		# timer1
		# 
		self._timer1.Interval = 2000
		self._timer1.Tick += self.Timer1Tick
		# 
		# groupBox5
		# 
		self._groupBox5.Controls.Add(self._syncLabel1)
		self._groupBox5.Controls.Add(self._syncLabel2)
		self._groupBox5.Controls.Add(self._label7)
		self._groupBox5.Controls.Add(self._label6)
		self._groupBox5.Controls.Add(self._syncButton2)
		self._groupBox5.Controls.Add(self._syncButton1)
		self._groupBox5.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._groupBox5.Location = System.Drawing.Point(392, 12)
		self._groupBox5.Name = "groupBox5"
		self._groupBox5.Size = System.Drawing.Size(360, 110)
		self._groupBox5.TabIndex = 10
		self._groupBox5.TabStop = False
		self._groupBox5.Text = "参数同步（目标1⇔目标2）"
		self._groupBox5.Visible = False
		# 
		# radioButton3
		# 
		self._radioButton3.Location = System.Drawing.Point(177, 22)
		self._radioButton3.Name = "radioButton3"
		self._radioButton3.Size = System.Drawing.Size(104, 24)
		self._radioButton3.TabIndex = 2
		self._radioButton3.Tag = "sync"
		self._radioButton3.Text = "参数同步"
		self._radioButton3.UseVisualStyleBackColor = True
		self._radioButton3.CheckedChanged += self.RadioButtonCheckedChanged
		# 
		# syncButton1
		# 
		self._syncButton1.Font = System.Drawing.Font("微软雅黑", 12, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 134)
		self._syncButton1.Location = System.Drawing.Point(128, 29)
		self._syncButton1.Name = "syncButton1"
		self._syncButton1.Size = System.Drawing.Size(95, 28)
		self._syncButton1.TabIndex = 0
		self._syncButton1.Tag = "1"
		self._syncButton1.Text = "→"
		self._syncButton1.UseVisualStyleBackColor = True
		self._syncButton1.Click += self.SyncButtonClick
		# 
		# syncButton2
		# 
		self._syncButton2.Font = System.Drawing.Font("微软雅黑", 12, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, 134)
		self._syncButton2.Location = System.Drawing.Point(128, 63)
		self._syncButton2.Name = "syncButton2"
		self._syncButton2.Size = System.Drawing.Size(95, 28)
		self._syncButton2.TabIndex = 0
		self._syncButton2.Tag = "2"
		self._syncButton2.Text = "←"
		self._syncButton2.UseVisualStyleBackColor = True
		self._syncButton2.Click += self.SyncButtonClick
		# 
		# clipCheckBox
		# 
		self._clipCheckBox.Location = System.Drawing.Point(13, 81)
		self._clipCheckBox.Name = "clipCheckBox"
		self._clipCheckBox.Size = System.Drawing.Size(105, 24)
		self._clipCheckBox.TabIndex = 12
		self._clipCheckBox.Text = "仅剪切板"
		self._clipCheckBox.UseVisualStyleBackColor = True
		# 
		# label6
		# 
		self._label6.Font = System.Drawing.Font("微软雅黑", 15, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._label6.Location = System.Drawing.Point(30, 39)
		self._label6.Name = "label6"
		self._label6.Size = System.Drawing.Size(68, 39)
		self._label6.TabIndex = 1
		self._label6.Text = "目标1"
		self._label6.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# label7
		# 
		self._label7.Font = System.Drawing.Font("微软雅黑", 15, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._label7.Location = System.Drawing.Point(259, 39)
		self._label7.Name = "label7"
		self._label7.Size = System.Drawing.Size(68, 39)
		self._label7.TabIndex = 1
		self._label7.Text = "目标2"
		self._label7.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# radioButton4
		# 
		self._radioButton4.Location = System.Drawing.Point(258, 22)
		self._radioButton4.Name = "radioButton4"
		self._radioButton4.Size = System.Drawing.Size(88, 24)
		self._radioButton4.TabIndex = 3
		self._radioButton4.TabStop = True
		self._radioButton4.Tag = "custom"
		self._radioButton4.Text = "自定义脚本"
		self._radioButton4.UseVisualStyleBackColor = True
		self._radioButton4.CheckedChanged += self.RadioButtonCheckedChanged
		# 
		# groupBox6
		# 
		self._groupBox6.Controls.Add(self._maskClipBut)
		self._groupBox6.Controls.Add(self._updateMaskBut)
		self._groupBox6.Controls.Add(self._checkBox1)
		self._groupBox6.Controls.Add(self._compare)
		self._groupBox6.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._groupBox6.Location = System.Drawing.Point(392, 130)
		self._groupBox6.Name = "groupBox6"
		self._groupBox6.Size = System.Drawing.Size(360, 110)
		self._groupBox6.TabIndex = 11
		self._groupBox6.TabStop = False
		self._groupBox6.Text = "自定义脚本"
		self._groupBox6.Visible = False
		# 
		# syncLabel2
		# 
		self._syncLabel2.ForeColor = System.Drawing.Color.Green
		self._syncLabel2.Location = System.Drawing.Point(237, 69)
		self._syncLabel2.Name = "syncLabel2"
		self._syncLabel2.Size = System.Drawing.Size(117, 23)
		self._syncLabel2.TabIndex = 8
		self._syncLabel2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# syncLabel1
		# 
		self._syncLabel1.ForeColor = System.Drawing.Color.Green
		self._syncLabel1.Location = System.Drawing.Point(6, 69)
		self._syncLabel1.Name = "syncLabel1"
		self._syncLabel1.Size = System.Drawing.Size(116, 23)
		self._syncLabel1.TabIndex = 8
		self._syncLabel1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
		# 
		# hotKey1
		# 
		self._hotKey1.Location = System.Drawing.Point(786, 22)
		self._hotKey1.Name = "hotKey1"
		self._hotKey1.Size = System.Drawing.Size(99, 23)
		self._hotKey1.TabIndex = 12
		self._hotKey1.Tag = "0"
		self._hotKey1.Text = "quickSave(&s)"
		self._hotKey1.UseVisualStyleBackColor = True
		self._hotKey1.Click += self.HotKey1Click
		# 
		# miniCheckBox
		# 
		self._miniCheckBox.Location = System.Drawing.Point(14, 82)
		self._miniCheckBox.Name = "miniCheckBox"
		self._miniCheckBox.Size = System.Drawing.Size(104, 24)
		self._miniCheckBox.TabIndex = 7
		self._miniCheckBox.Text = "Mini Mode"
		self._miniCheckBox.UseVisualStyleBackColor = True
		self._miniCheckBox.CheckedChanged += self.MiniCheckBoxCheckedChanged
		# 
		# logGroup
		# 
		self._logGroup.Controls.Add(self._logBox)
		self._logGroup.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._logGroup.Location = System.Drawing.Point(12, 425)
		self._logGroup.Name = "logGroup"
		self._logGroup.Size = System.Drawing.Size(358, 114)
		self._logGroup.TabIndex = 12
		self._logGroup.TabStop = False
		self._logGroup.Text = "Output"
		# 
		# logBox
		# 
		self._logBox.Location = System.Drawing.Point(13, 22)
		self._logBox.Name = "logBox"
		self._logBox.ReadOnly = True
		self._logBox.Size = System.Drawing.Size(331, 82)
		self._logBox.TabIndex = 0
		self._logBox.Text = ""
		# 
		# compare
		# 
		self._compare.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._compare.Location = System.Drawing.Point(174, 23)
		self._compare.Name = "compare"
		self._compare.Size = System.Drawing.Size(93, 25)
		self._compare.TabIndex = 1
		self._compare.Tag = "0"
		self._compare.Text = "COMPARE"
		self._compare.UseVisualStyleBackColor = True
		self._compare.Click += self.Compare
		# 
		# checkBox1
		# 
		self._checkBox1.Checked = True
		self._checkBox1.CheckState = System.Windows.Forms.CheckState.Checked
		self._checkBox1.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Underline, System.Drawing.GraphicsUnit.Point, 134)
		self._checkBox1.Location = System.Drawing.Point(16, 23)
		self._checkBox1.Name = "checkBox1"
		self._checkBox1.Size = System.Drawing.Size(62, 24)
		self._checkBox1.TabIndex = 2
		self._checkBox1.Text = "Mask"
		self._checkBox1.UseVisualStyleBackColor = True
		self._checkBox1.MouseEnter += self.ShowMask
		# 
		# updateMaskBut
		# 
		self._updateMaskBut.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._updateMaskBut.Location = System.Drawing.Point(75, 23)
		self._updateMaskBut.Name = "updateMaskBut"
		self._updateMaskBut.Size = System.Drawing.Size(93, 25)
		self._updateMaskBut.TabIndex = 3
		self._updateMaskBut.Tag = "0"
		self._updateMaskBut.Text = "更新Mask"
		self._updateMaskBut.UseVisualStyleBackColor = True
		self._updateMaskBut.Click += self.UpdateClick
		# 
		# maskClipBut
		# 
		self._maskClipBut.Font = System.Drawing.Font("微软雅黑", 9, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, 134)
		self._maskClipBut.Location = System.Drawing.Point(174, 78)
		self._maskClipBut.Name = "maskClipBut"
		self._maskClipBut.Size = System.Drawing.Size(93, 25)
		self._maskClipBut.TabIndex = 4
		self._maskClipBut.Tag = "0"
		self._maskClipBut.Text = "Mask Clip"
		self._maskClipBut.UseVisualStyleBackColor = True
		self._maskClipBut.Click += self.MaskClip
		# 
		# MainForm
		# 
		self.ClientSize = System.Drawing.Size(913, 551)
		self.Controls.Add(self._logGroup)
		self.Controls.Add(self._hotKey1)
		self.Controls.Add(self._groupBox6)
		self.Controls.Add(self._groupBox5)
		self.Controls.Add(self._groupBox4)
		self.Controls.Add(self._groupBox3)
		self.Controls.Add(self._groupBox2)
		self.Controls.Add(self._groupBox1)
		self.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog
		self.MaximizeBox = False
		self.Name = "MainForm"
		self.StartPosition = System.Windows.Forms.FormStartPosition.Manual
		self.Text = "HFSS Toolbox"
		self.TopMost = True
		self.Click += self.UpdateClick
		self._groupBox1.ResumeLayout(False)
		self._groupBox1.PerformLayout()
		self._groupBox2.ResumeLayout(False)
		self._groupBox2.PerformLayout()
		self._groupBox3.ResumeLayout(False)
		self._groupBox4.ResumeLayout(False)
		self._groupBox4.PerformLayout()
		self._groupBox5.ResumeLayout(False)
		self._groupBox6.ResumeLayout(False)
		self._logGroup.ResumeLayout(False)
		self.ResumeLayout(False)
		
	def ConfigFormater(self, str):	#配置文件读取器
		nlines = [ "" if s[0]=="#" else s for s in str]
		
		loop = True
		while loop:
			try:
				nlines.remove("\n")
			except:
				loop = False
		
		loop = True
		while loop:
			try:
				nlines.remove("")
			except:
				loop = False
		
		clist = "{"+",".join(nlines)+"}"
		cdict = dict(eval(clist))
		return cdict

	def NotReady(self, n):
		self.State[n] = False
		self._stateLabel[n].ForeColor = System.Drawing.Color.FromArgb(192, 0, 0)
		self._stateLabel[n].Text = "⚫ Not Ready"
		
	def Ready(self, n):
		self.State[n] = True
		self._stateLabel[n].ForeColor = System.Drawing.Color.Green
		self._stateLabel[n].Text = "⚫ Ready"
		
	def FileNotReady(self):
		self.FileState = False
		self._fileStateLabel.ForeColor = System.Drawing.Color.FromArgb(192, 0, 0)
		self._fileStateLabel.Text = "⚫ File not Ready"
	
	def FileReady(self):
		self.FileState = True
		self._fileStateLabel.ForeColor = System.Drawing.Color.Green
		self._fileStateLabel.Text = "⚫ File Ready"
	
	def DebugInfo(self, istr):
		if not self.debug:
			return
		self.AddInfoMessage("[Info-" + str(self.infoNum) + "]" + istr)
		self.infoNum +=1
	
	def LogGen(self, text, type):
		self._logBox.SelectionStart = self._logBox.TextLength;
		self._logBox.SelectionLength = 0;
		self._logBox.SelectionColor = type.color
		self._logBox.AppendText('[' + self.time_gen('%H:%M:%S') + ']' + type.headtext + ' ' + text + '\n');
		self._logBox.SelectionColor = self._logBox.ForeColor;
		self._logBox.ScrollToCaret()
	
	def GetButtonClick(self, sender, e):
		n = int(sender.Tag)
		self.NotReady(n)
		
		#1，查找Project名称
		self.oProject[n] = self.oDesktop.GetActiveProject()
		if self.oProject[n] == None:
			self._projectNameBox[n].Text = "No Active Project Found!"
			return
		else:
			self._projectNameBox[n].Text = self.oProject[n].GetName()
			self.oDesign[n] = self.oProject[n].GetActiveDesign()
		
		#2，查找Design名称
		if self.oDesign[n] == None:
			self._designNameBox[n].Text = "No Active Design Found!"
			return
		else:
			self._designNameBox[n].Text = self.oDesign[n].GetName()
			self.oEditor[n] = self.oDesign[n].SetActiveEditor("3D Modeler")
		
		#3，判断是否准备好
		if self.oEditor[n] != None:
			self.Ready(n)
			
	def NameKeyIn(self, sender, e):
		n = int(sender.Tag)
		self.NotReady(n)
		
		#1，检查Project名称
		pList = self.ProjectUpdate(n)
		if (self._projectNameBox[n].Text in pList):
			try:
				self.oProject[n] = self.oDesktop.SetActiveProject(self._projectNameBox[n].Text)
			except:
				return
		else:
			return
		
		#2，检查Design名称
		dList = self.DesignUpdate(n)
		if (self._designNameBox[n].Text in dList):
			try:
				self.oDesign[n] = self.oProject[n].SetActiveDesign(self._designNameBox[n].Text)
			except:
				return
		else:
			return

		self.oEditor[n] = self.oDesign[n].SetActiveEditor("3D Modeler")
		
		#3，判断是否准备好
		if self.oEditor[n] != None:
			self.Ready(n)
	
	def ProjectUpdate(self, n):	#更新项目下拉列表
		self._projectCombo[n].Items.Clear()
		projectList = self.oDesktop.GetProjects()
		if projectList == []:
			return []
		projectNameList = [ p.GetName() for p in projectList ]
		projectNameList.sort()
		projectArray = System.Array[System.Object](projectNameList)
		self._projectCombo[n].Items.AddRange(projectArray)
		#self.projectCombo.SelectedIndex = 0 #不可用！防止循环触发！
		
		#self.DebugInfo("ProjectUpdate")
		return projectNameList
		
	def ProjectSelect(self, sender, e):
		n = int(sender.Tag)
		try:
			self.ProjectUpdate(n)
		except:
			return
		
	def ProjectSelectChange(self, sender, e):
		n = int(sender.Tag)
		if (self._projectNameBox[n].Text == self._projectCombo[n].SelectedItem):	#选择的是一样的，故不动
			return
		
		self.NotReady(n)
		
		if(self.ProjectUpdate != []):
			self.oProject[n] = self.oDesktop.SetActiveProject(self._projectCombo[n].SelectedItem)					
		else:
			return
		self._projectNameBox[n].Text = self._projectCombo[n].SelectedItem
		self._designNameBox[n].Text = "No Active Design Found!"	#未选择design		
		
		#尝试选中一个design
		if (self.DesignUpdate(n) != []):
			self._designCombo[n].SelectedIndex = 0
		else:
			return
		#self.oDesign = self.oProject.SetActiveDesign(self._designCombo.SelectedItem)	#不需要，回调函数自动触发
		
		#self.DebugInfo("ProjectSelectChange")
		
	def DesignUpdate(self, n):		#更新Design下拉列表
		self._designCombo[n].Items.Clear()		
		designList = self.oProject[n].GetDesigns()
		if designList == []:
			return []
		designNameList = [ d.GetName() for d in designList ]
		designNameList.sort()
		designArray = System.Array[System.Object](designNameList)
		self._designCombo[n].Items.AddRange(designArray)
		#self.designCombo.SelectedIndex = 0	#不可用！防止循环触发！
		
		#self.DebugInfo("DesignUpdate")
		return designNameList
	
	def DesignSelect(self, sender, e):
		n = int(sender.Tag)
		
		try:
			self.DesignUpdate(n)
		except:
			return
		
	def DesignSelectChange(self, sender, e):
		n = int(sender.Tag)
		if( self._designNameBox[n].Text == self._designCombo[n].SelectedItem):	#选择的是一样的，故不动
			return
		
		self.NotReady(n)
		
		if(self.DesignUpdate != []):
			self.oDesign[n] = self.oProject[n].SetActiveDesign(self._designCombo[n].SelectedItem)			
		else:
			return
		
		#如果没有出错
		self._designNameBox[n].Text = self._designCombo[n].SelectedItem
		#self.oEditor[n] = self.oDesign[n].SetActiveEditor("3D Modeler")
		
		#判断是否准备好
		#if self.oEditor[n] != None:
		#	self.Ready(n)
		
		#self.DebugInfo("DesignSelectChange")
	
	def SwiftButtonClick(self, sender, e):
		n = int(sender.Tag)
		try:
			dList = self.DesignUpdate(n)
		except:
			return
		if len(dList) == 0:
			return
		try:
			nd = dList.index(self._designNameBox[n].Text)
		except:
			nd = -1
		
		self._designNameBox[n].Text = dList[(nd+1) % len(dList)]
		
		pass
	
	def GetSelectFun(self):
		cList = [rb.Checked for rb in self._funRadioButton]
		funindex = cList.index(True)
		funstr = self._funRadioButton[funindex].Tag
		return funstr

	def FileSelectButtonClick(self, sender, e):		
		if self._openFileDialog1.ShowDialog() == DialogResult.OK:
			self._fileNameBox.Text = self._openFileDialog1.FileName
		pass

	def FileNameBoxTextChanged(self, sender, e):
		self.FileNotReady()
		if (os.path.exists(self._fileNameBox.Text)):
			self.FileReady()
		pass

	def SaveButtonClick(self, sender, e):
		clip = self._clipCheckBox.Checked
		if self.SOR == 'save':
			self.SaveOrLoad('save', 0, self._fileNameBox.Text, self._noteBox.Text, clip)
		else:
			rn = 0	#防止剪切板选中时出错
			if not clip:
				try:
					rn = int(self._noteBox.Text)
				except:
					self.LogGen('请输入正确的参数编号！', LogType.Error)
					return					
			self.SaveOrLoad('reload', 0, self._fileNameBox.Text, "", clip, rn)
		pass
	
	def time_gen(self, format_string = "%Y-%m-%d %H:%M:%S"):	#时间序列生成器
	    time_array = time.localtime(time.time())
	    other_style_time = time.strftime(format_string, time_array)
	    return other_style_time
	
	def SaveOrLoad(self, sor, n, path, note, clip=False, reload_number=1):
		if not self.State[n]:	#项目状态不对直接返回
			self.LogGen('项目信息状态错误！', LogType.Error)
			return
		
		project_name = self._projectNameBox[n].Text
		design_name = self._designNameBox[n].Text
		
		prop_list = self.oEditor[n].GetProperties("LocalVariableTab","LocalVariables")#获取 参数名称 列表
		value_list = [self.oDesign[n].GetPropertyValue("LocalVariableTab","LocalVariables",prop) for prop in prop_list]#获取 参数值 列表
		prop_dict = dict(zip(prop_list,value_list))
		
		if sor == 'save':	#开始保存
			if not clip:	#若没有选中保存到剪切板，则检查文件状态			
				if not self.FileState:	#文件状态不对就返回
					self.LogGen('文件状态错误！', LogType.Error)
					return
				
				f = open(path,'ra+')
				lines = f.readlines()
				
				if(len(lines)):
					n = len(lines)/2
				else:
					n = 0
			
				mark_str = '#' + str(int(n+1)) + '\t' + self.time_gen() + '\t' + project_name + '\t' + design_name + '\t' + note	#说明文字，实际上没用
				f.write(mark_str + '\n')
				f.write(str(prop_dict) + '\n')
				f.close()
				Clipboard.SetText(mark_str + '\r\n' + str(prop_dict))
				self.LogGen(str(len(prop_list)) + "个参数已保存!" + " [编号#" + str(int(n+1)) + "]", LogType.Info)
			else:
				mark_str = '#' + 'Null' + '\t' + self.time_gen() + '\t' + project_name + '\t' + design_name + '\t' + note	#只保存到剪切板时
				Clipboard.SetText(mark_str + '\r\n' + str(prop_dict))
				self.LogGen(str(len(prop_list)) + "个参数已保存到剪切板!", LogType.Info)			
			
		if sor == 'reload':	#读取
			
			if not clip:
				if not self.FileState:	#文件状态不对就返回
					self.LogGen('文件状态错误！', LogType.Error)
					return
				f = open(path,'r')
				lines = f.readlines()
				f.close()
				try:
					reload_line = lines[reload_number*2-1]
				except:
					#self._saveTipLable.ForeColor = System.Drawing.Color.FromArgb(192, 0, 0)
					#self._saveTipLable.Text = "[Warning]数据不存在!"
					#self._timer1.Enabled = True
					self.LogGen('数据不存在!',LogType.Error)
					return
			else:
				reload_line = Clipboard.GetText()
			
			try:
				reload_line = reload_line[reload_line.index('{'):]	#去除无用信息
				reload_line_temp = reload_line
				reload_line = reload_line.replace("’","'").replace("‘","'")
				if not reload_line == reload_line_temp:
					self.LogGen('输入存在中文引号！请注意！',LogType.Warning)
				reload_dict = dict(eval(reload_line))
			except:
				#self._saveTipLable.ForeColor = System.Drawing.Color.FromArgb(192, 0, 0)
				#self._saveTipLable.Text = "[Warning]数据格式错误!"
				#self._timer1.Enabled = True
				self.LogGen('数据格式错误!',LogType.Error)
				return
			reload_porp_list = reload_dict.keys()
			reload_porp_value = reload_dict.values()
			load_prop = str(len(reload_porp_list))	#读取到参数数量
			
			#写入
			prop_same = set(prop_list).intersection(set(reload_porp_list))
			prop_same_list = list(prop_same)
			same_prop = len(prop_same_list)		#相同参数数量
			nonset_prop = 0
			
			for prop in prop_same_list:	#循环设置参数
				if prop_dict[prop] == reload_dict[prop]:	#不一样的才设置
					nonset_prop += 1
					continue
				self.oDesign[n].SetPropertyValue("LocalVariableTab","LocalVariables",prop,reload_dict[prop])
			
			self.LogGen("回滚完成！同名" + str(same_prop) + "个，回滚" + str(same_prop - nonset_prop) + "个，相同" + str(nonset_prop) + "个",LogType.Info)
		pass
	
	def RadioButtonCheckedChanged(self, sender, e):
		tag = str(sender.Tag)
		
		if tag == 'save':
			self._groupBox4.Visible = True
			self._groupBox5.Visible = False
			self._groupBox6.Visible = False
			self.SOR = 'save'
			#self._clipCheckBox.Visible = False
			self._clipCheckBox.Text = '仅剪切板'
			self._noteLabel.Text = "Note"
			self._saveButton.Text = "SAVE!"
			self._groupBox4.Text = "参数保存（目标1）"
			self._noteBox.Text = ""
		
		if tag == 'reload':
			self._groupBox4.Visible = True
			self._groupBox5.Visible = False
			self._groupBox6.Visible = False
			self.SOR = 'reload'
			#self._clipCheckBox.Visible = True
			self._clipCheckBox.Text = '从剪切板'
			self._noteLabel.Text = "Reload #"
			self._saveButton.Text = "Reload"
			self._groupBox4.Text = "参数回滚（目标1）"
			self._noteBox.Text = ""
			
		if tag == 'sync':
			self._groupBox4.Visible = False
			self._groupBox5.Visible = True
			self._groupBox6.Visible = False
			
		if tag == 'custom':
			self._groupBox4.Visible = False
			self._groupBox5.Visible = False
			self._groupBox6.Visible = True
			
		pass

	def Timer1Tick(self, sender, e):
		#---------------save部分-------------------
		self._saveTipLable.Text = ""
		self._saveTipLable.ForeColor = System.Drawing.Color.Green
		
		#---------------sync部分-------------------
		self._syncLabel1.Text = ""
		self._syncLabel2.Text = ""
		
		#--------------定时器关闭-------------------
		self._timer1.Enabled = False

	def PropSync(self, direction=1):
		if not(self.State[0] and self.State[1]):	#两个项目都要准备好
			return
		
		prop_list1 = self.oEditor[0].GetProperties("LocalVariableTab","LocalVariables")#获取参数列表1
		prop_list2 = self.oEditor[1].GetProperties("LocalVariableTab","LocalVariables")#获取参数列表2
		
		prop_same = set(prop_list1).intersection(set(prop_list2))
		prop_same_list = list(prop_same)
		
		for prop in prop_same_list:
			if direction == 1:
				p1 = self.oDesign[0].GetPropertyValue("LocalVariableTab","LocalVariables",prop)
				#####一样的不同步
				self.oDesign[1].SetPropertyValue("LocalVariableTab","LocalVariables",prop,p1)
			else:
				p2 = self.oDesign[1].GetPropertyValue("LocalVariableTab","LocalVariables",prop)
				self.oDesign[0].SetPropertyValue("LocalVariableTab","LocalVariables",prop,p2)
		
		if direction == 1:
			self._syncLabel2.Text = "已同步" + str(len(prop_same_list)) + "个参数"
			self._timer1.Enabled = True
		else:
			self._syncLabel1.Text = "已同步" + str(len(prop_same_list)) + "个参数"
			self._timer1.Enabled = True
		
		pass

	def SyncButtonClick(self, sender, e):
		dirn = int(sender.Tag)
		self.PropSync(dirn)
		pass

	def FileNameBoxDoubleClick(self, sender, e):
		if not self.State[0]:
			return
		self._fileNameBox.Text = self.defaulPath + self.oProject[0].GetName() + ".txt"
		pass

	def HotKey1Click(self, sender, e):
		self.GetButtonClick(sender, e)
		self.FileNameBoxDoubleClick(sender, e)
		self.SaveOrLoad('save', 0, self._fileNameBox.Text, self._noteBox.Text)
		pass

	def MiniCheckBoxCheckedChanged(self, sender, e):
		if(self._miniCheckBox.Checked):
			ts = TempSender()
			ts.Tag = self.miniModeFunc
			self.RadioButtonCheckedChanged(ts, e)
			self._groupBox4.Location = System.Drawing.Point(12, 130)
			self._groupBox2.Visible = False
			self.ClientSize = System.Drawing.Size(382, 250)
		else:
			ts = TempSender()
			ts.Tag = self.GetSelectFun()
			self.RadioButtonCheckedChanged(ts, e)
			self._groupBox4.Location = System.Drawing.Point(12, 309)
			self._groupBox2.Visible = True
			self.ClientSize = self.defaultSize
		pass
	
	def Compare(self, sender, e):
		if not(self.State[0] and self.State[1]):	#两个项目都要准备好
			self.LogGen('项目信息状态错误！', LogType.Error)
			return
		
		prop_list1 = self.oEditor[0].GetProperties("LocalVariableTab","LocalVariables")#获取参数列表1
		prop_list2 = self.oEditor[1].GetProperties("LocalVariableTab","LocalVariables")#获取参数列表2		
							
		self.LogGen('开始比较:',LogType.Info)
				
		prop_same1 = set(prop_list1).intersection(set(self.globalmask))
		prop_same2 = set(prop_list2).intersection(set(self.globalmask))
		prop_same = set(prop_same1).intersection(set(prop_same2))
		if (not len(prop_same) == len(prop_same1)) or (not len(prop_same) == len(prop_same2)):
			self.LogGen('有不共同的参数没有同步',LogType.Warning)
		
		prop_same_list = list(prop_same)
		for prop in prop_same_list:	#循环比较参数
			p1 = self.oDesign[0].GetPropertyValue("LocalVariableTab","LocalVariables",prop)
			p2 = self.oDesign[1].GetPropertyValue("LocalVariableTab","LocalVariables",prop)
			if not p1 == p2:
				self.LogGen(prop + "不一样，目标1为" + p1 + "，目标2为" + p2 ,LogType.Info)
		
		pass

	def UpdateClick(self, sender, e):
		prop_mask = Clipboard.GetText()
		try:
				prop_mask = prop_mask[prop_mask.index('{'):]	#去除无用信息
				prop_mask_dict = dict(eval(prop_mask))
				self.globalmask = prop_mask_dict.keys()
				self.globalmask.sort()
		except:
				self.LogGen('Mask格式错误，更新失败',LogType.Error)
				return
		
		self.GenMaskText()
		self.LogGen('Mask已更新',LogType.Info)
		
		pass
	
	def GenMaskText(self):
		self.masktext = "Mask：\n"
		for prop in self.globalmask:
			self.masktext += prop + "\n"
		pass
	
	def ShowMask(self, sender, e):
		self._maskTip.Show(self.masktext, sender, 5000)
		pass
	
	def MaskClip(self, sender, e):
		reload_line = Clipboard.GetText()
			
		try:
			reload_line = reload_line[reload_line.index('{'):]	#去除无用信息
			reload_line_temp = reload_line
			reload_line = reload_line.replace("’","'").replace("‘","'")
			if not reload_line == reload_line_temp:
				self.LogGen('输入存在中文引号！请注意！',LogType.Warning)
			reload_dict = dict(eval(reload_line))
			reload_name = reload_dict.keys()
		except:
			self.LogGen('数据格式错误!',LogType.Error)
			return
		
		prop_same = set(reload_name).intersection(set(self.globalmask))
		
		same_dict = {key:value for key, value in reload_dict.items() if key in prop_same}
		
		Clipboard.SetText(str(same_dict))
		
		self.LogGen('已应用Mask到剪切板',LogType.Info)
		
		pass
