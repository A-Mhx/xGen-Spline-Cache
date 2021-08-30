import maya.cmds as cmds
import maya.mel as mel
import re
import os, sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QLabel, QWidget, QToolBox, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QSpinBox, QCheckBox, QMessageBox, QTabWidget, QGridLayout, QScrollArea



def createCache(descriptionList, nameList, start, end, prefix, version, path):
    os.chdir(path)
    print("Current working direction : %s" % os.getcwd())
    print("Current selection : " + str(descriptionList) + "\n")

    cacheList = []

    i = 0
    for obj in descriptionList:
        cmds.select( obj)
        description = cmds.ls( sl=True) [0]

        obj_cache = "-obj " + str(description)

        obj_name = nameList[i]

        save_name = path + prefix + '_' + obj_name + version + ".abc"
        print("Current cache : " + save_name)

        command = "-frameRange " + start + " " + end + " " + obj_cache + " -file " + save_name

        cmds.xgmSplineCache( create=True, j=command)

        cache_name = save_name.replace( path, '')
        print(cache_name)
        cacheList.append( cache_name)

        i += 1

        print("DONE : Cache " + str(description) + "\n")

    return(cacheList)


class MyWindowWidget(QTabWidget):

    def __init__(self, *args, **kwargs):
        super(MyWindowWidget, self).__init__(*args, **kwargs)

        self.setWindowTitle("Create XGen Spline Cache")
        self.setMinimumSize(500, 425)

        self.tab1 = QWidget()
        self.addTab(self.tab1,"Settings")
        self.tab1UI()

        self.tab2 = QWidget()
        self.addTab(self.tab2,"Rename")
        self.tab2UI()


    def tab1UI(self):
        #Create widgets
        self.__tool_box_descriptions = QToolBox(parent=self)

        self.__cb_all_descriptions = QCheckBox("Cache all Descriptions", self)
        self.__cb_selection = QCheckBox("Cache from Selection", self)

        self.__tool_box_frames = QToolBox(parent=self)

        self.__cb_time_slider = QCheckBox("Cache from Time Slider", self)
        self.__cb_single_frame = QCheckBox("Cache from Single Frame : ", self)
        self.__textfield_single_frame = QLineEdit(self)
        self.__cb_start_end = QCheckBox("Cache from Start/End : ", self)
        self.__cb_start = QLabel("Start : ", self)
        self.__textfield_start = QLineEdit(self)
        self.__cb_end = QLabel("End : ", self)
        self.__textfield_end = QLineEdit(self)

        self.__prefix = QLabel("Prefix : ", self)
        self.__textfield_prefix = QLineEdit(self)
        self.__cb_version = QCheckBox("Version : ", self)
        self.__sp_version = QSpinBox(self)

        self.__path = QLabel("Path : ", self)
        self.__textfield_path = QLineEdit(self)
        self.__btn_choose_path = QPushButton("Choose Path", self)

        self.__btn_create_cache = QPushButton("Create Cache", self)


        #Set default behaviour of widgets
        current_frame = str(int(cmds.currentTime( q=True)))
        self.__textfield_single_frame.setText( current_frame)

        start_time = str(int(cmds.playbackOptions( q=True, min=True)))
        self.__textfield_start.setText( start_time)
        end_time = str(int(cmds.playbackOptions( q=True, max=True)))
        self.__textfield_end.setText( end_time)

        file = cmds.file( q=True, sn=True, shn=True)
        file_name = file.replace( '.ma', '')
        file_name = file_name.replace( '.mb', '')

        self.__textfield_prefix.setText( file_name)

        self.__sp_version.setValue(1)

        path_name = cmds.file( q=True, sn=True)
        path_name = path_name.replace( file, '')
        path_name = path_name.replace( 'scenes', 'cache')

        self.__textfield_path.setText( path_name)


        #Param layouts
        param_descriptions = QWidget()
        descriptions_layout = QVBoxLayout(param_descriptions)
        descriptions_layout.setSpacing(10)
        descriptions_layout.setContentsMargins(10, 10, 10, 10)
        descriptions_layout.addWidget(self.__cb_all_descriptions)
        descriptions_layout.addWidget(self.__cb_selection)

        self.__tool_box_descriptions.addItem(param_descriptions, "XGen Descriptions")

        param_current_frame = QWidget()
        current_frame_layout = QHBoxLayout(param_current_frame)
        current_frame_layout.setSpacing(10)
        current_frame_layout.setContentsMargins(0, 0, 0, 0)
        current_frame_layout.addWidget(self.__cb_single_frame)
        current_frame_layout.addWidget(self.__textfield_single_frame)

        param_start_end = QWidget()
        start_end_layout = QHBoxLayout(param_start_end)
        start_end_layout.setSpacing(10)
        start_end_layout.setContentsMargins(0, 0, 0, 0)
        start_end_layout.addWidget(self.__cb_start)
        start_end_layout.addWidget(self.__textfield_start)
        start_end_layout.addWidget(self.__cb_end)
        start_end_layout.addWidget(self.__textfield_end)

        param_frames = QWidget()
        frames_layout = QVBoxLayout(param_frames)
        frames_layout.setSpacing(10)
        frames_layout.setContentsMargins(10, 10, 10, 10)
        frames_layout.addWidget(self.__cb_time_slider)
        frames_layout.addWidget(param_current_frame)
        frames_layout.addWidget(self.__cb_start_end)
        frames_layout.addWidget(param_start_end)

        self.__tool_box_frames.addItem(param_frames, "Frames")

        tool_box_layout = QVBoxLayout()
        tool_box_layout.setSpacing(10)
        tool_box_layout.setContentsMargins(0, 0, 0, 0)
        tool_box_layout.addWidget(self.__tool_box_descriptions)
        tool_box_layout.addWidget(self.__tool_box_frames)

        version_layout = QHBoxLayout()
        version_layout.setSpacing(10)
        version_layout.setContentsMargins(0, 0, 0, 0)
        version_layout.addWidget(self.__prefix)
        version_layout.addWidget(self.__textfield_prefix)
        version_layout.addWidget(self.__cb_version)
        version_layout.addWidget(self.__sp_version)

        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)
        path_layout.setContentsMargins(0, 0, 0, 0)
        path_layout.addWidget(self.__path)
        path_layout.addWidget(self.__textfield_path)
        path_layout.addWidget(self.__btn_choose_path)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.addWidget(self.__btn_create_cache)


        #Main layout
        param_test = QWidget()
        main_layout = QVBoxLayout(param_test)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(5, 5, 5, 0)
        main_layout.addLayout(tool_box_layout)
        main_layout.addLayout(version_layout)
        main_layout.addLayout(path_layout)
        main_layout.addLayout(btn_layout)


        #Grid
        self.__param_main_grid = QWidget()
        self.__main_grid = QGridLayout(self.__param_main_grid)
        self.__main_grid.setSpacing(0)
        self.__main_grid.setContentsMargins(10, 10, 10, 0)
        self.__main_grid.setRowStretch(1, 1)
        self.__main_grid.addWidget(param_test, 0, 0)
        self.__main_grid.addWidget(QLabel(""), 1, 0)

        self.tab1.setLayout(self.__main_grid)


        #Triggers
        self.__btn_choose_path.clicked.connect(self._on_btn_choose_path_clicked)
        self.__btn_create_cache.clicked.connect(self._on_btn_create_cache_clicked)

        return


    def tab2UI(self):
        #Lists
        totalDescriptionList = cmds.xgmSplineQuery( listSplineDescriptions=True)
        totalDescriptionList.sort()
        name_description_list = []

        self.__rename_list = []

        self.__len_total = len(totalDescriptionList)

        i = 0
        for i in range(self.__len_total):
            if ":" in str(totalDescriptionList[i]):
                description_name = totalDescriptionList[i].partition(":") [-1]
                name_description_list.append( description_name)

            else:
                description_name = str(totalDescriptionList[i])
                name_description_list.append( description_name)

            i += 1


        #First Line
        self.__rename_from = QLabel("From")
        self.__rename_arrow = QLabel("->")
        self.__rename_to = QLabel("To")

        param_labels_rename = QWidget()
        labels_rename_layout = QHBoxLayout(param_labels_rename)
        labels_rename_layout.setSpacing(10)
        labels_rename_layout.setContentsMargins(10, 5, 10, 5)
        labels_rename_layout.addWidget(self.__rename_from)
        labels_rename_layout.addWidget(self.__rename_arrow)
        labels_rename_layout.addWidget(self.__rename_to)


        #Description Grid
        param_grid = QWidget()
        grid = QGridLayout(param_grid)
        grid.setRowStretch(self.__len_total, self.__len_total)

        for i in range(self.__len_total):
            for j in range(3):
                if j == 0:
                    grid.addWidget(QLabel(str(totalDescriptionList[i])), i, j)

                elif j == 1:
                    grid.addWidget(QLabel("->"), i, j)

                elif j == 2:
                    self.__textfield_grid = QLineEdit(self)
                    self.__rename_list.append([name_description_list[i], self.__textfield_grid])
                    self.__textfield_grid.setText( str(name_description_list[i]))
                    grid.addWidget(self.__textfield_grid, i, j)


        #Rename Layout
        scrollArea = QScrollArea()
        scrollArea.setWidget(param_grid)
        scrollArea.setWidgetResizable(True)

        self.__rename_layout = QVBoxLayout()
        self.__rename_layout.setSpacing(10)
        self.__rename_layout.setContentsMargins(15, 15, 15, 15)
        self.__rename_layout.addWidget(param_labels_rename)
        self.__rename_layout.addWidget(scrollArea)

        self.tab2.setLayout(self.__rename_layout)

        return


    def _on_btn_choose_path_clicked(self):
        path_name = cmds.fileDialog2( dialogStyle=2, fileMode=3) [0]
        self.__textfield_path.setText( path_name + '/')

        return


    def _on_btn_create_cache_clicked(self):
        #Check Settings
        A, B = 0, 0

        if self.__cb_all_descriptions.isChecked():
            A += 1

        if self.__cb_selection.isChecked():
            A += 1

        if A != 1:
            QMessageBox.critical(self, "Error", "Select only one option in the Description Folder.")
            return

        if self.__cb_time_slider.isChecked():
            B += 1

        if self.__cb_single_frame.isChecked():
            B += 1

        if self.__cb_start_end.isChecked():
            B += 1

        if B != 1:
            QMessageBox.critical(self, "Error", "Select only one option in the Frames Folder.")
            return


        ####    Get info from Settings
        #Descriptions
        if self.__cb_all_descriptions.isChecked():
            descriptionList = cmds.xgmSplineQuery( listSplineDescriptions=True)
            descriptionList.sort()

        elif self.__cb_selection.isChecked():
            descriptionList = []

            sel = cmds.ls( sl=True)
            cmds.select( sel, hi=True)
            selHier = cmds.ls( sl=True)

            for obj in selHier:
                nodeType = cmds.nodeType( obj)

                if nodeType == 'xgmSplineDescription':
                    cmds.select( obj)
                    description = cmds.pickWalk( d="up") [0]
                    descriptionList.append( description)

            descriptionList.sort()


        #Frames
        if self.__cb_time_slider.isChecked():
            start = str(cmds.playbackOptions( q=True, min=True))
            end = str(cmds.playbackOptions( q=True, max=True))

        elif self.__cb_single_frame.isChecked():
            start = self.__textfield_single_frame.text()
            end = self.__textfield_single_frame.text()

        elif self.__cb_start_end.isChecked():
            start = self.__textfield_start.text()
            end = self.__textfield_end.text()


        #Name Caches
        prefix = self.__textfield_prefix.text()

        if self.__cb_version.isChecked():
            version = str(self.__sp_version.value())

            if len(version) == 1:
                version = '_v00' + version

            elif len(version) == 2:
                version = '_v0' + version

        else:
            version = ''

        path = self.__textfield_path.text()

        nameList = []

        i, j = 0, 0
        for i in range(len(descriptionList)):
            if ":" in str(descriptionList[i]):
                obj_name = descriptionList[i].partition(":") [-1]

            else:
                obj_name = str(descriptionList[i])

            for j in range(self.__len_total):
                old_name = str(self.__rename_list[j][0])
                new_name = self.__rename_list[j][1]

                if obj_name == old_name:
                    name = new_name.text()
                    nameList.append( name)


        #Create Caches
        cacheList = createCache(descriptionList, nameList, start, end, prefix, version, path)

        for i in range(len(cacheList)):
            if i == 0:
                message = '\n' + str(cacheList[i]) + '_\n'

            elif i == len(cacheList)-1:
                message = message.replace( '_\n', '\n' + str(cacheList[i]) + '\n')

            else:
                message = message.replace( '_\n', '\n' + str(cacheList[i]) + '_\n')

        QMessageBox.information(self, "Success", "XGen Spline Cache.s :\n" + message + "\nSaved in " + path)

        return



if __name__ == "__main__":
    myWindows = MyWindowWidget()
    myWindows.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
    myWindows.show()

