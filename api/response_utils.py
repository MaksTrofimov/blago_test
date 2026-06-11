import json

def extract_objects_list(json_data):
   
    if isinstance(json_data, list):
        return json_data

    if not isinstance(json_data, dict):
        raise AssertionError(
            f"Expected JSON object or array, but got {type(json_data)}"
        )

    common_list_keys = [
        "data",
        "items",
        "results",
        "companies",
        "list",
        "models",
    ]

    for key in common_list_keys:
        value = json_data.get(key)
        if isinstance(value, list):
            return value

    for value in json_data.values():
        if isinstance(value, list):
            return value

    for value in json_data.values():
        if isinstance(value, dict):
            try:
                return extract_objects_list(value)
            except AssertionError:
                continue

    raise AssertionError(
        f"Could not find objects list in JSON response. "
        f"Top-level keys: {list(json_data.keys())}"
    )
def get_object_identifier(obj):
    
    if not isinstance(obj, dict):
        raise AssertionError(
            f"Expected object to be dict, but got {type(obj)}"
        )

    possible_id_keys = [
        "id",
        "company_id",
        "companyId",
        "object_id",
        "objectId",
        "slug",
    ]

    for key in possible_id_keys:
        value = obj.get(key)
        if value not in (None, ""):
            return key, value

    raise AssertionError(
        f"Could not find identifier in object. "
        f"Object keys: {list(obj.keys())}"
    )


def find_object_by_identifier(objects, id_key, expected_id):
    
    for obj in objects:
        if not isinstance(obj, dict):
            continue

        if str(obj.get(id_key)) == str(expected_id):
            return obj

    raise AssertionError(
        f"Object with {id_key}='{expected_id}' was not found"
    )


def get_object_name(obj):
    
    possible_name_keys = [
        "name",
        "title",
        "caption",
        "company_name",
        "companyName",
    ]

    for key in possible_name_keys:
        value = obj.get(key)
        if isinstance(value, str) and value.strip():
            return key, value.strip()

    raise AssertionError(
        f"Could not find object name. "
        f"Object keys: {list(obj.keys())}"
    )
def to_pretty_json(data):
   
    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    )


def get_objects_preview(objects, limit=5):
    
    return objects[:limit]

def get_identifier_values(objects, id_key):
    
    values = set()

    for obj in objects:
        if not isinstance(obj, dict):
            continue

        value = obj.get(id_key)
        if value not in (None, ""):
            values.add(str(value))

    return values


def generate_non_existing_identifier(existing_values):
    
    normalized_values = {str(value) for value in existing_values}

    numeric_values = []

    for value in normalized_values:
        try:
            numeric_values.append(int(value))
        except ValueError:
            pass

    if numeric_values and len(numeric_values) == len(normalized_values):
        candidate = str(max(numeric_values) + 1000000)
    else:
        candidate = "non-existing-object-for-autotest"

    counter = 1

    while candidate in normalized_values:
        candidate = f"non-existing-object-for-autotest-{counter}"
        counter += 1

    return candidate

def get_company_short_info(company):
   
    id_key, company_id = get_object_identifier(company)
    name_key, company_name = get_object_name(company)

    return {
        "id_field": id_key,
        "id": company_id,
        "name_field": name_key,
        "name": company_name,
    }


def get_companies_short_preview(companies, limit=10):
   
    return [
        get_company_short_info(company)
        for company in companies[:limit]
    ]


def get_value_by_possible_keys(obj, possible_keys):
   
    for key in possible_keys:
        value = obj.get(key)

        if value not in (None, "", [], {}):
            return value

    return None


def get_company_main_info(company):
   
    short_info = get_company_short_info(company)

    main_info = {
        "id": short_info["id"],
        "name": short_info["name"],
    }

    optional_fields = {
        "description": [
            "description",
            "short_description",
            "shortDescription",
            "annotation",
            "text",
        ],
        "city": [
            "city",
            "town",
            "locality",
        ],
        "region": [
            "region",
            "region_name",
            "regionName",
        ],
        "address": [
            "address",
            "legal_address",
            "legalAddress",
        ],
        "phone": [
            "phone",
            "phone_number",
            "phoneNumber",
            "telephone",
        ],
        "email": [
            "email",
            "mail",
        ],
        "site": [
            "site",
            "website",
            "url",
        ],
        "collected_amount": [
            "collected",
            "collected_amount",
            "collectedAmount",
            "sum",
            "amount",
        ],
        "donations_count": [
            "donations_count",
            "donationsCount",
            "payments_count",
            "paymentsCount",
        ],
    }

    for output_key, possible_keys in optional_fields.items():
        value = get_value_by_possible_keys(company, possible_keys)

        if value is not None:
            main_info[output_key] = value

    return main_info

def find_company_by_any_identifier(objects, expected_id):

    possible_id_keys = [
        "id",
        "company_id",
        "companyId",
        "object_id",
        "objectId",
        "slug",
    ]

    for obj in objects:
        if not isinstance(obj, dict):
            continue

        for key in possible_id_keys:
            if str(obj.get(key)) == str(expected_id):
                return key, obj

    raise AssertionError(
        f"Company with id '{expected_id}' was not found in API response"
    )

def find_object_by_any_identifier_recursive(data, expected_id):
    """
    Рекурсивно ищет объект с заданным идентификатором во всей JSON-структуре.
    Используется, если нужный объект находится не в первом извлеченном списке,
    а глубже во вложенных данных.
    """

    possible_id_keys = [
        "id",
        "company_id",
        "companyId",
        "object_id",
        "objectId",
        "slug",
    ]

    if isinstance(data, dict):
        for key in possible_id_keys:
            if str(data.get(key)) == str(expected_id):
                return key, data

        for value in data.values():
            try:
                return find_object_by_any_identifier_recursive(value, expected_id)
            except AssertionError:
                continue

    if isinstance(data, list):
        for item in data:
            try:
                return find_object_by_any_identifier_recursive(item, expected_id)
            except AssertionError:
                continue

    raise AssertionError(
        f"Object with id '{expected_id}' was not found in JSON structure"
    )


def response_contains_company_reference(response_text, company_id, company_title=None):
    """
    Проверяет, что полный ответ backend содержит ссылку или данные открытой организации.
    Используется как резервная проверка для ответов, где данные представлены
    в виде HTML-фрагмента внутри JSON.
    """

    id_variants = [
        f"/companies/view/{company_id}",
        f"/companies\\/view\\/{company_id}",
        str(company_id),
    ]

    has_id_reference = any(variant in response_text for variant in id_variants)

    if not company_title:
        return has_id_reference

    normalized_response = " ".join(response_text.lower().split())
    normalized_title = " ".join(company_title.lower().split())

    return has_id_reference or normalized_title in normalized_response