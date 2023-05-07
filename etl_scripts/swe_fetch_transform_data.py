
import requests
import io
import pandas as pd

url = 'https://api.scb.se/OV0104/v1/doris/sv/ssd/START/NR/NR0001/Konjunkturklockan'

myobj = {
  "query": [],
  "response": {
    "format": "csv"
  }
}

reply = requests.post(url, json = myobj)
df_kk_raw = pd.read_csv(io.StringIO(reply.text))

df_kk_cur_raw = df_kk_raw[[i for i in df_kk_raw.columns if 'läge' in i or 'indikator' in i ]]
df_kk_chg_raw = df_kk_raw[[i for i in df_kk_raw.columns if 'Förändring' in i or 'indikator' in i ]]

df_kk_cur = df_kk_cur_raw.T
df_kk_cur.rename(columns=df_kk_cur.iloc[0], inplace = True)
df_kk_cur.drop(df_kk_cur.index[0], inplace = True)

df_kk_cur = df_kk_cur.reset_index().rename(columns={'index':'date'})

df_kk_cur['date'] = pd.to_datetime(df_kk_cur.date.str.replace("Konjunkturläge ","").str.replace("M","-"))

df_kk_cur = df_kk_cur.set_index('date').apply(pd.to_numeric, errors='coerce', downcast='float', axis=1)

df_kk_chg = df_kk_chg_raw.T
df_kk_chg.rename(columns=df_kk_chg.iloc[0], inplace = True)
df_kk_chg.drop(df_kk_chg.index[0], inplace = True)

df_kk_chg = df_kk_chg.reset_index().rename(columns={'index':'date'})

df_kk_chg['date'] = pd.to_datetime(df_kk_chg.date.str.replace("Förändring från föregående period ","").str.replace("M","-"))

df_kk_chg = df_kk_chg.set_index('date').apply(pd.to_numeric, errors='coerce', downcast='float', axis=1)

df_kk_chg = df_kk_chg.rename(columns=dict([(i, i.replace(" ","_").replace("-","_")) for i in df_kk_chg.columns]))
df_kk_cur = df_kk_cur.rename(columns=dict([(i, i.replace(" ","_").replace("-","_")) for i in df_kk_cur.columns]))

df_kk_chg_melt = pd.melt(df_kk_chg, ignore_index=False).rename(columns=dict(value='direction')).reset_index()
df_kk_cur_melt = pd.melt(df_kk_cur, ignore_index=False).rename(columns=dict(value='current')).reset_index()

df_kk_all = df_kk_chg_melt.merge(df_kk_cur_melt, left_on=['variable', 'date'], right_on=['variable', 'date'])

fname = "../../data/swe_bcycle_data.pkl"
df_kk_all.to_pickle(fname)
