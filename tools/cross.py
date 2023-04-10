def get_cross_coord(x1, y1, x2, y2, endx=20, endy=20):
    """
    It needs further rework particular in case of decreasing
    when 'endx' and 'endy' become more than x2 - x1 and y2 - y1
    """
    ribx = (x2 - x1 - endx) / 2
    riby = (y2 - y1 - endy) / 2

    def get_n():
        base_y = y1 + riby
        cur_x = x1 + ribx
        return [(cur_x, base_y), (cur_x, y1), (cur_x + endx, y1), (cur_x + endx, base_y)]

    def get_e():
        cur_y = y1 + riby
        base_x = x1 + ribx + endx
        return [(x2, cur_y), (x2, cur_y + endy), (base_x, cur_y + endy)]

    def get_s():
        base_y = y1 + riby + endy
        cur_x = x1 + ribx
        return [(cur_x + endx, y2), (cur_x, y2), (cur_x, base_y)]

    def get_w():
        return [(x1, y1 + riby + endy), (x1, y1 + riby)]

    coord = get_n() + get_e() + get_s() + get_w()
    return coord