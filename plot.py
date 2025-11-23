import numpy as np
import pandas as pd
import plotly.express as px
import params
import financials


def fix_k(k: str, main_df: pd.DataFrame):
    ki = k.split('_')
    for i in range(1, 3):
        he1 = params.PARAMETER_LANG_MAP['he']['input']['amortizations'][i] == ki[0]
        en1 = params.PARAMETER_LANG_MAP['en']['input']['amortizations'][i].lower() == ki[0]
        if he1 or en1:
            for j in params.PARAMETER_LANG_MAP['he']['tables']['interest_rate_type'].keys():
                he2 = params.PARAMETER_LANG_MAP['he']['tables']['interest_rate_type'][j]
                en2 = params.PARAMETER_LANG_MAP['en']['tables']['interest_rate_type'][j].lower()
                if (he2 == ki[1]) or (en2 == ki[1]):
                    for c in main_df.columns:
                        if (main_df[c].iloc[1].lower() == he2) or (main_df[c].iloc[1].lower() == en2):
                            return c


def payments(total_monthly_payments: dict, main_df: pd.DataFrame, language='he'):
    max_len_df = max(list(map(lambda k: len(total_monthly_payments[k]['ipmt']), total_monthly_payments.keys())))
    df = {}
    for k in sorted(total_monthly_payments.keys()):
        if k == 'total':
            continue
        arr = total_monthly_payments[k]['pmt']
        t = fix_k(k, main_df)
        if len(arr) < max_len_df:
            df[t] = np.pad(arr, (0, max_len_df - len(arr)), constant_values=0)
        else:
            df[t] = arr
    df = pd.DataFrame.from_dict(df)
    key_mapping = dict((k, v) for k, v in zip(range(len(df.columns)), df.columns))
    color_discrete_map = {key_mapping.get(k, k): v for k, v in params.COLOR_DISCRETE_MAP.items()}
    fig = px.bar(df, color_discrete_map=color_discrete_map)
    fig.update_layout(template='plotly_dark',
                      legend={'orientation': 'h',
                              # 'font': {'size': 16},
                              'yanchor': 'top', 'y': 0.99,
                              'xanchor': 'left', 'x': 0.8,
                              'title_text': ''},
                      xaxis={'title': {'text': 'חודשים' if language=='he' else 'Months)'}},
                      yaxis={'title': {'text': 'עלות חודשית ₪' if language=='he' else 'Monthly payment (ILS, ₪'}},
                      title_text='תשלומים לאורך זמן' if language=='he' else 'Payments Over Time',
                      title_x=0.5,
                      title_xanchor='center')
    return fig


def assumptions(input_dict: dict, language='he'):
    loan_principal = input_dict['asset_cost'] - input_dict['capital']
    funding_rate = loan_principal / input_dict['asset_cost']
    df = financials.update_yearly_to_monthly_rates_with_risk(funding_rate, False)
    max_len = max(list(map(lambda k: len(df[k]), df.keys())))
    for k in df.keys():
        _len = len(df[k])
        if _len < max_len:
            df[k] = np.pad(df[k], (0, max_len - _len), mode='constant', constant_values=(0, 0))
    df = pd.DataFrame.from_dict(df) * 12 * 100 # monthly to yearly, decimal to %
    d = {
        'fixed_rate': 'ריבית קבועה' if language=='he' else 'Fixed rate',
        'madad_rate': 'ריבית מדד' if language=='he' else 'Madad rate',
        'prime_rate': 'ריבית פריים' if language=='he' else 'Prime rate',
    }
    df.rename(columns=d, inplace=True)
    key_mapping = dict((k, v) for k, v in zip(range(len(df.columns)), df.columns))
    color_discrete_map = {key_mapping.get(k, k): v for k, v in params.COLOR_DISCRETE_MAP.items()}
    fig = px.line(df, color_discrete_map=color_discrete_map)
    fig.update_layout(template='plotly_dark',
                      legend={'orientation': 'h',
                              # 'font': {'size': 16},
                              'yanchor': 'top', 'y': 0.99,
                              'xanchor': 'left', 'x': 0.8,
                              'title_text': ''},
                      xaxis={'title': {'text': 'חודשים' if language=='he' else 'Months'}},
                      yaxis={'title': {'text': 'ריבית שנתית %' if language=='he' else 'Yearly rate %'}},
                      title_text='מודל ריביות לאורך זמן' if language=='he' else 'Rates Model Over Time',
                      title_x=0.5,
                      title_xanchor='center')
    return fig




if __name__ == '__main__':
    ...
