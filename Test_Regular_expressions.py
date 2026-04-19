from pprint import pprint
import csv
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ

# 1. Обработка ФИО
contacts_processed = []
for contact in contacts_list:
    full_name = " ".join(contact[:3]).split()

    lastname = full_name[0] if len(full_name) > 0 else ""
    firstname = full_name[1] if len(full_name) > 1 else ""
    surname = full_name[2] if len(full_name) > 2 else ""

    organization = contact[3]
    position = contact[4]
    phone = contact[5]
    email = contact[6]

    contacts_processed.append([lastname, firstname, surname, organization, position, phone, email])

# 2. Приведение телефонов к нужному формату
phone_pattern = re.compile(
    r'(\+7|8)?\s*\(?(\d{3})\)?\s*[\-]?(\d{3})[\-]?(\d{2})[\-]?(\d{2})(\s*\(?(доб\.?)\s*(\d+)\)?)?'
)

for contact in contacts_processed:
    phone = contact[5]
    if phone:
        match = phone_pattern.search(phone)
        if match:
            # Формируем основной номер
            formatted_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
            # Добавляем добавочный номер, если есть
            if match.group(7):
                formatted_phone += f" доб.{match.group(8)}"
            contact[5] = formatted_phone

# 3. Объединение дублирующихся записей (группируем по фамилии и имени)
contacts_dict = {}
for contact in contacts_processed:
    key = (contact[0], contact[1])  # группируем по фамилии и имени
    if key in contacts_dict:
        # Объединяем с существующей записью: берем максимально полные данные
        existing = contacts_dict[key]
        for i in range(len(contact)):
            if contact[i] and not existing[i]:
                existing[i] = contact[i]

            if i == 2 and contact[i] and not existing[i]:
                existing[i] = contact[i]
    else:
        contacts_dict[key] = contact.copy()


contacts_list_cleaned = list(contacts_dict.values())

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list_cleaned)

print("\nОбработанные данные:")
pprint(contacts_list_cleaned)