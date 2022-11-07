import matplotlib.pyplot as plt
from cycler import cycler
import numpy as np
import matplotlib
import argparse


def bind_init_args(parser):
    parser.add_argument('--font_size', default=20, type=int)
    parser.add_argument('--legend_font_size', default=18, type=int)
    parser.add_argument('--tick_size', default=16, type=int)

def set_math_font(remove_type3=False):
    matplotlib.rcParams['mathtext.fontset'] = 'stix'
    matplotlib.rcParams['font.family'] = 'STIXGeneral'

    # Manuscript Central does not support Type 3 PostScript
    # Remove as follows, see http://phyletica.org/matplotlib-fonts/
    if remove_type3:
        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['ps.fonttype'] = 42

#https://stackoverflow.com/questions/11367736/matplotlib-consistent-font-using-latex
def init(font_size=None, legend_font_size=None, modify_cycler=True, tick_size=None, args=None):
    if args:
        font_size = args.font_size
        legend_font_size = args.legend_font_size
        tick_size = args.tick_size
    custom_cycler = (cycler(color=['r', 'b', 'g', 'y', 'k', 'm', 'c']*4) +
                     cycler(linestyle=['-', '--', ':', '-.']*7))
    if modify_cycler: plt.rc('axes', prop_cycle=custom_cycler)
    set_math_font()
    if font_size: matplotlib.rcParams.update({'font.size': font_size})
    if legend_font_size: plt.rc('legend', fontsize=legend_font_size)    # legend fontsize
    # https://stackoverflow.com/questions/3899980/how-to-change-the-font-size-on-a-matplotlib-plot
    if tick_size:
        matplotlib.rcParams['xtick.labelsize'] = tick_size
        matplotlib.rcParams['ytick.labelsize'] = tick_size
    # https://stackoverflow.com/questions/6390393/matplotlib-make-tick-labels-font-size-smaller

def fmt_ax(ax, xlab, ylab, leg, grid=1, grid_kwargs={}):
    if leg: ax.legend(loc='best')
    if xlab: ax.set_xlabel(xlab)
    if ylab: ax.set_ylabel(ylab)
    if grid: ax.grid(alpha=0.7, linestyle='-.', linewidth=0.3, **grid_kwargs)
    ax.tick_params(axis='both')


# https://stackoverflow.com/questions/51323505/how-to-make-relim-and-autoscale-in-a-scatter-plot
def update_datalim(ax, scatter):
    #ax.ignore_existing_data_limits = True
    ax.update_datalim(scatter.get_datalim(ax.transData))
    ax.autoscale_view()

def get_data_setter(ax, obj):
    if isinstance(obj, matplotlib.collections.PathCollection):
        setter = lambda xv, yv: (obj.set_offsets(np.array([xv, yv]).T), update_datalim(ax, obj))
        return obj.get_offsets().T, setter
    elif isinstance(obj, matplotlib.lines.Line2D):
        setter = lambda xv, yv: (obj.set_xdata(xv), obj.set_ydata(yv))
        return (obj.get_xdata(), obj.get_ydata()), setter
    else: return None

def relim_axis(ax, xl=None, xu=None, yl=None, yu=None):
    lim = lambda idx, xv_, yv_: (xv_[idx], yv_[idx])
    ax.ignore_existing_data_limits = True
    for obj in ax.get_children(): # get_lines also works if line plot
        ret = get_data_setter(ax, obj)
        if ret is None: continue
        (xv, yv), setter = ret
        if not xl is None: xv, yv = lim(xv>=xl, xv, yv)
        if not xu is None: xv, yv = lim(xv<=xu, xv, yv)
        if not yl is None: xv, yv = lim(yv>=yl, xv, yv)
        if not yu is None: xv, yv = lim(yv<=yu, xv, yv)
        setter(xv, yv)
        ax.ignore_existing_data_limits = False
    ax.relim(), ax.autoscale_view()

def save_show_fig(args, plt, file_path, tight_layout=True, transparent=False):
    if tight_layout: plt.tight_layout()
    if args.save:
        ext_str = ','.join(args.ext)
        if len(args.ext)>1: ext_str = f'{{{ext_str}}}'
        print(f'Saving figure to {file_path}.{ext_str}')
        for ext in args.ext:
            plt.savefig('%s.%s'%(file_path,ext), bbox_inches='tight', pad_inches=args.pad_inches, transparent=transparent)
    else: plt.show()

def set_ax_props(args, ax):
    if args.hide_ylabel: ax.set_ylabel(None)
    if args.xlog: ax.set_xscale('log')
    if args.ylog: ax.set_yscale('log')
    if not args.xmin is None: ax.set_xlim(left=args.xmin)
    if not args.xmax is None: ax.set_xlim(right=args.xmax)
    if not args.ymin is None: ax.set_ylim(bottom=args.ymin)
    if not args.ymax is None: ax.set_ylim(top=args.ymax)

def bind_plotting_args(parser):
    parser.add_argument('--xmax', type=float)
    parser.add_argument('--xmin', type=float)
    parser.add_argument('--ymin', type=float)
    parser.add_argument('--ymax', type=float)
    parser.add_argument('--xlog', action='store_true')
    parser.add_argument('--ylog', action='store_true')
    parser.add_argument('--hidex', action='store_true')
    parser.add_argument('--hide_ylabel', action='store_true')
    parser.add_argument('--nolegend', action='store_true')
    parser.add_argument('--ax_size', help='width, height {scale} per axis', type=float, nargs='+', action=AxSizeAction, default=[8,5])
    parser.add_argument('--imprv_percentage', type=float, nargs=4, action='append')
    parser.add_argument('--font_size_imprv', type=int, default=20)
    parser.add_argument('--title', type=str)

def plot_improvement(args, ax):
    # plot vertical double arrow lines with an percentage annotation
    if not args.imprv_percentage is None:
        for xval,bot,top,sgn in args.imprv_percentage:
            imprv = int(100*(top-bot)/top)
            ax.annotate(s='', xy=(xval, bot), xytext=(xval, top), arrowprops=dict(arrowstyle='<->'))
            ha = 'right' if sgn<0 else 'left'
            ax.annotate(f'{imprv}%', xy=(xval+np.sign(sgn)*0.2, (top+bot)/2), ha=ha, va='center', size=args.font_size_imprv)

def bind_fig_save_args(parser):
    parser.add_argument('--save', help='save plots', action='store_true')
    exts_ = ['png', 'pdf']
    parser.add_argument('--ext', help='plot save extention', nargs='*', default=exts_, choices=exts_)
    parser.add_argument('--pad_inches', type=float, default=None) # good choice is 0.03

def get_subplot_config(count):
    return {1:(1,1), 2:(1,2), 3:(1,3), 4:(2,2),
            5:(2,3), 6:(2,3),
            7:(3,3), 8:(3,3), 9:(3,3),
            10:(3,4), 11:(3,4), 12:(3,4),
            13:(4,4), 14:(4,4), 15:(4,4), 16:(4,4),
            17:(4,5), 18:(4,5), 19:(4,5), 20:(4,5),
            21:(4,6), 22:(4,6), 23:(4,6), 24:(4,6),
           }[count]

def get_subplot_axes(ax_size, count=None, rows_cols=None, subplots_kwargs=None):
    # ax_size = [width, height] per axis
    # if fig is None: fig = plt.gcf()
    if count is None and rows_cols is None: raise('Incomplete arguments')
    if count is None: count = rows_cols[0]*rows_cols[1]
    if rows_cols is None or rows_cols[0]*rows_cols[1]<count:
        rows_cols = get_subplot_config(count)
    if subplots_kwargs is None: subplots_kwargs = {}
    fig, axes = plt.subplots(*rows_cols, **subplots_kwargs)
    fig.set_size_inches(ax_size[0]*rows_cols[1], ax_size[1]*rows_cols[0])
    # axes = [fig.add_subplot(*rows_cols,idx+1) for idx in range(count)]
    axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]
    return axes[:count], fig

def set_best_time_scale(ax, seconds, label=''):
    if seconds>3600*24 *5: div,unit,steps = 3600*24, 'days', [8.64]
    elif seconds>3600 *5: div,unit,steps = 3600, 'hrs', [9]
    elif seconds>60 *5: div,unit,steps = 60, 'min', [3,6,9]
    elif seconds>1 *1: div,unit,steps = 1, 's', [1,2,3,4,5,10]
    else: div,unit,steps = 1e-3, 'ms', [1,2,4,5,10]

    fmt = plt.FuncFormatter(lambda x,pos:'%g'%(x/div))
    loc = plt.MaxNLocator('auto', steps=steps)
    # hack to get rid of MaxNLocator adding 10 to steps, which results in ugly hour ticks
    # https://stackoverflow.com/questions/62148592/use-matplotlib-ticker-locator-to-put-ticks-only-if-location-is-divisible-by-a-gi
    if unit=='hrs':
        loc._extended_steps = loc._staircase(np.array([0.9, 1.8, 2.7, 3.6, 5.4, 7.2, 9]))
    ax.xaxis.set_major_formatter(fmt)
    ax.xaxis.set_major_locator(loc)
    return f'{label} ({unit})'

# https://stackoverflow.com/questions/4194948/python-argparse-is-there-a-way-to-specify-a-range-in-nargs
class AxSizeAction(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        l_ = len(values)
        if not (0<l_<4):
            msg=f'argument {self.dest} accepts only 1 or 2 or 3 arguments'
            raise parser.error(msg)
        if l_==1: (v1,v2), mul = self.default, values[0]
        if l_==2: (v1,v2), mul = values, 1.
        if l_==3: v1,v2,mul = values
        values = v1*mul,v2*mul
        setattr(args, self.dest, values)
