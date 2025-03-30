def sort_queryset(queryset, sort_param, order_param):
    if sort_param:
        # Se a ordem for 'desc', coloca um '-' antes do campo para ordenar de forma decrescente
        if order_param == 'desc':
            sort_param = '-' + sort_param
        return queryset.order_by(sort_param)
    return queryset
