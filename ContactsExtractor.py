from tkinter import filedialog, simpledialog


out_file_header = 'Nome,Segundo Nome,Sobrenome,Rua 1,Rua 2,CEP,Bairro,Cidade,Estado,' \
                      'Celular,Celular,Celular,Celular,Celular,Home E-mail\n'


def read_file_to_import():
    #in_file_contacts = filedialog.askopenfile('r')
    in_file_contacts = open('cadastro_to_import.txt', 'r')

    return in_file_contacts.read()

def split_file_into_head_and_body(in_file):
    in_file = in_file.split('Ordem: Alfabética  CEP')
    in_file_head = in_file[0]
    in_file_body = in_file[1]
    return in_file_head, in_file_body


def extract_process_code(in_file_head):
    contract_number = in_file_head.split('Contrato:')[1].split(' ')[0]
    return contract_number

def split_body_file_into_contacts(in_file_body):
    contact_card_list = in_file_body.split('Cliente:pesquisar ')[1:]
    return contact_card_list


def write_to_csv(data_to_write, csv_file):
    csv_file = open(csv_file, 'a')
    csv_file.write(data_to_write)
    csv_file.close()


def extract_phone_numbers(card_phone_number_list):
    phones_string = ''
    for phone in card_phone_number_list:
        phone_number = phone.split(':')[1].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        phone_number = phone_number.replace('Email', '')
        if phone_number.isdigit():
            phones_string = f"{phones_string},{phone_number}"
    missing_comas = (5 - (len(phones_string.split(',')))) * ','
    phones_string = f"{phones_string}{missing_comas}"
    return phones_string


def extract_email(string_email_raw):
    untill_space = string_email_raw.find(' ')
    untill_newline = string_email_raw.find('\n')
    limit_of_email_string = untill_space
    if untill_space > untill_newline:
        limit_of_email_string = untill_newline
    string_email = string_email_raw[:limit_of_email_string]
    return string_email


def card_dict_assembler(string_card):
    card_in_dict = {}
    card_in_dict['name'] = string_card.split('Nascimento:')[0]
    card_in_dict['middle_name'] = ''
    card_in_dict['last_name'] = f'{contract_number}-{company_acronyms}'
    card_in_dict['street_1'] = string_card.split('Endereço:')[1].split(',')[0]
    card_in_dict['street_2'] = string_card.split('Endereço:')[1].split(',')[0].split(' | ')[0]
    card_in_dict['postal_code'] = string_card.split('CEP: ')[1].split(' | ')[0]
    card_in_dict['district'] = string_card.split('BAIRRO: ')[1].split(' | ')[0]
    card_in_dict['town'] = string_card.split('Cidade: ')[1].split(' - ')[0]
    card_in_dict['state'] = string_card.split('Cidade: ')[1].split(' - ')[1][0:2]
    card_phone_number_list = string_card.split('Telefone:')[1].split('|')
    card_in_dict['contact_phones'] = extract_phone_numbers(card_phone_number_list)
    string_email_raw = string_card.split('Email:')[1]
    card_in_dict['home_email'] = extract_email(string_email_raw)
    return card_in_dict


def csv_card_assembler(card_in_dict):
    card_in_csv = f"{card_in_dict['name']},{card_in_dict['middle_name']},{card_in_dict['last_name']}," \
                  f"{card_in_dict['street_1']},{card_in_dict['street_2']},{card_in_dict['postal_code']}," \
                  f"{card_in_dict['district']},{card_in_dict['town']},{card_in_dict['state']}," \
                  f"{card_in_dict['contact_phones']},{card_in_dict['home_email']}\n"
    return card_in_csv


def main():
    in_file = read_file_to_import()
    in_file_head, in_file_body = split_file_into_head_and_body(in_file)
    contract_number = extract_process_code(in_file_head)
    company_acronyms = 'IMA'
    out_csv_file_name = f'Cadastro{company_acronyms}{contract_number}.csv'
    write_to_csv(out_file_header, out_csv_file_name)
    contact_card_list = split_body_file_into_contacts(in_file_body)

    for string_card in contact_card_list:
        card_in_dict = card_dict_assembler(string_card)
        card_in_csv = csv_card_assembler(card_in_dict)
        if len(card_in_csv) > 16:
            write_to_csv(card_in_csv, out_csv_file_name)

main()
