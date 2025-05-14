def identify_card_brand(card_number):
    """
    Identifica a bandeira de um cartão de crédito com base no padrão do número.

    Args:
        card_number (str): O número do cartão de crédito

    Returns:
        str: O nome da bandeira do cartão
    """
    # Remove espaços e traços para processamento
    card_number = card_number.replace(" ", "").replace("-", "")

    # Verifica se a entrada contém apenas dígitos
    if not card_number.isdigit():
        return "Inválido: Caracteres não numéricos encontrados"

    # Visa
    if card_number[0] == "4" and len(card_number) in [13, 16, 19]:
        return "Visa"

    # Mastercard
    if len(card_number) == 16 and (
        (int(card_number[:2]) >= 51 and int(card_number[:2]) <= 55)
        or (int(card_number[:4]) >= 2221 and int(card_number[:4]) <= 2720)
    ):
        return "Mastercard"

    # American Express
    if len(card_number) == 15 and card_number[:2] in ["34", "37"]:
        return "American Express"

    # Discover
    if (
        len(card_number) >= 16
        and len(card_number) <= 19
        and (
            card_number.startswith("6011")
            or (int(card_number[:3]) >= 644 and int(card_number[:3]) <= 649)
            or card_number.startswith("65")
        )
    ):
        return "Discover"

    # JCB
    if (
        len(card_number) >= 16
        and len(card_number) <= 19
        and int(card_number[:4]) >= 3528
        and int(card_number[:4]) <= 3589
    ):
        return "JCB"

    # Diners Club
    if (
        len(card_number) >= 14
        and len(card_number) <= 19
        and (
            card_number.startswith("36")
            or card_number.startswith("38")
            or card_number.startswith("39")
            or (int(card_number[:3]) >= 300 and int(card_number[:3]) <= 305)
        )
    ):
        return "Diners Club"

    # Elo (cartão brasileiro)
    elo_prefixes = [
        "401178",
        "401179",
        "431274",
        "438935",
        "451416",
        "457393",
        "457631",
        "457632",
        "504175",
        "627780",
        "636297",
        "636368",
        "636369",
        "506699",
        "5067",
        "4576",
        "4011",
    ]
    for prefix in elo_prefixes:
        if card_number.startswith(prefix):
            return "Elo"

    # Hipercard (cartão brasileiro)
    if card_number.startswith("606282") or card_number.startswith("3841"):
        return "Hipercard"

    return "Bandeira desconhecida"


def luhn_check(card_number):
    """
    Valida o número do cartão usando o algoritmo de Luhn.

    Args:
        card_number (str): O número do cartão de crédito

    Returns:
        bool: True se o número do cartão passar na verificação de Luhn, False caso contrário
    """
    # Remove espaços e traços
    card_number = card_number.replace(" ", "").replace("-", "")

    if not card_number.isdigit():
        return False

    # Converte para lista de inteiros
    digits = [int(d) for d in card_number]

    # Dobra cada segundo dígito da direita para a esquerda
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9

    # Soma todos os dígitos
    total = sum(digits)

    # Verifica se é divisível por 10
    return total % 10 == 0


def validate_card(card_number):
    """
    Valida um número de cartão de crédito e identifica sua bandeira.

    Args:
        card_number (str): O número do cartão de crédito a ser validado

    Returns:
        dict: Resultados contendo status de validação e bandeira do cartão
    """
    # Remove espaços e traços
    cleaned_number = card_number.replace(" ", "").replace("-", "")

    # Validação básica
    if not cleaned_number:
        return {
            "is_valid": False,
            "brand": "Inválido: Entrada vazia",
            "error": "O número do cartão não pode estar vazio",
        }

    if not cleaned_number.isdigit():
        return {
            "is_valid": False,
            "brand": "Inválido: Contém caracteres não numéricos",
            "error": "O número do cartão deve conter apenas dígitos",
        }

    if len(cleaned_number) < 13 or len(cleaned_number) > 19:
        return {
            "is_valid": False,
            "brand": "Inválido: Comprimento incorreto",
            "error": f"Comprimento do cartão ({len(cleaned_number)}) é inválido",
        }

    # Identifica a bandeira
    brand = identify_card_brand(cleaned_number)

    # Validação pelo algoritmo de Luhn
    is_valid = luhn_check(cleaned_number)

    return {
        "is_valid": is_valid,
        "brand": brand,
        "error": None if is_valid else "Falha na verificação de Luhn",
    }


def main():
    print("Validador de Cartão de Crédito")
    print("==============================")

    while True:
        card_input = input("\nDigite o número do cartão (ou 'q' para sair): ")

        if card_input.lower() == "q":
            break

        result = validate_card(card_input)

        if result["is_valid"]:
            print(f"✓ Cartão {result['brand']} válido")
        else:
            if result["brand"].startswith("Inválido"):
                print(f"✗ {result['brand']}")
            else:
                print(f"✗ Cartão inválido ({result['error']})")
                print(f"  Padrão detectado: {result['brand']}")

    print("\nObrigado por usar o Validador de Cartão de Crédito!")


if __name__ == "__main__":
    main()
