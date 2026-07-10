def remove_duplicates(contexts):
    seen = set()
    unique = []

    for ctx in contexts:
        text = ctx["text"].strip()

        if text not in seen:
            unique.append(ctx)
            seen.add(text)

    return unique