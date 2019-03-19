def resolve_abstract_inconsistency(abstract):
    for emp in abstract:
        for product in abstract[emp]:
            # TODO não funciona, ele possui os 2 anos mais um nao tem dados / reformular
            if len(abstract[emp][product]) < 2:
                year_to_save = None
                label_to_save = None
                business_code_to_save = None

                for year in abstract[emp][product]:
                    year_to_save = year - 1
                    label_to_save = abstract[emp][product][year]['business_code']
                    business_code_to_save = abstract[emp][product][year]['label']
                
                abstract[emp][product][year_to_save] = {
                    "amount": 0,
                    "business_code": business_code_to_save,
                    "label": label_to_save,
                    "value": 0,
                    "year": year_to_save
                }
    
    return abstract

def get_same_period_date(date):
    current = date
    latest = None
    diff = 0

    while not latest:
        day = current.day - diff
        try:
            if current.month == 1:
                latest = current.replace(month=12, year=current.year - 1, day=day)
            else:
                latest = current.replace(month=current.month -1, day=day)
        except Exception as e:
            diff += 1

    return {
        'current': {
            'date_ini': current.replace(day=1).strftime('%m/%d/%Y'),
            'date_fim': current.strftime('%m/%d/%Y')
        },
        'latest': {
            'date_ini': latest.replace(day=1).strftime('%m/%d/%Y'),
            'date_fim': latest.strftime('%m/%d/%Y')
        }
    }

