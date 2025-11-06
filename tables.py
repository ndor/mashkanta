import numpy as np
import pandas as pd
import params
import financials


make_float = lambda x: '{:,.2f}'.format(x)
make_int = lambda x: '{:,}'.format(int(x))


def input_args_to_df(input_dict: dict, language='en', dissregad_key_prefix='_') -> pd.DataFrame:
    d = {}
    for k in input_dict.keys():
        if k.startswith(dissregad_key_prefix):
            continue
        d[params.PARAMETER_LANG_MAP[language]['input_titles'][k]] = [input_dict[k]]
    df = pd.DataFrame.from_dict(d).T
    for i in range(len(df)):
        if type(df.iloc[i, 0]) == int:
            df.iloc[i, 0] = make_int(df.iloc[i, 0])
    df.rename(columns={df.columns[0]: params.PARAMETER_LANG_MAP[language]['tables']['input_parameters']}, inplace=True)
    return df


def df_to_summary_df(total_monthly_payments: pd.DataFrame, language='en') -> pd.DataFrame:
    # avg_yearly_rate = []
    # for k in total_monthly_payments.keys():
    #     if k == 'total':
    #         continue
    #     total_monthly_payments[k]

    df = pd.DataFrame(data=[[make_float(total_monthly_payments['total']['pmt'].sum() /
                                        total_monthly_payments['total']['ppmt'].sum()),
                            make_int(total_monthly_payments['total']['pmt'].sum()),
                            make_int(total_monthly_payments['total']['ipmt'].sum()),
                            make_int(total_monthly_payments['total']['pmt'][0]),
                            make_float(100 * 12 * (total_monthly_payments['total']['pmt'].sum() /
                                        total_monthly_payments['total']['ppmt'].sum()) /
                                       len(total_monthly_payments['total']['pmt'])),
                            make_int(len(total_monthly_payments['total']['pmt'])),
                            make_int(total_monthly_payments['total']['ppmt'].sum())]],
                      columns=params.PARAMETER_LANG_MAP[language]['tables']['summary_df']).T
    df.rename(columns={df.columns[0]: params.PARAMETER_LANG_MAP[language]['tables']['summary_results']}, inplace=True)
    return df


def main_table(input_dict: dict, total_monthly_payments: pd.DataFrame, language='en') -> pd.DataFrame:
    amortizations = input_dict['_amortizations']
    asset_cost = input_dict['asset_cost']
    capital = input_dict['capital']
    principal = asset_cost - capital
    funding_rate = principal / asset_cost
    monthly_rates = financials.update_yearly_to_monthly_rates_with_risk(funding_rate,
                                                                    is_married_couple=input_dict['_is_married_couple'])

    d = {
        'amortization_type': [],
        'rate_type': [],
        'nominal_rate': [],
        'duration': [],
        'monthly_1st_payment': [],
        # 'monthly_max_payment': '',
        'principal': [],
        'principal_portion': [],
        'interest_paid': [],
        'net_paid': [],
        'returned_ratio': [],
        # 'effective_overall_rate': []
    }

    for k in total_monthly_payments.keys():
        if 'total' in k:
            continue

        for a in ['prime', 'madad', 'fixed']:
            if a in k:
                d['rate_type'].append(params.PARAMETER_LANG_MAP[language]['tables']['interest_rate_type'][a])
                for rate in monthly_rates.keys():
                    if a in rate:
                        d['nominal_rate'].append(make_float(12 * 100 * np.average(monthly_rates[rate])))
                        break
                break

        if amortizations > 0:
            d['amortization_type'].append(input_dict['amortizations'])
        else:
            for _a, a in zip(params.PARAMETER_LANG_MAP['en']['input']['amortizations'],
                             params.PARAMETER_LANG_MAP[language]['input']['amortizations']):
                if _a.lower() in k:
                    d['amortization_type'].append(a)
                    break

        d['duration'].append(k.split('_')[-1])
        d['monthly_1st_payment'].append(make_int(total_monthly_payments[k]['pmt'][0]))
        d['principal'].append(make_int(total_monthly_payments[k]['ppmt'].sum()))
        d['principal_portion'].append(make_float(100 * total_monthly_payments[k]['ppmt'].sum() / principal))
        d['interest_paid'].append(make_int(total_monthly_payments[k]['ipmt'].sum()))
        d['net_paid'].append(make_int(total_monthly_payments[k]['pmt'].sum()))
        d['returned_ratio'].append(make_float(total_monthly_payments[k]['pmt'].sum() / total_monthly_payments[k]['ppmt'].sum()))

    df = pd.DataFrame.from_dict(d)
    df.rename(columns=params.PARAMETER_LANG_MAP[language]['tables']['main_df'], inplace=True)
    df = df.T
    df.rename(columns=params.PARAMETER_LANG_MAP[language]['tables']['main_df'], inplace=True)
    return df


if __name__ == '__main__':
    ...