import collections


def sorted_dict_by_key(unsorted_dict):
    return collections.OrderedDict(
        sorted(unsorted_dict.items(), key=lambda d: d[0]))


def pprint(chains):
    for i, chain in enumerate(chains):
        print(f'{"="*25} Chain {i} {"="*25}')
        for k, v in chain.items():
            if k == 'transactions':
                print(k)
                for d in v:
                    print(f'    {"-"*30}')
                    for key, value in d.items():
                        print(f'    {key:20}{value}')
                print(f'    {"-"*30}')
            else:
                print(f'{k:15}{v}')
    print(f'{"*"*25}')
