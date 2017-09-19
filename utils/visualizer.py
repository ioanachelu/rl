import matplotlib.patches as patches
import matplotlib.pylab as plt
import mpl_toolkits.mplot3d.axes3d as axes3d
import plotly.plotly as py
import plotly.tools as tls
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from matplotlib import cm
import tensorflow as tf
from configs import sf_flags
import os
FLAGS = tf.app.flags.FLAGS

class Visualizer:
    def __init__(self, environment):
        self.env = environment
        self.outputPath = os.path.join(FLAGS.draw_dir, FLAGS.algorithm)

        self.numRows, self.numCols = self.env.nb_cols,  self.env.nb_rows
        self.matrixMDP = self.env.MDP

    def plotBasisFunctions(self, eigenvalues, eigenvectors):
        '''3d plot of the basis function. Right now I am plotting eigenvectors,
           so each coordinate of the eigenvector correspond to the value to be
           plotted for the correspondent state.'''
        for i in range(len(eigenvalues)):
            # fig1 = plt.figure()
            # ax1 = fig1.add_subplot(111)
            #
            # ax1.set_title('Simple Heatmap with matplotlib and plotly')
            #
            # plotly_fig = tls.mpl_to_plotly(fig1)
            # Z = eigenvectors[:, i].reshape(self.numCols, self.numRows)
            # plotly_fig['data'] = [dict(z=Z, type="heatmap", zmin=np.min(Z), zmax=np.max(Z), colorscale='Viridis')]
            # plotly_fig['layout']['xaxis'].update({'autorange': True})
            # plotly_fig['layout']['yaxis'].update({'autorange': True})
            #
            # plot_url = py.plot(plotly_fig, filename='mpl-basic-heatmap')
            Z = eigenvectors[:, i].reshape(self.numCols, self.numRows)
            # fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
            X, Y = np.meshgrid(np.arange(self.numRows), np.arange(self.numCols))


            for ii in range(len(X)):
                for j in range(int(len(X[ii]) / 2)):
                    tmp = X[ii][j]
                    X[ii][j] = X[ii][len(X[ii]) - j - 1]
                    X[ii][len(X[ii]) - j - 1] = tmp

            new_Z = Z[X][Y]
            plt.pcolor(X, Y, Z, cmap=cm.Blues)

            # my_col = cm.jet(np.random.rand(Z.shape[0], Z.shape[1]))

            # surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
            #                 cmap=cm.Blues, linewidth=0, antialiased=False)
            # ax.zaxis.set_major_locator(LinearLocator(10))
            # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
            # Add a color bar which maps values to colors.
            # fig.colorbar(surf, shrink=0.5, aspect=5)

            # plt.gca().view_init(elev=30, azim=30)
            plt.savefig(os.path.join(self.outputPath, ("Eigenvector" + str(i) + '_eig' + '.png')))
            plt.close()

        plt.plot(eigenvalues, 'o')
        plt.savefig(self.outputPath + 'eigenvalues.png')

    def plotValueFunction(self, valueFunction, prefix):
        '''3d plot of a value function.'''
        fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
        X, Y = np.meshgrid(np.arange(self.numCols), np.arange(self.numRows))
        Z = valueFunction.reshape(self.numRows, self.numCols)

        for i in range(len(X)):
            for j in range(int(len(X[i]) / 2)):
                tmp = X[i][j]
                X[i][j] = X[i][len(X[i]) - j - 1]
                X[i][len(X[i]) - j - 1] = tmp

        my_col = cm.jet(np.random.rand(Z.shape[0], Z.shape[1]))

        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                        cmap=plt.get_cmap('jet'))
        plt.gca().view_init(elev=30, azim=30)
        plt.savefig(self.outputPath + prefix + 'value_function.png')
        plt.close()

    def plotPolicy(self, policy, prefix):
        plt.clf()
        for idx in range(len(policy)):
            i, j = self.env.get_state_xy(idx)

            dx = 0
            dy = 0
            if policy[idx] == 0:  # up
                dy = 0.35
            elif policy[idx] == 1:  # right
                dx = 0.35
            elif policy[idx] == 2:  # down
                dy = -0.35
            elif policy[idx] == 3:  # left
                dx = -0.35
            elif self.matrixMDP[i][j] != -1 and policy[idx] == 4:  # termination
                circle = plt.Circle(
                    (j + 0.5, self.numRows - i + 0.5 - 1), 0.025, color='k')
                plt.gca().add_artist(circle)

            if self.matrixMDP[i][j] != -1:
                plt.arrow(j + 0.5, self.numRows - i + 0.5 - 1, dx, dy,
                          head_width=0.05, head_length=0.05, fc='k', ec='k')
            else:
                plt.gca().add_patch(
                    patches.Rectangle(
                        (j, self.numRows - i - 1),  # (x,y)
                        1.0,  # width
                        1.0,  # height
                        facecolor="gray"
                    )
                )

        plt.xlim([0, self.numCols])
        plt.ylim([0, self.numRows])

        for i in range(self.numCols):
            plt.axvline(i, color='k', linestyle=':')
        plt.axvline(self.numCols, color='k', linestyle=':')

        for j in range(self.numRows):
            plt.axhline(j, color='k', linestyle=':')
        plt.axhline(self.numRows, color='k', linestyle=':')

        plt.savefig(self.outputPath + prefix + 'policy.png')
        plt.close()

    def plotLine(self, x_vals, y_vals, x_label, y_label, title, filename=None):
        plt.clf()

        plt.xlabel(x_label)
        plt.xlim(((min(x_vals) - 0.5), (max(x_vals) + 0.5)))
        plt.ylabel(y_label)
        plt.ylim(((min(y_vals) - 0.5), (max(y_vals) + 0.5)))

        plt.title(title)
        plt.plot(x_vals, y_vals, c='k', lw=2)
        # plt.plot(x_vals, len(x_vals) * y_vals[0], c='r', lw=2)

        if filename == None:
            plt.show()
        else:
            plt.savefig(self.outputPath + filename)
