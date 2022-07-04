from Modules import *
from MyBar import *


class MainWindow(QMainWindow):
    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(400, 400)
        self.titleBar = MyBar(self)
        # self.setStyleSheet("border : 3px dashed blue;")

        self.setFont(QFont('Seoge UI', 12))
        self.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.resize(640, self.titleBar.height() + 480)
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        self.editor = QPlainTextEdit()
        self.editor.setStyleSheet(" background-color: #272727;"
                                  "border: 0;"
                                  "font: 19px; "
                                  "font-family: JetBrains Mono;"
                                  )

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        layout.addWidget(self.editor)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")

        self.status.setMinimumHeight(40)
        self.status.setStyleSheet('''
                    color: #B8B8B8;
                    background-color : #1F1F1F;
                    padding: 5px;

                    ''')

        file_toolbar = QToolBar("File")
        file_toolbar.setStyleSheet('''
                background-color: #202020;
                padding: 5px;
                font: 7pt, 'Segoe UI ';

            ''')
        self.addToolBar(file_toolbar)

        # creating a file menu
        file_menu = self.menuBar().addMenu("&File")
        self.menuBar().setStyleSheet("""
               QMenuBar {
                        background-color: #202020;
                        padding: 5px;
                        font: 11px, 'Segoe UI ';
                    }
                    QMenuBar::item {
                        padding: 7px 15px;
                        background-color: #202020;
                        color: rgb(255,255,255);  
                        border-radius: 5px;
                    }
                    QMenuBar::item:selected {    
                        background-color: rgb(42, 130, 218);
                    }
                    QMenuBar::item:pressed {
                        background: rgb(30, 98, 166);
                    }


                    """)
        open_file_action = QAction("Open file", self)
        open_file_action.setStatusTip("Open file")

        # adding action to the open file
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction("Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction("Save As", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction("Print", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")
        edit_toolbar.setStyleSheet('''
                        background-color: #202020;
                        padding: 5px;
                        font: 7pt, 'Segoe UI ';

                    ''')


        # undo action
        undo_action = QAction("Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)

        # adding this to tool and menu bar
        edit_toolbar.addAction(undo_action)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)

        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        cut_action = QAction("Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(self.editor.cut)

        # adding this to menu and tool bar
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)
        copy_action = QAction("Copy", self)
        copy_action.setStatusTip("Copy selected text")

        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        # paste action
        paste_action = QAction("Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.triggered.connect(self.editor.paste)

        # adding this to menu and tool bar
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)
        select_action = QAction("Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)

        # adding this to menu and tool bar
        edit_toolbar.addAction(select_action)
        edit_menu.addAction(select_action)

        wrap_action = QAction("Wrap text to window", self)
        wrap_action.setStatusTip("Check to wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        # adding it to edit menu not to the tool bar
        edit_menu.addAction(wrap_action)
        slide = QSlider(Qt.Horizontal)
        slide.setRange(0, 70)
        slide.setValue(40)
        slide.setMaximumWidth(300)
        slide.valueChanged.connect(self.UpdateColor)
        edit_toolbar.addWidget(slide)
        edit_toolbar.addSeparator()

        self.update_title()
        self.show()

    def UpdateColor(self, value):
        print(value)
        self.editor.setStyleSheet(
            f'QWidget {{background-color: rgb({value},{value},{value}); color: rgb({255},{255},{255}); font: 19px; font-family: JetBrains Mono; }}')

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    # action called by file open action
    def file_open(self):

        # getting path and bool value
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                              "Text documents (*.txt);All files (*.*)")

        if path:
            try:
                with open(path, 'rU') as f:
                    text = f.read()

            except Exception as e:

                self.dialog_critical(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

    # action called by file save action
    def file_save(self):

        if self.path is None:
            return self.file_saveas()

        self._save_to_path(self.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                                              "All files (*.*)")

        if not path:
            return

        self._save_to_path(path)

    # save to path method
    def _save_to_path(self, path):

        text = self.editor.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)

        # if error occurs
        except Exception as e:
            self.dialog_critical(str(e))

        # else do this
        else:
            self.path = path
            self.update_title()

    # action called by print
    def file_print(self):

        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    # update title method
    def update_title(self):
        self.setWindowTitle("%s - Windows Notepad" % (os.path.basename(self.path)
                                                     if self.path else "Untitled "))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)

    def changeEvent(self, event):
        if event.type() == event.WindowStateChange:
            self.titleBar.windowStateChanged(self.windowState())

    def resizeEvent(self, event):
        self.titleBar.resize(self.width(), self.titleBar.height())
