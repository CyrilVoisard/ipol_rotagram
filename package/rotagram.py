# Objective : Plot and save the rotagram.

from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def rotagram(steps_lim_bis, segm, data_lb, output):
    segm = pd.DataFrame(segm)
    os.chdir(output)
    
    # figure and color definition
    fig, ax = plt.subplots(1, 3, gridspec_kw={'width_ratios': [20, 1, 1]}, figsize=(12, 10))
    ax[1].set_title('        Stance', fontsize=10, weight='bold')
    ax[2].set_title('phase       ', fontsize=10, weight='bold')
    ax[0].set_yticks([])
    ax[1].set_yticks([])
    ax[1].set_xticks([0])
    ax[2].set_xticks([0])
    ax[1].set_xticklabels(['Left\nfoot'], fontsize=8, horizontalalignment='center')
    ax[2].set_xticklabels(['Right\nfoot'], fontsize=8, horizontalalignment='center')

    color_r, line_r = 'blue', '-'
    color_l, line_l = 'red', '-'
    color_r_2, line_r = 'green', '-'
    color_l_2, line_l = 'orange', '-'

    # one table for the right foot, one for the left foot
    events_right = steps_lim_bis[steps_lim_bis["Foot"]== 1]
    events_left = steps_lim_bis[steps_lim_bis["Foot"] == 0]

    t = data_lb["PacketCounter"] - segm.iloc[1, 0]/ 100
    sc = - data_lb["Gyr_X"]

    # Fine black cumulative curve for u-turn
    cumulative_curve = np.cumsum(sc[segm.iloc[1, 0]-50: segm.iloc[2, 0]+50])
    coef = np.sign(cumulative_curve.iloc[-1])* 180 / cumulative_curve.iloc[-1]
    cumulative_curve = np.sign(cumulative_curve.iloc[-1]) * cumulative_curve * 180 / cumulative_curve.iloc[-1]
    leg3 = ax[0].plot(cumulative_curve, t[segm.iloc[1, 0]-50: segm.iloc[2, 0]+50], 'k')

    W = abs(min(cumulative_curve))
    W1 = abs(max(cumulative_curve))
    if W1 > W:
        W = W1
    W = max(abs(cumulative_curve))

    if max(cumulative_curve) > 100:
        ax[0].annotate('U-turn to the right', xy=(2, 1), xytext=(30, (-1)), fontsize=10, weight='bold')
    else:
        ax[0].annotate('U-turn to the left', xy=(2, 1), xytext=(-W + 30, (-1)), fontsize=10, weight='bold')


    # rotation plot for each stance phase
    for y in range(len(events_right)-1):
        if (events_right["TO"].tolist()[y+1] - segm.iloc[1, 0])*(events_right["HS"].tolist()[y] - segm.iloc[1, 0]) > 0:
            # plot
            leg_rf = ([events_right["HS"].tolist()[y], events_right["TO"].tolist()[y+1]] - segm.iloc[1, 0]) / 100
            leg1 = ax[2].plot([0, 0], leg_rf, line_r, linewidth=3, color=color_r)
            """
            ax[0].plot(np.cumsum(sc[int(events_right["HS"].tolist()[y]):int(events_right["TO"].tolist()[y+1])]) * coef,
                       t[int(events_right["HS"].tolist()[y]):int(events_right["TO"].tolist()[y+1])],
                       line_r, linewidth=3, color=color_r)
            """
            ax[0].plot(np.cumsum(sc[int(events_right["TO"].tolist()[y]):int(events_right["HS"].tolist()[y])]) * coef,
                       t[int(events_right["TO"].tolist()[y]):int(events_right["HS"].tolist()[y])],
                       line_r, linewidth=3, color=color_r_2)

    for y in range(len(events_left)-1):
        if (events_left["TO"].tolist()[y+1] - segm.iloc[1, 0])*(events_left["HS"].tolist()[y] - segm.iloc[1, 0]) > 0:
            # leg_lf = ([events_left["HS"].tolist()[y]  - len(data_lb), events_left["TO"].tolist()[y+1] - len(data_lb)] - segm.iloc[1, 0]) / 100
            leg_lf = ([events_left["HS"].tolist()[y], events_left["TO"].tolist()[y+1]] - segm.iloc[1, 0]) / 100
            leg2 = ax[1].plot([0, 0], leg_lf, line_r, linewidth=3, color=color_l)
            """"
            ax[0].plot(np.cumsum(sc[int(events_left["HS"].tolist()[y] - len(data_lb)):int(events_left["TO"].tolist()[y+1] - len(data_lb))]) * coef,
                       t[int(events_left["HS"].tolist()[y] - len(data_lb)):int(events_left["TO"].tolist()[y+1] - len(data_lb))],
                       line_l, linewidth=3, color=color_l)
                       """"
            ax[0].plot(np.cumsum(sc[int(events_left["TO"].tolist()[y]):int(events_left["HS"].tolist()[y])]) * coef,
                       t[int(events_left["TO"].tolist()[y]):int(events_left["HS"].tolist()[y])],
                       line_l, linewidth=3, color=color_l_2)
            # ax[0].plot(np.cumsum(sc[int(events_left["HS"].tolist()[y]):int(events_left["TO"].tolist()[y+1])]) * coef,
              #         t[int(events_left["HS"].tolist()[y]):int(events_left["TO"].tolist()[y+1])],
               #        line_l, linewidth=3, color=color_l)

        # coloring the areas of the figure
        ax[0].add_patch(
            patches.Rectangle(
                (-W, (segm.iloc[0, 0] - segm.iloc[1, 0]) / 100),  # (x,y)
                W,  # width
                (segm.iloc[3, 0] - segm.iloc[0, 0]) / 100,  # height
                facecolor="red",
                alpha=0.01
            )
        )
        ax[0].add_patch(
            patches.Rectangle(
                (0, (segm.iloc[0, 0] - segm.iloc[1, 0]) / 100),  # (x,y)
                W,  # width
                (segm.iloc[3, 0] - segm.iloc[0, 0]) / 100,  # height
                alpha=0.01,
                color=color_r
            )
        )
        ax[0].add_patch(
            patches.Rectangle(
                (-W, 0),  # (x,y)
                W * 2,  # width
                (segm.iloc[2, 0] - segm.iloc[1, 0]) / 100,  # height
                alpha=0.1,
                facecolor="yellow", linestyle='dotted'
            )
        )

        ax[1].add_patch(
            patches.Rectangle(
                (-W, (segm.iloc[0, 0] - segm.iloc[1, 0]) / 100),  # (x,y)
                W * 2,  # width
                (segm.iloc[3, 0] - segm.iloc[0, 0]) / 100,  # height
                alpha=0.01,
                facecolor="red"
            )
        )

        ax[1].add_patch(
            patches.Rectangle(
                (-W, 0),  # (x,y)
                W * 2,  # width
                (segm.iloc[2, 0] - segm.iloc[1, 0]) / 100,  # height
                alpha=0.1,
                facecolor="yellow", linestyle='dotted'
            )
        )

        ax[2].add_patch(
            patches.Rectangle(
                (-W, (segm.iloc[0, 0] - segm.iloc[1, 0]) / 100),  # (x,y)
                W * 2,  # width
                (segm.iloc[3, 0] - segm.iloc[0, 0]) / 100,  # height
                alpha=0.01,
                facecolor="blue"
            )
        )
        ax[2].add_patch(
            patches.Rectangle(
                (-W, 0),  # (x,y)
                W * 2,  # width
                (segm.iloc[2, 0] - segm.iloc[1, 0]) / 100,  # height
                alpha=0.1,
                facecolor="yellow", linestyle='dotted'
            )
        )

        # Légendes
        fig.suptitle('Rotagram', fontsize=13, weight='bold')
        ax[0].set_xticks([-W, (-W / 2), 0, W / 2, W])
        ax[0].set_xticklabels(['180°', '90°', '0°', '90°', '180°'], fontsize=8)
        ax[0].set_title('Trunk rotation angle (axial plane)', weight='bold', size=10)

        ax[0].tick_params(axis=u'both', which=u'both', length=0)
        e = str(((segm.iloc[2, 0] - segm.iloc[1, 0]) / 100)) + 's.'
        ax[1].tick_params(axis=u'both', which=u'both', length=0)
        ax[1].spines['right'].set_visible(False)
        ax[2].set_yticks(
            [((segm.iloc[0, 0] - segm.iloc[1, 0]) / 100) + 1.1, -0.5, ((segm.iloc[2, 0] - segm.iloc[1, 0]) / 100) / 2,
             ((segm.iloc[2, 0] - segm.iloc[1, 0]) / 100) + 0.5,
             ((segm.iloc[3, 0] - segm.iloc[1, 0]) / 100) - 1.1])
        e = str(((segm.iloc[2, 0] - segm.iloc[1, 0]) / 100)) + 's.'
        ax[2].set_yticklabels(['Gait\nstart', 'U-Turn\nstart', e, 'U-Turn\nend', 'Gait\nend'],
                              fontsize=8)
        ax[2].tick_params(axis=u'both', which=u'both', length=0)
        ax[2].spines['left'].set_visible(False)
        ax[2].yaxis.tick_right()

        ax[0].legend([leg1[0], leg2[0], leg3[0]], ['right', 'left', 'cumulative_angle'])
    
    # save fig
    plt.savefig(fname=("rota.svg"))

    return None
