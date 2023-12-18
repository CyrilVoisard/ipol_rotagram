# Objective : Plot and save the rotagram.

from matplotlib import patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def rotagram(steps_lim_bis, segm, signal_tr, output):
    segm = pd.DataFrame(segm)
    os.chdir(output)
    # Définition de la figure et des couleurs
    fig, ax = plt.subplots(1, 3, gridspec_kw={'width_ratios': [20, 1, 1]}, figsize=(12, 10))
    plt.ion()
    ax[1].set_title(' Durée', fontsize=10)
    ax[2].set_title('d\'appui', fontsize=10)
    ax[0].set_yticks([])
    ax[1].set_yticks([])
    ax[1].set_xticks([0])
    ax[2].set_xticks([0])
    ax[1].set_xticklabels(['Pied\ngauche'], fontsize=8, horizontalalignment='center')
    ax[2].set_xticklabels(['Pied\ndroit'], fontsize=8, horizontalalignment='center')

    color_r, line_r = 'blue', '-'
    color_l, line_l = 'red', '-'

    # Un tableau pour le pied droit, un pour le pied gauche
    step_r = steps_lim_bis[steps_lim_bis["Foot"]== 1]
    step_l = steps_lim_bis[steps_lim_bis["Foot"] == 0]

    t = ((signal_tr.iloc[:, 0] - signal_tr.iloc[0, 0]) - segm.iloc[1, 0]) / 100
    sc = - signal_tr.iloc[:, 8]  # Le négatif sert à avoir la droite en haut

    # Courbe cumulée noire fine
    courbe_fine = np.cumsum(sc[segm.iloc[1, 0] - 100: segm.iloc[2, 0] + 100])
    coef = np.sign(courbe_fine.iloc[-1])* 180 / courbe_fine.iloc[-1]
    courbe_fine = np.sign(courbe_fine.iloc[-1]) * courbe_fine * 180 / courbe_fine.iloc[-1]
    leg3 = ax[0].plot(courbe_fine, t[segm.iloc[1, 0] - 100: segm.iloc[2, 0] + 100], 'k')

    W = abs(min(courbe_fine))
    W1 = abs(max(courbe_fine))
    if W1 > W:
        W = W1
    W = max(abs(courbe_fine))

    if max(courbe_fine) > 100:
        ax[0].annotate('Demi tour vers la droite', xy=(2, 1), xytext=(30, (-1)), fontsize=10)
    else:
        ax[0].annotate('Demi tour vers la gauche', xy=(2, 1), xytext=(-W + 30, (-1)), fontsize=10)


    # Plot de la rotation
    for y in range(len(step_r)):
        print("test", step_r["HS"][y], step_r["TO"][y])
        print("test", segm.iloc[3, 0])
        if (step_r.iloc[y, 3] < segm.iloc[3, 0]):
            # Premier plot
            leg_rf = ([step_r["HS"][y], step_r["TO"][y]] - segm.iloc[1, 0]) / 100
            leg1 = ax[2].plot([0, 0], leg_rf, line_r, linewidth=3, color=color_r)

            ax[0].plot(np.cumsum(sc[int(step_r["HS"][y]):int(step_r["TO"][y])]) * coef,
                       t[int(step_r["HS"][y]):int(step_r["TO"][y])],
                       line_r, linewidth=3, color=color_r)

    for y in range(len(step_l)):
        if (step_l.iloc[y, 3] < 2*segm.iloc[3, 0]):
            leg_lf = ([step_l.iloc[y, 2]  - len(signal_tr), step_l.iloc[y, 3] - len(signal_tr)] - segm.iloc[1, 0]) / 100
            leg2 = ax[1].plot([0, 0], leg_lf, line_r, linewidth=3, color=color_l)

            print("len", len(t), int(step_l.iloc[y, 2]),int(step_l.iloc[y, 3]), len(sc[int(step_l.iloc[y, 2] - len(signal_tr)):int(step_l.iloc[y, 3] - len(signal_tr))]), len(leg_lf))
            print(np.cumsum(sc[int(step_l.iloc[y, 2] - len(signal_tr)):int(step_l.iloc[y, 3] - len(signal_tr))]) * coef)
            print(t[int(step_l.iloc[y, 2] - len(signal_tr)):int(step_l.iloc[y, 3] - len(signal_tr))])

            ax[0].plot(np.cumsum(sc[int(step_l.iloc[y, 2] - len(signal_tr)):int(step_l.iloc[y, 3] - len(signal_tr))]) * coef,
                       t[int(step_l.iloc[y, 2] - len(signal_tr)):int(step_l.iloc[y, 3] - len(signal_tr))],
                       line_l, linewidth=3, color=color_l)

        # Coloration des aires de la figure
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
        # ax[0].title("Angle de rotation du tronc" + ref, fontsize=12)
        axd = ax[0].twiny()
        ax[0].set_xticks([-W, (-W / 2), 0, W / 2, W])
        # ax[0].set_xticklabels(['Demi-tour vers la gauche','Demi-tour vers la droite'], fontsize=8)
        ax[0].set_xticklabels(['180°', '90°', '0°', '90°', '180°'], fontsize=8)
        axd.set_xlim(ax[0].get_xlim())
        axd.set_xticks([0])
        axd.set_xticklabels(['Angle de rotation du tronc'])

        ax[0].tick_params(axis=u'both', which=u'both', length=0)
        # ax[0].set_yticks([((segm[0] - segm[1]) / 100)+1.1, -0.5,((segm[2] - segm[1]) / 100)/2,((segm[2] - segm[1]) / 100)+0.5,((segm[3] - segm[1]) / 100)-1.1])
        e = str(((segm.iloc[2, 0] - segm.iloc[1, 0]) / 100)) + 's.'
        #  ax[0].set_yticklabels(['Debut\nde la\nmarche','Debut \ndemi-tour',e,'Fin\ndemi-tour','Fin\nde la\nmarche'], fontsize=8)
        # # ax[0].set_ylabel('Pied gauche'),rotation=90
        ax[1].tick_params(axis=u'both', which=u'both', length=0)
        ax[0].spines['left'].set_visible(False)
        ax[1].spines['left'].set_visible(False)
        ax[2].set_yticks(
            [((segm.iloc[0, 0] - segm.iloc[1, 0]) / 100) + 1.1, -0.5, ((segm.iloc[2, 0] - segm.iloc[1, 0]) / 100) / 2,
             ((segm.iloc[2, 0] - segm.iloc[1, 0]) / 100) + 0.5,
             ((segm.iloc[3, 0] - segm.iloc[1, 0]) / 100) - 1.1])
        e = str(((segm.iloc[2, 0] - segm.iloc[1, 0]) / 100)) + 's.'
        ax[2].set_yticklabels(['Debut\nde la\nmarche', 'Debut\ndemi-tour', e, 'Fin\ndemi-tour', 'Fin\nde la\nmarche'],
                              fontsize=8)
        ax[2].tick_params(axis=u'both', which=u'both', length=0)
        ax[2].spines['left'].set_visible(False)
        ax[2].yaxis.tick_right()

        # ax.set_title('U-Turn Rotagram for ' + ref, fontsize=16)
        # ax.legend([leg1[0], leg2[0], leg3[0]], ['right', 'left', 'cumulative_angle'])

        # fig.set_size_inches(20, 12)

    # On est déjà dans le bon répertoire
    plt.show()
    plt.ioff()
    plt.savefig(fname=("rota.svg"))

    return None
