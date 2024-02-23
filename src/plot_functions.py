import matplotlib.pyplot as plt
import seaborn as sns
import random

def plot_sud_dist(data):
    
    random.seed(1)
    colors = random.sample(sns.color_palette('pastel'),10)+['plum']
    cat_to_color = dict(zip(list(data.keys()), colors))
    
    colors = [cat_to_color[v] for v in data.keys()]
    
    plt.subplots(figsize=(8,20))
    explode = (0.01,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1)
    plt.pie(data.values(),
            labels = data.keys(),
            explode=explode,
            colors=colors,
#             autopct='%1.2f%%',
#             shadow=False,
#             startangle=45,
#             textprops={'fontsize':14}
           )
    plt.xticks(size=16)
    plt.show()

    
colors = [
    '#56b3e9',
    '#0071b2',
    '#f0e442',
#     '#e69d00',
#     '#009e74', 
    '#808080',
#     '#d55c00',
    '#cc79a7', 
#     '#000000'
]
# colors = sns.color_palette('rocket_r')

def plot_error_perf(ax, data):
    g = sns.histplot(data=data, x='substance', weights='performance score', hue='metrics',
                     multiple='stack', palette=colors, binwidth=.9, edgecolor='w',linewidth=2,
                     ax=ax)
    for c in g.containers:
        labels = [round(v.get_height(),2) if v.get_height() > 0 else '' for v in c]

        g.bar_label(c,labels=labels, label_type='center', size=8)


    # plt.legend(loc = 'center right', prop = {'size':10})
    ax.set_xticks(range(0,11), labels=substance_group, fontsize=10, rotation=90)
    ax.set_yticks(range(0,110,10), labels=range(0,110,10), fontsize=10)

    # plt.xlim(range(11), substance_group)
    ax.set_ylabel(f'\nnote (with information) count (%)', fontsize=11)
    ax.set_xlabel(f'\nsubstance use disorder category', fontsize=11)

    sns.move_legend(g, 'upper left', title=None,
                   bbox_to_anchor=(.11,1.01), ncol=2,
                    frameon=True, facecolor='w')
    plt.setp(ax.get_legend().get_texts(), fontsize='8')
#     plt.show()


plt.subplots_adjust(hspace=5, wspace=5)

# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(19, 12))

fig = plt.figure(figsize=(12, 8))

ax1 = plt.subplot(1,2,1)
ax2 = plt.subplot(1,2,2)
axes=[ax1,ax2]

plot_error_perf(axes[0],dfPerfList_llm_all)
plot_error_perf(axes[1],dfPerfList_rule_all)

axes[0].text(-0.12, 1.1, 'a', ha='left', va='top', transform=axes[0].transAxes, fontsize=14, weight='bold')
axes[1].text(-0.12, 1.1, 'b', ha='left', va='top', transform=axes[1].transAxes, fontsize=14, weight='bold')

plt.tight_layout()
plt.show()


# fig.savefig(f"/SUD-Extract-LLM/FIGURES/error_perf.pdf",
#             format='pdf', dpi=600,
#             bbox_inches='tight'
#            )
# fig.savefig(f"/SUD-Extract-LLM/FIGURES/error_perf.svg",
#             format='svg', dpi=600,
#             bbox_inches='tight'
#            )



fig = plt.figure(figsize=(6,6))

colors = [
    '#56b3e9',
    '#f0e442',
    '#009e74', 
    '#e69d00',
    '#0071b2',
    '#808080',
#     '#d55c00',
#     '#cc79a7', 
#     '#000000'
]

ax = sns.histplot(data=df_pred_ct, x='substance', weights='note count', hue='candidate answer count',
                 multiple='stack', palette=colors, binwidth=1, edgecolor='w',linewidth=1
                 )
for c in ax.containers:
    labels = [round(v.get_height(), 2) if v.get_height() > 0 else '' for v in c]
    
    ax.bar_label(c,labels=labels, label_type='center', size=8)

    
# plt.legend(loc = 'center right', prop = {'size':8})
plt.xticks(fontsize=10, rotation=90)
plt.yticks(fontsize=10)

# plt.xlim(range(11), substance_group)
plt.ylabel(f'note count (%)', fontsize=11)
plt.xlabel(f'substance use disorder category', fontsize=11)

sns.move_legend(ax, 'upper right')

plt.setp(ax.get_legend().get_texts(), fontsize='9')
plt.setp(ax.get_legend().get_title(), fontsize='9')

plt.show()


# fig.savefig(f"/SUD-Extract-LLM/FIGURES/candidateans_count.pdf",
#             format='pdf', dpi=600,
#             bbox_inches='tight'
#            )
# fig.savefig(f"/SUD-Extract-LLM/FIGURES/candidateans_count.svg",
#             format='svg', dpi=600,
#             bbox_inches='tight'
#            )



def plot_perf(ax, which_score):
    
    width=.4
    ind=np.arange(len(df_llm))

    ax.barh(ind, df_llm[f'{which_score}_f1'], width, color = colors[0], label='LLM', linewidth=1, edgecolor='w')
    ax.barh(ind+width, df_rule[f'{which_score}_f1'],  width, color = colors[1], label='RegEx', linewidth=1, edgecolor='w')

    for p in ax.patches:
        percentage = '{:.2f}%'.format(p.get_width())
        x = p.get_x() + p.get_width() + .85
        y = p.get_y() + p.get_height() -.04
        perc_text = percentage
        ax.annotate(perc_text, (x,y),
                    fontsize=6)

    ax.set_yticks([x+width/2 for x in range(0,11)], substance_group, fontsize=10)
    ax.legend(loc = 'center right', prop = {'size':8})
    if which_score=='relaxed':
        ax.set_xticks(range(0,101,10), range(0,101,10), fontsize=10)
    else:
        ax.set_xticks(range(0,90,10), range(0,90,10), fontsize=10)
    ax.set_xlabel(f'F1-score ({which_score} match)', fontsize=11)
    ax.set_ylabel(f'substance use disorder category', fontsize=11)
    ax.invert_yaxis()

    
    
fig, ax = plt.subplots(1, figsize=(8, 4), constrained_layout=True)

# which_score = 'strict'
# plot_perf(ax, which_score)
# plt.show()

which_score = 'relaxed'
plot_perf(ax, which_score)
plt.show()

# fig.savefig(f"/SUD-Extract-LLM/FIGURES/result_llm_rule_{which_score}f1.pdf",
#             format='pdf', dpi=600,
#             bbox_inches='tight'
#            )
# fig.savefig(f"/SUD-Extract-LLM/FIGURES/result_llm_rule_{which_score}f1.svg",
#             format='svg', dpi=600,
#             bbox_inches='tight'
#            )


plt.subplots_adjust(hspace=3, wspace=5)

fig, axes = plt.subplots(2, figsize=(8, 8), constrained_layout=True)


colors = [
    '#0071b2',
    '#f0e442',
]


which_score = 'strict'
plot_perf(axes[0], which_score)
axes[0].text(-0.52, 1.1, 'a', ha='left', va='top', transform=axes[0].transAxes, fontsize=15, weight='bold')

which_score = 'relaxed'
plot_perf(axes[1], which_score)
axes[1].text(-0.52, 1.1, 'b', ha='left', va='top', transform=axes[1].transAxes, fontsize=15, weight='bold')

plt.show()


# fig.savefig(f"/SUD-Extract-LLM/FIGURES/result_llm_rule.pdf",
#             format='pdf', dpi=600,
#             bbox_inches='tight'
#            )
# fig.savefig(f"/SUD-Extract-LLM/FIGURES/result_llm_rule.svg",
#             format='svg', dpi=600,
#             bbox_inches='tight'
#            )



