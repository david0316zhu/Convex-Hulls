#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import time
import random
import copy

# function that checks if three points a,b,c are clockwise positioned 
def is_clockwise(a, b, c):
    if (c[1] - a[1]) * (b[0] - a[0]) < (b[1] - a[1]) * (c[0] - a[0]):
        return True
    return False


# compute with naive method the convex hull of the points cloud pts 
# and store it as a list of vectors
# O(nh) time complexity
def convex_hull_2d_gift_wrapping(pts):
    pt = copy.deepcopy(pts)
    convex_hull_order = []
    original = len(pt)
    add = True
    left = pt[0]
    start = pt[0]
    while True:
        count = 2
        length = len(pt)
        if left != pt[1]:
            while count < length:
                if is_clockwise(left, pt[1], pt[count]):
                    count += 1
                else:

                    pt[count], pt[1] = pt[1], pt[count]

                    count = 2

            left = pt[1]
            convex_hull_order.append(pt[0])
            pt.remove(pt[0])
            if add:
                pt.append(start)
                add = False

            if pt[0] == start:
                break

    return convex_hull_order


def anti_clockwise(arr):
    copy_arr = copy.deepcopy(arr)
    new = [copy_arr[0]]
    copy_arr.reverse()
    
    for i in range(0, len(copy_arr)-1):
        new.append(copy_arr[i])
    return new


# compute with divide and conquer method the convex hull of the points  
# cloud pts and store it as a list of vectors
def merge(left, right):
    
    removal_r = []
    removal_l = []
    #Create sequence of clockwise and anticlockwise for leftmost right points and rightmost left point
    max_l = max(left)
    min_r = min(right)
    num_l = left.index(max_l)
    num_r = right.index(min_r)
    remove_nl = []
    remove_nr =[]
    for i in left:
        if i == max_l:
            break
        if left.index(i) < num_l:
            remove_nl.append(i)
    for j in remove_nl:
        left.remove(j)
        left.append(j)
    for k in right:
        if k == max_l:
            break
        if right.index(k) < num_r:
            remove_nr.append(k)
    for l in remove_nr:
        right.remove(l)
        right.append(l)
        
    acw_l = anti_clockwise(left)
    acw_r = anti_clockwise(right)
    # find the most right point in the left convex hull
    l_xp = left[0]
    # find the most left point in the right convex hull
    r_xp = right[0]
    top_rx = right[0]
    top_lx = left[0]
    prev_rpt = 0
    prev_lpt = 0
    
    #loop through to find upper tangent
    #add expired points to be removed
    while True:
        for rpt in right:
            if rpt != top_rx:
                if not is_clockwise(top_lx, top_rx, rpt):
                    
                    removal_r.append(top_rx)
                    
                    top_rx = rpt

        for lpt in acw_l:
            if lpt != top_lx:
                if is_clockwise(top_rx, top_lx, lpt):
                    removal_l.append(top_lx)
                    top_lx = lpt

        if prev_rpt == top_rx and prev_lpt == top_lx:
            break
        prev_rpt = top_rx
        prev_lpt = top_lx

    top_rx = right[0]
    top_lx = left[0]
    prev_rpt = 0
    prev_lpt = 0
    #loop through to find lower tangent
    #add expired points to be removed
    #add filler to show second removal of leftmost/rightmost point
    while True:
        for rpt in acw_r:
            if rpt != top_rx:
                if is_clockwise(top_lx, top_rx, rpt):
                    if top_rx == r_xp:
                        removal_r.append("filler")
                        removal_r.append(top_rx)
                        top_rx = rpt
                        continue
                    removal_r.append(top_rx)
                    top_rx = rpt  
                    
        for lpt in left:
            if lpt != top_lx:
                
                if not is_clockwise(top_rx, top_lx, lpt):
                    if top_lx == l_xp:
                        removal_l.append("filler")
                        removal_l.append(top_lx)
                        top_lx = lpt
                        continue
                    removal_l.append(top_lx)
                    top_lx = lpt
                
        if prev_rpt == top_rx and prev_lpt == top_lx:
            break
        prev_rpt = top_rx
        prev_lpt = top_lx

    new_left = []
    new_right = []
    add_start = 0
    ad_start = 0
    count_r = 0
    count_l = 0
    #find occurance of leftmost right pt
    for ct_r in removal_r:
        if ct_r == r_xp:
            count_r += 1
    #find occurance of rightmost left pt
    for ct_l in removal_l:
        if ct_l == l_xp:
            count_l += 1
    #removal of expired points, rightmost/leftmost sperately remove
    #depending on removal of start of left/right or end of left/right
    for i in left:
        inside = False
        for j in removal_l:
            if j == i:
                if j == l_xp:
                    inside = True
                    
                    if count_l > 1:
                        removal_l.remove(j)
                        removal_l.remove(j)
                        continue
                    elif count_l == 1:
                        if removal_l.index(j) > 0:
                            add_start = "yes"
                            continue
                        else:
                            add_start = "no"
                            continue
                removal_l.remove(j)
                inside = True
        if not inside:
            new_left.append(i)
    if add_start == "yes":
        
        new_left.append(l_xp)
    elif add_start == "no":
        new_left.insert(0, l_xp)
    
    for r in right:
        inside = False
        for t in removal_r:
            if t == r:
                if t == r_xp:
                    inside = True
                    if count_r > 1:
                        
                        removal_r.remove(t)
                        
                        removal_r.remove(t)
                        continue
                    elif count_r == 1:
                        if removal_r.index(t) > 0:
                            ad_start = "yes"
                            continue
                        else:
                            ad_start = "no"
                            continue
                removal_r.remove(t)
                inside = True
        if not inside:
            new_right.append(r)
    
    if ad_start == "yes":
        new_right.insert(0, r_xp)
        
    elif ad_start == "no":
        new_right.append(r_xp)
        
    if count_r == 0:
        new_right.append(r_xp)
    #append right list to left list
    for f in new_right:
        new_left.append(f)

    final_list = new_left
    return final_list


def convex_hull_2d_divide_conquer(ps):

    if len(ps) < 5:
        return convex_hull_2d_gift_wrapping(ps)
    val = len(ps)//2
    left_half = convex_hull_2d_divide_conquer(ps[0: val])
    right_half = convex_hull_2d_divide_conquer(ps[val:])

    return merge(left_half, right_half)


NUMBER_OF_POINTS = 400
# generate random points and sort them according to x coordinate
pts=[]
for i in range(NUMBER_OF_POINTS): pts.append([random.random(), random.random()])
pts = sorted(pts, key=lambda x: x[0])



# compute the convex hulls
print("Computing convex hull using gift wrapping technique ... ", end="")
t = time.time()


hull_gift_wrapping = convex_hull_2d_gift_wrapping(pts)

print("done ! It took ", time.time() - t, " seconds")

print("Computing convex hull using divide and conquer technique ... ", end="")
t = time.time()

hull_divide_conquer = convex_hull_2d_divide_conquer(pts)

print("done ! It took ", time.time() - t, " seconds")






# close the convex hull for display
hull_gift_wrapping.append(hull_gift_wrapping[0])
hull_divide_conquer.append(hull_divide_conquer[0])


# display the convex hulls
if NUMBER_OF_POINTS < 1000:
    fig = plt.figure()
    ax = fig.add_subplot(131)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    ax.title.set_text('Points')
    ax = fig.add_subplot(132)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    ax.plot([x[0] for x in hull_gift_wrapping], [x[1] for x in hull_gift_wrapping], "ro--")
    ax.title.set_text('Gift Wrapping')
    ax = fig.add_subplot(133)
    ax.plot([x[0] for x in pts], [x[1] for x in pts], "ko")
    ax.plot([x[0] for x in hull_divide_conquer], [x[1] for x in hull_divide_conquer], "ro--")
    ax.title.set_text('Divide/Conquer')
    plt.show(block=False)
