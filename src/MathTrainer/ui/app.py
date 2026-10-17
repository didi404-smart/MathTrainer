from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QLineEdit, QHBoxLayout, QStackedWidget
)
from PySide6.QtGui import QIntValidator

try:
    from MathTrainer.generators import addition_generators, subtraction_generators
except ImportError:
    # если src не помечен как Sources Root в PyCharm
    from src.MathTrainer.generators import addition_generators, subtraction_generators


LEVELS = [
    ("до 20", 20),
    ("до 50", 50),
    ("до 100", 100),
    ("до 1000", 1000),
    ("до 100000", 100_000),
    ("до 1000000000", 1_000_000_000),
]

STYLE_OK = (
    "font-size: 22px; padding: 10px;"
    "border: 2px solid #222; border-radius: 12px;"
    "background: #FFFFFF; color: #000000;"
)

STYLE_ERR = (
    "font-size: 22px; padding: 10px;"
    "border: 2px solid #D32F2F; border-radius: 12px;"
    "background: #FFEBEE; color: #000000;"
)

STYLE_SUCCESS = (
    "font-size: 22px; padding: 10px;"
    "border: 2px solid #2E7D32; border-radius: 12px;"
    "background: #E8F5E9; color: #000000;"
)


class MainMenuPage(QWidget):
    def __init__(self, open_levels):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("Главное меню")
        title.setStyleSheet("font-size: 26px;")
        layout.addWidget(title)

        btn_add = QPushButton("Сложение")
        btn_add.setStyleSheet("font-size: 20px; padding: 12px;")
        btn_add.clicked.connect(lambda: open_levels("Сложение", addition_generators))
        layout.addWidget(btn_add)

        btn_sub = QPushButton("Вычитание")
        btn_sub.setStyleSheet("font-size: 20px; padding: 12px;")
        btn_sub.clicked.connect(lambda: open_levels("Вычитание", subtraction_generators))
        layout.addWidget(btn_sub)

        layout.addStretch(1)


class LevelsPage(QWidget):
    def __init__(self, open_trainer, go_back):
        super().__init__()
        self.open_trainer = open_trainer
        self.go_back = go_back

        self.topic_name = ""
        self.generator = None

        layout = QVBoxLayout(self)

        btn_back = QPushButton("← Назад")
        btn_back.clicked.connect(self.go_back)
        layout.addWidget(btn_back)

        self.lblTitle = QLabel("Выберите уровень")
        self.lblTitle.setStyleSheet("font-size: 22px;")
        layout.addWidget(self.lblTitle)

        for text, limit in LEVELS:
            btn = QPushButton(text)
            btn.setStyleSheet("font-size: 18px; padding: 10px;")
            btn.clicked.connect(lambda _=False, lim=limit: self.open_trainer(self.topic_name, self.generator, lim))
            layout.addWidget(btn)

        layout.addStretch(1)

    def set_topic(self, topic_name, generator):
        self.topic_name = topic_name
        self.generator = generator
        self.lblTitle.setText(f"Выберите уровень ({topic_name})")


class TrainerPage(QWidget):
    def __init__(self, go_back_to_levels):
        super().__init__()
        self.go_back_to_levels = go_back_to_levels

        self.topic_name = ""
        self.generator = None
        self.limit = 20
        self.current_task = None

        self.first_mistake_happened = False
        self.solved = False

        root = QVBoxLayout(self)

        top = QHBoxLayout()
        self.btnBack = QPushButton("← Назад")
        self.btnBack.clicked.connect(self.go_back_to_levels)
        top.addWidget(self.btnBack)
        top.addStretch(1)
        root.addLayout(top)

        self.lblTitle = QLabel("")
        self.lblTitle.setStyleSheet("font-size: 18px; color: #444;")
        root.addWidget(self.lblTitle)

        self.lblTask = QLabel("Задача")
        self.lblTask.setStyleSheet("font-size: 32px;")
        root.addWidget(self.lblTask)

        self.editAnswer = QLineEdit()
        self.editAnswer.setPlaceholderText("Введите ответ")
        self.editAnswer.setValidator(QIntValidator(-2_147_483_648, 2_147_483_647, self))
        self.editAnswer.setStyleSheet(STYLE_OK)
        root.addWidget(self.editAnswer)

        self.lblCorrectAnswer = QLabel("")
        self.lblCorrectAnswer.setStyleSheet("font-size: 18px; color:  	#D3D3D3;")
        self.lblCorrectAnswer.hide()
        root.addWidget(self.lblCorrectAnswer)

        row = QHBoxLayout()
        self.btnCheck = QPushButton("Проверить")
        self.btnShow = QPushButton("Показать ответ")
        self.btnNext = QPushButton("Следующая задача")

        self.btnShow.hide()
        self.btnNext.hide()

        row.addWidget(self.btnCheck)
        row.addWidget(self.btnShow)
        row.addWidget(self.btnNext)
        root.addLayout(row)

        root.addStretch(1)

        self.btnCheck.clicked.connect(self.check_answer)
        self.btnShow.clicked.connect(self.show_answer)
        self.btnNext.clicked.connect(self.next_task)

        self.editAnswer.returnPressed.connect(self.check_answer)
        self.editAnswer.textEdited.connect(self.on_text_edited)

    def start(self, topic_name: str, generator, limit: int):
        self.topic_name = topic_name
        self.generator = generator
        self.limit = limit
        self.lblTitle.setText(f"Режим: подготовка • {topic_name} {limit=}")
        self.next_task()

    def reset_ui_for_new_task(self):
        self.first_mistake_happened = False
        self.solved = False
        self.btnShow.hide()
        self.btnNext.hide()
        self.lblCorrectAnswer.hide()
        self.lblCorrectAnswer.setText("")
        self.editAnswer.setStyleSheet(STYLE_OK)

    def next_task(self):
        self.current_task = self.generator(self.limit)
        self.lblTask.setText(self.current_task.text)
        self.editAnswer.clear()
        self.reset_ui_for_new_task()
        self.editAnswer.setFocus()

    def on_text_edited(self, _text: str):
        self.editAnswer.setStyleSheet(STYLE_OK)
        if self.solved:
            self.solved = False
            self.btnNext.hide()

    def check_answer(self):
        if self.current_task is None:
            return

        s = self.editAnswer.text().strip()
        if not s or self.solved:
            return

        if int(s) == self.current_task.answer:
            self.editAnswer.setStyleSheet(STYLE_SUCCESS)
            self.btnNext.show()
            self.btnShow.hide()
            self.lblCorrectAnswer.hide()
            self.solved = True
        else:
            self.editAnswer.setStyleSheet(STYLE_ERR)
            if not self.first_mistake_happened:
                self.first_mistake_happened = True
                self.btnShow.show()
                self.btnNext.show()

    def show_answer(self):
        self.lblCorrectAnswer.setText(f"Правильный ответ: {self.current_task.answer}")
        self.lblCorrectAnswer.show()


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MathTrainer")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.page_menu = MainMenuPage(open_levels=self.open_levels)
        self.page_levels = LevelsPage(open_trainer=self.open_trainer, go_back=self.open_menu)
        self.page_trainer = TrainerPage(go_back_to_levels=self.open_levels_page)

        self.stack.addWidget(self.page_menu)
        self.stack.addWidget(self.page_levels)
        self.stack.addWidget(self.page_trainer)

        self.open_menu()

    def open_menu(self):
        self.stack.setCurrentWidget(self.page_menu)

    def open_levels(self, topic_name, generator):
        self.page_levels.set_topic(topic_name, generator)
        self.open_levels_page()

    def open_levels_page(self):
        self.stack.setCurrentWidget(self.page_levels)

    def open_trainer(self, topic_name, generator, limit: int):
        self.page_trainer.start(topic_name, generator, limit)
        self.stack.setCurrentWidget(self.page_trainer)


def main():
    app = QApplication([])
    w = App()
    w.resize(900, 600)
    w.show()
    app.exec()


if __name__ == "__main__":
    main()