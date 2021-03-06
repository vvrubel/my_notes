Информация о химическом соединении хранится в компьютере в виде файлов определенного формата. В зависимости от того, какие данные об определенном веществе хочет сохранить пользователь, типы файлов, используемых в ходе компьютерного моделирования биомолекул, можно разделить на следующие группы:
1. файлы , в которых хранится 1D-информация;
2. файлы, в которых хранится 2D-информация;
3. файлы, в которых хранится 3D-информация.
К первой группе можно отнести форматы SMILES, SMARTS, FASTA, InChi и т.д. Во вторую и третью группу входят форматы MOL, MOL2, SDF, PDB.

В ходе выполнения данной лабораторной работы Вы познакомитесь с форматами SMILES и FASTA.


SMILES (Simplified Molecular Input Line Entry Specification – спецификация упрощенного представления молекул в строке ввода) — система правил (спецификация) однозначного описания состава и структуры молекулы химического вещества с использованием строки символов ASCII (https://stepik.org/media/attachments/lesson/31804/smiles_format.pdf).
SMILES – строка, полученная путём вывода символов вершин молекулярного графа﻿ в порядке, соответствующем их обходу в глубину.

Можно выделить следующие основные типы ﻿записи SMILES:
«Общий SMILES» (Generic SMILES).
«Уникальный SMILES» (Unique SMILES) — версия спецификации, включающая правила канонизации, позволяющие записать формулу молекулы любого вещества однозначным образом.
«Изомерный SMILES» (Isomeric SMILES) — версия спецификации, позволяющая учиытвать изотопный состав, хиральность, конфигурацию двойных связей.
«Абсолютный SMILES» (Absolute SMILES) — уникальный+изомерный﻿
﻿Перед тем, как записать молекулу в виде строки SMILES из нее, обычно, удаляют все атомы водорода.
Правила представления молекул в виде строки SMILES заключаются в следующем:
Атомы обычно записываются в квадратных скобках: [Au]. В то же время для атомов-органогенов обычно скобки опускают: B, C, N, O, P, S, F, Cl, Br, I. Изотопы атомов записываются в квадратных скобках с указанием массы атома: [13C]. Атомы в составе ароматических циклов обычно записываются строчными буквами вместо прописных. При необходимости указать формальный заряд частицы атомы водорода и символ заряда записываются в явном виде.
Для обозначения связей используются: дефис (-) (одинарная связь); двоеточие (:) (ароматическая связь); знак равно (=) (двойная связь); диез (#) (тройная связь).
При разветвлениях молекулы боковой заместитель записывается в круглых скобках: CCC(=O)O
Для записи циклических соединений цикл разрывают по одному из атомов и записывают строку, соответствующую получившейся "линейной" молекуле. При этом строка начинается и заканчивается с атома, по которому разорвали цикл: C1CCCCC1 (циклогексан); с1ccccc1 (бензол).
Различные изомеры молекул могут быть записаны с использованием символов / и \ : F/C=C/F (транс-дифторэтилен); F/C=C\F (цис-дифторэтилен).


Как Вы уже знаете для хранения информации о пространственной структуре макромолекул используется формат pdb. В то же время в базах данных лигандов молекулы обычно хранятся в формате mol или sdf.

Формат Mol был разработан компанией Tripos для использования в приложении SYBYL. Файлы в данном формате представляют собой обычный текстовый файл следующего вида, представленного на иллюстрации (пример для L-аланина).
https://ucarecdn.com/1ded821f-cb44-43e0-b2ec-0f1c26ca6227/

Формат SD или [SDF](https://en.wikipedia.org/wiki/Chemical_table_file#Molfile) является расширением формата Mol. Структурно он представляет собой текстовый файл в формате mol, в котором, кроме этого, содержится информация о специфических свойствах молекулы (физико-химические параметры и т.д.). В файлах такого формата также можно хранить информацию о большом числе соединений (в одном файле хранится больше одной молекулы). Многие компании и поставщики химических соединений хранят свои данные о структурах в этом двумерном формате.
Разделителем между различными молекулами в одном о том же файле sdf являются четрыре символа доллара ($). Поэтому их нельзя использовать в названии или в строке описания молекулы.
https://ucarecdn.com/be744a07-be0c-4c92-9f87-733e497cd9f5/



Как Вы уже знаете, в биоинформатике существуют одномерные форматы представления данных о химической структуре. Одним из таких форматов является SMILES. Однако не менее часто используется и формат InChI. 
InChI (англ. International Chemical Identifier) — международный текстовый химический идентификатор. Представляет собой стандартизированный структурный код для обозначения молекул, разработанный, чтобы обеспечить стандартный и читабельный способ кодирования молекулярной информации и облегчить поиск такой информации в базах данных и в интернете. Разработан IUPAC и NIST в течение 2000-2005 годов. Дальнейшее развитие стандарта поддерживается начиная с 2010 года некоммерческой организацией InChI Trust, являющейся членом IUPAC.
Каждая строка InChI начинается с "InChI=" за которым следует номер версии. После этого в стандартной записи следует буква S. Далее расположено, собственно, описание молекулы, разделенное символом "/" на т.н. слои и подслои, начинающихся с определенной буквы (префикса). Наиболее важными являются следующие слои:
   Главный слой:
     химическая формула (нет префикса). Это единственный подслой, который есть в каждой записи InChI.
     связи атомов (префикс: "c"). В этом подслое описывается, какие атомы связаны друг с другом.
     атомы водорода (префикс: "h"). Описывет сколько атомов водорода связано со всеми остальными атомами.
   Зарядовый слой
           подслой протонов (префикс: "p")
           подслой заряда (префикс: "q")
   Стереохимический слой
           двойные связи (префикс: "b")
     и т.д.
   Изотопный слой(перфиксы: "i", "h", а также "b", "t", "m", "s" для стереохимического обозначения изотопов)
     и т.д.
Такое описание имеет одно основное преимущество, заключающееся в том, что пользователь может легко искать необходимую информацию только в определенных слоях.
Строка InChI однозначно описывает молекулу в отличие от строки SMILES. Что также является ее преимуществом.
Пример: этанол - InChI=1/C2H6O/c1-2-3/h3H,2H2,1H3

Строка InChIKey представляет собой хэшированную версию стандартного InChI (используется алгоритм SHA-256). Он был разработан специально для того, чтобы облегчить поиск химических соединений в сети Интернет, так как полный ключ InChI является слишком длинным и неудобным для поиска. Характерной особенностью данного формата является то, что две молекулы с очень маленькой вероятностью будут иметь один и тот же InChIKey.
Строка InChIKey состоит из 27 символов:
14 символов (хэш информации о связях строки InChI),
дефис,
8 символов(хэш оставшихся слоев строки InChI),
символ типа InChIKey,
символ, кодирующий версию InChIKey,
дефис,
символ, кодирующий протонирование молекулы.
Пример: морфин
InChI=1S/C17H19NO3/c1-18-7-6-17-10-3-5-13(20)16(17)21-15-12(19)4-2-9(14(15)17)8-11(10)18/h2-5,10-11,13,16,19-20H,6-8H2,1H3/t10-,11+,13-,16-,17-/m0/s1
InChIKey=BQJCRHHNABKAKU-KBQPJGBKSA-N 