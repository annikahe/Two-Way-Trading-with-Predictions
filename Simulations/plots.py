import pandas as pd
import matplotlib.pyplot as plt


def error_against_comp_ratio(eta, cr):
    d = {"$\eta$": eta, "return(FtP) / return(OFF)": cr}
    df = pd.DataFrame(data=d)
    df_sorted = df.sort_values('$\eta$')
    df_cleaned = df.groupby('$\eta$').mean().reset_index()

    df_cleaned.plot(x='$\eta$', y='return(FtP) / return(OFF)')