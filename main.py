import os
import sqlite3
import sys

from PySide2.QtWidgets import QApplication

from window import Start


def main():
    app = QApplication(sys.argv)
    _ = Start()
    sys.exit(app.exec_())


def create_db():
    rank = sqlite3.connect('rank.db')
    c = rank.cursor()

    for mode in ("Easy", "Medium", "Hard"):
        c.execute("CREATE TABLE {}("
                  "id int primary key not null, "
                  "user text, "
                  "time real"
                  ");".format(mode))

        insert = "INSERT INTO {}(id, user, time) VALUES (?, ?, ?);".format(mode)

        for i in range(1, 6):
            c.execute(insert, (i, None, None))

    rank.commit()
    rank.close()


if __name__ == '__main__':
    if not os.path.exists('rank.db'):
        create_db()
    main()
