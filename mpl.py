import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib


#https://stackoverflow.com/questions/11367736/matplotlib-consistent-font-using-latex
def init(font_size=None, legend_font_size=None, modify_cycler=True, tick_size=None):
    custom_cycler = (cycler(color=['r', 'b', 'g', 'y', 'k']) +
                     cycler(linestyle=['-', '--', ':', '-.', '-']))
    if modify_cycler: plt.rc('axes', prop_cycle=custom_cycler)
    matplotlib.rcParams['mathtext.fontset'] = 'stix'
    matplotlib.rcParams['font.family'] = 'STIXGeneral'
    if font_size: matplotlib.rcParams.update({'font.size': font_size})
    if legend_font_size: plt.rc('legend', fontsize=legend_font_size)    # legend fontsize
    # https://stackoverflow.com/questions/3899980/how-to-change-the-font-size-on-a-matplotlib-plot
    if tick_size:
        matplotlib.rcParams['xtick.labelsize'] = tick_size
        matplotlib.rcParams['ytick.labelsize'] = tick_size
    # https://stackoverflow.com/questions/6390393/matplotlib-make-tick-labels-font-size-smaller

def fmt_ax(ax, xlab, ylab, leg, grid=1):
    if leg: ax.legend(loc='best')
    if xlab: ax.set_xlabel(xlab)
    if ylab: ax.set_ylabel(ylab)
    if grid: ax.grid(alpha=0.7, linestyle='-.', linewidth=0.3)
    ax.tick_params(axis='both')

def save_show_fig(args, plt, file_path):
    plt.tight_layout()
    if args.save:
        for ext in args.ext:
            plt.savefig('%s.%s'%(file_path,ext), bbox_inches='tight')
    if not args.silent: plt.show()

def bind_fig_save_args(parser):
    parser.add_argument('--silent', help='do not show plots', action='store_true')
    parser.add_argument('--save', help='save plots', action='store_true')
    exts_ = ['png', 'pdf']
    parser.add_argument('--ext', help='plot save extention', nargs='*', default=exts_, choices=exts_)
