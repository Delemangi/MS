def lzw_compress(uncompressed: str) -> list[int]:
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}

    print(dictionary)

    w = ""
    result: list[int] = []

    for c in uncompressed:
        wc = w + c

        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])

    return result


def lzw_decompress(compressed: list[int]) -> str:
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}

    result: list[str] = []
    w = chr(compressed.pop(0))
    result.append(w)

    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError(f"Bad compressed k: {k}")

        result.append(entry)

        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry

    return "".join(result)


if __name__ == "__main__":
    original = "TOBEORNOTTOBEORTOBEORNOT"
    print(f"Original: {original}")

    compressed = lzw_compress(original)
    print(f"Compressed: {compressed}")

    decompressed = lzw_decompress(compressed)
    print(f"Decompressed: {decompressed}")

    if original != decompressed:
        raise ValueError("Decompressed data does not match original data")
