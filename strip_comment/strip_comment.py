# coding:utf-8

'''
状态 1  字符串外，未遇到 / （入口）
状态 2  字符串外，已遇到 /
状态 3  字符串内，未遇到 \\
状态 4  字符串内，已遇到 \\
状态 5  单行注释内
状态 6  多行注释内
状态 7  多行注释内，遇到 *
状态 8  多行注释内 & 字符串内，未遇到 \\
状态 9  多行注释内 & 字符串内，已遇到 \\

'''

statusMoveDef = {
    '\\' : (
        (3,4,0),
        (8,9,0),
    ),
    
    '/' :(
        (1,2,0),
        (2,5,1),
        (7,1,1),
    ),

    '*' : (
        (6,7,0),
        (2,6,1),
    ),

    '\"' : (
        (1,3,0),
        (3,1,0),
        (4,3,0),
        (6,8,0),
        (7,8,0),
        (8,6,0)
    ),

    '\n': (
        (5,1,0),
    ),

    '' : (
        (2,1,0),
        (4,3,0),
        (7,6,0),
        (9,8,0),
    )
}

def strip_comment(text):
    """
    >>> strip_comment("abcde")
    'abcde'
    >>> strip_comment("abcde// aaaa")
    'abcde'
    >>> strip_comment("abcde\\"aa\\"aa// aaaa")
    'abcde\"aa\"aa'
    >>> strip_comment("abcde\\"aa\\\\a\\"// aaaa")
    'abcde\"aa\\\\a"'
    >>> strip_comment("a/b//cde\\"aa\\\\a\\"// aaaa")
    'a/b'
    >>> strip_comment("a/b/cd/e\\"//a/a\\\\a\\"// aaaa")
    'a/b/cd/e\"//a/a\\\\a"'
    """
    rs = []
    status = 1
    oldStatus = 1
    for c in text:
        oldStatus = status
        status,delChar = status_move(status, c)
        # print(" %s status %d => %d, del:%d" % (c, oldStatus, status, delChar) )
        if delChar > 0: rs = rs[:-delChar]
        if 5 <= status <= 9:
            continue
        
        if oldStatus == 7 and status == 1:
            continue # shit 
        rs.append(c)

    return "".join(rs)

def status_move(cur, c):
    global statusMoveDef
    if c in statusMoveDef:
        for src, dst, delChar in statusMoveDef[c]:
            if cur == src:
                return dst, delChar
    else:
        for src, dst, delChar in statusMoveDef['']:
            if cur == src:
                return dst, delChar

    return cur, 0

if __name__ == "__main__":
    import sys
    fileName = sys.argv[1]

    with open(fileName) as f:
        text = f.read()
        text = strip_comment(text)
        print(text)
    pass

