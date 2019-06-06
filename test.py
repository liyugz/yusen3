
import difflib
def string_similar(s1, s2):  # 比较s1、s2连个字符串的相似度，返回相似度
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


print(string_similar('上海', '车上大小'))
