Title: Смертоносные нейтрино
Slug: lethal-neutrinos
Category: What If?
Date: 2013-11-28 12:39
Source: http://what-if.xkcd.com/73/
SourceNum: 73
SourceTitle: Lethal Neutrinos
Formulas: True

> Насколько близко нужно быть к сверхновой звезде, чтобы получить смертельную дозу нейтринного облучения?
> 
> (Подслушано на кафедре физики)

Фраза «смертельная доза нейтринного облучения» сама по себе странная. Я несколько раз прокрутил ее у себя в голове после того, как услышал.

Если вы не разбираетесь в физике, фраза прозвучит для вас вполне обычно, так что я объясню, что делает эту идею такой неожиданной:

Нейтрино — это призрачные частицы, которые едва ли вообще взаимодействуют с миром. Взгляните на свою ладонь — через нее ежесекундно проходит триллион нейтрино от Солнца.

![](/uploads/073-lethal-neutrinos/neutrinos_hand.png "Ну всё, прекрати смотреть на свои ладони.")

Вы не видите этого потока, потому что нейтрино практически не влияют на обыкновенную материю. Из этой лавины частиц в среднем лишь один нейтрино в несколько лет «зацепит» какой-нибудь атом вашего тела[^1].

Более того, эти частицы настолько эфемерны, что для них прозрачна вся наша планета: практически весь поток солнечных нейтрино проходит прямо сквозь Землю совершенно безучастно. Для обнаружения нейтрино люди строят громадные резервуары, наполненные сотнями тонн вещества, надеясь зарегистрировать воздействие хоть одной частицы, летящей от Солнца.

Получается, если мы хотим послать луч нейтрино из ускорителя частиц (который и производит нейтрино), всё, что нужно — это нацелить луч на детектор, даже если тот находится с другой стороны Земли!

![](/uploads/073-lethal-neutrinos/neutrinos_cngs_ru.png "Ух ты! Вот эти долетели быстрее света! Погодите, нет.")

Вот почему фраза «смертельная доза нейтринного облучения» звучит так странно — она несуразно сваливает в кучу большое и малое. Это сродни предложению «футбольный стадион, до краёв наполненный муравьями[^2]». Или английскому выражению «knock me over with a feather» (дословно: «пёрышко сбило меня с ног») — так говорят, когда сильно удивлены. Если у вас математическое образование, примерно тот же эффект на вас произведет выражение «ln(x)<sup>e</sup>» — и дело не в том, что при буквальной интерпретации оно не имеет _смысла_. Просто сложно представить себе, где его применить[^3].

Так и здесь: создать поток нейтрино, хоть одна частица из которого повлияет на материю, очень трудно. И потому совсем уж невообразима ситуация, когда частиц хватит, чтобы повлиять на человека.

Сверхновые[^4] создают такую ситуацию. Физик, который затронул эту тему, поделился со мной своим импровизированным правилом для оценки величин, когда речь идет о сверхновой: «Какой бы большой ни казалась тебе сверхновая, она больше».

Вот вопрос, который позволит оценить масштаб.

Что из перечисленного ярче (то есть передает больше энергии сетчатке):

1. Сверхновая, вспыхнувшая на месте Солнца, или

2. Взрыв водородной бомбы, _прижатой к вашему открытому глазу?_

![](/uploads/073-lethal-neutrinos/neutrinos_bomb.png "Нельзя ли поскорей ее взорвать? Тяжелая ведь.")

Согласно правилу нашего физика, правильный ответ — ярче окажется сверхновая. И она действительно ярче... _на девять порядков_.

Вот это и делает вопрос таким классным; сверхновые невообразимо огромны, а нейтрино невообразимо бесплотны. В какой точке эти две невообразимости сокращаются, давая результат в человеческих масштабах?

Ответ мы найдем в статье эксперта по излучениям Эндрю Карама[^5]. В ней поясняется, что при жизни некоторых сверхновых — в процессе коллапса звездного ядра в нейтронную звезду — может быть высвобождено 10<sup>57</sup> нейтрино (одна частица на каждый протон внутри звезды, который превращается в нейтрон).

Карам подсчитал, что объем нейтринного излучения на расстоянии в один парсек[^6] — около половины нанозиверта, то есть 1/500 дозы от поедания банана[^7].

Смертельная доза радиации — примерно 4 зиверта. Вычислить расстояние можно по закону обратных квадратов:

$$ 0,5\text{ нанозиверта} \times\left ( \frac{1\text{ парсек}}{x}\right )^2 = 5\text{ зивертов} $$
$$ x=0,00001118\text{ парсека}=2,3\text{ а.е.} $$

2,3 а. е. — это чуть дальше, чем от Солнца до Марса.

Коллапс ядра с возникновением сверхновой — участь звёзд-гигантов, так что если вы наблюдаете сверхновую с такого расстояния, то, скорее всего, находитесь во внешних слоях звезды, которая её породила.

![](/uploads/073-lethal-neutrinos/neutrinos_geometry_ru.png "Событие GRB 080319B было самым интенсивным из когда-либо наблюдавшихся. Особенно для тех, кто прохлаждался неподалёку на досках для сёрфинга.")

Мысль о том, что нейтринное излучение может нанести вред, возвращает нас к тому, как всё-таки огромны сверхновые. Если бы вам удалось рассмотреть сверхновую с расстояния в 1 а. е. — при этом неизвестно как избежав воспламенения, испарения или превращения в какую-нибудь диковинную плазму, — даже поток призрачных нейтрино оказался бы достаточно плотным, чтоб убить вас.

Двигаясь достаточно быстро, пёрышко _безусловно_ может сбить вас с ног.

![](/uploads/073-lethal-neutrinos/neutrinos_feather.png "Чувак, СНОВА? Ты вообще можешь подать по-человечески?")

[^1]: И того реже, если вы ребенок и в вашем теле меньше атомов-мишеней. Вероятнее всего, моё первое общение с нейтрино состоялось в возрасте лет десяти.
[^2]: И это всё равно меньше, чем 1% всех муравьёв в мире.
[^3]: Если хотите поиздеваться над математиками-первогодками, попросите их найти производную ln(x)<sup>e</sup>. _Выглядит_ так, будто в ответе что-то вроде «1», но нет.
[^4]: «Сверхновая» переводится на английский как «supernova». Автор отмечает, что во множественном числе допустимы формы «supernovae» и «supernovas», а вот «supernovii» писать не стоит. — *Прим. пер.*
[^5]: Эндрю Карам: «Дозы гамма- и нейтринного излучения при гамма-всплесках и поблизости от сверхновых звезд» // Health Physics 82, выпуск №4 (2002): стр. 491–499.
[^6]: 3,262 светового года, то есть ближе, чем от нас до Альфы Центавра.
[^7]: [xkcd.com/radiation](http://xkcd.com/radiation/)