import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton
from sidebar import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()
        self.ui.pilaWidgets.setCurrentIndex(0)
        self.ui.btnResumen.setChecked(True)

        self.ui.btnResumen.toggled.connect(lambda: self.cambiar_pagina(0))
        self.ui.btnResumen_2.toggled.connect(lambda: self.cambiar_pagina(0))
        self.ui.dashborad_btn_1.toggled.connect(lambda: self.cambiar_pagina(1))
        self.ui.dashborad_btn_2.toggled.connect(lambda: self.cambiar_pagina(1))
        #self.ui.btnOrders1.toggled.connect(lambda: self.cambiar_pagina(2))
        #self.ui.btnOrders2.toggled.connect(lambda: self.cambiar_pagina(2))
        #self.ui.btnProducts1.toggled.connect(lambda: self.cambiar_pagina(3))
        #self.ui.btnProducts2.toggled.connect(lambda: self.cambiar_pagina(3))
        #self.ui.btnCustomers1.toggled.connect(lambda: self.cambiar_pagina(4))
        #self.ui.btnCustomers2.toggled.connect(lambda: self.cambiar_pagina(4))

    ## Function for changing page to user page
    def on_user_btn_clicked(self):
        self.ui.pilaWidgets.setCurrentIndex(0)

    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                    + self.ui.full_menu_widget.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    def cambiar_pagina(self, index: int):
        self.ui.pilaWidgets.setCurrentIndex(index)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())



