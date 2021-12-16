global _count_processed_image
_count_processed_image = 0 

def add_count_processed_image():
    global _count_processed_image
    _count_processed_image += 1

def get_count_processed_image():
    global _count_processed_image
    return _count_processed_image