import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QSlider, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation
from PyQt5.QtGui import QFont
import random
import sqlite3

# SQLite-Datenbank-Klasse
class WordDatabase:
    def __init__(self):
        self.connection = sqlite3.connect('words.db')
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS words (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               word TEXT NOT NULL)''')
        self.connection.commit()
        self.populate_with_sample_data()

    def populate_with_sample_data(self):
        # Beispielwörter einfügen, falls Tabelle leer
        self.cursor.execute("SELECT COUNT(*) FROM words")
        if self.cursor.fetchone()[0] == 0:
            words = [("Buch",), ("Enten",), ("Möbel",), ("Zaun",), ("Tal",), ("Wolken",), ("Gas",), ("Garten",), ("Birne",), ("Hafen",), ("heraus",), ("Farben",), ("Tür",), ("hinein",), ("Schuhe",), ("Winter",), ("warten",), ("Fach",), ("Bilder",), ("Silben",), ("Tante",), ("Album",), ("Kalender",), ("Telefon",), ("Feder",), ("Karten",), ("Anlage",), ("Kabel",), ("Arbeiter",), ("Raupe",), ("Figuren",), ("Juwelen",), ("Gabel",), ("Zuschauer",), ("Wochen",), ("Aufgaben",), ("Ozean",), ("leuchten",), ("Jaguar",), ("Palme",), ("Geheimnis",), ("Dokumente",), ("Gesichter",), ("Nashörner",), ("Pinguine",), ("Roboter",), ("Salamander",), ("Warteraum",), ("Wanderer",), ("Gartentor",), ("Rauchzeichen",), ("Reparatur",), ("Rakete",), ("Marmelade",), ("Pampelmuse",), ("Taschentuch",), ("Sandalen",), ("Silbenbögen",), ("Elefanten",), ("Melodien",), ("Frau",), ("Fleisch",), ("Schwan",), ("Schlauch",), ("Zwerge",), ("Schnecken",), ("Schlaf",), ("Schleim",), ("Schritte",), ("Frosch",), ("frisch",), ("Zweige",), ("Fladen",), ("schreiben",), ("Flügel",), ("Flossen",), ("Schrift",), ("frei",), ("Schweine",), ("schmusen",), ("Freude",), ("Freiheit",), ("zwei",), ("Flamingo",), ("Schwalbe",), ("schneiden",), ("schminken",), ("Früchte",), ("Schnüre",), ("Schlüssel",), ("Frösche",), ("Freunde",), ("schmatzen",), ("schlürfen",), ("schlingen",), ("Flöhe",), ("Schnabel",), ("Schlitten",), ("Schnuller",), ("Schraube",), ("Fragezeichen",), ("Kugelschreiber",), ("Schleiereule",), ("Fleischsalate",), ("Gezwitscher",), ("Schmusekatze",), ("Zwillinge",), ("Unterschriften",), ("Schlüsselloch",), ("Schmetterlinge",), ("Fledermaus",), ("Schmerzen",), ("Fischflossen",), ("französisch",), ("Hundeschnauze",), ("Feinschmecker",), ("Winterschlaf",), ("zwischen",), ("Frischlinge",), ("Luftschlange",), ("Fisch",), ("Löwe",), ("Wal",), ("Nase",), ("Maus",), ("Schaf",), ("Sofa",), ("Name",), ("Mus",), ("Insel",), ("Filme",), ("Reise",), ("Eier",), ("Felsen",), ("wir",), ("Seife",), ("Rosen",), ("Euro",), ("Öle",), ("Eis",), ("Melone",), ("Ameise",), ("Maschine",), ("Limone",), ("Amsel",), ("Schale",), ("Rosine",), ("Mimose",), ("Ruine",), ("Aroma",), ("Ferien",), ("Würfel",), ("Schülerin",), ("Menschen",), ("Formular",), ("Malerei",), ("Lawine",), ("Romane",), ("Marone",), ("Sirene",) ("Mausefalle",), ("Wasserwellen",), ("Messerwerfer",), ("Sonnenschein",), ("Reisefilme",), ("Ameiseneier",), ("Maschinenöle",), ("Seifenwasser",), ("Leseschule",), ("Anemone",), ("Scheinwerfer",), ("Amselrufe",), ("Limonenschale",), ("Menschenaffen",), ("Rosenseife",), ("Lauferei",), ("Wassermelone",), ("Reiselaune",), ("Familie",), ("Euroschein",)]
            self.cursor.executemany("INSERT INTO words (word) VALUES (?)", words)
            self.connection.commit()

    def get_random_word(self):
        self.cursor.execute("SELECT word FROM words ORDER BY RANDOM() LIMIT 1")
        return self.cursor.fetchone()[0]

    def close(self):
        self.connection.close()

# PyQt5 GUI-Anwendung
class WordApp(QWidget):
    def __init__(self):
        super().__init__()

        self.db = WordDatabase()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Schnelllesen")

        # Label für das angezeigte Wort
        self.word_label = QLabel("Start drücken", self)
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setFixedSize(600, 400)  # Setze die Größe des Labels
        self.word_label.setFont(QFont('Sans Serif', 36))  # Schriftgröße

        # Start-Knopf
        self.start_button = QPushButton("Start", self)
        self.start_button.setFont(QFont('Sans Serif', 18))
        self.start_button.clicked.connect(self.start_game)

        # Slider für Anzahl der Worte
        self.word_count_slider = QSlider(Qt.Horizontal, self)
        self.word_count_slider.setMinimum(5)
        self.word_count_slider.setMaximum(20)
        self.word_count_slider.setValue(10)
        self.word_count_slider.setTickPosition(QSlider.TicksBelow)
        self.word_count_slider.setTickInterval(1)
        self.word_count_slider.valueChanged.connect(self.update_word_count)

        self.word_count_label = QLabel(f"Anzahl der Worte: {self.word_count_slider.value()}", self)
        self.word_count_label.setFont(QFont('Sans Serif', 14))

        # Slider für Intervallzeit (Dauer zwischen den Wörtern)
        self.interval_slider = QSlider(Qt.Horizontal, self)
        self.interval_slider.setMinimum(1)  # 1 Sekunde
        self.interval_slider.setMaximum(5)  # 5 Sekunden
        self.interval_slider.setValue(2)
        self.interval_slider.setTickPosition(QSlider.TicksBelow)
        self.interval_slider.setTickInterval(1)
        self.interval_slider.valueChanged.connect(self.update_interval)

        self.interval_label = QLabel(f"Intervall: {self.interval_slider.value()} Sekunden", self)
        self.interval_label.setFont(QFont('Sans Serif', 14))

        # Layouts setzen
        layout = QVBoxLayout()
        layout.addWidget(self.word_label)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.word_count_label)
        slider_layout.addWidget(self.word_count_slider)
        layout.addLayout(slider_layout)

        interval_layout = QHBoxLayout()
        interval_layout.addWidget(self.interval_label)
        interval_layout.addWidget(self.interval_slider)
        layout.addLayout(interval_layout)

        layout.addWidget(self.start_button)
        self.setLayout(layout)

        # Timer initialisieren
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_word)

        self.word_count = self.word_count_slider.value()  # Anzahl der zu zeigenden Worte
        self.interval_time = self.interval_slider.value() * 1000  # Intervall in Millisekunden
        self.words_shown = 0  # Anzahl der bisher gezeigten Worte

        # Animation für Label
        self.animation = QPropertyAnimation(self.word_label, b"windowOpacity")
        self.animation.setDuration(500)  # 500 ms für die Fade-Animation

        self.show()

    def update_word_count(self):
        self.word_count = self.word_count_slider.value()
        self.word_count_label.setText(f"Anzahl der Worte: {self.word_count}")

    def update_interval(self):
        self.interval_time = self.interval_slider.value() * 1000  # Intervall in Millisekunden
        self.interval_label.setText(f"Intervall: {self.interval_slider.value()} Sekunden")

    def start_game(self):
        self.words_shown = 0
        self.start_button.setEnabled(False)  # Deaktiviert den Start-Knopf während des Spiels
        self.timer.start(self.interval_time)  # Timer mit dem eingestellten Intervall starten

    def update_word(self):
        if self.words_shown < self.word_count:
            random_word = self.db.get_random_word()
            self.animate_word_change(random_word)
            self.words_shown += 1
        else:
            self.timer.stop()
            self.word_label.setText("Spiel beendet")
            self.start_button.setEnabled(True)

    def animate_word_change(self, word):
        # Fade-Out Animation
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start()

        # Nach dem Fade-Out das neue Wort setzen und wieder einblenden
        self.animation.finished.connect(lambda: self.set_new_word(word))

    def set_new_word(self, word):
        self.word_label.setText(word)

        # Fade-In Animation
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

    def closeEvent(self, event):
        self.db.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WordApp()
    sys.exit(app.exec_())
