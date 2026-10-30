from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.MathTrainer.generators.addition import addition_generators
from src.MathTrainer.generators.division import (
    division_all,
    division_one_digit,
    division_table_10_10,
    division_three_digit,
    division_two_digit,
)
from src.MathTrainer.generators.equations import (
    equations_add_sub,
    equations_mix,
    equations_mul_div,
)
from src.MathTrainer.generators.multiplication import (
    multiplication_all,
    multiplication_four_digit,
    multiplication_one_digit,
    multiplication_table_10_10,
    multiplication_three_digit,
    multiplication_two_digit,
)
from src.MathTrainer.generators.subtraction import subtraction_generators

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


def make_variants_division():
    return [
        ("Таблица деления (10×10)", division_table_10_10),
        ("Деление на однозначное", division_one_digit),
        ("Деление на двузначное", division_two_digit),
        ("Деление на трехзначное", division_three_digit),
        ("Все вместе", division_all),
    ]


def _equation_levels(generator, first_label="до 100"):
    return [
        (first_label, lambda: generator(100)),
        ("до 1000", lambda: generator(1000)),
        ("Случайно", generator),  # без limit предел выбирается случайно
    ]


def make_variants_equations():
    # вариант, у которого вместо функции стоит список, открывает подменю
    return [
        ("Сложение и вычитание", _equation_levels(equations_add_sub)),
        ("Умножение и деление", _equation_levels(equations_mul_div, "до 100 (таблица умножения)")),
        ("Смешанные", _equation_levels(equations_mix)),
    ]


TOPICS = {
    "Сложение": make_variants_addition,
    "Вычитание": make_variants_subtraction,
    "Умножение": make_variants_multiplication,
    "Деление": make_variants_division,
    "Уравнения": make_variants_equations,
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
    def __init__(self, open_trainer, open_submenu, go_back):
        super().__init__()
        self.open_trainer = open_trainer
        self.open_submenu = open_submenu
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

    def set_topic(self, topic_name, variants):
        self.lblTitle.setText(f"Выберите режим ({topic_name})")

        self._clear_container()
        for variant_name, target in variants:
            btn = QPushButton(variant_name)
            btn.setStyleSheet("font-size: 18px; padding: 10px;")
            if isinstance(target, list):  # подменю
                btn.clicked.connect(
                    lambda _=False, t=topic_name, v=variant_name, sub=target:
                    self.open_submenu(f"{t} • {v}", sub)
                )
            else:  # генератор задач
                btn.clicked.connect(
                    lambda _=False, t=topic_name, v=variant_name, gen=target:
                    self.open_trainer(t, v, gen)
                )
            self.btns_container.addWidget(btn)


class TrainerPage(QWidget):
    def __init__(self, go_back_to_variants):
        super().__init__()
        self.go_back_to_variants = go_back_to_variants

        self.topic_name = ""
        self.variant_name = ""
        self.generator0 = None
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
        self.lblTask.setStyleSheet("font-size: 28px;")
        self.lblTask.setAlignment(Qt.AlignCenter)
        self.lblTask.setWordWrap(True)
        root.addWidget(self.lblTask)

        self.editAnswer = QLineEdit()
        self.editAnswer.setPlaceholderText("Введите ответ")
        self.editAnswer.setValidator(QIntValidator(-2_147_483_648, 2_147_483_647, self))
        self.editAnswer.setStyleSheet(STYLE_OK)
        root.addWidget(self.editAnswer)

        self.lblCorrectAnswer = QLabel("")
        self.lblCorrectAnswer.setStyleSheet("font-size: 18px; color: #D3D3D3;")
        self.lblCorrectAnswer.setAlignment(Qt.AlignCenter)
        self.lblCorrectAnswer.setWordWrap(True)
        self.lblCorrectAnswer.hide()
        root.addWidget(self.lblCorrectAnswer)

        row = QHBoxLayout()
        self.btnCheck = QPushButton("Проверить")
        self.btnShow = QPushButton("Показать ответ")
        self.btnNext = QPushButton("Следующий пример")

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

        self.editAnswer.textEdited.connect(self.on_text_edited)

        # Enter/Return:
        # solved=False -> check_answer()
        # solved=True  -> next_task()
        self.sc_return = QShortcut(QKeySequence(Qt.Key_Return), self)
        self.sc_enter = QShortcut(QKeySequence(Qt.Key_Enter), self)
        for sc in (self.sc_return, self.sc_enter):
            sc.setContext(Qt.WidgetWithChildrenShortcut)
            sc.activated.connect(self.on_enter)

    def on_enter(self):
        if self.solved:
            self.next_task()
        else:
            self.check_answer()

    def start(self, topic_name, variant_name, generator0):
        self.topic_name = topic_name
        self.variant_name = variant_name
        self.generator0 = generator0
        self.lblTitle.setText(f"Режим: подготовка • {topic_name} • {variant_name}")
        self.next_task()

    def reset_ui_for_new_task(self):
        self.first_mistake_happened = False
        self.solved = False

        self.editAnswer.setDisabled(False)

        self.btnCheck.show()
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
        if not self.solved:
            self.editAnswer.setStyleSheet(STYLE_OK)

    def check_answer(self):
        if self.current_task is None or self.solved:
            return

        s = self.editAnswer.text().strip()
        if not s:
            return

        if int(s) == self.current_task.answer:
            self.editAnswer.setStyleSheet(STYLE_SUCCESS)
            self.editAnswer.setDisabled(True)

            # после правильного ответа — только одна кнопка
            self.btnCheck.hide()
            self.btnShow.hide()
            self.btnNext.show()
            self.btnNext.setFocus()

            self.lblCorrectAnswer.hide()
            self.solved = True
        else:
            self.editAnswer.setStyleSheet(STYLE_ERR)

            # после первой ошибки появляются "Показать ответ" и "Следующий пример"
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

        self.variants_history = []  # стек открытых экранов выбора: (название, варианты)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.page_menu = MainMenuPage(open_variants=self.open_variants)
        self.page_variants = VariantsPage(
            open_trainer=self.open_trainer,
            open_submenu=self.show_variants,
            go_back=self.variants_back,
        )
        self.page_trainer = TrainerPage(go_back_to_variants=self.open_variants_page)

        self.stack.addWidget(self.page_menu)
        self.stack.addWidget(self.page_variants)
        self.stack.addWidget(self.page_trainer)

        self.open_menu()

    def open_menu(self):
        self.stack.setCurrentWidget(self.page_menu)

    def open_variants(self, topic_name: str):
        self.variants_history = []
        self.show_variants(topic_name, TOPICS[topic_name]())

    def show_variants(self, title: str, variants):
        self.variants_history.append((title, variants))
        self.page_variants.set_topic(title, variants)
        self.open_variants_page()

    def variants_back(self):
        self.variants_history.pop()
        if self.variants_history:
            title, variants = self.variants_history[-1]
            self.page_variants.set_topic(title, variants)
        else:
            self.open_menu()

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