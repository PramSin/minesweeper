from PyQt5.QtWidgets import QApplication
from window import Start
import sys


def main():
    # m = MineSweeper(length, width, number)
    # m.play()
    app = QApplication(sys.argv)
    ex = Start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
