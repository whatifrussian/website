Title: Йода
Slug: yoda
Category: What If?
Date: 2012-08-11 01:24
Source: http://what-if.xkcd.com/3/
SourceNum: 3
SourceTitle: Yoda
Formulas: True
Description: Сколько Силы может произвести Йода?

> Сколько Силы может произвести Йода?
>
> — Райан Финни

![](/uploads/003-yoda/yoda_01_ru.png "Йода, контролирующий ветряные генераторы.")

Я, конечно, буду игнорировать приквелы.

Есть отличный комикс SMBC, [показывающий][1] геополитические последствия того, что Супермен будет вращать ручку, предоставляя неограниченный источник энергии. Мы можем представить Йоду, использующего Силу для того, чтобы заставлять работать генератор. Но насколько много энергии он сможет произвести?

Самым лучшим показателем силы Йоды в оригинальной трилогии был подъём X-Wing Люка из болота. Судя по всему, физическое перемещение объектов\ — это самое энергоёмкое употребление Силы среди представленных в трилогии.

Энергия, необходимая для того, чтобы поднять объект на высоту h, равна произведению массы объекта, ускорения свободного падения и высоты подъёма. Сцена с подъёмом X-Wing позволяет нам увидеть нижнюю границу пиковой выходной мощности Йоды.

Сперва нам нужно понять, насколько тяжёл был корабль. Масса X-Wing нигде не была однозначно установлена, но его длина\ — 12,5 метров. Истребитель F-22 в длину 19 метров и весит 19,7 тонн, таким образом пропорциональное уменьшение даёт нам вес X-Wing около 5 тонн.

![](/uploads/003-yoda/yoda_02_ru.png "Иллюстрация с X-Wing и F-22.")

$$ m_{x} = m_{f22} \times \left(\frac{12,5}{19}\right)^{3} \approx 5\,600\textrm{ кг} $$

Далее нам необходимо знать скорость подъёма. Я внимательно просмотрел сцену и замерил, насколько быстро Йода извлёк X-Wing из воды.

![](/uploads/003-yoda/yoda_03_ru.png "Персонаж смотрит Star Wars для научных исследований.")

Передняя стойка появляется из воды примерно через 3,5 секунды, и я предположил, что её длина примерно равна 1,4 метра (на основе сцены из эпизода «Новая надежда», где член экипажа висел на самолёте), что говорит нам о том, что X-Wing поднимался со скоростью 0,39 м/с.

И в конце концов нам нужно знать, какая сила гравитации была на планете Дагоба. Я думал, что застрял, потому что фанаты sci-fi хоть и помешаны на таком, но вряд ли существует каталог геофизических параметров на каждую планету, посещённую в «Звёздных войнах». Правильно?

Ничего подобного! Я недооценил сообщество. Вукипедия[^a] имеет такой каталог, и там написано, что ускорение свободного падения на Дагобе 0,9g. Соединяя это с массой X-Wing и скоростью подъёма, мы получим пиковую выходную мощность:

[^a]: [Wookieepedia][2]\ — энциклопедия «Звёздных войн». В Вукипедии есть [русский раздел][3].

$$ \frac{5\,600 \textrm{ кг} \times 0{,}9\mathrm{g} \times 1{,}4 \text{ метров}}{3{,}6 \text{ секунды}} = 19{,}2\textrm{ кВт} $$

Этой энергии достаточно, чтобы питать несколько пригородных домов. Также это эквивалентно 25 лошадиным силам, что сравнимо с мощностью мотора электроприводного автомобиля Smart.

![](/uploads/003-yoda/yoda_04_ru.png "Йода в моторном отделении автомобиля Smart.")

По текущим ценам на электричество стоимость энергии, производимой Йодой, будет около $2 в час.

Но телекинез\ — это только один тип Силы. Что насчёт молний, которыми Император бил Люка? Физическая природа Силы никогда не будет объяснена, но трансформаторы Тесла, которые производят [похожие молнии][4], выдают что-то около 10 [киловатт][5], что поставит энергоэффективность Императора наравне с Йодой. (Трансформатор Тесла производит много коротких импульсов тока. Если Император будет поддерживать электрическую дугу постоянно, как, например, в дуговом сварочном аппарате, то мощность легко перевалит за мегаватты.)

А что насчёт Люка? Я просмотрел сцену, где он использует Силу впервые, чтобы вытащить свой световой меч из снега. Привести цифры расчёта будет непросто, но я просмотрел сцену покадрово и пришёл к выводу, что пиковая выходная мощность составляет около 400 ватт. Это лишь малая часть 19,2 кВт Йоды и длится долю секунды.

Таким образом, Йода становится лучшим энергетическим источником. Но мировой уровень потребления достигает двух тераватт, и понадобится сто миллионов Йод, чтобы удовлетворить наши потребности. И из-за этого переход на Силу Йоды невыгоден, хотя она будет в буквальном смысле «зелёной».

![](/uploads/003-yoda/yoda_05_ru.png "Йода слушает MP3-плеер, управляя им при помощи Силы.")

[1]: http://www.smbc-comics.com/index.php?db=comics&id=2305#comic

[2]: http://starwars.wikia.com/wiki/Main_Page

[3]: http://ru.starwars.wikia.com/wiki/Заглавная_страница

[4]: http://www.youtube.com/watch?v=uNJjnz-GdlE

[5]: http://www.goodchildengineering.net/tesla-coils/drsstc-5-10kw-monster
