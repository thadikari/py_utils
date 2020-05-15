import matplotlib.pyplot as plt
from cycler import cycler
import matplotlib


#https://stackoverflow.com/questions/11367736/matplotlib-consistent-font-using-latex
def init(font_size=None, legend_font_size=None, modify_cycler=True, tick_size=None):
    custom_cycler = (cycler(color=['r', 'b', 'g', 'y', 'k', 'm', 'c']*4) +
                     cycler(linestyle=['-', '--', ':', '-.']*7))
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
        ext_str = ','.join(args.ext)
        if len(args.ext)>1: ext_str = f'{{{ext_str}}}'
        print(f'Saving figure to {file_path}.{ext_str}')
        for ext in args.ext:
            plt.savefig('%s.%s'%(file_path,ext), bbox_inches='tight')
    if not args.silent: plt.show()

def bind_fig_save_args(parser):
    parser.add_argument('--silent', help='do not show plots', action='store_true')
    parser.add_argument('--save', help='save plots', action='store_true')
    exts_ = ['png', 'pdf']
    parser.add_argument('--ext', help='plot save extention', nargs='*', default=exts_, choices=exts_)


def bind_subplot_args(parser, ax_size_default=[4,3]):
    parser.add_argument('--subplot', help='subplot config: rows_cols', default=None, type=int, nargs=2)
    parser.add_argument('--ax_size', help='width, height per axis', type=float, nargs=2, default=ax_size_default)

def get_subplot_config(count):
    return {1:(1,1), 2:(1,2), 3:(1,3), 4:(2,2), 5:(2,3),
            6:(2,3), 7:(3,3), 8:(3,3), 9:(3,3)}[count]

def get_subplot_axes(_a, count, fig=None):
    if fig is None: fig = plt.gcf()
    rows_cols = _a.subplot if _a.subplot else get_subplot_config(count)
    fig.set_size_inches(_a.ax_size[0]*rows_cols[1], _a.ax_size[1]*rows_cols[0])
    axes = [fig.add_subplot(*rows_cols,idx+1) for idx in range(count)]
    return axes, fig

def get_best_time_scale(seconds, label=None):
    if seconds>3600*24 *5: div,unit = 3600*24, 'days'
    elif seconds>3600 *5: div,unit = 3600, 'hrs'
    elif seconds>60 *5: div,unit = 60, 'min'
    else: div,unit = 1,'s'
    if label: return div,unit, f'{label} ({unit})'
    else: return div,unit
