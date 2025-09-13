if __name__ == '__main__':
    d: list[str | int] = []
    d.append('A')

    w: [str | int] = []
    w.append(12)

    print(d)
    print(w)

    print(type([str | int]))
