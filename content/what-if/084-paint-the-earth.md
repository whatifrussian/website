Title: Покрасить Землю
Slug: paint-the-earth
Category: What If?
Date: 2014-02-20 23:05
Source: http://what-if.xkcd.com/84/
SourceNum: 84
SourceTitle: Paint the Earth
Formulas: True
Description: Произвело ли человечество достаточно краски для того, чтобы покрыть ею всю сушу на Земле?

> Произвело ли человечество достаточно краски для того, чтобы покрыть ею всю сушу на Земле?
>
> — Джош (Болтон, штат Массачусетс)

Можно ответить нехитрым образом. Находим объемы мировой лакокрасочной промышленности и экстраполируем их в прошлое, чтобы выяснить количество всей произведенной краски. А еще не помешает условиться, как мы собираемся красить землю. Заметка: когда доберемся до Сахары, я не рекомендую пользоваться кистью.

![](/uploads/084-paint-the-earth/paint_sahara.png "Я слышал, что когда ещё не было цифровой цветокоррекции, один кинорежисёр так и сделал.")

Но сначала давайте задумаемся, как бы угадать ответ заранее. При подобного рода размышлениях, которые часто называют оценкой [Ферми][1], нас интересует исключительно грубое приближение. То есть в ответе должно быть примерно правильное количество цифр. Оценивая по методу Ферми, можно округлять[^1] все промежуточные значения до ближайшего порядка:

[^1]: Используя формулу $\text{Fermi}(x) = 10^{\text{round}(log_{10}x)}$,  означающую, что 3 округляется до 1, а 4\ — до 10.

![](/uploads/084-paint-the-earth/paint_age.png "Лап на кота: 10")

Предположим, что в среднем каждый человек в мире находится в ответе за две комнаты, и они обе покрашены. В моей гостиной покрасить можно примерно 50 квадратных метров, то есть в двух будет 100 квадратных метров. Умножаем это на 7,15 миллиарда человек, и ответ не дотянет до триллиона квадратных метров\ — это меньше площади Египта.

![](/uploads/084-paint-the-earth/paint_vote1.png "Я голосовал за рептилоидов, но мой голос не учли.")

Ткнем пальцем в небо и условимся, что в среднем один человек из тысячи проводит всё свое рабочее время за покраской чего-нибудь. Если, скажем, свою комнату я покрасил бы часа за три[^2], а всех когда-либо живших людей было 100 миллиардов, и каждый из них 30 лет по 8 часов в день занимался покраской, выходит 150 триллионов квадратных метров… практически точная площадь земной суши.

[^2]: Наверное, это слишком оптимистично, особенно если в комнате есть доступ к интернету.

![](/uploads/084-paint-the-earth/paint_vote2.png "Ничья!")

Сколько краски нужно, чтобы покрасить дом? Не такой я еще взрослый, чтобы соображать в этом, так что давайте снова угадывать по методу Ферми.

После прогулок по магазинам бытовых товаров у меня сложилось впечатление, что у них на складах примерно столько же лампочек, сколько банок краски. В обыкновенном доме может оказаться лампочек 20, так что предположим, что на покраску дома нужно 80 литров краски (если банки по 4 литра)[^3]. А что, звучит правдоподобно.

[^3]: Приближения очень грубые.

Средний дом в США стоит порядка \$200\ 000. Исходя из предположения, что одним литром краски можно покрыть примерно 8 квадратных метров, получаем квадратный метр краски на каждые \$300 недвижимости. Я смутно припоминаю, что стоимость всей недвижимости в мире\ — что-то вроде \$100 триллионов[^4], а значит, на покраску всего этого ушло где-то 300 миллиардов квадратных метров краски. А это примерная площадь штата Нью-Мексико.

[^4]: Источник: Мне это приснилось в одном очень скучном сне.

![](/uploads/084-paint-the-earth/paint_vote3.png "Рептилоиды требуют повторного подсчета голосов.")

Само собой, оба приближения со зданиями могут быть как преувеличены (многие здания не покрашены), так и преуменьшены (многие не-здания[^5] покрашены). И все же, глядя на эти поверхностные оценки по методу Ферми, я ставлю на то, что краски на всю сушу планеты не хватит.

[^5]: ПРИМЕРЫ НЕ-ЗДАНИЙ: утки, M&M\'s, машины, Солнце, каракатицы, микросхемы, Маклемор, молнии, козья кровь, дирижабли, ленточные черви, банки с огурцами, палочки для поджаривания зефиринок, аллигаторы, камертоны, минотавры, метеоры потока Персеиды, избирательные бюллетени, сырая нефть, проплаченные твиты и катапульты, метающие пригоршнями обручальные кольца.

Итак, как показал себя Ферми?

Согласно отчету «[Состояние всемирной лако-красочной индустрии][2]», в 2012 году во всем мире произвели 34 миллиарда литров краски и покрытий.

Здесь нам пригодится один классный трюк. Если некоторая величина\ — скажем, показатель мировой экономики\ — какое-то время имела ежегодный прирост *n*\ — допустим, 3% (0,03)\ — тогда доля последнего года от общего объема составляет $1-\tfrac{1}{1+n}$, а сам общий объем на данный момент будет равен объему за последний год, умноженному на $1+\tfrac{1}{n}$.

Если предположить, что последние десятилетия производство краски, как и мировая экономика, росло примерно на 3% в год, то общий объем произведенной краски равен текущему ежегодному объему, умноженному на 34[^6]. Получается чуть больше триллиона литров краски. При расходе 8 квадратных метров на литр[^7] этого хватит, чтобы покрасить 9 триллионов квадратных метров\ — примерная площадь Соединенных Штатов.

[^6]: $(1+\tfrac{1}{0,03})$

[^7]: «Квадратные метры на литр»\ — отвратительная единица, но это еще что. На той неделе я пытался читать техническую документацию, где на полном серьезе использовали акр-фут: фут × чейн × фурлонг[^a].

[^a]: Три единицы длины в имперской системе единиц, причем чейн давно устарел, а фурлонг используется разве что в контексте скачек.

Итак, ответ\ — нет, в мире недостаточно краски, чтобы покрыть ею всю сушу Земли, и при текущих темпах производства ее не станет достаточно до 2100 года.

Очко в пользу Ферми и его оценок.

![](/uploads/084-paint-the-earth/paint_movies.png "Два фильма под названием «Звездный путь», один «Звездный путь II», один «Звездный путь III» и КУЧА «Звездных путей X».")

[1]: http://ru.wikipedia.org/wiki/Ферми,_Энрико

[2]: http://www.pfonline.com/articles/the-state-of-the-global-coatings-industry
