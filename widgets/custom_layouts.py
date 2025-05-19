from PyQt5.QtWidgets import QHBoxLayout

def create_hbox_layout(*widgets, stretch=False):
    layout = QHBoxLayout()
    if stretch:
        layout.addStretch(1)
    for widget in widgets:
        layout.addWidget(widget)
    if stretch:
        layout.addStretch(1)
    return layout
