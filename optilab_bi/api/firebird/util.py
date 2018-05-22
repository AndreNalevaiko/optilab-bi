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