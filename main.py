import numpy as np
import optimizer
import warnings


warnings.filterwarnings('ignore')


def func(form_input: dict):
    asset_cost = form_input['asset_cost']
    capital = form_input['capital']
    # net_monthly_income = form_input['net_monthly_income']
    max_monthly_payment = form_input['max_monthly_payment']

    amortizations = form_input['_amortizations']
    equal_amortization = False
    if amortizations == 0:
        equal_amortization = None
    elif amortizations == 1:
        equal_amortization = True

    is_married_couple = form_input['is_married_couple']
    # is_single_asset = form_input['is_single_asset'] # TODO: incorporate

    prime = form_input['_prime_portion']
    if prime == 0:
        _prime = None
    elif prime == 1:
        _prime = 1 / 3
    else:
        _prime = 2 / 3

    # mortgage calculation:
    principal = asset_cost - capital
    max_first_payment_fraction = max_monthly_payment / principal
    funding_rate = principal / asset_cost
    optimal_result, net_payments = optimizer.optimize(max_first_payment_fraction,
                                                        funding_rate,
                                                        is_married_couple=is_married_couple,
                                                        equal_amortization=equal_amortization,
                                                        set_prime_portion=_prime)

    # # weighted interest:
    #     # flattening the dict:
    # _optimal_result = {}
    # if any(map(lambda x: any([(y in x) for y in ['prime', 'madad', 'fixed']]), optimal_result.keys())): # single type of amortization
    #     for k1 in optimal_result.keys():
    #         duration = list(optimal_result[k1].keys())[0]
    #         _optimal_result[f'{k1}_{duration}'] = optimal_result[k1][duration]
    # else:
    #     print('===', optimal_result.keys())
    #     for k1 in ['equal_optimal_result', 'spitzer_optimal_result']:
    #         for k2 in optimal_result[k1].keys():
    #             duration = list(optimal_result[k1][k2].keys())[0]
    #             _optimal_result[f'{k1.split("_")[0]}_{k2}_{duration}'] = optimal_result[k1][k2][duration]
    # optimal_result = _optimal_result
    # del _optimal_result

    # weighted interest:
        # flattening the dict:
    _optimal_result = {}
    for k1 in optimal_result.keys():
        for k2 in optimal_result[k1].keys():
            duration = list(optimal_result[k1][k2].keys())[0]
            _optimal_result[f'{k1.split("_")[0]}_{k2}_{duration}'] = optimal_result[k1][k2][duration]
    optimal_result = _optimal_result
    del _optimal_result

    # adding the sum (tot) of amortizations:
    array_length = []
    for k1, v in optimal_result.items():
        array_length.append(int(k1.split('_')[-1]))
    tot_pmt = np.zeros(max(array_length))
    tot_ipmt = np.zeros(max(array_length))
    tot_ppmt = np.zeros(max(array_length))
    for k1, v in optimal_result.items():
        duration = int(k1.split('_')[-1])
        tot_pmt[:duration] = tot_pmt[:duration] + v['pmt']
        tot_ipmt[:duration] = tot_ipmt[:duration] + v['ipmt']
        tot_ppmt[:duration] = tot_ppmt[:duration] + v['ppmt']
    optimal_result['total'] = {'pmt': tot_pmt, 'ipmt': tot_ipmt, 'ppmt': tot_ppmt}

    # updating total_monthly_payments to real cost:
    total_monthly_payments = {}
    for k1 in optimal_result.keys():
        total_monthly_payments[k1] = {}
        for p in ['pmt', 'ipmt', 'ppmt']:
            total_monthly_payments[k1][p] = np.ceil(optimal_result[k1][p] * principal).astype('int32')

    # html_out = beutify_HTML(total_monthly_payments,
    #                         asset_cost,
    #                         capital,
    #                         max_monthly_payment,
    #                         net_monthly_income,
    #                         is_married_couple,
    #                         is_single_asset,
    #                         amortizations,
    #                         prime)
    #
    # new = window.open()
    # new.document.body.innerHTML = html_out
    return optimal_result, total_monthly_payments




if __name__ == '__main__':

    from pprint import PrettyPrinter
    pp = PrettyPrinter().pprint

    asset_cost = 2150000
    capital = 950000
    max_monthly_payment = 20000
    net_monthly_income = 6000
    is_married_couple = False
    equal_amortization = None
    set_prime_portion = 0.333
    principal = asset_cost - capital
    max_first_payment_fraction = max_monthly_payment / principal
    funding_rate = principal / asset_cost

    optimal_result, net_payments = optimizer.optimize(max_first_payment_fraction,
                                                        funding_rate,
                                                        is_married_couple=is_married_couple,
                                                        equal_amortization=equal_amortization,
                                                        set_prime_portion=set_prime_portion)
    pp(optimal_result)

    # # multiplying with finance:
    # optimal_result_finance = {}
    # for k1, v in optimal_result.items():
    #     k2 = list(v.keys())[0]
    #     optimal_result_finance[k1] = np.ceil(v[k2] * principal).astype('int32')
    #     print(optimal_result_finance[k1].shape)
    # print('-'*44)
    # pp(optimal_result_finance)

