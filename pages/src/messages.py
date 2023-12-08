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
    "ukrainian_name": {"goods": "Виберіть тов""ари: ", "type": "Тип огляду:", "day": "День", "dynamic": "Динаміка",
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
    "russian_name": {"goods": "Виберите товары: ", "type": "Тип обзора:", "day": "День", "dynamic": "Динамика",
                     "about": "Страница обзора складских запасов", "instruction": """Выберите в боковом меню:
         - тип просмотра:
             - или конкретный день для обзора
             - или динамику чтобы посмотреть как изменялись запасы со временем
         - также в списке выберите или удалите необходимые товары
""", "start date": "Выберите начальную дату", "end date": "Виберете конечную дату", "one date": "Выберите день:",
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
    
     – current state of affairs in the company
     - archive of company information
    
     Currently implemented:
      - authorization module
      - module for viewing data on warehouse stocks
      - module for viewing data on the purchase and sale of raw materials, goods and finished products
     
     Work is underway to create modules:
       - cash flows,
       - balances for each counterparty,
       - reports on receivables and payables,
       - profit reports

     To start using and for safety reasons, you need to make sure
      that you are an authorized user,
     - so first register,
     - confirm your email,
     - log in.
     """, },
    "ukrainian_name": {"title": "Ласкаво просимо в Company observer",
                       "instruction": """
     Ця програма створена для надання оперативного доступу до:
    
     - поточний стан справ у компанії
     - архів інформації компанії
    
     На даний момент реалізовано:
      - модуль авторизації
      - модуль перегляду даних про складські запаси
      - модуль перегляду даних про закупівлю та реалізацію сировини, товарів та готової продукції
     
     Ведеться робота зі створення модулів:
       - Руху коштів,
       - балансів щодо кожного контрагенту,
       - звітів про дебіторську та кредиторську заборгованості,
       - Звітів про прибуток

     Для початку використання та з метою безпеки потрібно переконатися
      що Ви авторизований користувач,
     - тому для початку пройдіть реєстрацію,
     - підтвердіть свою електронну пошту,
     - увійдіть до системи.
     """, },
    "russian_name": {"title": "Добро пожаловать в Company observer",
                     "instruction": """ 
    Это приложение создано для предоставления оперативного доступа к:
    
    - текущему состоянию дел в компании
    - архиву информации компании
    
    В настоящий момент реализовано:
     - модуль авторизации 
     - модуль просмотра данных о складских запасах
     - модуль просмотра данных о закупке и реализации сырья, товаров и готовой продукции
     
    Ведется работа по созданию модулей:
      - движения денежных средств,
      - балансов по каждому контрагенту,
      - отчетов о дебиторской и кредиторской задолженностях,
      - отчетов о прибыли

    Для начала использования и в целях безопасности нужно убедиться
     что Вы авторизованый пользователь, 
    - поэтому для начала пройдите регистрацию, 
    - подтвердите свою электронную почту,
    - войдите в систему.
    """, },
    "turkish_name": {"title": "Şirket incelemesine hoş geldiniz",
                     "instruction": """
     Bu uygulama aşağıdakilere hızlı erişim sağlamak için oluşturuldu:
    
     - şirketteki mevcut durum
     - şirket bilgilerinin arşivi
    
     Şu anda uygulanıyor:
      - yetkilendirme modülü
      - depo stoklarına ilişkin verileri görüntülemek için modül
      - Hammadde, mal ve bitmiş ürünlerin alım ve satımına ilişkin verileri görüntülemek için modül
     
     Modül oluşturma çalışmaları devam ediyor:
       - nakit akışları,
       - her karşı taraf için bakiyeler,
       - Alacak ve borçlara ilişkin raporlar,
       - kar raporları

     Kullanmaya başlamak için ve güvenlik nedeniyle şunları yaptığınızdan emin olmanız gerekir:
      yetkili kullanıcı olduğunuzu,
     - yani ilk önce kayıt olun,
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
                       "empty": "Немає даних для обраного періоду"
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
                     },
}

