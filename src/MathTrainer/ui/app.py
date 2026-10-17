from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QStackedWidget,
)
from PySide6.QtGui import QIntValidator

# Импорт генератора (сделал "двойной" вариант, чтобы у тебя точно завелось
# при разных настройках путей в PyCharm / Poetry)
try:
    from MathTrainer.generators.addition import addition_generators
except ImportError:
    from src.MathTrainer.generators.addition import addition_generators


LEVELS = [
    ("Сложение до 20", 20),
    ("Сложение до 50", 50),
    ("Сложение до 100", 100),
    ("Сложение до 1000", 1000),
    ("Сложение до 100000", 100_000),
    ("Сложение до 1000000000", 1_000_000_000),
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
    def __init__(self, open_addition_levels):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("Главное меню")
        title.setStyleSheet("font-size: 26px;")
        layout.addWidget(title)

        btn_add = QPushButton("Сложение")
        btn_add.setStyleSheet("font-size: 20px; padding: 12px;")
        btn_add.clicked.connect(open_addition_levels)
        layout.addWidget(btn_add)

        layout.addStretch(1)


class AdditionLevelsPage(QWidget):
    def __init__(self, open_trainer, go_back):
        super().__init__()
        layout = QVBoxLayout(self)

        btn_back = QPushButton("← Назад")
        btn_back.clicked.connect(go_back)
        layout.addWidget(btn_back)

        title = QLabel("Выберите уровень (сложение)")
        title.setStyleSheet("font-size: 22px;")
        layout.addWidget(title)

        for text, limit in LEVELS:
            btn = QPushButton(text)
            btn.setStyleSheet("font-size: 18px; padding: 10px;")
            btn.clicked.connect(lambda _=False, lim=limit: open_trainer(lim))
            layout.addWidget(btn)

        layout.addStretch(1)


class TrainerPage(QWidget):
    def __init__(self, go_back_to_levels):
        super().__init__()
        self.go_back_to_levels = go_back_to_levels

        self.limit = 20
        self.current_task = None

        self.first_mistake_happened = False
        self.solved = False  # решена ли текущая задача

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

        # QIntValidator в Qt работает в диапазоне 32-bit int (для 1_000_000_000 ок)
        self.editAnswer.setValidator(QIntValidator(-2_147_483_648, 2_147_483_647, self))
        self.editAnswer.setStyleSheet(STYLE_OK)
        root.addWidget(self.editAnswer)

        # правильный ответ показываем снизу (НЕ в поле ввода)
        self.lblCorrectAnswer = QLabel("")
        self.lblCorrectAnswer.setStyleSheet("font-size: 18px; color:  	#D3D3D3;")
        self.lblCorrectAnswer.hide()
        root.addWidget(self.lblCorrectAnswer)

        row = QHBoxLayout()
        self.btnCheck = QPushButton("Проверить")
        self.btnShow = QPushButton("Показать ответ")
        self.btnNext = QPushButton("Следующая задача")

        # По твоим правилам: до первой ошибки и до правильного ответа этих кнопок нет
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

        # Enter = проверить
        self.editAnswer.returnPressed.connect(self.check_answer)

        # если начали править ответ после красного/зелёного — убираем подсветку
        self.editAnswer.textEdited.connect(self.on_text_edited)

    def start(self, limit: int):
        self.limit = limit
        self.lblTitle.setText(f"Режим: подготовка • сложение до {limit}")
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
        self.current_task = addition_generators(self.limit)
        self.lblTask.setText(self.current_task.text)
        self.editAnswer.clear()
        self.reset_ui_for_new_task()
        self.editAnswer.setFocus()

    def on_text_edited(self, _text: str):
        # если начали редактировать — сбрасываем подсветку
        self.editAnswer.setStyleSheet(STYLE_OK)

        # если задача уже была решена и начали менять — считаем, что снова "в процессе"
        if self.solved:
            self.solved = False
            self.btnNext.hide()

    def check_answer(self):
        if self.current_task is None:
            return

        s = self.editAnswer.text().strip()
        if not s:
            return

        # если уже решили задачу — повторная проверка не нужна
        if self.solved:
            return

        if int(s) == self.current_task.answer:
            # Правильно: подсветить зелёным и показать "следующая задача"
            self.editAnswer.setStyleSheet(STYLE_SUCCESS)
            self.btnNext.show()

            # "показать ответ" тут не нужно
            self.btnShow.hide()
            self.lblCorrectAnswer.hide()

            self.solved = True
        else:
            # Неправильно: подсветить красным
            self.editAnswer.setStyleSheet(STYLE_ERR)

            # После первой ошибки появляются кнопки "показать ответ" и "следующая задача"
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

        self.page_menu = MainMenuPage(open_addition_levels=self.open_addition_levels)
        self.page_levels = AdditionLevelsPage(open_trainer=self.open_trainer, go_back=self.open_menu)
        self.page_trainer = TrainerPage(go_back_to_levels=self.open_addition_levels)

        self.stack.addWidget(self.page_menu)
        self.stack.addWidget(self.page_levels)
        self.stack.addWidget(self.page_trainer)

        self.open_menu()

    def open_menu(self):
        self.stack.setCurrentWidget(self.page_menu)

    def open_addition_levels(self):
        self.stack.setCurrentWidget(self.page_levels)

    def open_trainer(self, limit: int):
        self.page_trainer.start(limit)
        self.stack.setCurrentWidget(self.page_trainer)


def main():
    app = QApplication([])
    w = App()
    w.resize(900, 600)
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
