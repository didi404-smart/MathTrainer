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

# Импорты под твою текущую структуру (через src.MathTrainer...)
from src.MathTrainer.generators.addition import addition_generators
from src.MathTrainer.generators.subtraction import subtraction_generators
from src.MathTrainer.generators.multiplication import (
    multiplication_table_10_10,
    multiplication_one_digit,
    multiplication_two_digit,
    multiplication_three_digit,
    multiplication_four_digit,
    multiplication_all,
)

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

ADD_SUB_LEVELS = [
    ("до 20", 20),
    ("до 50", 50),
    ("до 100", 100),
    ("до 1000", 1000),
    ("до 100000", 100_000),
    ("до 1000000000", 1_000_000_000),
]


def make_variants_addition():
    # generator0 должен быть функцией БЕЗ аргументов, которая возвращает Task
    return [(f"Сложение {name}", (lambda lim=lim: addition_generators(lim))) for name, lim in ADD_SUB_LEVELS]


def make_variants_subtraction():
    return [(f"Вычитание {name}", (lambda lim=lim: subtraction_generators(lim))) for name, lim in ADD_SUB_LEVELS]


def make_variants_multiplication():
    return [
        ("Таблица умножения (10×10)", multiplication_table_10_10),
        ("Умножение на однозначное", multiplication_one_digit),
        ("Умножение на двузначное", multiplication_two_digit),
        ("Умножение на трехзначное", multiplication_three_digit),
        ("Умножение на четырехзначное", multiplication_four_digit),
        ("Все вместе", multiplication_all),
    ]


TOPICS = {
    "Сложение": make_variants_addition,
    "Вычитание": make_variants_subtraction,
    "Умножение": make_variants_multiplication,
}


class MainMenuPage(QWidget):
    def __init__(self, open_variants):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("Главное меню")
        title.setStyleSheet("font-size: 26px;")
        layout.addWidget(title)

        for topic_name in TOPICS.keys():
            btn = QPushButton(topic_name)
            btn.setStyleSheet("font-size: 20px; padding: 12px;")
            btn.clicked.connect(lambda _=False, name=topic_name: open_variants(name))
            layout.addWidget(btn)

        layout.addStretch(1)


class VariantsPage(QWidget):
    def __init__(self, open_trainer, go_back):
        super().__init__()
        self.open_trainer = open_trainer
        self.go_back = go_back

        self.layout = QVBoxLayout(self)

        self.btn_back = QPushButton("← Назад")
        self.btn_back.clicked.connect(self.go_back)
        self.layout.addWidget(self.btn_back)

        self.lblTitle = QLabel("Выберите режим")
        self.lblTitle.setStyleSheet("font-size: 22px;")
        self.layout.addWidget(self.lblTitle)

        self.btns_container = QVBoxLayout()
        self.layout.addLayout(self.btns_container)

        self.layout.addStretch(1)

    def _clear_container(self):
        while self.btns_container.count():
            item = self.btns_container.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

    def set_topic(self, topic_name: str, variants: list[tuple[str, callable]]):
        self.lblTitle.setText(f"Выберите режим ({topic_name})")

        self._clear_container()
        for variant_name, generator0 in variants:
            btn = QPushButton(variant_name)
            btn.setStyleSheet("font-size: 18px; padding: 10px;")
            btn.clicked.connect(
                lambda _=False, t=topic_name, v=variant_name, gen=generator0: self.open_trainer(t, v, gen)
            )
            self.btns_container.addWidget(btn)


class TrainerPage(QWidget):
    def __init__(self, go_back_to_variants):
        super().__init__()
        self.go_back_to_variants = go_back_to_variants

        self.topic_name = ""
        self.variant_name = ""
        self.generator0 = None  # функция без аргументов -> Task
        self.current_task = None

        self.first_mistake_happened = False
        self.solved = False

        root = QVBoxLayout(self)

        top = QHBoxLayout()
        self.btnBack = QPushButton("← Назад")
        self.btnBack.clicked.connect(self.go_back_to_variants)
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
        # Результаты у тебя <= 999_900_000, это влезает в 32-bit int
        self.editAnswer.setValidator(QIntValidator(-2_147_483_648, 2_147_483_647, self))
        self.editAnswer.setStyleSheet(STYLE_OK)
        root.addWidget(self.editAnswer)

        self.lblCorrectAnswer = QLabel("")
        self.lblCorrectAnswer.setStyleSheet("font-size: 18px; color: #D3D3D3;")
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

    def start(self, topic_name: str, variant_name: str, generator0):
        self.topic_name = topic_name
        self.variant_name = variant_name
        self.generator0 = generator0

        self.lblTitle.setText(f"Режим: подготовка • {topic_name} • {variant_name}")
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
        self.current_task = self.generator0()
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

        self.page_menu = MainMenuPage(open_variants=self.open_variants)
        self.page_variants = VariantsPage(open_trainer=self.open_trainer, go_back=self.open_menu)
        self.page_trainer = TrainerPage(go_back_to_variants=self.open_variants_page)

        self.stack.addWidget(self.page_menu)
        self.stack.addWidget(self.page_variants)
        self.stack.addWidget(self.page_trainer)

        self.open_menu()

    def open_menu(self):
        self.stack.setCurrentWidget(self.page_menu)

    def open_variants(self, topic_name: str):
        variants = TOPICS[topic_name]()  # [(variant_name, generator0), ...]
        self.page_variants.set_topic(topic_name, variants)
        self.open_variants_page()

    def open_variants_page(self):
        self.stack.setCurrentWidget(self.page_variants)

    def open_trainer(self, topic_name: str, variant_name: str, generator0):
        self.page_trainer.start(topic_name, variant_name, generator0)
        self.stack.setCurrentWidget(self.page_trainer)


def main():
    app = QApplication([])
    w = App()
    w.resize(900, 600)
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
