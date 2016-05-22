import networkx as nx
import pandas as pd
from networkx.algorithms.centrality import betweenness_centrality
import matplotlib.pyplot as plt

def load_dists():
    tags, dists = [x.split(',') for x in open('../data/CleanData/VID-Junction-dist_reformatted.csv').readlines()]
    tags = [t.strip() for t in tags]
    return {tag: float(dists[i]) for i, tag in enumerate(tags) if len(tag) == 3}


def load_data():
    df = pd.read_csv('../data/CleanData/traveltimes_all_2014_15_16.csv')
    week = [pd.datetime.strptime(d, "%Y-%m-%d") for d in ['2016-05-09','2016-05-17']]
    kings_dayn = pd.datetime.strptime('2016-04-28', "%Y-%m-%d")
    kings_day = pd.datetime.strptime('2016-04-27', "%Y-%m-%d")

    df.tijd = pd.to_datetime(df.tijd)
    # df_kings = df[(df.tijd >= kings_day) & (df.tijd < kings_dayn)]
    
    df_week = df[(df.tijd >= week[0]) & (df.tijd < week[1])]
    # df = pd.concat([df_kings, df_week])
    # df = df_kings
    df = df_week

    dists = load_dists()
    routes = [c for c in df.columns if len(c) == 3]
    for c in routes:
        if c in dists:
            df[c] = df[c]/dists[c]
        else:
            del df[c]

    return df


def build_graph(row):
    g = nx.DiGraph()

    junctions = list('ABCDEFGHIJKLT')
    for a in junctions:
        for b in junctions:
            tag = '%s_%s' % (a,b)
            if tag in row:
                g.add_edge(a, b, weight=row[tag])

    return g


def create_centrality_df(df):
    centrs_dict = {}
    for i, row in df.iterrows():
        G = build_graph(row)
        centrs = betweenness_centrality(G, weight='weight')
        centrs_dict[row['tijd']] = centrs

    dfcentr = pd.DataFrame(centrs_dict).transpose()
    return dfcentr

if __name__ == '__main__':
    df = load_data()
    dfc = create_centrality_df(df)
    dfc.plot()
    plt.show()    

