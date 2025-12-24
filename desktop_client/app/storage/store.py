# Temporary in-memory storage
shift_store = {}


def assign_shift(employee_id, start, end):
    shift_store[employee_id] = {
        "shift_start": start,
        "shift_end": end
    }


def get_shift(employee_id):
    return shift_store.get(employee_id)
