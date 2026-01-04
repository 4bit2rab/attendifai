_capsule = None

def register_capsule(widget):
    global _capsule
    _capsule = widget

def get_capsule_widget():
    return _capsule
