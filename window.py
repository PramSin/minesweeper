from PySide2.QtCore import Qt, QBasicTimer, QSize, QRect
from PySide2.QtGui import QPainter, QPen, QColor, QFont, QPixmap, QIcon
from PySide2.QtWidgets import QMainWindow, QFormLayout, QActionGroup, \
    QPushButton, QDialog, QWidget, QInputDialog, QAction, QLCDNumber
from BasicRule import MineSweeper, EasyMode, MediumMode, HardMode

# noinspection PyUnresolvedReferences
import images


# noinspection PyAttributeOutsideInit
class Start(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('扫雷')
        self.setWindowIcon(QIcon(':/minesweeper.ico'))
        self.setFixedSize(1000, 700)
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.btn = QPushButton(self)
        self.btn.setMouseTracking(True)
        self.btn.setIcon(QIcon(':/开始游戏.png'))
        self.btn.setIconSize(QSize(280, 200))
        self.btn.setStyleSheet('QPushButton{border:None}')
        self.btn.move(350, 370)
        self.btn.clicked.connect(self.show_mode)
        self.msw = MineSweeperWindow(MineSweeper(0, 0, 0))
        self.show()

    def show_mode(self):
        self.choose = QDialog()
        self.choose.setFixedSize(300, 300)
        self.close()
        btn1 = QPushButton('简单', self.choose)
        btn1.move(90, 50)
        btn1.clicked.connect(self.set_easy)
        btn2 = QPushButton('中等', self.choose)
        btn2.move(90, 100)
        btn2.clicked.connect(self.set_medium)
        btn3 = QPushButton('困难', self.choose)
        btn3.move(90, 150)
        btn3.clicked.connect(self.set_hard)
        btn4 = QPushButton('自定义', self.choose)
        btn4.move(90, 200)
        btn4.clicked.connect(self.set_free)
        self.choose.setWindowTitle('模式选择')
        self.choose.setWindowModality(Qt.ApplicationModal)
        self.choose.show()

    def paintEvent(self, e):
        painter = QPainter(self)
        background = QPixmap(':/封面2.jpg')
        painter.drawPixmap(self.rect(), background)

    def mouseMoveEvent(self, e):
        if 400 <= e.x() <= 580 and 420 <= e.y() <= 520:
            self.btn.setGeometry(340, 366, 300, 214)
            self.btn.setIconSize(QSize(300, 214))
        else:
            self.btn.setGeometry(350, 370, 280, 200)
            self.btn.setIconSize(QSize(280, 200))

    def set_easy(self):
        self.choose.close()
        self.msw = MineSweeperWindow(EasyMode())
        self.msw.show()

    def set_medium(self):
        self.choose.close()
        self.msw = MineSweeperWindow(MediumMode())
        self.msw.show()

    def set_hard(self):
        self.choose.close()
        self.msw = MineSweeperWindow(HardMode())
        self.msw.show()

    def set_free(self):
        self.sf = SetFree()
        self.choose.close()
        self.sf.show()


# noinspection PyAttributeOutsideInit
class SetFree(QWidget):

    def __init__(self):
        super().__init__()
        layout = QFormLayout()
        self.len = 9
        self.wid = 9
        self.boom = 10
        self.len_btn = QPushButton('长')
        self.len_btn.clicked.connect(self.set_len)
        layout.addRow(self.len_btn)
        self.wid_btn = QPushButton('高')
        self.wid_btn.clicked.connect(self.set_wid)
        layout.addRow(self.wid_btn)
        self.boom_btn = QPushButton('炸弹数量')
        self.boom_btn.clicked.connect(self.set_boom)
        layout.addRow(self.boom_btn)
        self.close_btn = QPushButton('确认')
        self.close_btn.clicked.connect(self.goon)
        layout.addRow(self.close_btn)
        self.setLayout(layout)
        self.setWindowTitle('自定义设置')
        self.setFixedSize(300, 200)

    def set_len(self):
        length, ok = QInputDialog.getInt(self, '长', '输入长：', 9)
        if ok:
            self.len = length

    def set_wid(self):
        width, ok = QInputDialog.getInt(self, '高', '输入高：', 9)
        if ok:
            self.wid = width

    def set_boom(self):
        boom, ok = QInputDialog.getInt(self, '炸弹数量', '输入炸弹数量：', 10)
        if ok:
            self.boom = boom

    def goon(self):
        self.close()
        self.msw = MineSweeperWindow(MineSweeper(self.len, self.wid, self.boom))
        self.msw.show()


# noinspection PyAttributeOutsideInit
class MineSweeperWindow(QMainWindow):

    def __init__(self, mode):
        super().__init__()
        self.ms = mode
        self.init_ui()
        self.set_menu()

    def init_ui(self):
        """初始化游戏界面"""
        # 1.确定游戏界面的标题，大小和背景颜色
        self.setObjectName('MainWindow')
        self.setWindowTitle('扫雷')
        self.setWindowIcon(QIcon(':/minesweeper.ico'))
        self.setFixedSize(50 * self.ms.length + 100, 50 * self.ms.width + 180)
        self.setStyleSheet('#MainWindow{background-color: #f6edd2}')
        self.remain_boom = QLCDNumber(2, self)
        self.remain_boom.move(50, 50)
        self.remain_boom.setFixedSize(60, 50)
        self.remain_boom.setStyleSheet("border: 2px solid blue; color: red; background: black;")
        self.remain_boom.display('{:>02d}'.format(self.ms.b_num if self.ms.b_num >= 0 else 0))
        self.timer = QBasicTimer()
        self.second = 0
        self.time = QLCDNumber(3, self)
        self.time.move(50 * self.ms.length - 40, 50)
        self.time.setFixedSize(90, 50)
        self.time.setStyleSheet("border: 2px solid blue; color: red; background: black;")
        self.time.display('{:>03d}'.format(self.second))
        self.btn = QPushButton(self)
        self.btn.move(25 * self.ms.length + 20, 50)
        self.btn.setFixedSize(50, 50)
        self.btn.setIcon(QIcon(':/普通.png'))
        self.btn.setIconSize(QSize(45, 45))
        self.btn.setStyleSheet('QPushButton{border:None}')
        self.btn.clicked.connect(self.restart)
        self.over_signal = 0

    def set_menu(self):
        bar = self.menuBar()
        game = bar.addMenu('游戏(&G)')
        new_game = QAction('新游戏(&N)', self)
        new_game.setShortcut('Ctrl+N')
        new_game.triggered.connect(self.start)
        game.addAction(new_game)
        restart = QAction('重玩(&R)', self)
        restart.setShortcut('Ctrl+R')
        restart.triggered.connect(self.restart)
        game.addAction(restart)
        game.addSeparator()
        self.modes = QActionGroup(self)
        self.easy = QAction('简单(E)', self)
        self.easy.setCheckable(True)
        game.addAction(self.modes.addAction(self.easy))
        self.medium = QAction('中等(M)', self)
        self.medium.setCheckable(True)
        game.addAction(self.modes.addAction(self.medium))
        self.hard = QAction('困难(H)', self)
        self.hard.setCheckable(True)
        game.addAction(self.modes.addAction(self.hard))
        self.modes.triggered[QAction].connect(self.set_mode)
        if isinstance(self.ms, EasyMode):
            self.easy.setChecked(True)
        elif isinstance(self.ms, MediumMode):
            self.medium.setChecked(True)
        elif isinstance(self.ms, HardMode):
            self.hard.setChecked(True)

    def paintEvent(self, e):
        """绘制游戏内容"""
        qp = QPainter()

        def draw_map():
            """绘制版面"""
            # background = QPixmap(':/背景2.png')
            # qp.drawPixmap(self.rect(), background)
            # qp.setBrush(QColor('#e8ff9d'))
            # qp.drawRect(50, 130, 50 * self.ms.length, 50 * self.ms.width)
            for x in range(0, self.ms.length, 2):
                for y in range(0, self.ms.width, 2):
                    qp.setBrush(QColor('#007a15'))
                    qp.drawRect(50 * (x + 1), 50 * (y + 1) + 80, 50, 50)
                for y in range(1, self.ms.width, 2):
                    qp.setBrush(QColor('#00701c'))
                    qp.drawRect(50 * (x + 1), 50 * (y + 1) + 80, 50, 50)
            for x in range(1, self.ms.length, 2):
                for y in range(0, self.ms.width, 2):
                    qp.setBrush(QColor('#00701c'))
                    qp.drawRect(50 * (x + 1), 50 * (y + 1) + 80, 50, 50)
                for y in range(1, self.ms.width, 2):
                    qp.setBrush(QColor('#007a15'))
                    qp.drawRect(50 * (x + 1), 50 * (y + 1) + 80, 50, 50)
            # qp.setPen(QPen(QColor(111, 108, 108), 2, Qt.SolidLine))
            # for x in range(self.ms.length + 1):
            #     qp.drawLine(50 * (x + 1), 130, 50 * (x + 1), 50 * self.ms.width + 130)
            # for y in range(self.ms.width + 1):
            #     qp.drawLine(50, 50 * (y + 1) + 80, 50 * self.ms.length + 50, 50 * (y + 1) + 80)

        def draw_blanks():
            qp.setBrush(QColor('#f4f4f4'))
            for x in range(self.ms.length):
                for y in range(self.ms.width):
                    if isinstance(self.ms.g_map[y][x], str):
                        if self.ms.g_map[y][x] == '0$' or self.ms.g_map[y][x] == '1$':
                            # qp.setPen(QPen(QColor(219, 58, 58), 1, Qt.SolidLine))
                            # qp.setFont(QFont('Kai', 15))
                            flag = QPixmap(':/雷旗.png').scaled(50, 50)
                            qp.drawPixmap(QRect(50 * (x + 1), 50 * (y + 1) + 80, 50, 50), flag)
                            # qp.drawText(50 * (x + 1) + 18, 50 * (y + 1) + 115, '$')
                            continue
                        qp.setPen(QPen(QColor(111, 108, 108), 1, Qt.SolidLine))
                        qp.setFont(QFont('Kai', 15))
                        qp.drawRect(50 * (x + 1), 50 * (y + 1) + 80, 50, 50)
                        if self.ms.g_map[y][x] == '0':
                            continue
                        if self.ms.g_map[y][x] == '*':
                            flag = QPixmap(':/土豆雷.png').scaled(50, 50)
                            qp.drawPixmap(QRect(50 * (x + 1), 50 * (y + 1) + 80, 50, 50), flag)
                            continue
                        qp.setPen(QPen(QColor('black'), 5, Qt.SolidLine))
                        qp.drawText(50 * (x + 1) + 18, 50 * (y + 1) + 115, '{}'.format(self.ms.g_map[y][x]))
        qp.begin(self)
        draw_map()
        draw_blanks()
        qp.end()

    def mousePressEvent(self, e):
        """根据鼠标的动作，确定落子位置"""
        if self.over_signal == 1:
            return
        if self.ms.step == 0:
            self.timer.start(1000, self)
        if e.button() in (Qt.LeftButton, Qt.RightButton):
            mouse_x = e.windowPos().x()
            mouse_y = e.windowPos().y()
            if 50 <= mouse_x <= 50 * self.ms.length + 50 and 130 <= mouse_y <= 50 * self.ms.width + 130:
                game_x = int(mouse_x // 50) - 1
                game_y = int((mouse_y - 80) // 50) - 1
            else:
                return
            if e.button() == Qt.LeftButton:
                self.ms.click(game_x, game_y)
            else:
                self.ms.mark_mine(game_x, game_y)
        if self.ms.boom:
            self.repaint(0, 0, 50 * self.ms.length + 100, 50 * self.ms.width + 180)
            self.game_result()
            return
        elif self.ms.game_judge():
            self.repaint(0, 0, 50 * self.ms.length + 100, 50 * self.ms.width + 180)
            self.game_result()
            return
        self.repaint(0, 0, 50 * self.ms.length + 100, 50 * self.ms.width + 180)
        self.remain_boom.display('{:>02d}'.format(self.ms.b_num if self.ms.b_num >= 0 else 0))

    def timerEvent(self, e) -> None:
        self.second += 1
        self.time.display('{:>03d}'.format(self.second))

    def game_result(self):
        self.timer.stop()
        if self.ms.boom:
            self.btn.setIcon(QIcon(':/哭脸.png'))
            self.btn.setIconSize(QSize(45, 45))
        elif self.ms.game_judge():
            self.btn.setIcon(QIcon(':/笑脸.png'))
            self.btn.setIconSize(QSize(45, 45))
        self.over_signal = 1

    def set_mode(self, action: QAction):
        if action == self.easy:
            self.close()
            self.msw = MineSweeperWindow(EasyMode())
            self.msw.show()
        elif action == self.medium:
            self.close()
            self.msw = MineSweeperWindow(MediumMode())
            self.msw.show()
        elif action == self.hard:
            self.close()
            self.msw = MineSweeperWindow(HardMode())
            self.msw.show()

    def start(self):
        self.close()
        self.a = Start()
        self.a.show()

    def restart(self):
        self.ms.refresh()
        self.repaint()
        self.btn.setIcon(QIcon(':/普通.png'))
        self.remain_boom.display('{:>02d}'.format(self.ms.b_num if self.ms.b_num >= 0 else 0))
        self.second = 0
        self.timer.stop()
        self.time.display('{:>03d}'.format(self.second))
        self.over_signal = 0
