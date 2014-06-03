Title: Напишите нам
Slug: contact
Date: 2013-02-15 05:30
Source: False
Formulas: True
save_as: contact/index.html
url: contact/
<form method="post" id="feedback">
    <table>
    <tbody>
    <tr>
        <td class="label-cell"><label for="name">Ваше имя&nbsp;*</label></td>
        <td><input type="text" id="name" name="name" value="" maxlength="250"></td>
    </tr>
    <tr>
        <td class="label-cell"><label for="email">Ваш e-mail&nbsp;*</label></td>
        <td><input type="text" id="email" name="email" value="" maxlength="250"></td>
    </tr>
    <tr>
        <td class="label-cell"><label for="phone">Тема письма&nbsp;*</label></td>
        <td>
            <select name="topic" id="topic">
                <option>Пожелания по сайту</option>
                <option>Нашел ошибку на сайте</option>
                <option>Задать вопрос переводчикам</option>
                <option>Хочу принять участие в переводе</option>
                <option>Ответ на вопрос</option>
            </select>
        </td>
    </tr>
    <tr>
        <td class="label-cell"><label for="message">Cообщение&nbsp;*</label></td>
        <td><textarea class="text" name="message" id="message"></textarea></td>
    </tr>
    <tr>
        <td class="label-cell"><label for="captcha">3 + 3 =</label></td>
        <td><input type="text" id="captcha" name="captcha" value="" placeholder="Можно с калькулятором" maxlength="250"></td>
    </tr>
    <tr>
        <td class="label-cell"></td>
        <td><label><input name="sendcopy" value="" type="checkbox"> Отправить копию письма <nobr>на ваш e-mail</nobr></label></td>
    </tr>

    <tr>
        <td class="label-cell"></td>
        <td class="button-cell">
            <button class="big-button" id="submit" name="submit">Отправить</button>
            <button name="clear" type="reset" class="small-button" id="clear">Очистить форму</button>
        </td>
    </tr>
    </tbody>
    </table>
</form>
