from PyQt5 import QtWidgets, QtCore

app = QtWidgets.QApplication([])


def create_selection_card():
    card = QtWidgets.QWidget()
    card.setObjectName("collection_card")
    card_layout = QtWidgets.QVBoxLayout(card)

    # Add a label to the card
    label = QtWidgets.QLabel("Collection Card")
    label.setAlignment(QtCore.Qt.AlignCenter)
    card_layout.addWidget(label)

    return card


# Apply QSS stylesheet
app.setStyleSheet(
    """
                  
    #buttons {
        background-color: yellow;
    }
                  
    #window {
        background-color: green;
    }
                  
    #sidebar {
        background-color: red;
    }
                       
    #main {
        background-color: blue;
    }    

    #collection_card {
    
        background-color: white;
    }      
                  
"""
)

window = QtWidgets.QWidget()
window.setObjectName("window")
window.setWindowTitle("Prototype GUI")
window.setGeometry(100, 100, 1920, 1080)  # Adjusted for a larger window size

# sidebar layout
sidebar_widget = QtWidgets.QWidget()
sidebar_widget.setObjectName("sidebar")
sidebar_layout = QtWidgets.QVBoxLayout()
sidebar_layout.setAlignment(QtCore.Qt.AlignTop)
sidebar_widget.setLayout(sidebar_layout)


# Add some buttons to the sidebar
for i in range(5):
    button = QtWidgets.QPushButton(f"Button {i+1}")
    button.setObjectName("buttons")
    sidebar_layout.addWidget(button)

# main layout
main_widget = QtWidgets.QWidget()
main_widget.setObjectName("main")
main_layout = QtWidgets.QGridLayout(main_widget)  # Create layout with parent directly

# add 10 cards to the main layout in a grid (2 columns)
for i in range(10):
    card = create_selection_card()
    row = i // 2  # Integer division for row
    col = i % 2  # Modulo for column
    main_layout.addWidget(card, row, col)

layout = QtWidgets.QHBoxLayout(
    window
)  # Change to horizontal layout like flex-direction: row
layout.addWidget(sidebar_widget, 1)  # stretch factor of 1 (like flex: 1)
layout.addWidget(main_widget, 3)  # stretch factor of 3 (like flex: 3

window.show()
app.exec_()
