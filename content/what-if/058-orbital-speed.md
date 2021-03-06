Title: Орбитальная скорость
Slug: orbital-speed
Category: What If?
Date: 2013-08-15 13:10
Source: http://what-if.xkcd.com/58/
SourceNum: 58
SourceTitle: Orbital Speed
Formulas: True
Description: Что, если при входе в атмосферу тормозить космический корабль до скорости порядка нескольких миль в час с помощью двигателей, похожих на посадочные двигатели марсоходов? Можно ли тогда отказаться от тепловой защиты?

> Что, если при входе в атмосферу тормозить космический корабль до скорости порядка нескольких миль в час с помощью двигателей, похожих на посадочные двигатели марсоходов?[^a] Можно ли тогда отказаться от тепловой защиты?
>
> — Брайан
> <br><br>

> Возможно ли контролировать вход космического корабля в атмосферу таким образом, чтобы избежать аэродинамического сопротивления, избавившись тем самым от дорогой (и относительно хрупкой) тепловой защиты на обшивке?
>
> — Кристофер Меллоу
> <br><br>

> Можно ли (небольшую) ракету (с полезной нагрузкой) поднять до такой высоты в атмосфере, где ей хватит небольшого реактивного двигателя, чтобы достичь второй космической скорости?
>
> — Кенни Ван де Меле

[^a]: [Mars-sky-crane][1]\ — на английском, с картинками.

Ответы на все эти вопросы вращаются вокруг одной и той же идеи. Я затрагивал ее в прошлых выпусках, но сегодня хочу рассмотреть подробнее:

Основная сложность с выходом на орбиту заключается не в том, что космос высоко.

Попасть на орбиту сложно, потому что нужно двигаться очень _быстро_.

Космос не такой:

![](/uploads/058-orbital-speed/orbit_tall_ru.png "Схема не в масштабе.")

Космос вот _такой_:

![](/uploads/058-orbital-speed/orbit_wide_ru.png "Знаете, да, эта\ — в масштабе.")

**До космоса 100 километров.** Это далеко (я бы не хотел карабкаться туда по лестнице), но не _настолько_ далеко. Если вы находитесь в Сакраменто, Сиэтле, Канберре, Калькутте, Хайдарабаде, Пномпене, Каире, Пекине, центральной Японии, центральной Шри-Ланке или в Портленде, космос для вас ближе, чем море.

Отправиться в космос[^1] просто. На вашей машине, конечно, не получится совершить такое путешествие, но все же оно не вызовет больших трудностей. Можно отправить человека в космос с помощью маленькой метеорологической ракеты размером с фонарный столб. Самолет-ракетоплан X-15[^b] достиг космоса[^2], просто развив достаточно высокую скорость и направив нос чуть вверх[^3].

[^1]: А именно, до низкой опорной орбиты: это высота, на которой находится Международная космическая станция и до которой еще долетают шаттлы. [w:Низкая опорная орбита][2].

[^b]: Самолет-ракетоплан [w:North American X-15][3].

[^2]: Х-15 достиг 100 километров дважды, оба раза им управлял [Джо Уокер][4].

[^3]: Убедитесь, что вы направляете корабль вверх, а не вниз; в противном случае я вам не завидую.

![](/uploads/058-orbital-speed/orbit_x15_ru.png "Сегодня вы отправитесь в космос, а затем сразу вернетесь назад.")

Но _попасть_ в космос легко. Сложно _остаться_ там.

**Сила притяжения на околоземной орбите почти такая же, как на поверхности Земли.** МКС вовсе не за пределами действия гравитации: на нее действует примерно 90% от силы притяжения, ощущаемой нами на поверхности.

Чтобы избежать падения обратно в атмосферу, нужно двигаться по касательной **очень, очень быстро**.

Скорость, которую вы должны развить, примерно равна 8 километрам в секунду[^4]. Только малая доля энергии ракеты тратится на подъем из атмосферы, основная часть уходит на набор орбитальной скорости (ее тангенциальной составляющей).

[^4]: Немного меньше, если вы находитесь выше на низкой опорной орбите.

Это приводит нас к главной проблеме, мешающей выходу на орбиту: **для набора космической скорости нужно намного больше топлива, чем для набора орбитальной высоты.** Чтобы разогнать корабль до 8 км/с, нужно _много_ ракет-ускорителей. Достичь космической скорости тяжело; достичь космической скорости, везя на себе топливо для плавного возвращения назад, было бы крайне непрактично[^5].

[^5]: Экспоненциальный рост является основной проблемой ракетостроения: топливо, необходимое для увеличения скорости на один км/с увеличивает ваш вес в 1,4 раза. Чтобы добраться до орбиты, вам необходимо достигнуть скорости в 8 км/с, а значит вам понадобится много топлива: в $1{,}4\times1{,}4\times1{,}4\times1{,}4\times1{,}4\times1{,}4\times1{,}4\times1{,}4\approx 15$ раз больше начального веса корабля. Использование ракет для замедления создаст ту же проблему: каждый км/с уменьшения скорости увеличивает начальную массу на тот же коэффициент\ — 1,4. Если вы хотите замедлиться до нуля\ — и мягко упасть в атмосферу\ — потребность в топливе заставит вас _опять_ умножить вес на 15.

Возмутительные потребности в топливе\ — вот почему каждый космический корабль, входящий в атмосферу, тормозит, используя тепловые щиты вместо ракет: торможение о воздух является наиболее целесообразным способом замедления (и, отвечая на вопрос Брайана, марсоход Curiosity не был исключением. Несмотря на то, что он использовал ракеты, чтобы парить над поверхностью, в первую очередь марсоход использовал торможение о воздух, чтобы сбросить большую часть скорости).

**И все же, 8 км/с\ — насколько это быстро?**

Мне кажется, одна из главных причин путаницы заключается в том, что космонавты на орбите _не выглядят_ двигающимися так быстро: похоже, будто они медленно плывут над голубым шариком.

Но 8 км/с\ — это _молниеносно_ быстро. Когда смотришь на вечернее небо, иногда можно увидеть МКС, пролетающую мимо… а потом, спустя 90 минут, увидеть ее, пролетающую мимо, снова[^6]. За эти 90 минут МКС облетела всю планету.

[^6]: Существуют неплохие приложения и онлайн-сервисы. Больше всего мне нравится [ISS Detector][5], а используя поиск в Google, вы можете найти много других.

МКС движется так быстро, что если выстрелить с одного края футбольного поля[^7], Международная космическая станция пересечет поле до того, как пуля пролетит 10 метров[^8].

[^7]: Любого вида.

[^8]: Прием разрешен австралийскими правилами регби.

Давайте посмотрим, как выглядела бы прогулка по поверхности Земли на скорости 8 км/с.

Чтобы лучше почувствовать темп движения, давайте использовать ритм песни 1988 года группы The Proclaimers\ — *I\'m Gonna Be (500 Miles)*[^9]. Темп этой песни\ — примерно 131,9 ударов в минуту, так что представьте себе, что с каждым ударом вы двигаетесь вперед на 3 с лишним километра.

[^9]: Использование тактов для измерения времени также используется в сердечно-легочной реанимации, [Stayin\' Alive от Bee Gees][6] тоже хорошо подходит.

За время звучания первой строчки припева вы сможете пройти от Бронкса до Статуи Свободы.

![](/uploads/058-orbital-speed/orbit_nyc_ru.png "Вы бы двигались со скоростью 15 станций метро в секунду.")

Потребуется около двух строчек припева (4 такта), чтобы пересечь Ла-Манш между Англией и Францией.

С продолжительностью песни связано странное совпадение. Промежуток от начала до конца *I\'m Gonna Be*\ — 3 минуты 30 секунд[^10], а МКС двигается со скоростью 7,66 км/с.

[^10]: На основе длительности [официального видео из YouTube][7].

Это значит, что если астронавт на МКС будет слушать *I\'m Gonna Be*, с первого такта и до последних строк…

![](/uploads/058-orbital-speed/orbit_1000_ru.png "Просто сгореть в атмосфере над твоим порогом.")

…он преодолеет _ровно_ 1000 миль.

[1]: http://mars.jpl.nasa.gov/msl/mission/technology/insituexploration/edl/skycrane/

[2]: http://ru.wikipedia.org/wiki/Низкая_опорная_орбита

[3]: http://ru.wikipedia.org/wiki/North_American_X-15

[4]: http://ru.wikipedia.org/wiki/Уокер,_Джозеф

[5]: https://play.google.com/store/apps/details?id=com.runar.issdetector

[6]: http://www.youtube.com/watch?v=I_izvAbhExY

[7]: http://www.youtube.com/watch?v=tbNlMtqrYS0
