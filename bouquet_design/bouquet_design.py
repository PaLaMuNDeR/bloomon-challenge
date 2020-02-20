"""
Sample of input:

AS3a4b6k20
AL8d10r5t30

aS
aS
bL
rL
tS
"""


def parse_input(input, output):
    """
    :param input: file to read from
    :param output: file to write to
    :return: an array of designs and the dict of flowers

    For example:
    designs = ['AL10a15b5c30', 'AS10a10b25', 'BL15b1c21', 'BS10b5c16', 'CL20a15c45', 'DL20b28']
    flowers = {'cL': 129, 'bL': 123, 'aS': 303, 'cS': 45, 'aL': 249, 'bS': 150}
    """
    file_object = open(input, "r")
    designs = []
    flowers = {}
    designs_completed = False

    for line in file_object:
        if not designs_completed:
            if not line == '\n':
                designs.append(line[:-1])
            else:
                designs_completed = True
        else:
            flower = line[:-1]
            if flower in flowers.keys():
                flowers[flower] += 1
            else:
                flowers[flower] = 1

    file_object.close()
    return add_to_output(output, bouquet_design(designs, flowers))


def add_to_output(output, bouquets):
    """
    Write the bouquets to the output
    :param output: file
    :param bouquets: string of the bouquets
    :return:
    """
    file_object = open('output.txt', "w")
    file_object.write(bouquets)
    file_object.close()


def bouquet_design(designs, flowers):
    """
    Main function for processing the design of all the bouquets
    :param designs: the array of designs
    :param flowers: the dict of flowers
    :return: string of bouquets
    """
    bouquets = ''
    while designs:
        for design in designs:
            bouquet_size = design[1]
            counter = 2
            flowers_used = {}
            while counter < len(design):
                flower, amount_flower, counter = get_flower(design, counter)
                amount_flower = int(amount_flower)
                if not flower == '':
                    if flower+bouquet_size in flowers.keys() and flowers[flower+bouquet_size] >= int(amount_flower):
                        flowers_used[flower+bouquet_size] = amount_flower
                        flowers[flower+bouquet_size] -= amount_flower
                        counter += 1
                    else:
                        # Not enough flowers
                        flowers = return_flowers_back_to_pile(flowers_used, flowers)
                        designs.remove(design)
                        break
                else:
                    # We have reached the end of the string of bouquet design
                    amount_flowers_to_be_picked_up = check_amount_flowers_to_be_picked_up(amount_flower, flowers_used)
                    success, flowers_used, flowers = pick_additional_flowers(amount_flowers_to_be_picked_up, bouquet_size, flowers_used, flowers)
                    if success:
                        new_bouquet = new_bouquet_composed(flowers_used, design)
                        bouquets += new_bouquet + '\n'
                    else:
                        # There weren't enough flowers to compose the bouquet
                        # Returning flowers back to pile
                        flowers = return_flowers_back_to_pile(flowers_used, flowers)
                        designs.remove(design)
                    break

    return bouquets


def return_flowers_back_to_pile(flowers_used, flowers):
    """
    Returning flowers back to the pile
    :param flowers_used: the dict of flowers already used
    :param flowers: the dict with all the flowers
    :return: the dict with all the flowers
    """
    for flower in flowers_used:
        flowers[flower] += flowers_used[flower]
    return flowers


def new_bouquet_composed(flowers_used, design):
    """
    Print the composition of the new bouquet
    :param flowers_used: The flowers used for the bouquet
    :param design: The bouquet design
    :return: The composition of the new bouquet
    """
    new_bouquet = design[:2]
    flowers_used = dict(sorted(flowers_used.items()))
    for flower in flowers_used:
        new_bouquet += str(flowers_used[flower])
        new_bouquet += flower[0]

    return new_bouquet


def check_amount_flowers_to_be_picked_up(amount_flowers, flowers_used):
    """
    Check how much is the last number of the design of the bouquet and calculate how many additional flowers we need,
    based on what we must use
    :param amount_flowers: The amount of flowers needed to be picked up
    :param flowers_used: The dict with all flowers used
    :return: the delta of flowers needed
    """
    amount_already_used = 0
    for flower in flowers_used:
        amount_already_used += flowers_used[flower]

    return amount_flowers - amount_already_used


def pick_additional_flowers(amount_flower, bouquet_size, flowers_used, flowers):
    """
    Check what flowers are available to be picked up. If we need to pick additional 10 flowers,
    but each suitable model has availability of 5, we would put both of them.

    :param amount_flower: the amount of flowers needed to be added
    :param bouquet_size: the size of the flowers in the bouquet
    :param flowers_used: the dict with the flowers already used
    :param flowers: the dict with all the flowers available
    :return: success boolean, flowers_used dict, flowers dict
    """
    # check how many flowers have been used already for this bouquet

    success = tried_all_options = False

    while not tried_all_options:
        # Sort the flowers by amount of number
        sorted_flowers = sorted(flowers.items(), key=lambda kv: kv[1])

        # Check if the flower-size is proper or if there are 0 amount of this flower
        while not sorted_flowers[-1][0][1] == bouquet_size or sorted_flowers[-1][1] == 0:
            sorted_flowers.remove(sorted_flowers[-1])

        if len(sorted_flowers) > 0:
            if sorted_flowers[-1][1] >= amount_flower:
                flowers[sorted_flowers[-1][0]] -= amount_flower
                if sorted_flowers[-1][0] in flowers_used.keys():
                    flowers_used[sorted_flowers[-1][0]] += amount_flower
                else:
                    flowers_used[sorted_flowers[-1][0]] = amount_flower
                success = True
                tried_all_options = True
            else:
                # We might need to pick up more than one model for the filling
                amount_flower -= flowers[sorted_flowers[-1][0]]
                if sorted_flowers[-1][0] in flowers_used.keys():
                    flowers_used[sorted_flowers[-1][0]] += flowers[sorted_flowers[-1][0]]
                else:
                    flowers_used[sorted_flowers[-1][0]] = flowers[sorted_flowers[-1][0]]

                flowers[sorted_flowers[-1][0]] = 0
                success = False
                tried_all_options = False
        else:
            tried_all_options = True
            success = False

    return success, flowers_used, flowers


def get_flower(design, counter):
    """
    Get the next flower from the design, we pass the counter, because we might be progressing up the string with the
    next flower and reuse the function.
    Furthermore if a bouquet has more than 99 flowers, we would need to parse 3 chars for the amount, instead of two.

    :param design: design of bouquet
    :param counter: counter in the bouquet design
    :return: flower, amount, counter
    """
    flower = ''
    amount = ''
    for i in range(counter, len(design)):
        if design[i].isdigit():
            amount += design[i]
        else:
            flower = design[i]
            counter = i
            break
    return flower, amount, counter


parse_input('input.txt', 'output.txt')