# !pip install scipy
from scipy.special import perm, comb
from functools import reduce
from collections import Counter
import numpy as np
# import torch
from itertools import combinations
# from itertools import permutations


# num_to_ch = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l'}
ch_to_num = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11}
s = 'abcdefghijklmnopqrstuvwxyzABCD'
s = list(range(30))
w = Counter(s)
red_w = Counter(s[:15])
black_w = w - red_w

d = {}

def cal(tup, down, up):
    if tup == tuple():
        return 1
    elif tup in d:
        return perm(down, up) / d[tup]
    else:
        perm_list = list(map(lambda x: perm(x, x), tup))
        d[tup] = reduce(lambda x, y: x * y, perm_list)
        return perm(down, up) / d[tup]

'''
def get_infoset_data(bright_w, red_dark, black_dark, on_board_num, dark_num, off_red_dark, off_black_dark):
    red_dark_num = sum(red_dark.values())
    black_dark_num = sum(black_dark.values())
    #     print(red_dark_num,black_dark_num)
    common = red_common and black_common

    infoset_num = cal(tuple(sorted(bright_w.values())), 88 - dark_num, on_board_num - dark_num) * comb(15,
                                                                                                       red_dark_num) * comb(
        15, black_dark_num)
    #     print(infoset_num)

    infoset_nums[on_board_num] += infoset_num
    if off_dark_num:
        infoset_size = infoset_num * cal(tuple(sorted(red_dark.values())), red_dark_num, red_dark_num) * cal(
            tuple(sorted(black_dark.values())), black_dark_num, black_dark_num)
        infoset_sizes[on_board_num] += infoset_size
'''
#     print(red_dark, black_dark, infoset_num, infoset_size)
def dark_divide_two_parts(dark):
    red_dark, black_dark = {}, {}
    for k, v in Counter(dark).items():
        if ch_to_num[k] < 6:
            red_dark[k] = v
        else:
            black_dark[k] = v
    return (red_dark, black_dark)

def judge_infoset_common(on_dark, off_dark):
    if len(on_dark) == 0 or len(off_dark) == 0:
        return True
    elif len(on_dark) == 1 and on_dark.keys() == off_dark.keys():
        return True
    else:
        return False
#pass
def cal_half_infoset_size(on_dark, off_dark):
    on_num = sum(on_dark.values())
    #     off_num = sum(off_dark.values())
    all_darks_w = Counter(on_dark) + Counter(off_dark)
    guess_on_darks = list({_ for _ in combinations(all_darks_w.elements(), on_num)})
    n = 0
    for guess_on_dark in guess_on_darks:
        n += cal(tuple(sorted(Counter(guess_on_dark).values())), on_num, on_num)
    return n
#     pass
def check_dark_proper(on_red_dark_num, on_black_dark_num, off_red_dark_num, off_black_dark_num):
    if on_red_dark_num + off_red_dark_num == 15:
        if off_black_dark_num:
            return False
    if on_black_dark_num + off_black_dark_num == 15:
        if off_red_dark_num:
            return  False
    return True
    # pass

infoset_nums = [0] * 30
infoset_sizes = [0] * 30
for on_board_num in range(1, 31):
# for on_board_num in range(1, 2):

    on_boards = list({_ for _ in combinations(s, on_board_num)})
    off_board_num = 30 - on_board_num
    for on_board in on_boards:
        on_board_w = Counter(on_board)
        off_board_w = w - on_board_w
        off_board = list(off_board_w.elements())
        for on_dark_num in range(on_board_num + 1):
        # for on_dark_num in range(1, 2):
            if on_dark_num == 0:
                infoset_nums[on_board_num] += cal(tuple(sorted(on_board_w.values())), 88, on_board_num)
                infoset_sizes[on_board_num] += cal(tuple(sorted(on_board_w.values())), 88, on_board_num)
                continue
            on_darks = list({_ for _ in combinations(on_board, on_dark_num)})
            for on_dark in on_darks:
                on_dark_w = Counter(on_dark)
                bright_w = on_board_w - on_dark_w
                on_red_dark, on_black_dark = dark_divide_two_parts(on_dark)
                on_red_dark_num = sum(on_red_dark.values())
                on_black_dark_num = sum(on_black_dark.values())
                # red_common = True if on_red_dark_num == 0 else False
                # black_common = True if on_black_dark_num == 0 else False
                #     print(red_dark_num,black_dark_num)
                on_red_dark_size = 0 if on_red_dark_num == 0 else cal(tuple(sorted(on_red_dark.values())), on_red_dark_num, on_red_dark_num)
                on_black_dark_size = 0 if on_red_dark_num == 0 else cal(tuple(sorted(on_black_dark.values())), on_black_dark_num, on_black_dark_num)
                infoset_num = cal(tuple(sorted(bright_w.values())), 88 - on_dark_num,
                                  on_board_num - on_dark_num) * comb(15, on_red_dark_num) * comb(15, on_black_dark_num)
                for off_dark_num in range(off_board_num + 1):
                # for off_dark_num in range(1, 2):
                    if off_dark_num == 0:
                        infoset_nums[on_board_num] += infoset_num
                        infoset_sizes[on_board_num] += infoset_num * on_red_dark_size * on_black_dark_size
                        continue
                    if on_dark_num + off_dark_num == 30:
                        if on_dark_num != 30:
                            break
                    off_darks = list({_ for _ in combinations(off_board, off_dark_num)})
                    for off_dark in off_darks:
                        off_red_dark, off_black_dark = dark_divide_two_parts(off_dark)
                        off_red_dark_num = sum(off_red_dark.values())
                        off_black_dark_num = sum(off_black_dark.values())
                        if not check_dark_proper(on_red_dark_num, on_black_dark_num, off_red_dark_num, off_black_dark_num):
                            break
                        red_common = judge_infoset_common(on_red_dark, off_red_dark)
                        black_common = judge_infoset_common(on_black_dark, off_black_dark)
                        #get_infoset_data(bright_w, on_red_dark, on_black_dark, on_board_num, on_dark_num, off_red_dark, off_black_dark)
                        common = red_common and black_common
                        #print(infoset_num)

                        if not common:
                            infoset_nums[on_board_num] += infoset_num
                            red_size = 0 if red_common else on_black_dark_size * cal_half_infoset_size(on_red_dark, off_red_dark)
                            black_size = 0 if black_common else on_red_dark_size * cal_half_infoset_size(on_black_dark, off_black_dark)
                            infoset_sizes[on_board_num] += infoset_num * (red_size + black_size)
                        else:
                            continue

                        # infoset_sizes[on_board_num] += infoset_size
    print(infoset_nums, infoset_sizes, sum(infoset_sizes) / sum(infoset_nums))

print(np.array(infoset_nums) * 81, np.array(infoset_sizes) * 81, sum(infoset_sizes) / sum(infoset_nums))
