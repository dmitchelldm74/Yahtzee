def KV(data):
    type = {}
    l = data.replace(':', ' : ').replace('\n', ' ; ').split()
    key = ""
    build = ""
    while l != []:
        n = l.pop(0)
        if n == ':':
            key = build
            build = ''
        elif n == ';':
            type[key] = build
            build = ''
        else:
            build += n
    return type