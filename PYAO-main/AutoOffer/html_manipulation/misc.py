def format_bed_bath(bed, bath, half_bath):

    layout = [bed, bath, half_bath]

    layout_nums = ''

    # Find the ones that are not none and put them in a group (Ex. 32 or 421)
    for num in layout:
        if num is None:
            num=0
        layout_nums = f"{layout_nums}{num}"

    # Puts a slash between digits (Ex. 3/2 or 4/2/1)
    # Makes sure there is more than one digit
    if len (layout_nums) >= 2:
        layout_input = '/'.join (layout_nums)
    else:
        layout_input = layout_nums

    return layout_input
