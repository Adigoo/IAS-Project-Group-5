def postprocessing(res_lst):
    res_list = {
        "pc" :res_lst[0],
        "ac" : res_lst[1],
        "fan" : res_lst[2],
        "light" : res_lst[3]
    }
    return res_lst