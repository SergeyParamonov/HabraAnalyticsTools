Статьи с описанием скриптов:  
http://habrahabr.ru/post/221087/ -- hubs.py  
http://habrahabr.ru/post/220465/ -- venn.py


Примеры:

создание диаграммы
python venn.py -d space programming fido  
или  
python venn.py --draw space programming fido  
если данные не присутствуют, то программа автоматически проверит наличие данных на хабре и начнет скачивание, примерно 15-20 минут на хаб 

вывод доступных имен хабов и их полные названия, все операции производятся по коротким латинским именам из списка (они же используются в url на хабре)  
python venn.py --hubs

диаграмма вместе с базовой статистикой  
python venn.py --stats -d space programming fido  

вывод только базовой статистики без диаграмм: ключ --onlystats или -o
python venn.py -o space programming fido 

удаление хаба из списка (не удаляет данные!!!)  
python venn.py --removehublink space  

добавление хаба в список (не скачивает данные!!!)  
python venn.py --addhublink space  

обновление данных хаба, скачивает данные ~15-20 минут
python venn.py --updatehub space  

диаграммы и\или стаистика без заголовка про пиццу и котят
python venn.py -s -d space programming

добавление компании и её скачивание данных (так же обновляет данные, если уже что-то скачено)
pytnon venn.py --downloadcompany yandex

Структура программы для построения диаграмм Венна
src/ папка хранит исходники  
src/reader.py -- высокоуровневые функции для интерефейса, определяет есть ли необходимость качать данные, откуда и вызывает соотвествующие функции  
src/analyzeHubs.py -- основные инструменты для анализа хабов, парсинга, 
src/draw.py --  содержит фукнцию для рисования диаграмм и подсчета базовой статистики по пересечениям  
src/parseHubs.py -- собирает данные по именам хабов, компаний и составляет списки для словарей в meta/ ; после составления этих словарей, данный файл не является необходимым

data/ папка хранит данные 

о пользователях хабов data/hubs, 
читателях компаний data/companies 

служебные данные data/meta: различные вспомогательные данные, список хабов и их полных имен, логи   
data/meta/parsing_log  -- лог скачивания данных  
data/meta/hubs_name_link.csv  -- список хабов и их описаний  
data/meta/companies_name_link.csv -- список компаний и их описаний  

usage: venn.py [-h] [--hubs] [--draw hubname [hubname ...]] [--stats]  
[--onlystats hubname [hubname ...]] [--removehubdata hubname]  
[--removehublink hubname] [--addhublink hubname]  
[--updatehub hubname] [--silentheader]  
[--downloadcompany company_name]  

optional arguments:  
-h, --help            show this help message and exit  
--hubs                Print the list of available hubs from habrahabr  
--onlystats hubname [hubname ...], -o hubname [hubname ...] Print statistics (at least 2 hubs must be given) and exit  
--removehubdata hubname Remove the data for the selected hub  
--removehublink hubname Remove the link for the selected hub  
--addhublink hubname  Add a link for a hub  
--updatehub hubname   Update user list of a hub  
--silentheader, -s    Do not show the header about pizza and kittens  
--downloadcompany company_name, -c company_name Download the data given company name e.g. yandex  

drawing commands:  
--draw hubname [hubname ...], -d hubname [hubname ...]  
Make Venn diagram for the 1st and 2nd hubs (must be given) and optinally the 3rd  
--stats               Must be used with --draw, print statistics about hubs intersection  
