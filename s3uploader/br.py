import numpy as np
import matplotlib.pyplot as plt

def getAxSize(fig, ax):

    bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    ax_width, ax_height = bbox.width, bbox.height
    ax_width *= fig.dpi
    ax_height *= fig.dpi

    return ax_width, ax_height

def curlyBrace(fig, ax, p1, p2, k_r=0.1, bool_auto=True, str_text='', int_line_num=2, fontdict={}, **kwargs):
# def curlyBrace(fig, ax, p1, p2, k_r=0.1, bool_auto=True, str_text='', int_line_num=2, fontdict={}, **kwargs):

    pt1 = [None, None]
    pt2 = [None, None]

    ax_width, ax_height = getAxSize(fig, ax)

    ax_xlim = list(ax.get_xlim())
    ax_ylim = list(ax.get_ylim())

    # log scale consideration
    if 'log' in ax.get_xaxis().get_scale():

        if p1[0] > 0.0:

            pt1[0] = np.log(p1[0])

        elif p1[0] < 0.0:

            pt1[0] = -np.log(abs(p1[0]))

        else:

            pt1[0] = 0.0

        if p2[0] > 0.0:

            pt2[0] = np.log(p2[0])

        elif p2[0] < 0.0:

            pt2[0] = -np.log(abs(p2[0]))

        else:

            pt2[0] = 0

        for i in range(0, len(ax_xlim)):

            if ax_xlim[i] > 0.0:

                ax_xlim[i] = np.log(ax_xlim[i])

            elif ax_xlim[i] < 0.0:

                ax_xlim[i] = -np.log(abs(ax_xlim[i]))

            else:

                ax_xlim[i] = 0.0

    else:

        pt1[0] = p1[0]
        pt2[0] = p2[0]

    if 'log' in ax.get_yaxis().get_scale():

        if p1[1] > 0.0:

            pt1[1] = np.log(p1[1])

        elif p1[1] < 0.0:

            pt1[1] = -np.log(abs(p1[1]))

        else:

            pt1[1] = 0.0

        if p2[1] > 0.0:

            pt2[1] = np.log(p2[1])

        elif p2[1] < 0.0:

            pt2[1] = -np.log(abs(p2[1]))

        else:

            pt2[1] = 0.0

        for i in range(0, len(ax_ylim)):

            if ax_ylim[i] > 0.0:

                ax_ylim[i] = np.log(ax_ylim[i])

            elif ax_ylim[i] < 0.0:

                ax_ylim[i] = -np.log(abs(ax_ylim[i]))

            else:

                ax_ylim[i] = 0.0

    else:

        pt1[1] = p1[1]
        pt2[1] = p2[1]

    # get the ratio of pixels/length
    xscale = ax_width / abs(ax_xlim[1] - ax_xlim[0])
    yscale = ax_height / abs(ax_ylim[1] - ax_ylim[0])

    # this is to deal with 'equal' axes aspects
    if bool_auto:

        pass

    else:

        xscale = 1.0
        yscale = 1.0

    # convert length to pixels, 
    # need to minus the lower limit to move the points back to the origin. Then add the limits back on end.
    pt1[0] = (pt1[0] - ax_xlim[0]) * xscale
    pt1[1] = (pt1[1] - ax_ylim[0]) * yscale
    pt2[0] = (pt2[0] - ax_xlim[0]) * xscale
    pt2[1] = (pt2[1] - ax_ylim[0]) * yscale

    # calculate the angle
    theta = np.arctan2(pt2[1] - pt1[1], pt2[0] - pt1[0])

    # calculate the radius of the arcs
    r = np.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1]) * k_r

    # arc1 centre
    x11 = pt1[0] + r * np.cos(theta)
    y11 = pt1[1] + r * np.sin(theta)

    # arc2 centre
    x22 = (pt2[0] + pt1[0]) / 2.0 - 2.0 * r * np.sin(theta) - r * np.cos(theta)
    y22 = (pt2[1] + pt1[1]) / 2.0 + 2.0 * r * np.cos(theta) - r * np.sin(theta)

    # arc3 centre
    x33 = (pt2[0] + pt1[0]) / 2.0 - 2.0 * r * np.sin(theta) + r * np.cos(theta)
    y33 = (pt2[1] + pt1[1]) / 2.0 + 2.0 * r * np.cos(theta) + r * np.sin(theta)

    # arc4 centre
    x44 = pt2[0] - r * np.cos(theta)
    y44 = pt2[1] - r * np.sin(theta)

    # prepare the rotated
    q = np.linspace(theta, theta + np.pi/2.0, 50)

    # reverse q
    # t = np.flip(q) # this command is not supported by lower version of numpy
    t = q[::-1]

    # arc coordinates
    arc1x = r * np.cos(t + np.pi/2.0) + x11
    arc1y = r * np.sin(t + np.pi/2.0) + y11

    arc2x = r * np.cos(q - np.pi/2.0) + x22
    arc2y = r * np.sin(q - np.pi/2.0) + y22

    arc3x = r * np.cos(q + np.pi) + x33
    arc3y = r * np.sin(q + np.pi) + y33

    arc4x = r * np.cos(t) + x44
    arc4y = r * np.sin(t) + y44

    # convert back to the axis coordinates
    arc1x = arc1x / xscale + ax_xlim[0]
    arc2x = arc2x / xscale + ax_xlim[0]
    arc3x = arc3x / xscale + ax_xlim[0]
    arc4x = arc4x / xscale + ax_xlim[0]

    arc1y = arc1y / yscale + ax_ylim[0]
    arc2y = arc2y / yscale + ax_ylim[0]
    arc3y = arc3y / yscale + ax_ylim[0]
    arc4y = arc4y / yscale + ax_ylim[0]

    # log scale consideration
    if 'log' in ax.get_xaxis().get_scale():

        for i in range(0, len(arc1x)):

            if arc1x[i] > 0.0:

                arc1x[i] = np.exp(arc1x[i])

            elif arc1x[i] < 0.0:

                arc1x[i] = -np.exp(abs(arc1x[i]))

            else:

                arc1x[i] = 0.0

        for i in range(0, len(arc2x)):

            if arc2x[i] > 0.0:

                arc2x[i] = np.exp(arc2x[i])

            elif arc2x[i] < 0.0:

                arc2x[i] = -np.exp(abs(arc2x[i]))

            else:

                arc2x[i] = 0.0

        for i in range(0, len(arc3x)):

            if arc3x[i] > 0.0:

                arc3x[i] = np.exp(arc3x[i])

            elif arc3x[i] < 0.0:

                arc3x[i] = -np.exp(abs(arc3x[i]))

            else:

                arc3x[i] = 0.0

        for i in range(0, len(arc4x)):

            if arc4x[i] > 0.0:

                arc4x[i] = np.exp(arc4x[i])

            elif arc4x[i] < 0.0:

                arc4x[i] = -np.exp(abs(arc4x[i]))

            else:

                arc4x[i] = 0.0

    else:

        pass

    if 'log' in ax.get_yaxis().get_scale():

        for i in range(0, len(arc1y)):

            if arc1y[i] > 0.0:

                arc1y[i] = np.exp(arc1y[i])

            elif arc1y[i] < 0.0:

                arc1y[i] = -np.exp(abs(arc1y[i]))

            else:

                arc1y[i] = 0.0

        for i in range(0, len(arc2y)):

            if arc2y[i] > 0.0:

                arc2y[i] = np.exp(arc2y[i])

            elif arc2y[i] < 0.0:

                arc2y[i] = -np.exp(abs(arc2y[i]))

            else:

                arc2y[i] = 0.0

        for i in range(0, len(arc3y)):

            if arc3y[i] > 0.0:

                arc3y[i] = np.exp(arc3y[i])

            elif arc3y[i] < 0.0:

                arc3y[i] = -np.exp(abs(arc3y[i]))

            else:

                arc3y[i] = 0.0

        for i in range(0, len(arc4y)):

            if arc4y[i] > 0.0:

                arc4y[i] = np.exp(arc4y[i])

            elif arc4y[i] < 0.0:

                arc4y[i] = -np.exp(abs(arc4y[i]))

            else:

                arc4y[i] = 0.0

    else:

        pass

    # plot arcs
    ax.plot(arc1x, arc1y, **kwargs)
    ax.plot(arc2x, arc2y, **kwargs)
    ax.plot(arc3x, arc3y, **kwargs)
    ax.plot(arc4x, arc4y, **kwargs)

    # plot lines
    ax.plot([arc1x[-1], arc2x[1]], [arc1y[-1], arc2y[1]], **kwargs)
    ax.plot([arc3x[-1], arc4x[1]], [arc3y[-1], arc4y[1]], **kwargs)

    summit = [arc2x[-1], arc2y[-1]]

    if str_text:

        int_line_num = int(int_line_num)

        str_temp = '\n' * int_line_num
        
        # convert radians to degree and within 0 to 360
        ang = np.degrees(theta) % 360.0

        if (ang >= 0.0) and (ang <= 90.0):

            rotation = ang

            str_text = str_text + str_temp

        if (ang > 90.0) and (ang < 270.0):

            rotation = ang + 180.0

            str_text = str_temp + str_text

        elif (ang >= 270.0) and (ang <= 360.0):

            rotation = ang

            str_text = str_text + str_temp

        else:

            rotation = ang

        ax.axes.text(arc2x[-1], arc2y[-1], str_text, ha='center', va='center', rotation=rotation, fontdict=fontdict)

    else:

        pass

    arc1 = [arc1x, arc1y]
    arc2 = [arc2x, arc2y]
    arc3 = [arc3x, arc3y]
    arc4 = [arc4x, arc4y]

    return theta, summit, arc1, arc2, arc3, arc4