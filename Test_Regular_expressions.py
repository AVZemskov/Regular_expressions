from pprint import pprint
import csv
import re

# # читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pprint(contacts_list)


# 1. Обработка ФИ
def normalize_fio(contact):
    full_name_str = " ".join(contact[:3]).strip()

    parts = []
    for part in full_name_str.split():
        if ',' in part:
            parts.extend(part.split(','))
        else:
            parts.append(part)

    parts = [p for p in parts if p]

    lastname = parts[0] if len(parts) > 0 else ""
    firstname = parts[1] if len(parts) > 1 else ""
    surname = parts[2] if len(parts) > 2 else ""

    return lastname, firstname, surname

contacts_normalized = []
header = contacts_list[0]
contacts_normalized.append(header)

for contact in contacts_list[1:]:
    lastname, firstname, surname = normalize_fio(contact)

    organization = contact[3] if len(contact) > 3 else ""
    position = contact[4] if len(contact) > 4 else ""
    phone = contact[5] if len(contact) > 5 else ""
    email = contact[6] if len(contact) > 6 else ""

    contacts_normalized.append([lastname, firstname, surname, organization, position, phone, email])

print("\nПосле нормализации ФИО:")
pprint(contacts_normalized)


#  2. ОБЪЕДИНЕНИЕ ДУБЛИКАТОВ
def are_same_person(contact1, contact2):
    if contact1[0] and contact2[0] and contact1[0] != contact2[0]:
        return False
    if contact1[1] and contact2[1] and contact1[1] != contact2[1]:
        return False
    if contact1[2] and contact2[2] and contact1[2] != contact2[2]:
        return False
    if contact1[0] and contact1[1] and contact1[0] == contact2[0] and contact1[1] == contact2[1]:
        return True

    return False


def merge_contacts(contact1, contact2):
    merged = contact1.copy()
    for i in range(len(contact2)):
        if contact2[i] and not merged[i]:
            merged[i] = contact2[i]
    return merged


unique_contacts = []
for contact in contacts_normalized[1:]:
    found = False
    for i, existing in enumerate(unique_contacts):
        if are_same_person(existing, contact):
            unique_contacts[i] = merge_contacts(existing, contact)
            found = True
            break
    if not found:
        unique_contacts.append(contact)

contacts_deduplicated = [header] + unique_contacts

print("\nПосле объединения дубликатов:")
pprint(contacts_deduplicated)


# 3.  Приведение телефонов к нужному формату
def normalize_phone(phone):
    if not phone:
        return ""

    pattern = re.compile(
        r'(\+7|8)?\s*\(?(\d{3})\)?\s*[-]?\s*(\d{3})[-]?\s*(\d{2})[-]?\s*(\d{2})'
        r'(?:\s*\(?(доб\.?)\s*(\d+)\)?)?'
    )

    match = pattern.search(str(phone))
    if not match:
        return phone

    formatted = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"

    if match.group(7):
        formatted += f" доб.{match.group(7)}"
    return formatted

for contact in contacts_deduplicated[1:]:
    contact[5] = normalize_phone(contact[5])
pprint(contacts_deduplicated)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(contacts_deduplicated)

print("\nОбработанные данные:")
pprint(contacts_deduplicated)
