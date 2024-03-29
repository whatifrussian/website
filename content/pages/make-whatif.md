Title: Перевод и оформление «Что если?»
Slug: make-whatif
Category: Прочее
Date: 2014-06-20 08:00
Source: False
Formulas: True
save_as: make-whatif/index.html
url: make-whatif/

В этом документе собраны краткие описания процессов, в рамках которых статьи проекта [What If?][1] переводятся и публикуются на сайте [«Что если?»][2]. Документ предназначен для тех, кто хочет разобраться в том, как работает наша кухня переводов и как взаимодействуют между собой переводчики, — то есть главным образом для новых участников.

## Основные принципы перевода

1. Переводы публикуются каждую неделю, как правило, в понедельник (до 23:59 по московскому времени).
2. Мы переводим и оформляем текст так, чтобы его было приятно читать, конвертируем единицы измерения, иногда поясняем неочевидные для русскоязычного читателя моменты.
3. Мы очень внимательно относимся к тому, как именно написана статья. Мы стараемся не допускать пунктуационных, орфографических, смысловых ошибок и выдерживать стиль оригинала.

Да-да, это же написано и в разделе [О нас][3] :-).

## Подготовка, перевод и публикация

Если вы переводчик, но по какой-то причине не имеете доступа к одному из упоминаемых далее ресурсов: не получаете писем о новом переводе из списка рассылки, не можете участвовать в групчате, или проблема в чем-то другом, — [напишите нам][4].

1. Рэндалл Монро публикует новую статью, координатор оформляет «главу» на Нотабеноиде и по почте (через список рассылки) уведомляет переводчиков. (*См. раздел «Оформление „главы“ на Нотабеноиде».*)
2. Переводим фрагменты на Нотабеноиде и обсуждаем варианты перевода. Голосуем, чтобы облегчить работу тому, кто будет сводить выпуск. (*См. раздел «Перевод» и [рекомендации для переводчиков][5].*)
3. Когда перевод надписей на картинках устоялся, его нужно нарисовать (обычно мы занимаемся этим в день выпуска). Договариваемся о том, кто рисует, через групчат. (*См. раздел «Отрисовка изображений».*)
4. Координатор сводит выпуск, учитывая комментарии к фрагментам и голосование. Иногда быстрые правки принимаются в ходе обсуждения в групчате.
5. Обсуждаем в групчате варианты анонсов, обычно обсуждение инициирует координатор.
6. Координатор публикует перевод и размещает ссылки во [ВКонтакте][6] и в [Twitter][7]\'е. Можно делать перепосты :-). (*См. раздел «Размещение статьи на сайте».*)

Обязанности координатора обычно выполняет [Dront][8].

## Оформление «главы» на Нотабеноиде

Статью нужно будет сконвертировать из html в markdown, поэтому потребуется утилита [html2text][9] или расширение [StackEdit][10] для Chrome.

### Установка html2text

Для Windows:

1. Устанавливаем интерпретатор Python c [официального сайта][11].
    * Для сборки сайта пока что необходима вторая версия, поэтому лучше скачивать «Latest Python 2 Release».
2. При установке выбираем «Add python.exe to path».
3. Скачиваем [html2text.py][12]. Этот файл нам и нужен.

Для Linux:

1. Устанавливаем пакет html2text с помощью менеджера пакетов дистрибутива.

### Конвертация и создание «главы» на Нотабеноиде

1. Открываем исходный текст последней статьи What If? (Ctrl+U) и сохраняем все, что между тегами `<article>` и `</article>` в файл (для примера: `a.html`).
2. Конвертируем в markdown командой[^1]: `html2text -b0 a.html > a.md`, или через StackEdit: меню `Open from` → `Convert HTML to Markdown`, вставляем текст между `<atricle>` и `</article>`, сохраняем в `a.md`.
3. В полученном файле нужно:
    * Добавить символы `>` в начало каждой строки с вопросом и «пустую» строку с символом `>` перед указанием автора вопроса.
    * Изменить базу url\'ов картинок на `/uploads/NNN-article-name/` (например, /imgs/a/51/freefall_candy.png → /uploads/051-free-fall/freefall_candy.png).
    * Оформить текст с картинок и title-текст, как описано далее в этом разделе. (*См. подраздел «Оформление текста с изображений».*)
    * Поправить знаки сносок: `[n]` → `[^n]`.
    * Добавить текст сносок непосредственно после тех абзацев, где они эти сноски встречаются.
4. Создаем новую «главу» в [«книге» переводов What If?][13], импортируем в нее содержимое `a.md`, тип переносов строк: `Два переноса`.
5. Проверяем разбивку на фрагменты. В первом фрагменте должно быть название выпуска.
6. Отправляем переводчикам уведомление со ссылкой на «главу».

[^1]: Если пакет установлен, но команды html2text нет, попробуйте pyhtml2text.

### Ошибки html2text при работе на Windows:

Если при конвертировании выводятся сообщения вроде
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x97 in position 218: invalid start byte
```
значит нужно удалить «подозрительные» символы, обычно это тире или кавычки. Под Linux такой проблемы не возникает. (Может, Python3 решит проблему под Windows?)

### Оформление текста с изображений

Для перевода просто помещаем надписи с картинки в `[labels]` и `[/labels]`, а title-текст в кавычках внутри круглых скобок после url\'а. Выглядит это так:

```
![](/uploads/101-plastic-dinosaurs/cycle.png "It\'s the ciiiiiiircle of deaaaaaath ♫")
[labels]
Sunlight
CO_{2}
Water
Photosynthesis
Food chain
Oil
Oil rigs
Water vapor
Cars
Speed
CO_{2}
[/labels]
```

## Перевод

### Часто используемая функциональность Markdown

У языка разметки Markdown много диалектов, но используемый нами в целом соответствует [каноничному][14]. Если быть точным, мы используем библиотеку [Python-Markdown][15] и соответствующий синтаксис. Здесь собраны часто используемые варианты оформления:

* Разметка текста: `*курсив*`, `**жирный**`.
* Ссылки: `[текст ссылки][1]`, ниже `[1]: http://example.com "заголовок страницы"`. Ссылки должны оставаться человекочитаемыми: сокращать их и кодировать в %xx-нотацию не нужно (`http://ru.wikipedia.org/wiki/Я` предпочтительней `http://ru.wikipedia.org/wiki/%D0%AF`). Если ссылка ведет на страницу нашего сайта, базовую часть лучше опустить: `/page-name-here`. Для англоязычных материалов (за исключением видеороликов) заголовок приводится в переводе, но с указанием на язык страницы.
* Изображения: `![](http://example.com/image.png) "Всплывающий текст для изображения."`). Ссылка на картинку с нашего сайта обычно выглядит так: `/uploads/id-slug/original_name.png`. (*Про загрузку изображений см. раздел «Размещение статьи на сайте».*)
* Сноски:
```
Lorem ipsum[^1][^2] dolor sit amet, consectetur adipisicing elit[^a]
[^1]: Lorem ipsum — название классического текста-«рыбы».
[^2]:
    Эта сноска содержит два параграфа.

    Обратите внимание на расстановку отступов.
[^a]: Эта сноска отобразится как [#], и в конец добавится «— Прим. пер».
```
* Под- и надстрочный текст: `H_{2}O` и `E=mc^{2}`.
* Формулы оборачиваются в `$` (внутристрочные) или в `$$` (на отдельной строке): `$F_i(x)$`, `$$F_i(x) = i*log_2(x)$$`. Часто нужны:
    * десятичная запятая: `$1{,}5$` → $1{,}5$;
    * разделитель разрядов (тонкий пробел): `$10\,000$` → $10\,000$;
    * текст (в т.\ ч. русский): `$10\text{ кг}$` → $10\text{ кг}$;
    * знаки умножения и примерного равенства: `$2 \times 2 \approx 5$` → $2 \times 2 \approx 5$.
* Если для статьи включены формулы (`Formulas: True`), то, чтобы знак доллара не воспринимался как начало или конец формулы, его нужно экранировать: `от \$30 до \$40`. Если в строке один знак доллара, то экранировать его не обязательно, а если формулы выключены, то и вовсе нельзя: обратный слеш выведется рядом со знаком доллара.
* Вопрос оформляется следующим образом:
```
> Что, если я соберусь поплавать в бассейне для отработанного ядерного топлива? Нужно ли мне нырять, чтобы получить фатальную дозу радиации? Насколько долго я смогу продержаться на поверхности?
>
> — Джонатан Бастьен-Филиатро
```

### Рекомендации для переводчиков

В ходе работы у нас выработались определенные рекомендации для переводчиков. Получилось немало, поэтому теперь они живут на [отдельной странице][16].

## Отрисовка изображений

Для перевода картинок нам нужны две вещи: графический редактор (здесь инструкция для GIMP) и шрифт.

* Сборку GIMP для Windows можно скачать [здесь][17], рекомендуется ставить последнюю стабильную версию.
* Шрифт можно скачать [отсюда][18].

Интерфейс у GIMP не очень простой, но необходимые нам операции несложные:

1. Сперва нам нужно удалить текст: выделяем его (`R`) и жмем `Delete`.
2. Выбираем инструмент «Текст» (`T`), выбираем шрифт и размер, копируем перевод, позиционируем его.
3. Выбираем самый нижний слой (через `Ctrl+L`). Теперь снова можно выделять кусок картинки и очищать его.

На самом деле, для красивой отрисовки нужно совершить несколько больше действий, но их описание еще не подготовлено.

TODO: Перевести в markdown статьи про отрисовку XKCD на планшете и про отрисовку с помощью Sarkasm Ink в GIMP.

## Размещение статьи на сайте

### До начала работы

1. На компьютере должны быть установлены:
    * [Python 2.7][19];
    * [Pelican][20];
    * [Fabric][21];
    * [Beautiful Soup 4][22];
    * [git][23];
    * rsync (под Windows нет).
2. Нужно зарегистрироваться на [github.com][24] (в т.\ ч. сгенерировать ключ) и убедиться, что вы включены в организацию [whatifrussian][25].
3. Передать **публичный** ключ (`id_rsa.pub`) librarian (aka Nikita Menkovich), чтобы он предоставил вам доступ к сайту.
4. Склонировать репозиторий [website][26].

### Размещение на сайте

Если установка Pelican и всего прочего свежая, то нужно убедиться, что все необходимое установлено корректно и работает. Для этого нужно перейти в терминале в директорию репозитория (`website`) и выполнить `fab build:local` — если выполнится успешно, значит, все в порядке (за исключением, возможно, rsync).

Публикация нового выпуска состоит из следующих шагов:

1. Перейти в терминале в директорию репозитория (`website`).
2. Сделать заготовку для новой статьи (файл .md): `fab new:nnn`, где nnn — номер новой статьи.
3. Экспортировать статью из Notabenoid\'а в файл .md, выбрав нужные варианты.
4. Добавить оригинальные и переведенные изображения.
5. Собрать: `publish:dev`, проверить: [http://dev.chtoes.li][27]; поправить недочеты и повторить.
6. Отправить новый материал в основной репозиторий: `git add content && git commit -v && git push`.
    * Если что-то пошло не так, то дать команду `git pull -r` и попробовать заново с пункта 5.
7. Опубликовать на сайте: `fab publish:prod`, проверить: [https://chtoes.li][28].
8. Опубликовать во [ВКонтакте][29] и [Twitter][30]\'е.

Мы размещаем оригинальные изображения и их переводы в директории `content/uploads/nnn-article-name`, где `nnn` — номер статьи, а `article-name` — ее название в нижнем регистре с заменой букв на дефисы. Названия переведенных изображений оканчиваются на `_ru.png` и за исключением части `_ru` совпадают с оригинальными. Если переводить на картинке нечего, то загружается только оригинал.

При проверке статьи в dev-версии сайта нужно убедиться, что отображаются именно переведенные картинки и, если это не так, скорректировать их url\'ы в тексте статьи (добавить `_ru` перед `.png`).

[1]: http://what-if.xkcd.com

[2]: https://chtoes.li

[3]: /about/

[4]: mailto:contact@chtoes.li

[5]: /translations-style/

[6]: http://vk.com/whatifrussian

[7]: http://twitter.com/whatifrussian

[8]: http://vk.com/id114286

[9]: https://github.com/html2text/html2text

[10]: https://chrome.google.com/webstore/detail/stackedit/iiooodelglhkcpgbajoejffhijaclcdg?hl=en-US&utm_source=chrome-ntp-launcher

[11]: https://www.python.org/downloads/windows/

[12]: http://i.libc6.org/media/opensource/html2text.py

[13]: http://notabenoid.org/book/41531

[14]: http://daringfireball.net/projects/markdown/

[15]: https://pythonhosted.org/Markdown/

[16]: /translations-style/

[17]: http://nightly.darkrefraction.com/gimp/

[18]: https://github.com/theshock/theshock.github.com/blob/9bb56783a34e920f6e290b5b8e0aff9df23a75ba/trash/xkcdRightHand.ttf?raw=true

[19]: https://www.python.org/downloads/

[20]: http://docs.getpelican.com/en/3.3.0/getting_started.html#installing-pelican

[21]: http://www.fabfile.org/installing.html

[22]: http://www.crummy.com/software/BeautifulSoup/

[23]: http://git-scm.com/downloads

[24]: https://github.com

[25]: https://github.com/whatifrussian

[26]: https://github.com/whatifrussian/website

[27]: http://dev.chtoes.li

[28]: https://chtoes.li

[29]: http://vk.com/whatifrussian

[30]: http://twitter.com/whatifrussian
