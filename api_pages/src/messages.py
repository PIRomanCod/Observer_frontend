stock_messages = {
    "english_name": {"goods": "Select products: ", "type": "Review Type:", "day": "Day", "dynamic": "Dynamic",
                     "about": "Stock Overview Page", "instruction": """Select from the side menu:
          - view type:
              - or a specific day for review
              - or dynamics to see how stocks changed over time
          - also select or delete the required products from the list""", "start date": "Select start date",
                     "end date": "Select an end date", "one date": "Select day:",
                     "dynamic graf title": "Stocks dynamic",
                     "daily table title": "Stock for the date, mt",
                     "empty data": "No info for choosen dates",
                     "date": "Date", "name": "Product", "quantity": "Quantity, mt",
                     "quantity_difference": "Dynamic with ",
                     },
    "ukrainian_name": {"goods": "Виберіть товари: ", "type": "Тип огляду:", "day": "День", "dynamic": "Динаміка",
                       "about": "Сторінка огляду складських запасів", "instruction": """ Виберіть у боковому меню:
          - Тип перегляду:
              - або конкретний день для огляду
              - або динаміку щоб подивитися як змінювалися запаси з часом
          - також у списку виберіть або видаліть потрібні товари
""", "start date": "Виберіть початкову дату", "end date": "Виберіть кінцеву дату", "one date": "Оберіть день:",
                       "dynamic graf title": "Дінаміка запасів", "daily table title": "Запаси на дату, тонн",
                       "empty data": "Немає інформації для вибраних дат",
                       "date": "Дата", "name": "Продукт", "quantity": "Кількість, тонн",
                       "quantity_difference": "Динаміка з ",
                       },
    "russian_name": {"goods": "Выберите товары: ", "type": "Тип обзора:", "day": "День", "dynamic": "Динамика",
                     "about": "Страница обзора складских запасов", "instruction": """Выберите в боковом меню:
         - тип просмотра:
             - или конкретный день для обзора
             - или динамику чтобы посмотреть как изменялись запасы со временем
         - также в списке выберите или удалите необходимые товары
""", "start date": "Выберите начальную дату", "end date": "Выберите конечную дату", "one date": "Выберите день:",
                     "dynamic graf title": "Динамика запасов", "daily table title": "Запасы на дату, тонн",
                     "empty data": "Нет информации на выбранные даты",
                     "date": "Дата", "name": "Продукт", "quantity": "Количество, тонн",
                     "quantity_difference": "Динамика с ",
                     },
    "turkish_name": {"goods": "Ürünleri seçin: ", "type": "İnceleme Türü:", "day": "Gün", "dynamic": "Dinamikler",
                     "about": "Stok genel bakış sayfası", "instruction": """Yan menüden seçim yapın:
          - görünüm türü:
              - veya inceleme için belirli bir gün
              - veya hisse stoklar zaman içinde nasıl değiştiğini görmek için dinamikler
          - ayrıca gerekli ürünleri listeden seçin veya kaldırın
""", "start date": "Başlangıç tarihini seçin", "end date": "Bir bitiş tarihi seçin", "one date": "Gün seçin:",
                     "dynamic graf title": "Stoklar dinamikleri", "daily table title": "Tarih için stok, mt",
                     "empty data": "Seçilen tarihler için bilgi yok",
                     "date": "Tarih", "name": "Ürün", "quantity": "Miktar, mt",
                     "quantity_difference": "Dinamik ile ",
                     },
}

seeded_id = {
    "ham ayçi̇cek yağ": 1, "refined ayçi̇cek yağ": 2, "asi̇tli̇ yağ": 3, "kanola yağ": 4, "steari̇n": 5,
    "wax": 6, "gli̇seri̇n": 7, "tortu posasi": 8, "ayçi̇cek tortusu": 9, "soapstock": 10, "su tanki": 11,
    "misir yağ": 12, "extract tortusu": 13, "asi̇tli̇ tortusu": 14, "bos": 15, "other": 16
}

languages_id = {
    1: "english_name",
    2: "ukrainian_name",
    3: "russian_name",
    4: "turkish_name",
}

hello_messages = {
    "english_name": {"title": "Welcome to Company observer",
                     "instruction": """
     This application was created to provide quick access to:

 - the state of operation capital on the selected date
 - current prices for raw materials, goods and finished products
 - production volumes
 - stock status
 - cash flow
 - the state of accounts receivable and accounts payable
 - balance for each counterparty
 - archive of company information

 To start using and for safety reasons, you need to make sure that
 that you are an authorized user.

 How to see more?
 - first, register
 - confirm your email,
 - log in.
     """, },
    "ukrainian_name": {"title": "Ласкаво просимо в Company observer",
                       "instruction": """
Ця програма створена для надання оперативного доступу до:

 - стану оборотних коштів на обрану дату
 - актуальним цінам на сировину, товари та готову продукцію
 - обсягів виробництва
 - стану складських запасів
 - руху грошових коштів
 - стану дебіторської та кредиторської заборгованостей
 - балансу за кожним контрагентом
 - архіву інформації компанії

 Для початку використання та з метою безпеки потрібно переконатися,
 що Ви авторизований користувач.

 Як побачити більше?
 - для початку пройдіть реєстрацію,
 - підтвердіть свою електронну пошту,
 - увійдіть до системи.
     """, },
    "russian_name": {"title": "Добро пожаловать в Company observer",
                     "instruction": """ 
    Это приложение создано для предоставления оперативного доступа к:
    
    - состоянию оборотных средств на выбранную дату
    - актуальным ценам на сырье, товары и готовую продукцию
    - объемам производства   
    - состоянию складских запасов
    - движению денежных средств
    - состоянию дебиторской и кредиторской задолженностей
    - балансу по каждому контрагенту
    - архиву информации компании      

    Для начала использования и в целях безопасности нужно убедиться,
     что Вы авторизованный пользователь.
     
     Как увидеть больше?
    - для начала пройдите регистрацию, 
    - подтвердите свою электронную почту,
    - войдите в систему.
    """, },
    "turkish_name": {"title": "Şirket incelemesine hoş geldiniz",
                     "instruction": """
     Bu uygulama aşağıdakilere hızlı erişim sağlamak için oluşturuldu:

 - seçilen tarihte işletme sermayesinin durumu
 - Hammadde, mal ve nihai ürünlerin güncel fiyatları
 - üretim hacimleri
 - stok durumu
 - nakit akımı
 - alacak hesaplarının ve borç hesaplarının durumu
 - her karşı taraf için bakiye
 - şirket bilgilerinin arşivi

 Kullanmaya başlamak için ve güvenlik nedenlerinden dolayı aşağıdakileri yaptığınızdan emin olmanız gerekir:
 yetkili kullanıcı olduğunuzu.

 Daha fazlasını nasıl görebilirim?
 - ilk önce kayıt olun
 - e-postanızı onaylayın,
 - giriş yapmak.
     """, },
}

deals_messages = {
    "english_name": {"subplot_titles": ['Goods, USD', 'Companies, USD', 'Goods, tn'],
                     "title": "Action list",
                     "Choose action": "Choose action",
                     "Company list": "Company list",
                     "Monthly report": "Monthly report",
                     "Choose month": "Choose month",
                     "Choose year": "Choose year",
                     "buy": "Purchase of raw materials and goods for the month",
                     "price": "Weighted average prices",
                     "full": "Details",
                     "sell": "Sales of goods per month",
                     "empty": "There is no data for chosen period",
                     },
    "ukrainian_name": {"subplot_titles": ['Товари, USD', 'Компанії, USD', 'Товари, тн'],
                       "title": 'Список дій',
                       "Choose action": "Вибери дію",
                       "Company list": "Список компаній",
                       "Monthly report": "Місячний звіт",
                       "Choose month": "Вибери місяць",
                       "Choose year": "Вибери рік",
                       "buy": "Закупівля сировини та товарів за місяць",
                       "price": "Середньозважені ціни",
                       "full": "Докладно",
                       "sell": "Реалізація товарів за місяць",
                       "empty": "Немає даних для обраного періоду",
                       },

    "russian_name": {"subplot_titles": ['Товары, USD', 'Компании, USD', 'Товары, тн'],
                     "title": "Список действий",
                     "Choose action": "Выбрать действие",
                     "Company list": "Список компаний",
                     "Monthly report": "Ежемесячный отчет",
                     "Choose month": "Выберите месяц",
                     "Choose year": "Выбери год",
                     "buy": "Закупка сырья и товаров за месяц",
                     "price": "Средневзвешенные цены",
                     "full": "Подробно",
                     "sell": "Реализация товаров за месяц",
                     "empty": "Нет данных за выбранный период",
                     },
    "turkish_name": {"subplot_titles": ['Mal, ABD Doları', 'Şirketler, ABD Doları', 'Mal, tn'],
                     "title": "Aksiyon listesi",
                     "Choose action": "Eylem seçin",
                     "Company list": "Şirket listesi",
                     "Monthly report": "Aylık rapor",
                     "Choose month": "Ayı seç",
                     "Choose year": "Yıl seç",
                     "buy": "Aylık hammadde ve mal alımı",
                     "price": "Ağırlıklı ortalama fiyatlar",
                     "full": "Detaylar",
                     "sell": "Aylık mal satışı",
                     "empty": "Seçilen döneme ait veri yok",
                     },
}

balance_messages = {
    "english_name": {"title": "Action list",
                     "Choose action": "Choose action",
                     "Balance per company": "Company balance",
                     "Balance per period": "Balance per period",
                     "Choose month": "Choose month",
                     "Choose year": "Choose year",
                     "Total balance": "Total balance",
                     "price": "Weighted average prices",
                     "full": "Details",
                     "sell": "Sales of goods per month",
                     "empty": "There is no data for chosen period",
                     "choose": "choose company: ",
                     "current balance": "Current balance with - ",
                     "cumulative": "Cumulative total",
                     "exchange_rate": "Exchange rate",
                     'error_response': 'The request ended with an error',
                     'total': "Total",
                     'category': "By expense category",
                     'graph': "Charts",
                     "debit_usd": 'Debit, USD',
                     "credit_usd": 'Credit, USD',
                     "subplot_titles": ['Debit turnover, USD', 'Credit turnover, USD'],
                     "category_balance": 'Balance by category',
                     "turnovers": "Turnovers table",
                     "by_company": "By company",
                     "recievbles": "Receivables",
                     "debts": "Accounts payable",
                     "subplot_titles2": ['Balance, TL', 'Balance, USD'],
                     'turn_category': "Turnovers by expense category",
                     "turn_company": "Turnovers by company",

                     "": ""},
    "ukrainian_name": {"title": 'Список дій',
                       "Choose action": "Вибери дію",
                       "Balance per company": "Баланс за компанією",
                       "Balance per period": "Баланс за період",
                       "Choose month": "Вибери місяць",
                       "Choose year": "Вибери рік",
                       "Total balance": "Загальний баланс",
                       "price": "Середньозважені ціни",
                       "full": "Докладно",
                       "sell": "Реалізація товарів за місяць",
                       "empty": "Немає даних для обраного періоду",
                       "choose": "оберіть компанію: ",
                       "current balance": "Поточний баланс з - ",
                       "cumulative": "Наростаючий підсумок",
                       "exchange_rate": "Обмінний курс",
                       'error_response': 'Запит завершився з помилкою',
                       'total': "Всього",
                       'category': "За категорією витрат",
                       'graph': "Графіки",
                       "debit_usd": 'Дебит, USD',
                       "credit_usd": 'Кредит, USD',
                       "subplot_titles": ['Оборот з дебіту, USD', 'Оборот з кредиту, USD'],
                       "category_balance": 'Баланс за категоріями',
                       "turnovers": "Таблиця оборотів",
                       "by_company": "У розрізі компаній",
                       "recievbles": "Дебіторська заборгованість",
                       "debts": "Кредиторська заборгованість",
                       "subplot_titles2": ['Баланс, TL', 'Баланс, USD'],
                       'turn_category': "Оборот за категоріями",
                       "turn_company": "Оборот у розрізі компаній",
                       },

    "russian_name": {"title": "Список действий",
                     "Choose action": "Выбрать действие",
                     "Balance per company": "Баланс по компаниям",
                     "Balance per period": "Баланс за период",
                     "Choose month": "Выберите месяц",
                     "Choose year": "Выбери год",
                     "Total balance": "Итоговый баланс",
                     "price": "Средневзвешенные цены",
                     "full": "Подробно",
                     "sell": "Реализация товаров за месяц",
                     "empty": "Нет данных за выбранный период",
                     "choose": "выберите компанию: ",
                     "current balance": "Текущий баланс с - ",
                     "cumulative": "Нарастающим итогом",
                     "exchange_rate": "Обменный курс",
                     'error_response': 'Запрос завершился с ошибкой',
                     'total': "Итого",
                     'category': "В разрезе категорий расходов",
                     'graph': "Графики",
                     "debit_usd": 'Дебіт, USD',
                     "credit_usd": 'Кредіт, USD',
                     "subplot_titles": ['Оборот по дебиту, USD', 'Оборот по кредиту, USD'],
                     "category_balance": 'Баланс по категориям',
                     "turnovers": "Таблица оборотов",
                     "by_company": "В разрезе компаний",
                     "recievbles": "Дебиторская задолженность",
                     "debts": "Кредиторская задолженность",
                     "subplot_titles2": ['Баланс, TL', 'Баланс, USD'],
                     'turn_category': "Оборот по категориям",
                     "turn_company": "Оборот в разрезе компаний",

                     "": "",

                     },
    "turkish_name": {"title": "Aksiyon listesi",
                     "Choose action": "Eylem seçin",
                     "Balance per company": "Dönem başına bakiye",
                     "Balance per period": "Aylık rapor",
                     "Choose month": "Ayı seç",
                     "Choose year": "Yıl seç",
                     "Total balance": "Toplam bakiye",
                     "price": "Ağırlıklı ortalama fiyatlar",
                     "full": "Detaylar",
                     "sell": "Aylık mal satışı",
                     "empty": "Seçilen döneme ait veri yok",
                     "choose": "şirket seçin: ",
                     "current balance": "Mevcut bakiye - ",
                     "cumulative": "Birikimli toplam",
                     "exchange_rate": "Döviz kuru",
                     'error_response': 'İstek bir hatayla sona erdi',
                     'total': "Toplam",
                     'category': "Gider kategorisine göre",
                     'graph': "Grafikler",
                     "debit_usd": 'Borç, USD',
                     "credit_usd": 'Kredi, USD',
                     "subplot_titles": ['Borç cirosu, USD', 'Kredi cirosu, USD'],
                     "category_balance": 'Kategoriye göre bakiye',
                     "turnovers": "Ciro tablosu",
                     "by_company": "Şirkete göre",
                     "recievbles": "Alacak hesapları",
                     "debts": "Borç hesapları",
                     "subplot_titles2": ['Bakiye, TL', 'Bakiye, USD'],
                     'turn_category': "Kategori bazında ciro",
                     "turn_company": "Şirket bazında ciro",

                     },
}

movements_messages = {
    "english_name": {"title": "Action list",
                     "Choose action": "Choose action",
                     "Rests for now": "Rests for now",
                     "Last date of movements": "Last date of money's movements:",
                     "Rest by Banks": "Balances by banks",
                     "Rest by Currency": "Balances by currency",
                     "Details": "Details",
                     "Total by currency": "Total by currency",
                     "Movements by bank": "Movements by bank",
                     "Payment_way": "Bank",
                     "All for period": "All for period",
                     "Threshold for tl": "Threshold for tl",
                     "Show self movements?": "Show self movements?",
                     "Chart title": "Visualization of cash flow",
                     "": "",
                     },

    "ukrainian_name": {"title": 'Список дій',
                       "Choose action": "Вибери дію",
                       "Rests for now": "Поточні залишки",
                       "Last date of movements": "Дата останнього руху коштів",
                       "Rest by Banks": "Баланс за банком",
                       "Rest by Currency": "Баланс за валютою",
                       "Details": "Докладно",
                       "Total by currency": "Всього за валютами",
                       "Movements by bank": "Рух коштів по банкам",
                       "Payment_way": "Банк",
                       "All for period": "Рух по всім банкам за період",
                       "Threshold for tl": "Нижня межа платежів",
                       "Show self movements?": "Відобразити внутрішні переводи?",
                       "Chart title": "Візуалізація руху грошових коштів",

                       },

    "russian_name": {"title": "Список действий",
                     "Choose action": "Выбрать действие",
                     "Rests for now": "Текущие остатки",
                     "Last date of movements": "Дата последнего движения средств",
                     "Rest by Banks": "Баланс по банкам",
                     "Rest by Currency": "Баланс по валютам",
                     "Details": "Подробно",
                     "Total by currency": "Всего в разрезе валют",
                     "Movements by bank": "Движение средств по банкам",
                     "Payment_way": "Банк",
                     "All for period": "Движение по всем банкам за период",
                     "Threshold for tl": "Нижняя граница платежей",
                     "Show self movements?": "Отображать внутренние переводы?",
                     "Chart title": "Визуализация движения денежных средств",
                     },

    "turkish_name": {"title": "Aksiyon listesi",
                     "Choose action": "Eylem seçin",
                     "Rests for now": "Mevcut bakiyeler",
                     "Last date of movements": "Para hareketlerinin son tarihi",
                     "Rest by Banks": "Banka bakiyeleri",
                     "Rest by Currency": "Dövize göre bakiye",
                     "Details": "Detaylar",
                     "Total by currency": "Para birimine göre toplam",
                     "Movements by bank": "Bankalara göre hareketler",
                     "Payment_way": "Banka",
                     "All for period": "Döneme ilişkin tüm bankalardaki hareket",
                     "Threshold for tl": "Daha düşük ödeme limiti",
                     "Show self movements?": "Dahili transferler gösterilsin mi?",
                     "Chart title": "Nakit akışının görselleştirilmesi",
                     "": "",

                     },
}
