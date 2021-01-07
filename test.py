df_miss['A375'] = df_miss.loc[:, 'A7595':'A135155'].sum(axis=1) + df_miss.loc[:, 'A155A':'A155D'].sum(axis=1)
df_miss['A395'] = df_miss['A375'] - df_miss['A7595']
