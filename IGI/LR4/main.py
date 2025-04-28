import re

from task1 import task1
from task2 import task2
from task3 import task3

#task1()

redex = re.compile(r'[.?!;, ()\[\]{}]', 0)

text = ('Вспо[]могательные функции для gffgr работы с файлами (чтение, запись, архивирование) вынесены в отдельный модуль (например, file_io.py). '
        '• Функции анализа текста реализованы в классе TextAnalyzer (модуль text_analysis.py), который содержит все необходимые методы для анализа (подсчёт предложений, средняя длина, поиск смайликов, выделение пар символов и т.д.).'
        ' • Основной модуль (например, main.py или task2.py) содержит меню с пунктами на русском языке, а комментарии и документация (docstrings) – на английском. • Программа обеспечивает повторное выполнение без выхода, а также выводит на экран сведения об архиве созданного файла с результатами.')
l = [word for word in redex.split(text) if len(word) > 0]
#print(l)

text2 = ':---( ;-) :-----]]]] ;-)H'




print(re.sub(r'([a-z][A-Z])', r'_?_\1_?_', text2))

print(sum(1 for i in l if len(i) < 7))
for item in (word for word in sorted(l, key=lambda x: len(x)) if word.endswith('а')):
    print(item)

print(sorted(l, key=lambda w:len(w), reverse=True))

list = (re.findall('[;:]-*([\[\]\(\)])\1*', text2))

print()

task2()
task3()