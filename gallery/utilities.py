from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def pagination(request, data_list, list_len):
    total_len = len(data_list)
    paginator = Paginator(data_list, list_len)
    page = request.GET.get('page')
    last_data = data_list[0]

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    index = data.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0

    if index < 2:
        end_index = 5 - start_index
    else:
        end_index = index + 3 if index <= max_index - 3 else max_index

    page_range = list(paginator.page_range[start_index:end_index])

    return {"data": data, "last_data": last_data, "page_range": page_range,
            "total_len": total_len, "max_index": max_index - 2}
