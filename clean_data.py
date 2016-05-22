import pandas as pd
from collections import defaultdict
import numpy as np


fname = 'Zwolle_routes_dump_wk.201619.csv'

map_codes = {'378': 'F',
            '393': 'E',
            '394': 'B',
            '398': 'I',
            '399': 'A',
            '400': 'J',
            '404': 'G',
            '406': 'C',
            '407': 'D',
            '408': 'L',
            '410': 'H',
            '411': 'K',
            '392': 'T'
}

src_cols = ['Zwolle_bb_01a',
 'Zwolle_bb_01b',
 'Zwolle_bb_02a',
 'Zwolle_bb_02b',
 'Zwolle_bb_03a',
 'Zwolle_bb_03b',
 'Zwolle_bb_04a',
 'Zwolle_bb_04b',
 'Zwolle_bb_05a',
 'Zwolle_bb_05b',
 'Zwolle_bb_06a',
 'Zwolle_bb_06b',
 'Zwolle_bb_07a',
 'Zwolle_bb_07b',
 'Zwolle_bb_08a',
 'Zwolle_bb_08b',
 'Zwolle_bb_09a',
 'Zwolle_bb_09b',
 'Zwolle_bb_11a',
 'Zwolle_bb_11b',
 'Zwolle_bb_12a',
 'Zwolle_bb_12b',
 'Zwolle_bb_13a',
 'Zwolle_bb_13b',
 'Zwolle_bb_14a',
 'Zwolle_bb_14b',
 'Zwolle_bb_15a',
 'Zwolle_bb_15b',
 'Zwolle_bb_16a',
 'Zwolle_bb_16b',
 'Zwolle_bb_17a',
 'Zwolle_bb_17b',
 'Zwolle_bb_18a',
 'Zwolle_bb_18b',
 'Zwolle_bb_19a',
 'Zwolle_bb_19b',
 'Zwolle_bb_20a',
 'Zwolle_bb_20b',
 'Zwolle_bb_21a',
 'Zwolle_bb_21b',
 'Zwolle_bb_22a',
 'Zwolle_bb_22b',
 'Zwolle_bb_23a',
 'Zwolle_bb_23b',
 'Zwolle_bb_24a',
 'Zwolle_bb_24b',
 'Zwolle_bb_25a',
 'Zwolle_bb_25b',
 'Zwolle_bb_26a',
 'Zwolle_bb_26b',
 'Zwolle_bb_27a',
 'Zwolle_bb_27b',
 'Zwolle_bb_28a',
 'Zwolle_bb_28b',
 'Zwolle_bb_29a',
 'Zwolle_bb_29b',
 'Zwolle_bb_30a',
 'Zwolle_bb_30b',
 'Zwolle_bb_31a',
 'Zwolle_bb_31b']

tgt_cols = ['R_vbm399_394',
 'R_vbm394_399',
 'R_vbm321_407',
 'R_vbm407_321',
 'R_vbm394_393',
 'R_vbm393_394',
 'R_vbm394_408',
 'R_vbm408_394',
 'R_vbm408_409',
 'R_vbm409_408',
 'R_vbm409_390',
 'R_vbm390_409',
 'R_vbm390_403',
 'R_vbm403_390',
 'R_vbm389_284',
 'R_vbm284_389',
 'R_vbm390_389',
 'R_vbm389_390',
 'R_vbm389_387',
 'R_vbm387_389',
 'R_vbm387_388',
 'R_vbm388_387',
 'R_vbm388_391',
 'R_vbm391_388',
 'R_vbm391_395',
 'R_vbm395_391',
 'R_vbm391_276',
 'R_vbm276_391',
 'R_vbm276_400',
 'R_vbm400_276',
 'R_vbm391_397',
 'R_vbm397_391',
 'R_vbm392_397',
 'R_vbm397_392',
 'R_vbm388_392',
 'R_vbm392_388',
 'R_vbm392_411',
 'R_vbm411_392',
 'R_vbm411_410',
 'R_vbm410_411',
 'R_vbm411_378',
 'R_vbm378_411',
 'R_vbm393_378',
 'R_vbm378_393',
 'R_vbm378_404',
 'R_vbm404_378',
 'R_vbm404_322',
 'R_vbm322_404',
 'R_vbm410_404',
 'R_vbm404_410',
 'R_vbm410_398',
 'R_vbm398_410',
 'R_vbm398_283',
 'R_vbm283_398',
 'R_vbm393_407',
 'R_vbm407_393',
 'R_vbm407_406',
 'R_vbm406_407',
 'R_vbm406_394',
 'R_vbm394_406']

m = defaultdict(str)
m.update({src: tgt_cols[i] for i, src in enumerate(src_cols)})
trymap = lambda c: m[c] or c


def change_header(h):
    for c, l in map_codes.items():
        h = h.replace(c, l)
    h = h.replace('rt_', '')
    h = trymap(h)
    h = h.replace('R_vbm', '')
    return h


def reshape_data(fname):
    df = pd.read_csv(fname)
    df.columns = [change_header(c) for c in df.columns]

    df = df[df.tijd.dt.day == 12]
    df = df[df.tijd.dt.month == 5]

    fcols = [c for c in cols if len(c) == 3 or c == 'tijd']
    df = df[fcols]

    df = df.replace("\\N",np.nan)
    df[df.columns[1:]] = df[df.columns[1:]].astype(float)

    df.tijd = pd.to_datetime(df.tijd)
    dfg = df.groupby(df.tijd.dt.hour).mean()

    dfg.to_csv('traveltimes_avghourly_2016-05-12.csv')

    df.to_csv('traveltimes_minute_2016-05-12.csv')

    return df

def combine_at_junction(df, junction):
    cols = df.columns
    for c1 in cols:
        for c2 in cols:
            if c1[-1] == junction and c2[0] == junction:
                nc = c1[0] + '_' + c2[-1]
                if nc[0] != nc[-1]:
                    df[nc] = df[c1] + df[c2]
    return df

def reformat_expand_junction_dists():
    df = pd.read_csv('VID-Junction-dist.csv',delimiter=';')
    df['tag'] = df.Tot + '_' + df.Van
    df.index = df.tag
    df = df[['Afstand in m','tag']]
    df = df.transpose()
    df2 = df.iloc[:1,:]

    df = pd.read_csv('VID-Junction-dist.csv',delimiter=';')
    df['tag'] = df.Van + '_' + df.Tot
    df.index = df.tag
    df = df[['Afstand in m','tag']]
    df = df.transpose()
    df3 = df.iloc[:1,:]

    df4 = pd.concat([df2,df3],axis=1)

    for j in ['B','E','K']:
        combine_at_junction(df4,j)
