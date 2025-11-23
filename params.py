'''
http://www.yorku.ca/amarshal/mortgage.htm
https://www.moti.org.il/intrests
'''

SEED = 108

# resolution params:
CALC_INCREMENTS = 30
dt_m = 12
dt_y = 5
MAX_DURATION = CALC_INCREMENTS * dt_m
MIN_DURATION = dt_y * dt_m
BANK_BASE = {'spitzer': {'fixed': {}, 'madad': {}, 'prime': {}}, 'equal': {'fixed': {}, 'madad': {}, 'prime': {}}}
DURATIONS = list(range(MIN_DURATION, MAX_DURATION + MIN_DURATION, MIN_DURATION))  # duration in step, by years strides

# financial constraint params:
MAX_UNFIXED_PORTON = 0.667
MIN_UNFIXED_PORTON = 0.1
MIN_FIXED_PORTION = 0.333
MAX_FUNDING_RATE_FOR_FIRST_APPARTMENT = 0.75
MAX_FUNDING_RATE_FOR_NON_FIRST_APPARTMENT = 0.5
ALLOWABLE_MONTHLY_FRACTION = 0.35

UNMARRIED_ADDED_RISK = 0.05

# rate array params: TODO - auto update
FIXED_VALUE = 0.04
MADAD_INITIAL_VALUE = 0.025
PRIME_INITIAL_VALUE = 0.045
INITIAL_STEADY_PERIOD_MONTHS_DURATION = 12
STEADY_RAMP_MONTHS_DURATION = 84
LONG_RANGE_CENTERLINE = 0.03
BANKS_MARGINE = 0.015
PRIME_ADDED_YEARLY_RATE = -0.0064

min_monthly_payment = lambda asset_cost, capital: ((asset_cost - capital) * 2.7 *
                        (1 + max(FIXED_VALUE, MADAD_INITIAL_VALUE, PRIME_INITIAL_VALUE + BANKS_MARGINE)) / (30 * 12))


PARAMETER_LANG_MAP = {
    'he':{
        'tabs': ['חישוב אוטומטי', 'מידע על משתני החישוב', 'אודות'], # 'אודות הפרוייקט'],
        'input_titles': {
            'guide': {'button': 'ⓘ מדריך',
                      'info': '''מלאו את הנתונים האישיים שלכם בטופס זה, לחצו על כפתור "הרץ חישוב",
                             וקבלו את הרכב המשכנתא האופטימלי העומד בתקן בנק ישראל. 
                             זה יאפשר לכם לנהל משא ומתן על הריביות והתנאים של כל בנק ישראלי, 
                             ולבחור את הבנק הנותן את התנאים הטובים ביותר.'''},
            'language': 'שפה',
            'asset_cost': 'מחיר הנכס ₪',
            'capital': 'הון עצמי ₪',
            'net_monthly_income': 'הכנסה חודשית נטו ₪',
            'max_monthly_payment': 'תשלום חודשי מקסימלי ₪',
            'amortizations': 'בחרו סוג מסלול החזר',
            'is_married_couple': 'אתם זוג נשוי?',
            'is_single_asset': 'זה נכס יחיד?',
            'prime_portion': 'בחרו תכולת מסלולי פריים רצויה',
            'submit': 'הרץ חישוב',
        },

        'input': {
            'amortizations': ['שילוב מיטבי', 'קרן שווה', 'קרן שפיצר'], # [0, 1, 2] -> [optimize, equal, spitzer]
            'is_married_couple': ['לא', 'כן'], # [0, 1] -> [no, yes]
            'is_single_asset': ['לא', 'כן'], # [0, 1] -> [no, yes]
            'prime_portion': ['אחוז מיטבי', '33 %', '66 %'],  # [0, 1, 2] -> optimize, 1/3, 2/3
        },

        'tables': {
            'input_parameters': 'נתוני משתמש',
            'summary_results': 'תוצאות',
            'summary_df': ['מחיר משוקלל לשקל',
                           'סה"כ לתשלום ₪',
                           'סה"כ עלות ₪',
                           'תשלום ראשון ₪',
                           'ריבית כללית מהוונת %',
                           'מספר חודשי תשלום',
                           'סך הקרן ₪'],
            'main_df': {
                'amortization_type': 'סוג קרן',
                'rate_type': 'סוג ריבית',
                'nominal_rate': 'ריבית נומינלית',
                'duration': 'משך מסלול (חודשים)',
                'monthly_1st_payment': 'תשלום חודשי ראשון ₪',
                # 'monthly_max_payment': '',
                'principal': 'גודל הלוואה ₪',
                'principal_portion': 'גודל הלוואה יחסי %',
                'interest_paid': 'תשלום ריבית ₪',
                'net_paid': 'סה"כ תשלום ₪',
                'returned_ratio': 'יחס החזר (תשלום לשקל)',
                # 'effective_overall_rate': '',

                0: 'מסלול 1',
                1: 'מסלול 2',
                2: 'מסלול 3',
                3: 'מסלול 4',
                4: 'מסלול 5',
                5: 'מסלול 6',
            },

            'interest_rate_type': {
                'fixed': 'קל"צ',
                'madad': 'ק"צ',
                'prime': 'פריים',
            },
        },

        'plot': {

            },

        'waiver':
            f'<center> {".אין לראות את האתר והכלים בו כהמלצה פיננסית מכל סוג, ויוצריו אינם אחראיים לצעדי המשתמשים בהקשר זה"} </center>' +
            f'<center> {":כל הזכויות שמורות ליוצר"} </center>' +
            f'<center><a href="www.linkedin.com/in/natanel-d-133b68398" target="_blank" rel="noopener"> {"נתנאל דוידוביץ"} </a></center>'
        ,

        'info_': {
            0: '''
                <!DOCTYPE html>
                <html dir="rtl" lang="he">
                    <head>
                        <meta charset="utf-8" />
                        <meta name="viewport" content="width=device-width,initial-scale=1" />
                        <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
                        <title>Amortization Info</title>
                    </head>
                    <body>
                        <h5>מה סוגי לוחות הסילוקין?</h5>
                        <div>
                            <p>
                                ישנם מספר לוחות סילוקין למשכנתאות. הכלי האוטומטי (כרגע) מתייחס לשנים:
                            </p>
                            <p>
                                1. קרן שפיצר, בה:
                                התשלום החודשי אחיד במשך חיי המשכנתא.
                                רכיב הריבית (התשלום לבנק) פוחת במהלך התקופה.
                                רכיב ההחזר על הקרן (ההלוואה) גדל.
                                שילוב זה מאפשר תשלום חודשי (יחסית) קבוע.
                            </p>
                            <p>
                                2. קרן שווה, בה:
                                התשלום החודשי פוחת במשך חיי המשכנתא.
                                רכיב הריבית (התשלום לבנק) פוחת במהלך התקופה.
                                רכיב ההחזר על הקרן (ההלוואה) קבוע.
                                שילוב זה מאפשר תשלום חודשי פוחת.
                            </p>
                        </div>
                    </body>
                </html>
            ''',
            1: '''
                <!DOCTYPE html>
                <html dir="rtl" lang="he">
                    <head>
                        <meta charset="utf-8" />
                        <meta name="viewport" content="width=device-width,initial-scale=1" />
                        <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
                        <title>Personal Details Info</title>
                    </head>
                    <body>

                        <h5>פרטים אישיים והשפעתם יחד עם הנחות החישוב</h5>
                        <div>
                            <p>
                                <br><b>הנחות צד לווה</b>
                                <br>מבוסס על מגבלות לקיחת המשכנתא.
                                <br>מחיר דירה מינימלי: 100,000 ₪.
                                <br>מחיר דירה מקסימלי: 100,000,000 ₪.
                                <br>תקופת החזר מינימלית: 60 חודשים (5 שנים).
                                <br>תקופת החזר מקסימלית: 360 חודשים (30 שנים).
                                <br>ההחזר החודשי לא יעלה על 35% מסך ההכנסות נטו.
                                <br>כרגע, בכלי האוטומטי אין התחשבות במיקום הנכס (משפיע על הערכת שמאי).
                                <br>כרגע, בכלי האוטומטי אין התחשבות בגיל הלווה. ההנחה שמשך ההלוואה נלקח בחשבון בשיקולי הלווה.
                            </p>
                            <p>
                                <br><b>הנחות צד מלווה</b>
                                <br>מבוסס על מגבלות לקיחת המשכנתא.
                                <br>עוגני התמהילים צמודים לאג"ח ממשלתי.
                                <br>מרווח השוק תלוי באחוז המימון.
                                <br>מרווח השוק תלוי בהאם הצד הלווה יחיד או זוג.
                                <br>מימון מקסימלי לדירה יחידה: 75%.
                                <br>מימון מקסימלי לדירה נוספת: 50%.
                                <br>תכולה מקסימלית של מסלולי הפריים: 66%.
                                <br>תכולה מינימלית של מסלולי ריבית קבועה : 33%.
                                <br>ערכה של ריבית הפריים הוא סכום ריבית בנק-ישראל + 1.5%.
                <!--                <br>ריבית בנק ישראל עדכנית.-->
                            </p>
                        </div>

                    </body>
                </html>

            ''',
            2: '''
                <!DOCTYPE html>
                <html dir="rtl" lang="he">
                    <head>
                        <meta charset="utf-8" />
                        <meta name="viewport" content="width=device-width,initial-scale=1" />
                        <link rel="stylesheet" href="https://pyscript.net/latest/pyscript.css" />
                        <title>Prime Info</title>
                    </head>
                    <body>

                        <h5>מה סוגי הריביות וההבדלים ביניהן?</h5>
                        <div>
                            <p>
                                ישנם מספר סוגי ריביות למשכנתאות. הכלי האוטומטי (כרגע) מתייחס לשלושת הראשונים:
                            </p>
                            <p>
                                1. ריבית קבועה (לא צמודה למדד - קל"צ):
                                הריבית נקבעת בעת גיוס המשכנתא ונשארת קבועה במשך חייה.
                            </p>
                            <p>
                                2. ריבית קבועה צמודת מדד (ק"צ):
                                הריבית נקבעת בעת גיוס המשכנתא ונשארת קבועה ביחס למדד המחירים לצרכן במשך חייה.
                            </p>
                            <p>
                                3. ריבית פריים:
                                הריבית נקבעת בעת גיוס המשכנתא ונשארת קבועה ביחס לריבית בנק ישראל במשך חייה.
                            </p>
                            <p>
                                4. ריבית משתנה (לא צמודת מדד - מל"צ):
                                הריבית נקבעת בעת גיוס המשכנתא ומתעדכנת במשך חייה אחת לכמה שנים. התקופה שבין העדכונים ניתנת לבחירה - לרוב אחת ל 5 שנים.
                            </p>
                            <p>
                                5. ריבית משתנה צמודת מדד (מ"צ):
                                הריבית נקבעת בעת גיוס המשכנתא ונשארת קבועה ביחס למדד המחירים לצרכן, ומתעדכנת במשך חייה אחת לכמה שנים. התקופה שבין העדכונים ניתנת לבחירה - לרוב אחת ל 5 שנים.
                            </p>
                            <p>
                                סביר כי הריביות אשר ימצא הכלי האוטומטי יוכלו להשתפר עבור סוגי המסלולים הנלקחים בחשבון בחישוב, במקרה וילקחו במשכנתא שלכם, מסלולים בריבית משתנה (מ"צ ומל"צ), שכן באלו, הבנק מעדכן את הריביות בכל תקופה כדי לפצות על מרווח השוק באם יש כזה מהתקופה שתמה.
                                <br>
                                מאחר ויש אי וודאות רבה לגבי מרווח זה בנוסף לאי הוודאות העתידי הנכלל במודל - לקיחת מסלולים משתנים אינה סבירה עבור חישוב אוטומטי אמין של מסלולים בתמהיל.
                            </p>
                        </div>

                    </body>
                </html>
            ''',
        },
        'info': {
            0: {'title': '##### מה סוגי לוחות הסילוקין?',
                'body': '''
                    ישנם מספר לוחות סילוקין למשכנתאות. הכלי האוטומטי (כרגע) מתייחס לשנים:

                    1. קרן שפיצר, בה:
                    התשלום החודשי אחיד במשך חיי המשכנתא.
                    רכיב הריבית (התשלום לבנק) פוחת במהלך התקופה.
                    רכיב ההחזר על הקרן (ההלוואה) גדל.
                    שילוב זה מאפשר תשלום חודשי (יחסית) קבוע.

                    2. קרן שווה, בה:
                    התשלום החודשי פוחת במשך חיי המשכנתא.
                    רכיב הריבית (התשלום לבנק) פוחת במהלך התקופה.
                    רכיב ההחזר על הקרן (ההלוואה) קבוע.
                    שילוב זה מאפשר תשלום חודשי פוחת.
                ''',
                'image': 'info/he_0.png',
                },
            1: {'title': '##### פרטים אישיים והשפעתם יחד עם הנחות החישוב',
                'body': '''
                    הנחות צד לווה:
                    מבוסס על מגבלות לקיחת המשכנתא
                    דירה מינימלי: 100,000 ₪.
                    מחיר דירה מקסימלי: 100,000,000 ₪.
                    תקופת החזר מינימלית: 60 חודשים (5 שנים).
                    תקופת החזר מקסימלית: 360 חודשים (30 שנים).
                    ההחזר החודשי לא יעלה על 40% מסך ההכנסות נטו.
                    כרגע, בכלי האוטומטי אין התחשבות במיקום הנכס (משפיע על הערכת שמאי).
                    כרגע, בכלי האוטומטי אין התחשבות בגיל הלווה. ההנחה שמשך ההלוואה נלקח בחשבון בשיקולי הלווה.

                    הנחות צד מלווה:
                    מבוסס על מגבלות לקיחת המשכנתא.
                    עוגני התמהילים צמודים לאג"ח ממשלתי.
                    מרווח השוק תלוי באחוז המימון.
                    מרווח השוק תלוי בהאם הצד הלווה יחיד או זוג.
                    מימון מקסימלי לדירה יחידה: 75%.
                    מימון מקסימלי לדירה נוספת: 50%.
                    תכולה מקסימלית של מסלולי הפריים: 66%.
                    תכולה מינימלית של מסלולי ריבית קבועה : 33%.
                    ערכה של ריבית הפריים הוא סכום ריבית בנק-ישראל + 1.5%.
                    <!--ריבית בנק ישראל עדכנית.-->
                ''',
                'image': 'info/he_1.png',
                },
            2: {'title': '##### מה סוגי הריביות וההבדלים ביניהן?',
                'body': '''
                    ישנם מספר סוגי ריביות למשכנתאות. הכלי האוטומטי (כרגע) מתייחס לשלושת הראשונים:
                    1. ריבית קבועה (לא צמודה למדד - קל"צ):
                    הריבית נקבעת בעת גיוס המשכנתא ונשארת קבועה במשך חייה.
                    2. ריבית קבועה צמודת מדד (ק"צ):
                    הריבית נקבעת בעת גיוס המשכנתא ונשארת קבועה ביחס למדד המחירים לצרכן במשך חייה.
                    3. ריבית פריים:
                    הריבית נקבעת בעת גיוס המשכנתא ונשארת קבועה ביחס לריבית בנק ישראל במשך חייה.
                    4. ריבית משתנה (לא צמודת מדד - מל"צ):
                    הריבית נקבעת בעת גיוס המשכנתא ומתעדכנת במשך חייה אחת לכמה שנים. התקופה שבין העדכונים ניתנת לבחירה - לרוב אחת ל 5 שנים.
                    5. ריבית משתנה צמודת מדד (מ"צ):
                    הריבית נקבעת בעת גיוס המשכנתא ונשארת קבועה ביחס למדד המחירים לצרכן, ומתעדכנת במשך חייה אחת לכמה שנים. התקופה שבין העדכונים ניתנת לבחירה - לרוב אחת ל 5 שנים.
                    סביר כי הריביות אשר ימצא הכלי האוטומטי יוכלו להשתפר עבור סוגי המסלולים הנלקחים בחשבון בחישוב, במקרה וילקחו במשכנתא שלכם, מסלולים בריבית משתנה (מ"צ ומל"צ), שכן באלו, הבנק מעדכן את הריביות בכל תקופה כדי לפצות על מרווח השוק באם יש כזה מהתקופה שתמה.
                    מאחר ויש אי וודאות רבה לגבי מרווח זה בנוסף לאי הוודאות העתידי הנכלל במודל - לקיחת מסלולים משתנים אינה סבירה עבור חישוב אוטומטי אמין של מסלולים בתמהיל.
                ''',
                'image': 'info/he_2.png',
                },
            },
        'about': {
            0: {'image': 'info/he_3.png', },
            # 1: {'image': 'info/he_4.png', },
            # 2: {'image': 'info/he_5.png', },
        },
    },

    'en':{
        'tabs': ['Automatic calculation', 'Calculation parameters information', 'About'],
        'input_titles': {
            'guide': {'button': 'ⓘ Guide',
                      'info': '''Fill in your personal parameters in this form, push the "Run calculation" button, 
                                and get the optimized mortgage composition that adhere to the Bank Of Israel standard. 
                                This will allow you to negotiate the rates and terms of any Israeli bank, 
                                and choose the one that is most favorable'''},
            'language': 'Language',
            'asset_cost': 'Asset cost (ILS, ₪)',
            'capital': 'Down payment (ILS, ₪)',
            'net_monthly_income': 'Net monthly income (ILS, ₪)',
            'max_monthly_payment': 'Max allowable monthly payment (ILS, ₪)',
            'amortizations': 'Select amortization method',
            'is_married_couple': 'Are you married?',
            'is_single_asset': 'Is it your only house?',
            'prime_portion': 'Select prime interest portion',
            'submit': 'Run calculation',
        },

        'input': {
            'amortizations': ['Optimized combo', 'Equal', 'Spitzer'], # [0, 1, 2] -> [optimize, equal, spitzer]
            'is_married_couple': ['No', 'Yes'], # [0, 1] -> [no, yes]
            'is_single_asset': ['No', 'Yes'], # [0, 1] -> [no, yes]
            'prime_portion': ['Optimized combo', '33 %', '66 %'],  # [0, 1, 2] -> optimize, 1/3, 2/3
        },

        'tables': {
            'input_parameters': 'User parameters',
            'summary_results': 'Results',
            'summary_df': ['Weighted average to 1 (ILS, ₪)',
                           'Total for payment (ILS, ₪)',
                           'Total cost (ILS, ₪)',
                           '1st monthly payment (ILS, ₪)',
                           'Capitalized interest %',
                           'Number of monthly payments',
                           'Total loan (ILS, ₪)'],
            'main_df': {
                'amortization_type': 'Amortization type',
                'rate_type': 'Rate type',
                'nominal_rate': 'Nominal rate',
                'duration': 'Payment duration (# months)',
                'monthly_1st_payment': '1st Monthly payment (ILS, ₪)',
                # 'monthly_max_payment': '',
                'principal': 'Total loan (ILS, ₪)',
                'principal_portion': 'Total loan portion %',
                'interest_paid': 'Interest paid (ILS, ₪)',
                'net_paid': 'Net paid (ILS, ₪)',
                'returned_ratio': 'Return ration (ILS, ₪)',
                # 'effective_overall_rate': '',

                0: 'Track 1',
                1: 'Track 2',
                2: 'Track 3',
                3: 'Track 4',
                4: 'Track 5',
                5: 'Track 6',
            },

            'interest_rate_type': {
                'fixed': 'Fixed',
                'madad': 'Madad',
                'prime': 'Prime',
            },
        },

        'plot': {

            },

        'waiver':
            f'<center> {"The site and its tools should not be viewed as financial advice of any kind, and its creators are not responsible for the actions of users in this context."} </center>' +
            f'<center> {"All rights reserved to the creator:"} </center>' +
            f'<center><a href="www.linkedin.com/in/natanel-d-133b68398" target="_blank" rel="noopener"> {"Natanel Davidovits"} </a></center>'
        ,

        'info': {
            0: {'title': '##### What are the types of return tables?',
                'body': '''
                    There are several amortization schedules for mortgages. The automatic tool (currently) refers to the following two:

                    1. Spitzer Fund, in which:
                    The monthly payment is uniform over the duration of the mortgage.
                    The interest component (payment to the bank) decreases over the period.
                    The repayment component on the principal (loan) increases.
                    This combination allows for a (relatively) constant monthly payment.

                    2. Equal principal, in which:
                    The monthly payment decreases over the life of the mortgage.
                    The interest component (payment to the bank) decreases over the period.
                    The principal (loan) repayment component is fixed.
                    This combination allows for a decreasing monthly payment.
                ''',
                'image': 'info/en_0.png',
                },
            1: {'title': '##### Personal details and their impact along with calculation assumptions',
                'body': '''
                    Borrower assumptions:
                    Based on mortgage restrictions.
                    Minimum apartment: 100,000 NIS.
                    Maximum apartment price: 100,000,000 NIS.
                    Minimum repayment period: 60 months (5 years).
                    Maximum repayment period: 360 months (30 years).
                    Monthly repayment will not exceed 35% of total net income.
                    Currently, this automatic tool does not take into account the borrower's age. The assumption is that the loan term is taken into account in the borrower's considerations.
                    
                    Lender's assumptions:
                    Based on mortgage underwriting restrictions.
                    The anchors of the mixes are linked to government bonds.
                    The market spread depends on the financing percentage.
                    The market spread depends on whether the borrower is a single or a couple.
                    Maximum financing for a single apartment: 75%.
                    Maximum financing for an additional apartment: 50%.
                    Maximum portion of the prime amortization track: 66%.
                    Minimum portion of fixed interest amortization tracks: 33%.
                    The value of the prime interest is the amount of the Bank of Israel interest rate + 1.5%.
                    <!--Current Bank of Israel interest rate.-->
                ''',
                'image': 'info/en_1.png',
                },
            2: {'title': '##### What are the types of interest rates and the differences between them?',
                'body': '''
                    There are several types of mortgage interest rates. The automatic tool (currently) refers to the first three:
                    1. Fixed interest rate (not index-linked):
                    The interest rate is determined when the mortgage is raised and remains fixed for its entire duration.
                    2. Fixed interest rate index-linked:
                    The interest rate is determined when the mortgage is raised and remains fixed in relation to the consumer price index throughout its entire duration.
                    3. Prime interest rate:
                    The interest rate is determined when the mortgage is raised and remains fixed in relation to the Bank of Israel interest rate throughout its entire duration.
                    4. Variable interest rate (not index-linked):
                    The interest rate is determined when the mortgage is raised and is updated every few years throughout its entire duration. The period between updates is optional - usually once every 5 years.
                    5. Index-linked variable interest rate (Madad):
                    The interest rate is determined when the mortgage is raised and remains fixed in relation to the consumer price index, and is updated every few years throughout its life. The period between updates is optional - usually once every 5 years.
                    It is likely that the interest rates found by the automatic tool could improve for the types of tracks taken into account in the calculation, if variable interest rate tracks are taken into account in your mortgage, since in these, the bank updates the interest rates each period to compensate for the market margin, if there is one from the previous period.
                    Since there is a great deal of uncertainty about this interval in addition to the future uncertainty included in the model - taking variable tracks is not reasonable for reliable automatic calculation of tracks in the mix.
                ''',
                'image': 'info/en_2.png',
                },
            },
        'about': {
            0: {'image': 'info/en_3.png', },
            # 1: {'image': 'info/en_4.png', },
            # 2: {'image': 'info/en_5.png', },
        },
    },
}


LANGS = {'עברית 🇮🇱': 'he', 'English 🇬🇧': 'en'}


NUMERICAL_FORMAT = '%u'


COLOR_DISCRETE_MAP = {0: '#4503fc', 1: '#855cf7', 2: '#c6b4fa'}


EN2HEB_translation = {
    'Couple': 'זוג',
    'Single': 'יחיד',
    'Yes': 'כן',

    'Spitzer + Equal': 'שפיצר + קרן-שווה',
    'Spitzer': 'שפיצר',
    'Equal': 'קרן-שווה',

    'Max (66 %)': 'מקסימלית - (% 66)',
    'Old max (33 %)': 'מקסימלי ישן - (% 33)',
    'Optimized portions': 'חלוקה מיטבית אוטומטית',


    'Family status': 'מצב משפחתי',
    'Is your only house': 'דירה יחידה',
    'Amortization method': 'לוחות סילוקין לחישוב',
    'Desired prime-interest portion': 'תכולת פריים רצויה',
    'Mortgage size (ILS, ₪)': 'גודל הקרן ₪',
    'Leverage rate': 'אחוז מימון',
    'Parameter': 'פרמטר',

    'Weighted average per ILS': 'מחיר משוקלל לשקל',
    'Tot to be payed (ILS, ₪)': 'סה"כ לתשלום ₪',
    'Tot cost (ILS, ₪)': 'סה"כ עלות ₪',
    '1st monthly payment (ILS, ₪)': 'תשלום חודשי ראשון ₪',
    'Weighted average interest %': 'ריבית משוקללת %',
    'Number of month to pay': 'מספר חודשי תשלום',
    'Tot mortgage (ILS, ₪)': 'סך הקרן ₪',

    'Interest type': 'סוג ריבית',
    'Nominal interest rate %': 'ריבית %',

    'Fixed interest rate': 'קל"צ',
    'Madad interest rate': 'ק"צ',
    'Prime interest rate': 'פריים'
}

