def conditional_option(option, condition):
    if not option:
        option = "NO{segment}"
    return option
