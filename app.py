import pandas as pd
import streamlit as st
import params
import tables
import plot
import main

# if 'language_key' not in st.session_state:
#     st.session_state['language_key'] = 'he'
# if 'funding' not in st.session_state:
#     st.session_state['funding'] = params.MAX_FUNDING_RATE_FOR_FIRST_APPARTMENT
# if 'asset_cost' not in st.session_state:
#     st.session_state['asset_cost'] = int(1e5)
# if 'capital' not in st.session_state:
#     st.session_state['capital'] = int((1 - st.session_state['funding']) * st.session_state['asset_cost'])


langs = list(sorted(params.LANGS.keys()))


st.set_page_config(layout='wide')


def set_language():
    st.session_state['language_key'] = params.LANGS[st.sidebar.segmented_control(None,
                                                                                 default=langs[1],
                                                                                 options=langs,
                                                                                 selection_mode='single',
                                                                                 key='language')]


def set_amortizations():
    st.sidebar.segmented_control(
        params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input_titles']['amortizations'],
        default=params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input']['amortizations'][0],
        options=params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input']['amortizations'],
        selection_mode='single', key='amortizations')


def set_is_married_couple():
    st.sidebar.segmented_control(
        params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input_titles']['is_married_couple'],
        default=params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input']['is_married_couple'][0],
        options=params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input']['is_married_couple'],
        selection_mode='single', key='is_married_couple')


def set_is_single_asset():
    st.sidebar.segmented_control(
        params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input_titles']['is_single_asset'],
        default=params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input']['is_single_asset'][1],
        options=params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input']['is_single_asset'],
        selection_mode='single', key='is_single_asset')

    if (params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input']['is_single_asset']
        .index(st.session_state['is_single_asset']) == 0):
        st.session_state['funding'] = params.MAX_FUNDING_RATE_FOR_NON_FIRST_APPARTMENT
    else:
        st.session_state['funding'] = params.MAX_FUNDING_RATE_FOR_FIRST_APPARTMENT


def set_prime_portion():
    st.sidebar.segmented_control(
        params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input_titles']['prime_portion'],
        default=params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input']['prime_portion'][0],
        options=params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input']['prime_portion'],
        selection_mode='single', key='prime_portion')


def set_asset_cost():
    st.sidebar.number_input(
        params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input_titles']['asset_cost'],
        min_value=int(1e5), max_value=int(1e8), value='min', step=1000, placeholder=None, key='asset_cost',
        format=params.NUMERICAL_FORMAT)


def set_capital():
    st.sidebar.number_input(
        params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input_titles']['capital'],
        min_value=int((1 - st.session_state['funding']) * st.session_state['asset_cost']),
        max_value=st.session_state['asset_cost'], value='min', step=1000, placeholder=None, key='capital',
        format=params.NUMERICAL_FORMAT)


def set_net_monthly_income():
    st.sidebar.number_input(
        params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input_titles']['net_monthly_income'],
        min_value=int(3 * params.max_monthly_payment(st.session_state['asset_cost'], st.session_state['capital'])), # 30 years of net monthly income
        max_value=st.session_state['asset_cost'] // (12 * 5), value='min', step=10, placeholder=None, key='net_monthly_income',
        format=params.NUMERICAL_FORMAT)


def set_max_monthly_payment():
    st.sidebar.number_input(
        params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input_titles']['max_monthly_payment'],
        min_value=int(params.max_monthly_payment(st.session_state['asset_cost'], st.session_state['capital'])), # 30 years of net monthly income
        max_value=st.session_state['net_monthly_income'] // 3, value='min', step=10, placeholder=None, key='max_monthly_payment',
        format=params.NUMERICAL_FORMAT)


def prep_input():
    return {
        'asset_cost': st.session_state['asset_cost'],
        'capital': st.session_state['capital'],
        'net_monthly_income': st.session_state['net_monthly_income'],
        'max_monthly_payment': st.session_state['max_monthly_payment'],
        'is_married_couple': st.session_state['is_married_couple'],
        'is_single_asset': st.session_state['is_single_asset'],
        'amortizations': st.session_state['amortizations'],
        'prime_portion': st.session_state['prime_portion'],
        '_amortizations': params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input']['amortizations']
                                                                            .index(st.session_state['amortizations']),
        '_prime_portion': params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input']['prime_portion']
                                                                            .index(st.session_state['prime_portion']),
        '_is_married_couple': params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input']['is_married_couple']
                                                                    .index(st.session_state['is_married_couple']) == 1,
    }


def display_tables(input_dict: dict, total_monthly_payments: dict):
    input_df = tables.input_args_to_df(input_dict, language=st.session_state['language_key'])
    summary_df = tables.df_to_summary_df(total_monthly_payments, language=st.session_state['language_key'])
    main_df = tables.main_table(input_dict, total_monthly_payments, language=st.session_state['language_key'])
    col1, col2, col3 = st.columns(3)
    with col1:
        st.dataframe(input_df, hide_index=False, use_container_width=True)
    with col2:
        st.dataframe(summary_df, hide_index=False, use_container_width=True)
    with col3:
        st.dataframe(main_df, hide_index=False, use_container_width=True)
    return main_df


def display_plots(input_dict: dict, total_monthly_payments: dict, main_df: pd.DataFrame):
    fig = plot.payments(total_monthly_payments, main_df, language=st.session_state['language_key'])
    st.plotly_chart(fig, use_container_width=True)
    fig = plot.assumptions(input_dict, language=st.session_state['language_key'])
    st.plotly_chart(fig, use_container_width=True)


def display_result():
    input_dict = prep_input()
    msg = 'מחשב...' if st.session_state['language_key'] == 'he' else 'Calculating...'
    with st.spinner(text=msg):
        optimal_result, total_monthly_payments = main.func(input_dict)
    main_df = display_tables(input_dict, total_monthly_payments)
    display_plots(input_dict, total_monthly_payments, main_df)


def waiver():
    st.html(params.PARAMETER_LANG_MAP[st.session_state['language_key']]['waiver'])


def project_info():
    # if st.session_state['language_key'] == 'he':
    #     rtl_style = """
    #     <style>
    #     body, html {
    #         direction: RTL;
    #         unicode-bidi: bidi-override;
    #         text-align: right;
    #     }
    #     p, div, input, label, h1, h2, h3, h4, h5, h6 {
    #         direction: RTL;
    #         unicode-bidi: bidi-override;
    #         text-align: right;
    #     }
    #     </style>
    #     """
    # st.html(rtl_style)
    # #     # st.markdown(rtl_style, unsafe_allow_html=True)
    # # st.html(params.PARAMETER_LANG_MAP[st.session_state['language_key']]['info'][0])
    # # st.divider()
    # # st.html(params.PARAMETER_LANG_MAP[st.session_state['language_key']]['info'][1])
    # # st.divider()
    # # st.html(params.PARAMETER_LANG_MAP[st.session_state['language_key']]['info'][2])
    if st.session_state['language_key'] == 'he':
        max_pad = max([max(list(map(len,
                        params.PARAMETER_LANG_MAP[st.session_state['language_key']]['info'][k]['body'].split('\n'))))
                       for k in params.PARAMETER_LANG_MAP[st.session_state['language_key']]['info'].keys()] +
                      [max(list(map(len,
                        params.PARAMETER_LANG_MAP[st.session_state['language_key']]['info'][k]['title'])))
                       for k in params.PARAMETER_LANG_MAP[st.session_state['language_key']]['info'].keys()]
                      )
        for k in sorted(params.PARAMETER_LANG_MAP[st.session_state['language_key']]['info'].keys()):
            title = params.PARAMETER_LANG_MAP[st.session_state['language_key']]['info'][k]['title']
            ds = max_pad - len(title)
            st.markdown(title.rjust(ds))

            body = params.PARAMETER_LANG_MAP[st.session_state['language_key']]['info'][k]['body']
            body_lines = body.split('\n')
            b = ''
            for line in body_lines:
                line = line.strip()
                ds = max_pad - len(line)
                b += line.rjust(ds) + '\n'
            st.text(b)
            st.divider()
    else:
        for k in sorted(params.PARAMETER_LANG_MAP[st.session_state['language_key']]['info'].keys()):
            st.markdown(params.PARAMETER_LANG_MAP[st.session_state['language_key']]['info'][k]['title'])
            st.text(params.PARAMETER_LANG_MAP[st.session_state['language_key']]['info'][k]['body'])
            st.divider()


def guide():
    with st.sidebar.popover(params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input_titles']['guide']['button']):
        st.text(params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input_titles']['guide']['info'])


def app():
    set_language()
    st.sidebar.divider()
    guide()

    main, info = st.tabs(params.PARAMETER_LANG_MAP[st.session_state['language_key']]['tabs'])
    with main:
        set_amortizations()
        set_prime_portion()
        set_is_married_couple()
        set_is_single_asset()
        set_asset_cost()
        set_capital()
        set_net_monthly_income()
        set_max_monthly_payment()
        if st.sidebar.button(params.PARAMETER_LANG_MAP[st.session_state['language_key']]['input_titles']['submit'],
                             type='primary'):
            display_result()
        st.divider()
    with info:
        project_info()


    waiver()


app()





# if __name__ == '__main__':
#     ...