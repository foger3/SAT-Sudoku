import os, pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt
from statannot import add_stat_annotation
import scipy

if not os.path.isdir("figures_paper/"):
    os.makedirs("figures_paper/")

if not os.path.isdir("statistics/"):
    os.makedirs("statistics/")
    
# read csv results 
path_to_results = 'tests_results.txt'
results = pd.read_csv(path_to_results)

#######################################################
###################### Plotting #######################
#######################################################

# @ helper functions
# Boxplot graph
def boxplot(data, performance_measure):
    f, ax = plt.subplots(figsize=(30, 20))
    order = data.heuristic.unique()
    sns.boxplot(x="heuristic", y=performance_measure, data=data, order=order,
                whis=[0, 100], width=.6, palette="vlag")
    sns.stripplot(x="heuristic", y=performance_measure, data=results,
              size=4, color=".3", linewidth=0)
    plt.title(f'Solver performance ({performance_measure})', fontsize = 40)
    plt.xticks(fontsize = 30, rotation = 45)
    plt.yticks(fontsize = 30)
    plt.xlabel('Heuristic', fontsize = 40)
    plt.ylabel(performance_measure, fontsize = 40)
    #if performance_measure == 'duration':
    #    plt.ylim((0, 20))
    #elif performance_measure == 'backtracks':
    #    plt.ylim((0, 5000))
    #annotate with statistical testing
    add_stat_annotation(ax, data=data, x='heuristic', y=performance_measure, order=order,
                    box_pairs=[("DPLL", "JW-OS"), ("DPLL", "JW-TS"), ("DPLL+JW-OS", "DPLL"),
                               ("DPLL+JW-TS", "DPLL"), ("DPLL", "MLV"), ("DPLL", "JW-OS+MLV"),
                               ("DPLL", "JW-OS+MLV"), ("DPLL", "JW-OS+MLV"), ("DPLL", "JW-OS+MLV"),("DPLL", "JW-TS+MLV"), 
                               ("DPLL", "Random+MLV")],
                    test='Wilcoxon', text_format='full', loc='inside', verbose=2)
    
    f.savefig(f'figures_paper/boxplot_{performance_measure}_statsannotation_MW')
    return 


# Frequency graph (with)
def frequency_plot(data, performance_measure):
    if performance_measure == 'duration':
        bin = 'bin_duration'
    elif performance_measure == 'backtracks':
        bin = 'bin_backtrack'
        
    sns.set_theme(style="whitegrid")
    f, ax = plt.subplots(figsize=(15, 6))
    sns.countplot(data= data, x=bin, hue ='heuristic')
    plt.title(f'Solver performance ({performance_measure})', fontsize = 20)
    plt.xticks(rotation = 90)
    f.savefig(f'figures_paper/frequencyplot_{performance_measure}')
    return

# Create bins for the plotting
bins_duration = []
bins_backtrack = []

for duration in results.duration:
    if (duration >= 0) & (duration < 2):
        bins_duration.append('0-2')
    elif (duration >= 2) & (duration < 5):
        bins_duration.append('2-4')
    elif (duration >= 5) & (duration < 7):
        bins_duration.append('4-6')
    elif (duration >= 7) & (duration < 15):
        bins_duration.append('6-8')
    elif (duration >= 15):
        bins_duration.append('8+')

for backtracks in results.backtracks:
    if (backtracks >= 0) & (backtracks < 30):
        bins_backtrack.append('0-30')
    elif (backtracks >= 30) & (backtracks < 60):
        bins_backtrack.append('30-60')
    elif (backtracks >= 60) & (backtracks < 90):
        bins_backtrack.append('60-90')
    elif (backtracks >= 90) & (backtracks < 120):
        bins_backtrack.append('90-120')
    elif (backtracks >= 120):
        bins_backtrack.append('120+')

results['bin_duration'] = bins_duration
results['bin_backtrack'] = bins_backtrack

# generate plots
boxplot(results, 'backtracks')
boxplot(results, 'duration')
frequency_plot(results, 'backtracks')
frequency_plot(results, 'duration')

#######################################################
###################### Statistics #####################
#######################################################

# Get summary of descriptive statistics
results_summary = results.groupby(by='heuristic')[['backtracks', 'duration']].describe() # get descriptive stats, mean/std
results_summary.to_csv('statistics/results_summary.csv')

# Wilcoxon test
heuristics = results.heuristic.unique()
compared_heuristics = []
pvals = []
stats = []

for heuristic_1 in heuristics:
    for heuristic_2 in heuristics:
        if heuristic_1 != heuristic_2:
            res = scipy.stats.wilcoxon(results.loc[results.heuristic == heuristic_1].backtracks,
                                 results.loc[results.heuristic == heuristic_2].backtracks, 
                                 zero_method='wilcox', 
                                 correction=False, 
                                 alternative='two-sided', 
                                 method='auto')
            compared_heuristics.append(heuristic_1 +'&' + heuristic_2)
            pvals.append(res.pvalue)
            stats.append(res.statistic)

stats = pd.DataFrame({'compared_heuristics': compared_heuristics, 
                     'pvalue': pvals, 
                     'statistic' : stats})

# save statistics
stats.to_csv('statistics/Statistics_Wilcoxon_backtracks.csv')

